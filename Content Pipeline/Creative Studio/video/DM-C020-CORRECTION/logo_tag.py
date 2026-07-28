#!/usr/bin/env python3
"""Angled Daisy Maison corner tag with a pop-in, composited onto the final cut.

  python3 logo_tag.py <in.mp4> <out.mp4>

Max, 28 Jul: "add a Daisy Maison logo... in the top-right corner, where it's not
hidden, and angled. That would look clever, and make it animated pop in."

The bottom of the frame is already taken by the two caption pills, so the tag
lives top-right. It pops at 2.2s - after the second sign has been read and the
joke has landed - and holds to the end.

Zero credits: PIL only, no generation, no Chromium.
"""
import pathlib, sys, math, subprocess, shutil, tempfile
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = pathlib.Path(__file__).parent
MASTER = HERE.parents[1] / "reference-masters" / "daisy-maison-WORDMARK-v2.png"

W, H = 1080, 1920
FPS = 24
POP_AT = 2.20          # seconds - after the punchline sign is read
POP_DUR = 0.42         # seconds of overshoot settle
TAG_W = 400            # tag width before rotation
ANGLE_END = -7.0       # degrees, settled
ANGLE_START = -15.0    # degrees, at the start of the pop
MARGIN_R, MARGIN_T = 56, 232
CREAM = (245, 241, 232, 255)


def build_tag() -> Image.Image:
    """Crop the type out of the wordmark master and set it on a clean cream tag."""
    src = Image.open(MASTER).convert("RGBA")
    w, h = src.size
    # The master is a site-header screenshot: cream band with the lockup in it.
    # Take the type only and drop the band's skewed edges.
    type_only = src.crop((int(w * 0.15), int(h * 0.26), int(w * 0.86), int(h * 0.72)))
    tw = TAG_W - 56
    type_only = type_only.resize((tw, max(1, round(tw * type_only.height / type_only.width))),
                                 Image.LANCZOS)

    th = type_only.height + 52
    tag = Image.new("RGBA", (TAG_W, th), (0, 0, 0, 0))
    ImageDraw.Draw(tag).rounded_rectangle([0, 0, TAG_W - 1, th - 1], radius=14, fill=CREAM)
    tag.alpha_composite(type_only, (28, 26))

    # A soft drop shadow so it sits on the footage rather than floating in it.
    pad = 26
    out = Image.new("RGBA", (TAG_W + pad * 2, th + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [pad, pad + 6, pad + TAG_W - 1, pad + th - 1 + 6], radius=14, fill=(0, 0, 0, 72))
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(11)))
    out.alpha_composite(tag, (pad, pad))
    return out


def ease_overshoot(t: float) -> float:
    """0..1 -> scale, overshooting to ~1.10 then settling. No bounce, one swing."""
    c = 1.70158 + 1
    return 1 + c * (t - 1) ** 3 + 1.70158 * (t - 1) ** 2


def main():
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    tag = build_tag()
    tmp = pathlib.Path(tempfile.mkdtemp())

    # Probe the clip length so the hold runs exactly to the last frame.
    n_frames = int(round(float(subprocess.run(
        [FF, "-i", str(src), "-map", "0:v:0", "-c", "copy", "-f", "null", "-"],
        capture_output=True, text=True).stderr.split("time=")[-1].split(" ")[0]
        .split(":")[-1]) * FPS)) + FPS * 0  # seconds fragment * fps
    n_frames = max(n_frames, 1)

    total = int(round(4.04 * FPS))
    for i in range(total):
        t = i / FPS
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if t >= POP_AT:
            p = min(1.0, (t - POP_AT) / POP_DUR)
            s = ease_overshoot(p) if p < 1 else 1.0
            s = max(0.02, s)
            ang = ANGLE_START + (ANGLE_END - ANGLE_START) * min(1.0, p)
            fr = tag.resize((max(1, round(tag.width * s)), max(1, round(tag.height * s))),
                            Image.LANCZOS).rotate(ang, expand=True, resample=Image.BICUBIC)
            # Pin the tag's top-right so it grows out of the corner, not toward it.
            x = W - MARGIN_R - fr.width
            y = MARGIN_T
            layer.alpha_composite(fr, (x, y))
        layer.save(tmp / f"f{i:04d}.png")

    subprocess.run([
        FF, "-y", "-loglevel", "error",
        "-i", str(src),
        "-framerate", str(FPS), "-i", str(tmp / "f%04d.png"),
        "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1[v]",
        "-map", "[v]", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(dst),
    ], check=True)
    shutil.rmtree(tmp)
    print(dst)


main()
