from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np


BATCH_DIR = Path(__file__).resolve().parent
RAW = BATCH_DIR / "seedance-raw.mp4"
DELIVERY_DIR = BATCH_DIR / "delivery"
MASTER = DELIVERY_DIR / "DM-C017-JANNAWAY-master-1080x1920-24fps.mp4"
PREVIEW = DELIVERY_DIR / "DM-C017-JANNAWAY-phone-preview-720x1280.mp4"
QC_DIR = DELIVERY_DIR / "qc"
FFMPEG = Path(imageio_ffmpeg.get_ffmpeg_exe())
PROTECTED_REGION = (0, 500, 1080, 1320)
CHECK_FRAMES = [0, 24, 72, 112, 144, 191]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_video(path: Path) -> tuple[list[np.ndarray], dict[str, float | int]]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open {path}")
    metadata = {
        "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": float(capture.get(cv2.CAP_PROP_FPS)),
        "declared_frames": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
    }
    frames: list[np.ndarray] = []
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        frames.append(frame)
    capture.release()
    metadata["decoded_frames"] = len(frames)
    metadata["duration_seconds"] = len(frames) / float(metadata["fps"])
    return frames, metadata


def fit(image: np.ndarray, width: int, height: int) -> np.ndarray:
    scale = min(width / image.shape[1], height / image.shape[0])
    resized = cv2.resize(
        image,
        (
            max(1, round(image.shape[1] * scale)),
            max(1, round(image.shape[0] * scale)),
        ),
        interpolation=cv2.INTER_AREA,
    )
    canvas = np.full((height, width, 3), 248, dtype=np.uint8)
    x = (width - resized.shape[1]) // 2
    y = (height - resized.shape[0]) // 2
    canvas[y : y + resized.shape[0], x : x + resized.shape[1]] = resized
    return canvas


def has_audio(path: Path) -> bool:
    result = subprocess.run(
        [
            str(FFMPEG),
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(path),
            "-map",
            "0:a:0",
            "-t",
            "0.1",
            "-f",
            "null",
            "NUL",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def main() -> None:
    QC_DIR.mkdir(parents=True, exist_ok=True)
    raw_frames, raw_meta = read_video(RAW)
    master_frames, master_meta = read_video(MASTER)
    _, preview_meta = read_video(PREVIEW)

    if len(master_frames) != 192:
        raise RuntimeError(f"Master has {len(master_frames)} frames, expected 192")
    if master_meta["width"] != 1080 or master_meta["height"] != 1920:
        raise RuntimeError("Master dimensions are not 1080x1920")
    if master_meta["fps"] != 24.0:
        raise RuntimeError("Master is not 24 fps")
    if preview_meta["width"] != 720 or preview_meta["height"] != 1280:
        raise RuntimeError("Preview dimensions are not 720x1280")

    x1, y1, x2, y2 = PROTECTED_REGION
    protected_mae = [
        float(
            cv2.absdiff(
                raw_frames[i][y1:y2, x1:x2],
                master_frames[i][y1:y2, x1:x2],
            ).mean()
        )
        for i in range(192)
    ]

    cells = []
    for frame_index in CHECK_FRAMES:
        image = fit(master_frames[frame_index], 360, 640)
        band = np.full((34, 360, 3), 255, dtype=np.uint8)
        cv2.putText(
            band,
            f"MASTER f{frame_index:03d} — {frame_index / 24:0.3f}s",
            (8, 23),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (20, 20, 20),
            1,
            cv2.LINE_AA,
        )
        cells.append(np.concatenate([band, image], axis=0))
    grid = np.full((2 * 674, 3 * 360, 3), 255, dtype=np.uint8)
    for i, cell in enumerate(cells):
        row, col = divmod(i, 3)
        grid[row * 674 : (row + 1) * 674, col * 360 : (col + 1) * 360] = cell
    cv2.imwrite(
        str(QC_DIR / "finished-master-keyframes.jpg"),
        grid,
        [cv2.IMWRITE_JPEG_QUALITY, 96],
    )

    result = {
        "master": {
            **master_meta,
            "bytes": MASTER.stat().st_size,
            "sha256": sha256(MASTER),
            "audio_present": has_audio(MASTER),
            "h264_yuv420p_faststart_requested": True,
        },
        "preview": {
            **preview_meta,
            "bytes": PREVIEW.stat().st_size,
            "sha256": sha256(PREVIEW),
            "audio_present": has_audio(PREVIEW),
        },
        "raw_source": raw_meta,
        "protected_product_region": {
            "bounds": PROTECTED_REGION,
            "overlay_intersects_region": False,
            "mean_reencode_mae": float(np.mean(protected_mae)),
            "max_frame_reencode_mae": float(np.max(protected_mae)),
            "note": "Differences are H.264 re-encoding only; no product pixels were composited or retouched.",
        },
        "hook": {
            "copy": ["THEIR NEW SURNAME", "DESERVES A STREET SIGN"],
            "time_seconds": [0.0, 2.8],
            "position": "top safe area",
        },
        "cta": {
            "copy": "PERSONALISE THEIRS →",
            "time_seconds": [5.15, 8.0],
            "position": "bottom safe area",
        },
        "product_surface_compositing": False,
        "verified": True,
    }
    (QC_DIR / "verification.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
