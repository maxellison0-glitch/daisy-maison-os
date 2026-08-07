#!/usr/bin/env python3
"""Burn the on-screen hook onto a slide - staggered position, colour off the frame.

WHY. Max, 30 Jul 2026: "If we're gonna do carousels, I would stagger the on-screen
hook so it's up, down, up, down, or just move them around. In the same place, it
just starts to look like AI placement. Colour too. If you can change the colour of
the bubble to match the vibe of the video, that would be good."

Both are the same problem. A pill stamped at the same coordinates in the same
colour on every slide is a template, and a template reads as machine-made however
good the photograph underneath is.

TWO RULES THIS ENFORCES

1. POSITION. Nine slots - three vertical bands x three horizontal - and no two
   consecutive slides may share either coordinate. Slot 1 is always top, because
   that is the frame a scrolling viewer sees; after that it walks.

   The middle vertical band does not exist. The face and the sign's printed
   wording fill roughly 25-85% of a 4:5 frame and they are the two things the
   viewer came for. See ../PUBLISH_READINESS.md.

2. COLOUR comes from what the SIGN IS, declared per slide, and every value is a
   REAL production colourway out of
   projects/daisy-street-sign/production/product-rules.json - the same file the
   laser reads. If the pill is sage, it is the sage we actually print.

   `--auto-colour` samples the frame instead, and it is the wrong tool 90% of the
   time. Written, run, and demoted the same afternoon: sampling all five office
   frames returned blush for every one of them, because a white unit full of
   timber, kraft boxes and skin has exactly one hue. Hue-matching a beige room can
   only ever return beige. "Match the vibe" means the garden bar is grass and the
   Christmas sign is burgundy - that is semantic, and a histogram cannot see it.

   Text colour is whichever of ink/paper clears WCAG AA (4.5:1) against the fill,
   computed, not eyeballed. Blush with white text is unreadable and looks like a
   bug.

Usage:
    python3 hook_pill.py --font Poppins-ExtraBold.ttf \
        --slide frame1.png "this is a warning, not a decoration" \
        --slide frame2.png "the finally is doing a lot of work" \
        --out-dir ./out
"""

import argparse
import colorsys
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RULES = os.path.normpath(os.path.join(
    HERE, "..", "..", "projects", "daisy-street-sign", "production",
    "product-rules.json"))

INK = (14, 14, 14)          # --ink   #0E0E0E
PAPER = (255, 255, 255)     # --paper #FFFFFF
BURGUNDY = "#6E1B2D"        # VIDEO_CAPTION_SYSTEM.md 1.2, the brand accent

W, H = 1080, 1350           # 4:5
BANDS = {"top": 0.075, "low": 0.855}
COLS = {"left": 0.30, "centre": 0.50, "right": 0.70}


def colourways():
    """The printed colourways, plus burgundy. One source of truth."""
    try:
        with open(RULES) as fh:
            cw = dict(json.load(fh)["colourways"])
    except (OSError, KeyError):
        cw = {}
    cw["burgundy"] = BURGUNDY
    # Grey is excluded on purpose: VIDEO_CAPTION_SYSTEM.md 1.2 says "No grey."
    cw.pop("grey", None)
    return {k: hex_rgb(v) for k, v in cw.items()}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def accent_hue(im, exclude_centre=True):
    """The frame's own accent: the modal hue among its saturated pixels.

    Skips the centre column when asked, because the presenter wears a black
    t-shirt across the middle of every one of these frames and black has no hue.
    Returns None when the frame is genuinely neutral - a white workshop often is -
    and the caller falls back to burgundy rather than inventing a colour.
    """
    small = im.convert("RGB").resize((160, 200), Image.LANCZOS)
    px = small.load()
    hist = [0.0] * 36
    for y in range(200):
        for x in range(160):
            if exclude_centre and 52 <= x < 108 and 60 <= y < 170:
                continue
            r, g, b = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s < 0.22 or not 0.18 < v < 0.92:
                continue
            hist[int(h * 36) % 36] += s * v      # weight by how vivid it is
    total = sum(hist)
    if total < 40:
        return None
    i = max(range(36), key=lambda k: hist[k])
    return (i + 0.5) / 36.0


def pick_colour(im, palette, avoid=()):
    """Nearest printed colourway to the frame's accent, skipping `avoid`.

    `avoid` is what makes this useful rather than decorative. First run of this
    tool matched all five office frames to blush, because every one of them is
    timber, kraft boxes and skin - all warm, all near hue 0. A colour rule that
    returns the same colour five times is the template problem it was written to
    solve. So the frame still chooses, but it chooses from what the previous slide
    did not use, and a carousel gets five different pills.
    """
    hue = accent_hue(im)
    ranked = []
    if hue is not None:
        def dist(item):
            r, g, b = item[1]
            h, s, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s < 0.08:                      # black has no hue to match against
                return 9.0
            d = abs(h - hue)
            return min(d, 1 - d)             # hue is circular
        ranked = sorted(palette.items(), key=dist)
    ranked += [("burgundy", palette["burgundy"])]

    for name, rgb in ranked:
        if name in avoid:
            continue
        text = PAPER if contrast(rgb, PAPER) >= contrast(rgb, INK) else INK
        if contrast(rgb, text) >= 4.5:
            return name, rgb, text, None
    rgb = palette["burgundy"]
    return "burgundy", rgb, PAPER, "nothing else cleared AA"


def slots(n):
    """n (band, column) pairs where neither coordinate repeats back to back."""
    out = [("top", "centre")]
    bands, cols = ["low", "top"], ["left", "right", "centre"]
    for i in range(1, n):
        band = bands[(i - 1) % 2]
        col = cols[(i - 1) % 3]
        if col == out[-1][1]:
            col = cols[i % 3]
        out.append((band, col))
    return out


def crop45(path, top_frac=0.07):
    im = Image.open(path).convert("RGB")
    ch = int(im.width / 0.8)
    y0 = min(int(im.height * top_frac), max(0, im.height - ch))
    return im.crop((0, y0, im.width, y0 + ch)).resize((W, H), Image.LANCZOS)


def draw(im, text, band, col, fill, textcol, font_path, opacity=245):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    size = 86
    while size > 28:
        f = ImageFont.truetype(font_path, size)
        b = dr.textbbox((0, 0), text, font=f)
        if (b[2] - b[0]) + 92 < W - 190:
            break
        size -= 2
    b = dr.textbbox((0, 0), text, font=f)
    tw, th = b[2] - b[0], b[3] - b[1]
    px, py = 46, 28
    pw, ph = tw + px * 2, th + py * 2
    cx = int(W * COLS[col])
    x0 = max(40, min(W - 40 - pw, cx - pw // 2))     # never off the edge
    y = int(H * BANDS[band])
    dr.rounded_rectangle([x0, y, x0 + pw, y + ph], radius=ph // 2,
                         fill=fill + (opacity,))
    dr.text((x0 + px - b[0], y + py - b[1]), text, font=f, fill=textcol)
    return Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB"), size


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slide", nargs="+", action="append",
                    metavar="IMG TEXT [COLOURWAY]", required=True,
                    help="colourway is a name from product-rules.json, or "
                         "burgundy; omit it only with --auto-colour")
    ap.add_argument("--auto-colour", action="store_true",
                    help="sample the frame instead of declaring the colour. "
                         "Rarely right - see the module docstring.")
    ap.add_argument("--font", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--force-colour", help="a colourway name, same on every slide")
    ap.add_argument("--sheet", action="store_true", help="also write SHEET.jpg")
    a = ap.parse_args()

    palette = colourways()
    os.makedirs(a.out_dir, exist_ok=True)
    placement = slots(len(a.slide))
    made, used = [], []

    for i, spec in enumerate(a.slide):
        img, text = spec[0], spec[1]
        declared = spec[2] if len(spec) > 2 else None
        base = crop45(img)
        if declared:
            if declared not in palette:
                raise SystemExit(f"'{declared}' is not a production colourway. "
                                 f"Have: {', '.join(sorted(palette))}")
            rgb, name = palette[declared], declared
            textcol = PAPER if contrast(rgb, PAPER) >= contrast(rgb, INK) else INK
            rejected = None if contrast(rgb, textcol) >= 4.5 else "fails AA"
        elif not a.auto_colour:
            raise SystemExit(f"slide {i+1} has no colourway. Add one, or pass "
                             f"--auto-colour and accept what the histogram says.")
        elif a.force_colour:
            rgb = palette[a.force_colour]
            name = a.force_colour
            textcol = PAPER if contrast(rgb, PAPER) >= contrast(rgb, INK) else INK
            rejected = None
        else:
            name, rgb, textcol, rejected = pick_colour(base, palette, avoid=used[-2:])
        used.append(name)
        band, col = placement[i]
        out, size = draw(base, text, band, col, rgb, textcol, a.font)
        p = os.path.join(a.out_dir, f"slide-{i + 1}.jpg")
        out.save(p, quality=94)
        made.append(out)
        note = f" (wanted {rejected}, failed AA)" if rejected else ""
        print(f"  slide-{i+1}  {band:>3}/{col:<6} {name:<10} "
              f"{'white' if textcol == PAPER else 'ink'} text  "
              f"{contrast(rgb, textcol):.1f}:1  {size}px{note}")

    if a.sheet and made:
        tw, th = 340, 425
        sheet = Image.new("RGB", (tw * len(made), th), "white")
        for i, im in enumerate(made):
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (i * tw, 0))
        sheet.save(os.path.join(a.out_dir, "SHEET.jpg"), quality=90)
        print(f"  {os.path.join(a.out_dir, 'SHEET.jpg')}")


if __name__ == "__main__":
    main()
