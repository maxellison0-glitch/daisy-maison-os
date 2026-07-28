#!/usr/bin/env python3
"""Composite a caption overlay onto the Correction clip. Zero credits.

  python3 finish.py <source.mp4> <overlay-name> [out.mp4]

The overlay is a full-frame transparent 1080x1920 PNG from render_overlays.py.
Source is upscaled 720x1280 -> 1080x1920 (lanczos) first so the caption is
rendered at its design size rather than scaled up with the footage.

The hook holds from 0.15s to the end. It does not animate in - a hard cut-in is
what the platforms' own captions do, and a pop-in on a 4s clip eats the hook.
"""
import subprocess, sys, pathlib
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = pathlib.Path(__file__).parent

src = pathlib.Path(sys.argv[1])
name = sys.argv[2]
overlay = HERE / "overlays" / f"{name}.png"
out = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else HERE / "finished" / f"{src.stem}--{name}.mp4"
out.parent.mkdir(parents=True, exist_ok=True)

if not overlay.exists():
    sys.exit(f"no overlay {overlay}")

cmd = [
    FF, "-y",
    "-i", str(src),
    "-i", str(overlay),
    "-filter_complex",
    "[0:v]scale=1080:1920:flags=lanczos,setsar=1[bg];"
    "[bg][1:v]overlay=0:0:enable='gte(t,0.15)'[v]",
    "-map", "[v]",
    "-c:v", "libx264", "-preset", "slow", "-crf", "17",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    "-an",
    str(out),
]
subprocess.run(cmd, check=True, capture_output=True)
print(out)
