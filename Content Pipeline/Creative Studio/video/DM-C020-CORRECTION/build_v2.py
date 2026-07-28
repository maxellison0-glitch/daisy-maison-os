#!/usr/bin/env python3
"""DM-C020 The Correction v2 — staggered pills, timed SFX, clean loop.

  python3 build_v2.py              # writes v2/ and v2-loop/

Max, 28 Jul: "stagger it… maybe one could come in from the left, one could come
in from the right. Little animation sounds. That is genuinely what takes it to
that level 10… Everything has to be timed well. You can't have any glitches."

Every element is placed per frame, so timing is exact rather than approximate.
Zero credits: Chromium renders the pills once, PIL animates them, ffmpeg mixes
SFX that already ship with the media-use skill.

TIMELINE (24fps, 97 frames, 4.04s)
  0.25s  pill 1 "same order."  slides in from the LEFT   + whoosh-short
  1.35s  pill 2 "both signs."  slides in from the RIGHT  + whoosh-short
  2.20s  Daisy Maison tag pops top-right                 + pop
  3.75s  (loop build only) everything eases back out so the last frame
         matches the first and the replay does not jump
"""
import pathlib, subprocess, shutil, tempfile, asyncio, math, sys
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = pathlib.Path(__file__).parent
SFX = HERE.parents[3] / ".agents" / "skills" / "media-use" / "audio" / "assets" / "sfx"
MASTER = HERE.parents[1] / "reference-masters" / "daisy-maison-WORDMARK-v2.png"
SRC = HERE / "raw" / "take-01.mp4"

W, H, FPS = 1080, 1920, 24
TOTAL = 97                      # frames in the source clip
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

P1_IN, P2_IN, TAG_IN = 0.25, 1.35, 2.20
SLIDE = 0.38                    # seconds of travel
OUT_AT = 3.75                   # loop build only

P1_Y, P2_Y = 1150, 1272         # pill baselines, above the platform UI band
SIDE = 80                       # safe inset
TAG_W, TAG_R, TAG_T = 400, 56, 232
ANG_A, ANG_B = -15.0, -7.0
CREAM = (245, 241, 232, 255)


# ---------------------------------------------------------------- assets
async def render_pills():
    from playwright.async_api import async_playwright
    tpl = (HERE / "pills.html").read_text()
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME)
        pg = await b.new_page(viewport={"width": 1400, "height": 400})
        for key, cls, txt in [("p1", "white", "same order."), ("p2", "burg", "both signs.")]:
            (HERE / "_p.html").write_text(tpl.replace("CLS", cls).replace("TEXT", txt))
            await pg.goto((HERE / "_p.html").as_uri())
            await pg.wait_for_timeout(300)
            el = await pg.query_selector("body")
            path = HERE / "overlays" / f"pill-{key}.png"
            await el.screenshot(path=str(path), omit_background=True)
            out[key] = Image.open(path).convert("RGBA")
        await b.close()
    (HERE / "_p.html").unlink(missing_ok=True)
    return out


def build_tag():
    src = Image.open(MASTER).convert("RGBA")
    w, h = src.size
    t = src.crop((int(w * .15), int(h * .26), int(w * .86), int(h * .72)))
    tw = TAG_W - 56
    t = t.resize((tw, round(tw * t.height / t.width)), Image.LANCZOS)
    th = t.height + 52
    tag = Image.new("RGBA", (TAG_W, th), (0, 0, 0, 0))
    ImageDraw.Draw(tag).rounded_rectangle([0, 0, TAG_W - 1, th - 1], radius=14, fill=CREAM)
    tag.alpha_composite(t, (28, 26))
    pad = 26
    o = Image.new("RGBA", (TAG_W + pad * 2, th + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", o.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 6, pad + TAG_W - 1, pad + th + 5],
                                         radius=14, fill=(0, 0, 0, 72))
    o.alpha_composite(sh.filter(ImageFilter.GaussianBlur(11)))
    o.alpha_composite(tag, (pad, pad))
    return o


# ---------------------------------------------------------------- easing
def out_quint(t):                       # decelerate hard, no bounce, no wobble
    return 1 - (1 - t) ** 5

def in_quad(t):
    return t * t

def overshoot(t):
    c = 2.70158
    return 1 + c * (t - 1) ** 3 + 1.70158 * (t - 1) ** 2


# ---------------------------------------------------------------- frames
def frames(tmp, loop):
    pills = asyncio.run(render_pills())
    tag = build_tag()
    p1, p2 = pills["p1"], pills["p2"]
    p1_rest, p2_rest = SIDE, W - SIDE - p2.width      # settle positions
    tag_rest_x = W - TAG_R

    for i in range(TOTAL):
        t = i / FPS
        f = Image.new("RGBA", (W, H), (0, 0, 0, 0))

        # global ease-out for the loop build
        g = 1.0
        if loop and t >= OUT_AT:
            g = 1 - in_quad(min(1.0, (t - OUT_AT) / (TOTAL / FPS - OUT_AT)))

        def slide(img, t_in, rest_x, from_left, y):
            if t < t_in:
                return
            p = min(1.0, (t - t_in) / SLIDE)
            e = out_quint(p)
            off = (rest_x + img.width) if from_left else (W - rest_x)
            x = rest_x + (-off * (1 - e) if from_left else off * (1 - e))
            if g < 1.0:                                    # slide back out to loop
                x = rest_x + (-off if from_left else off) * (1 - g)
            layer = img
            if g < 1.0:
                layer = img.copy()
                layer.putalpha(layer.getchannel("A").point(lambda v: int(v * g)))
            f.alpha_composite(layer, (round(x), y))

        slide(p1, P1_IN, p1_rest, True, P1_Y)
        slide(p2, P2_IN, p2_rest, False, P2_Y)

        if t >= TAG_IN:
            p = min(1.0, (t - TAG_IN) / 0.42)
            s = max(0.02, overshoot(p) if p < 1 else 1.0)
            a = ANG_A + (ANG_B - ANG_A) * p
            fr = tag.resize((max(1, round(tag.width * s)), max(1, round(tag.height * s))),
                            Image.LANCZOS).rotate(a, expand=True, resample=Image.BICUBIC)
            if g < 1.0:
                fr.putalpha(fr.getchannel("A").point(lambda v: int(v * g)))
            f.alpha_composite(fr, (tag_rest_x - fr.width, TAG_T))

        f.save(tmp / f"f{i:04d}.png")


# ---------------------------------------------------------------- mux
def mux(tmp, dst, loop):
    """Video first, then a silent bed with three SFX dropped on the exact beats."""
    # Each cue is the moment the sound must be HEARD. The mp3s carry leading
    # silence before their transient (measured: whoosh 0.123s, pop 0.117s), so
    # the delay is the cue MINUS that lead-in. Without this every hit lands a
    # tenth of a second late and reads as out of sync.
    cues = [(P1_IN, "whoosh-short.mp3", 0.55, 0.123),
            (P2_IN, "whoosh-short.mp3", 0.70, 0.123),
            (TAG_IN, "pop.mp3", 0.45, 0.117)]
    ins, filt, mixin = [], [], []
    for n, (at, name, vol, lead) in enumerate(cues):
        d = max(0, int(round((at - lead) * 1000)))
        ins += ["-i", str(SFX / name)]
        filt.append(f"[{n+2}:a]adelay={d}|{d},volume={vol}[a{n}]")
        mixin.append(f"[a{n}]")
    filt.append(f"{''.join(mixin)}amix=inputs={len(cues)}:normalize=0[mixed]")
    filt.append("[1:a][mixed]amix=inputs=2:normalize=0,atrim=0:4.04,aresample=48000[aout]")

    cmd = [FF, "-y", "-loglevel", "error",
           "-framerate", str(FPS), "-i", str(tmp / "f%04d.png"),
           "-f", "lavfi", "-t", "4.04", "-i", "anullsrc=r=48000:cl=stereo",
           *ins,
           "-i", str(SRC),
           "-filter_complex",
           ";".join(filt) + f";[{len(cues)+2}:v]scale={W}:{H}:flags=lanczos,setsar=1[bg];"
                            "[bg][0:v]overlay=0:0:shortest=1[v]",
           "-map", "[v]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dst)]
    subprocess.run(cmd, check=True)


def build(loop, dst):
    tmp = pathlib.Path(tempfile.mkdtemp())
    frames(tmp, loop)
    dst.parent.mkdir(parents=True, exist_ok=True)
    mux(tmp, dst, loop)
    shutil.rmtree(tmp)
    print(dst)


build(False, HERE / "v2" / "correction-v2.mp4")
build(True, HERE / "v2" / "correction-v2-loop.mp4")
