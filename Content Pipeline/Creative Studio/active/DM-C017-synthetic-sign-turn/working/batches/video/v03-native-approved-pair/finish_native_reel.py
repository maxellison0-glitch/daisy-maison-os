from __future__ import annotations

import json
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
import numpy as np


BATCH_DIR = Path(__file__).resolve().parent
RAW_VIDEO = BATCH_DIR / "seedance-raw.mp4"
DELIVERY_DIR = BATCH_DIR / "delivery"
SOUNDTRACK = DELIVERY_DIR / "DM-C017-JANNAWAY-original-soundtrack.wav"
MASTER = DELIVERY_DIR / "DM-C017-JANNAWAY-master-1080x1920-24fps.mp4"
PREVIEW = DELIVERY_DIR / "DM-C017-JANNAWAY-phone-preview-720x1280.mp4"
FFMPEG = Path(imageio_ffmpeg.get_ffmpeg_exe())

SAMPLE_RATE = 48_000
DURATION_SECONDS = 8.0
FRAME_COUNT = 192


def make_soundtrack() -> None:
    rng = np.random.default_rng(17017)
    sample_count = int(SAMPLE_RATE * DURATION_SECONDS)
    t = np.arange(sample_count, dtype=np.float64) / SAMPLE_RATE

    white = rng.normal(0.0, 1.0, sample_count)
    kernel = np.ones(240, dtype=np.float64) / 240
    room = np.convolve(white, kernel, mode="same") * 0.045

    fast_kernel = np.ones(14, dtype=np.float64) / 14
    soft_noise = np.convolve(white, fast_kernel, mode="same")
    whoosh_phase = np.clip((t - 0.60) / 4.20, 0.0, 1.0)
    whoosh_env = np.sin(np.pi * whoosh_phase) ** 2
    whoosh_env[(t < 0.60) | (t > 4.80)] = 0.0
    whoosh = soft_noise * whoosh_env * 0.055

    reveal_time = np.maximum(t - 4.72, 0.0)
    reveal_env = np.exp(-reveal_time * 4.8) * (t >= 4.72)
    chime = (
        np.sin(2 * np.pi * 520 * reveal_time)
        + 0.55 * np.sin(2 * np.pi * 780 * reveal_time)
        + 0.28 * np.sin(2 * np.pi * 1040 * reveal_time)
    ) * reveal_env * 0.075
    settle = (
        np.sin(2 * np.pi * 92 * reveal_time)
        * np.exp(-reveal_time * 14.0)
        * (t >= 4.72)
        * 0.12
    )

    mono = room + whoosh + chime + settle
    pan = np.sin(np.pi * whoosh_phase) * 0.10
    left = mono * (1.0 - pan)
    right = mono * (1.0 + pan)
    stereo = np.column_stack([left, right])
    peak = float(np.max(np.abs(stereo)))
    if peak:
        stereo *= 0.56 / peak
    pcm = np.clip(stereo * 32767, -32768, 32767).astype("<i2")

    with wave.open(str(SOUNDTRACK), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE)
        output.writeframes(pcm.tobytes())


def run(command: list[str]) -> None:
    completed = subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Command failed ({completed.returncode}):\n"
            + " ".join(command)
            + "\n"
            + completed.stderr[-8000:]
        )


def make_master() -> None:
    font = "C\\:/Windows/Fonts/arialbd.ttf"
    video_filter = ",".join(
        [
            "trim=start_frame=0:end_frame=192",
            "setpts=PTS-STARTPTS",
            "fps=24",
            (
                "drawtext="
                f"fontfile='{font}':"
                "text='THEIR NEW SURNAME':"
                "x=(w-text_w)/2:y=116:fontsize=72:"
                "fontcolor=white:borderw=4:bordercolor=black@0.78:"
                "box=1:boxcolor=black@0.30:boxborderw=22:"
                "enable='between(t,0,2.80)'"
            ),
            (
                "drawtext="
                f"fontfile='{font}':"
                "text='DESERVES A STREET SIGN':"
                "x=(w-text_w)/2:y=228:fontsize=57:"
                "fontcolor=white:borderw=4:bordercolor=black@0.78:"
                "box=1:boxcolor=black@0.30:boxborderw=20:"
                "enable='between(t,0,2.80)'"
            ),
            (
                "drawtext="
                f"fontfile='{font}':"
                "text='PERSONALISE THEIRS →':"
                "x=(w-text_w)/2:y=1580:fontsize=58:"
                "fontcolor=black:"
                "box=1:boxcolor=white@0.90:boxborderw=24:"
                "enable='between(t,5.15,8.00)'"
            ),
        ]
    )
    run(
        [
            str(FFMPEG),
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(RAW_VIDEO),
            "-i",
            str(SOUNDTRACK),
            "-filter_complex",
            f"[0:v]{video_filter}[v]",
            "-map",
            "[v]",
            "-map",
            "1:a:0",
            "-frames:v",
            str(FRAME_COUNT),
            "-t",
            str(DURATION_SECONDS),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-profile:v",
            "high",
            "-level",
            "4.1",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            str(SAMPLE_RATE),
            "-ac",
            "2",
            "-movflags",
            "+faststart",
            str(MASTER),
        ]
    )


def make_preview() -> None:
    run(
        [
            str(FFMPEG),
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(MASTER),
            "-vf",
            "scale=720:1280:flags=lanczos",
            "-frames:v",
            str(FRAME_COUNT),
            "-t",
            str(DURATION_SECONDS),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "22",
            "-profile:v",
            "main",
            "-level",
            "3.1",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-ar",
            str(SAMPLE_RATE),
            "-ac",
            "2",
            "-movflags",
            "+faststart",
            str(PREVIEW),
        ]
    )


def main() -> None:
    DELIVERY_DIR.mkdir(parents=True, exist_ok=True)
    make_soundtrack()
    make_master()
    make_preview()
    result = {
        "master": str(MASTER),
        "master_bytes": MASTER.stat().st_size,
        "preview": str(PREVIEW),
        "preview_bytes": PREVIEW.stat().st_size,
        "soundtrack": str(SOUNDTRACK),
        "soundtrack_bytes": SOUNDTRACK.stat().st_size,
        "frame_count": FRAME_COUNT,
        "fps": 24,
        "duration_seconds": DURATION_SECONDS,
        "product_surface_compositing": False,
        "allowed_finishing_only": [
            "top hook typography",
            "bottom CTA typography",
            "original synthetic room/whoosh/reveal sound",
            "H.264/AAC encoding",
            "delivery scaling",
        ],
    }
    (DELIVERY_DIR / "finish-manifest.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
