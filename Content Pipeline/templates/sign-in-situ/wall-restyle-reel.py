"""THE LITTLE MADAM — cat reel, three wall styles.

Everything here is free and local. No generation, no credits.

Four jobs per frame:
  1. paint the feather string out              (Max: "I don't like that we've overlaid it")
  2. repaint the wall, keeping its own lighting (Max: "I don't like the colour")
  3. composite the reprinted sign, locked       (0px drift, proven on this clip)
  4. captions + wordmark end card, off the cat house this time

The wall repaint keeps VALUE and replaces HUE/SATURATION, so every gradient,
the sunlit patch top-right and the contact shadow all survive — it reads as the
same room painted a different colour, not as a flat fill.
"""
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from destring import find_string, erase

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1080, 1934, 24
TRIM_FRAMES = 16                    # the 0.65s where the feather crosses the sign
HOLD = 30                           # held last frame, so the end card has 1.25s
WM_IN = 5.02                        # wordmark rises as the second caption leaves

HERE = os.path.dirname(os.path.abspath(__file__))
PLATE = os.path.join(HERE, "madam-plate.png")     # reprinted sign, full plate
SIGN_BOX_1080 = (214, 516, 866, 696)              # sign + margin, in 1080-wide space

# --- the three wall styles. Hue in degrees, saturation as a multiplier target.
STYLES = {
    # Deliberately far apart — three near-identical pale neutrals is not a choice.
    "A-warm-white": dict(hue=32.0, sat=0.075, vgain=1.14,
                         label="soft warm white"),
    "B-cool-grey":  dict(hue=210.0, sat=0.055, vgain=1.00,
                         label="cool chalky grey"),
    "C-deep-clay":  dict(hue=18.0, sat=0.280, vgain=0.72,
                         label="deep clay plaster"),
}

WALL_HUE = 44.0        # measured mean hue of the sage wall, degrees
WALL_TOL = 19.0        # membership falloff (half-width to zero)


# ---------------------------------------------------------------- colour maths
def rgb2hsv(a):
    a = a / 255.0
    mx = a.max(2); mn = a.min(2); d = mx - mn
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.zeros_like(mx)
    nz = d > 1e-6
    idx = nz & (mx == r); h[idx] = ((g - b)[idx] / d[idx]) % 6
    idx = nz & (mx == g); h[idx] = ((b - r)[idx] / d[idx]) + 2
    idx = nz & (mx == b); h[idx] = ((r - g)[idx] / d[idx]) + 4
    h = h * 60.0
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0.0)
    return h, s, mx


def hsv2rgb(h, s, v):
    h = np.mod(h, 360.0) / 60.0
    i = np.floor(h).astype(int)
    f = h - i
    p = v * (1 - s); q = v * (1 - s * f); t = v * (1 - s * (1 - f))
    i = i % 6
    out = np.zeros(h.shape + (3,), float)
    for k, (rr, gg, bb) in enumerate([(v, t, p), (q, v, p), (p, v, t),
                                      (p, q, v), (t, p, v), (v, p, q)]):
        m = i == k
        out[m] = np.stack([rr, gg, bb], -1)[m]
    return np.clip(out * 255.0, 0, 255)


def repaint_wall(a, style):
    """Replace the wall's hue/saturation, keep its value. Soft hue membership."""
    h, s, v = rgb2hsv(a)
    # Membership: close to the wall's hue, actually coloured, and not the far-right
    # scene through the doorway (which is a different room and must stay put).
    # Clipped-linear, NOT gaussian. A gaussian gave PARTIAL membership across the
    # sunlit patch (hue 39.5 there vs 47 in shadow), so the repaint strength varied
    # and a strong colour came out blotchy. This is flat 1.0 across the whole wall's
    # hue span and 0 by the time it reaches the cat house at 23.5 degrees.
    w = np.clip((1.0 - np.abs(h - WALL_HUE) / WALL_TOL) * 2.4, 0, 1)
    # The strip of wall left of the door was left sage — a bright band of the OLD
    # colour down every frame. It is in shade, and its hue drifts continuously from 45
    # at y900 to 125 at y1800 while its saturation falls to 0.08, so BOTH the main
    # lobe and the saturation gate gave it partial weight and a first attempt at a
    # second narrow lobe came back blotchy. It needs one flat wide lobe instead:
    # full membership across hue 35..135, on a lower saturation knee, inside x < 260.
    # The cat house sits at hue 19-24 and the door frame at 17, so both fall outside
    # and stay untouched — the boundary lands on hue, not on a hand-drawn edge.
    g = np.clip((h - 35.0) / 12.0, 0, 1) * np.clip((135.0 - h) / 12.0, 0, 1)
    g *= np.clip((s - 0.045) / 0.020, 0, 1)
    g[:, 260:] = 0.0
    w = w * np.clip((s - 0.055) / 0.06, 0, 1)       # ignore near-neutral trim
    w = np.maximum(w, g)
    w[:, 1012:] = 0.0                                # doorway to the right
    w = np.asarray(Image.fromarray((w * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(2.0)), float) / 255.0

    nh = np.full_like(h, style["hue"])
    ns = np.full_like(s, style["sat"])
    nv = np.clip(v * style["vgain"], 0, 1)
    painted = hsv2rgb(nh, ns, nv)
    m = w[..., None]
    return a * (1 - m) + painted * m


# ------------------------------------------------------------------- captions
def caption_layer(text, top, size=62):
    """House standard: bold white, black stroke behind the fill (Max's CapCut look)."""
    import base64
    fdir = "/home/user/daisy-maison-os/projects/diffuser/reel-pipeline/fonts"
    face = ""
    fp = os.path.join(fdir, "TikTokSans-ExtraBold.woff2")
    if os.path.exists(fp):
        b64 = base64.b64encode(open(fp, "rb").read()).decode()
        face = ("@font-face{font-family:'TT';src:url(data:font/woff2;base64,"
                + b64 + ") format('woff2');font-weight:800}")
        fam = "TT"
    else:
        fam = "'DejaVu Sans',sans-serif"
    stroke = max(4, int(size * 0.085))
    html = (
        "<!doctype html><meta charset=utf8><style>*{margin:0;padding:0}"
        f"html,body{{width:{W}px;height:{H}px;background:transparent}}{face}</style>"
        f"<div style=\"position:absolute;top:{top}px;left:60px;right:60px;"
        f"text-align:center;font-family:{fam};font-weight:800;font-size:{size}px;"
        f"line-height:1.14;color:#fff;letter-spacing:-.005em;"
        f"-webkit-text-stroke:{stroke}px #0B0B0B;paint-order:stroke fill;"
        f"text-shadow:0 3px 9px rgba(0,0,0,.55),0 0 26px rgba(0,0,0,.35)\">{text}</div>"
    )
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, "c.html"); op = os.path.join(td, "c.png")
        open(hp, "w").write(html)
        subprocess.run(
            ["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless=new",
             "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
             "--default-background-color=00000000",
             f"--window-size={W},{H + 260}", f"--screenshot={op}", "file://" + hp],
            check=True, capture_output=True)
        return Image.open(op).convert("RGBA").crop((0, 0, W, H))


def wordmark_lettering(target_w):
    """The wordmark master is a cream CARD with dark serif on it. Composited over a
    repainted wall that reads as a pasted rectangle — and on the warm-white style the
    cream card almost vanishes into the wall. So key the lettering out of the card
    (alpha from how much darker than the card each pixel is) and lay it down as white
    type with a soft shadow, which sits correctly on all three walls."""
    src = np.asarray(Image.open(
        "/home/user/daisy-maison-os/Content Pipeline/Creative Studio/"
        "reference-masters/daisy-maison-WORDMARK-v2.png").convert("RGBA"), float)
    card_a = src[..., 3] > 200
    lum = src[..., :3].mean(2)
    paper = float(np.percentile(lum[card_a], 96))        # the cream, not the type
    ink = float(np.percentile(lum[card_a], 1))
    a = np.clip((paper - lum) / max(paper - ink, 1.0), 0, 1) * card_a
    ys, xs = np.nonzero(a > 0.06)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]   # trim the card away
    al = Image.fromarray((a * 255).astype(np.uint8))
    w = target_w
    h = max(1, int(round(al.height * w / al.width)))
    al = al.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    shadow = Image.new("RGBA", out.size, (0, 0, 0, 0))
    shadow.putalpha(Image.new("L", out.size, 0))
    sh = Image.new("L", out.size, 0); sh.paste(al, (20, 23))
    sh = sh.filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v * 0.55))
    shadow = Image.merge("RGBA", (Image.new("L", out.size, 8),) * 3 + (sh,))
    white = Image.merge("RGBA", (Image.new("L", out.size, 255),) * 3
                        + (Image.new("L", out.size, 0),))
    wa = Image.new("L", out.size, 0); wa.paste(al, (20, 20))
    white.putalpha(wa)
    out.alpha_composite(shadow)
    out.alpha_composite(white)
    return out


def ease_out_quint(u):
    return 1 - pow(1 - u, 5)


def masked_in(layer, t, t0, t1, t2, t3, travel=34):
    """Mask-reveal up, hold, mask away down. Never a fade."""
    if t < t0 or t > t3:
        return None
    if t < t1:
        u = ease_out_quint((t - t0) / (t1 - t0)); dy = int((1 - u) * travel); op = u
    elif t <= t2:
        dy, op = 0, 1.0
    else:
        u = ease_out_quint((t - t2) / (t3 - t2)); dy = int(u * travel); op = 1 - u
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(layer, (0, dy))
    if op < 1:
        al = out.split()[3].point(lambda v: int(v * op))
        out.putalpha(al)
    return out


# ----------------------------------------------------------------------- main
def main():
    frames = sorted(os.listdir(os.path.join(HERE, "fr")))[TRIM_FRAMES:]
    n = len(frames)
    dur = n / FPS
    print("%d frames, %.2fs" % (n, dur))

    # the reprinted sign patch, at clip scale
    plate = Image.open(PLATE).convert("RGB").resize((W, int(W * 2752 / 1536)),
                                                    Image.LANCZOS)
    sx0, sy0, sx1, sy1 = SIGN_BOX_1080
    sign_mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sign_mask).rounded_rectangle(SIGN_BOX_1080, radius=10, fill=255)
    sign_mask = sign_mask.filter(ImageFilter.GaussianBlur(9))
    sm = np.asarray(sign_mask, float)[..., None] / 255.0

    # captions and end card
    c1 = caption_layer("We&rsquo;ve settled who owns<br>this house.", 232, 60)
    c2 = caption_layer("It&rsquo;s in writing now.", 258, 68)
    wm = wordmark_lettering(int(W * 0.62))
    ww, wh = wm.size
    wm_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wm_layer.alpha_composite(wm, ((W - ww) // 2, 300))   # wall space, clear of the house

    # String geometry, fitted PER FRAME.
    #
    # Two bugs found here, both worth keeping written down:
    #  1. The first version fitted rows 20..950, which spans the sign at y 516..696.
    #     The lettering is a far stronger ridge than the string, so the fit followed
    #     the sign, the erase band missed the string by 8-23px, and the render came
    #     back with the string still in it AND a clean streak beside it.
    #  2. The second version fitted once on a mid frame and reused it. Wrong: the
    #     feather toy SWINGS. Frame 60 has the string at x=586 @ y150 on a -0.044
    #     slope; frame 62 has it at x=593 on a +0.010 slope. One line cannot cover
    #     both, so it has to be re-fitted every frame.
    #
    # Fit on bare wall only (y 30..470), and carry the previous frame's line forward
    # if a fit fails or jumps implausibly, so a single bad frame cannot smear the wall.
    coefs = []
    prev = None
    for fn in frames:
        a = np.asarray(Image.open(os.path.join(HERE, "fr", fn)).convert("RGB")).astype(float)
        c = find_string(a, 30, 470, 470, 720)
        if c is None or (prev is not None and abs(c[1] - prev[1]) > 14):
            c = prev
        prev = c if c is not None else prev
        coefs.append(prev)
    assert coefs[0] is not None, "no string found on the first frame"
    xs = [c[0] * 300 + c[1] for c in coefs]
    print("string x @ y300: %.1f .. %.1f (swings %.1fpx)"
          % (min(xs), max(xs), max(xs) - min(xs)))

    plate_np = np.asarray(plate, float)

    # The source clip is only 5.21s, which left the end card 0.15s on screen. Hold the
    # last frame for HOLD frames so the wordmark actually gets read.
    order = list(range(n)) + [n - 1] * HOLD
    print("output %d frames, %.2fs" % (len(order), len(order) / FPS))

    for key, style in STYLES.items():
        outdir = os.path.join(HERE, "out-" + key)
        shutil.rmtree(outdir, ignore_errors=True); os.makedirs(outdir)
        prev_src = -1
        # the sign patch must be repainted with the SAME transform, or the wall
        # margin inside the patch would still be sage and betray the composite
        patch_full = repaint_wall(plate_np, style)
        base = None
        for i, src in enumerate(order):
            t = i / FPS
            if src != prev_src:
                a = np.asarray(Image.open(os.path.join(HERE, "fr", frames[src]))
                               .convert("RGB")).astype(float)
                # Wider band than the string itself — lower down it defocuses to ~20px.
                # Skip the sign box: the plate composite overwrites it anyway, and
                # running the band through the lettering only risks the feathered mask
                # edge letting damaged wall show at the border.
                a = erase(a, coefs[src], 0, sy0 - 6, half=9, feather=9)
                a = erase(a, coefs[src], sy1 + 6, 1120, half=9, feather=9)
                a = repaint_wall(a, style)
                a = a * (1 - sm) + patch_full[:H] * sm      # lock the sign
                base = np.clip(a, 0, 255).astype(np.uint8)
            prev_src = src
            img = Image.fromarray(base).convert("RGBA")
            for layer, wins in ((c1, (0.30, 0.72, 2.55, 2.85)),
                                (c2, (3.85, 4.25, 4.80, 5.06))):
                l = masked_in(layer, t, *wins)
                if l is not None:
                    img.alpha_composite(l)
            if t >= WM_IN:
                u = min(1.0, (t - WM_IN) / 0.42)
                dy = int((1 - ease_out_quint(u)) * -40)
                l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                l.alpha_composite(wm_layer, (0, dy))
                al = l.split()[3].point(lambda v: int(v * min(1.0, u * 1.4)))
                l.putalpha(al)
                img.alpha_composite(l)
            img.convert("RGB").save(os.path.join(outdir, "f%04d.png" % i))
        out = os.path.join(HERE, "MADAM-%s.mp4" % key)
        subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", os.path.join(outdir, "f%04d.png"),
                        "-c:v", "libx264", "-preset", "slow", "-crf", "19",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
                       check=True)
        print("wrote", out, "-", style["label"])


if __name__ == "__main__":
    main()
