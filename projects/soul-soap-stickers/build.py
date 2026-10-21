#!/usr/bin/env python3
"""Soul Soap by Daisy Maison: saying stickers on Label Planet LP15/51SQ sheets.

Sheet (Label Planet's published template): A4 portrait, 3 across x 5 down,
51 x 51 mm labels on a 52.9 mm pitch, top/bottom margin 17.2 mm, left/right
margin 26.6 mm, rounded corners. Colour grounds bleed 0.95 mm (half the gap);
text stays at least 3 mm inside each label edge.

Every coordinate in a design is millimetres from that label's top-left corner.
Text lines are placed by BASELINE, using baseline ratios measured in Chromium
for each font at line-height 1.

    python3 build.py        # writes build/*.html (+ canvas files if --canvas DIR)
    node render.cjs         # PDFs, PNG previews and the fit check
"""
import json
import math
import pathlib
import re
import sys
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE / "build"

# ---- Label Planet LP15/51SQ -------------------------------------------------
PAGE_W, PAGE_H = 210.0, 297.0
LABEL, PITCH = 51.0, 52.9
MARGIN_X, MARGIN_Y = 26.6, 17.2
COLS, ROWS = 3, 5
BLEED = 0.95
SAFE = 3.0

# ---- Palette (sampled from the approved mockups, cleaned up for print) ------
COCOA = "#5A2D1E"
RED = "#CF2A27"
CREAM = "#F7EBD6"
PINK = "#F7A1BC"
CORAL = "#EB6443"
TAN = "#C28453"
MUSTARD = "#F1B33E"
INK = "#2B1A12"

# ---- Type: (CSS family, weight, baseline ratio at line-height 1) ------------
COOPER = ("'Caprasimo', serif", 400, 0.84)       # soft Cooper-style serif
GROOVY = ("'Shrikhand', serif", 400, 0.80)       # 70s italic display
ROUND = ("'Fredoka', sans-serif", 700, 0.86)     # bubbly rounded
CAPS = ("'Montserrat', sans-serif", 600, 0.86)   # spaced small caps (kerned)
CAPSB = ("'Montserrat', sans-serif", 700, 0.86)
CAP_H = 0.70                                      # Montserrat cap height / em

BRAND = "SOUL SOAP · DAISY MAISON"


def mm(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return ("0" if s in ("-0", "") else s) + "mm"


def n(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


# ---- Text -------------------------------------------------------------------
def line(text, base, size, font, color, track=0.0, shadow=None, fit=45.0, cx=LABEL / 2, width=LABEL):
    """One line centred on `cx`, its baseline at `base` mm."""
    fam, weight, bl = font
    top = base - bl * size
    css = [
        "position: absolute",
        f"left: {mm(cx - width / 2)}",
        f"top: {mm(top)}",
        f"width: {mm(width)}",
        "box-sizing: border-box",
        "text-align: center",
        "white-space: nowrap",
        f"font-family: {fam}",
        f"font-weight: {weight}",
        f"font-size: {mm(size)}",
        "line-height: 1",
        f"color: {color}",
    ]
    if track:
        # letter-spacing also trails the last glyph; pad the left to re-centre
        css += [f"letter-spacing: {n(track)}em", f"padding-left: {n(track)}em"]
    if shadow:
        col, depth = shadow
        steps = max(3, round(depth / 0.1))
        layers = [f"{mm(depth * i / steps)} {mm(depth * i / steps)} 0 {col}" for i in range(1, steps + 1)]
        css.append("text-shadow: " + ", ".join(layers))
    return f'<div data-fit="{n(fit)}" style="{"; ".join(css)}">{text}</div>'


def brand(color, base=45.3, size=1.8, track=0.2):
    return line(BRAND, base, size, CAPS, color, track=track)


# ---- Shapes (drawn in label millimetres, bleed included) -----------------------
class Gfx(str):
    """A label's shapes. As a string it is that label's own positioned <svg>
    (the Design canvas uses it). The print sheets lift `.inner` into one
    page-wide SVG instead, because Chrome snaps each positioned box to whole
    pixels (up to 0.13 mm) but never moves anything inside an SVG."""

    def __new__(cls, inner):
        box = LABEL + 2 * BLEED
        s = super().__new__(cls, (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{n(-BLEED)} {n(-BLEED)} {n(box)} {n(box)}" '
            f'style="position: absolute; left: {mm(-BLEED)}; top: {mm(-BLEED)}; width: {mm(box)}; height: {mm(box)}; overflow: hidden">'
            f"{inner}</svg>"))
        s.inner = inner
        return s


svg = Gfx


HEART_D = ("M50 16 C54 6 62 0 73.5 0 C88.5 0 100 11.5 100 27.5 C100 52 72 72 53.2 88.2 "
           "C51.4 89.8 48.6 89.8 46.8 88.2 C28 72 0 52 0 27.5 C0 11.5 11.5 0 26.5 0 C38 0 46 6 50 16 Z")
HEART_H = 89.4


def heart(cx, top, w, fill, stroke=None, sw=0.35, rot=0):
    """Heart `w` mm wide, top edge at `top`, centred on `cx`."""
    s = w / 100
    h = HEART_H * s
    t = f"translate({n(cx)} {n(top + h / 2)}) rotate({n(rot)}) translate({n(-w / 2)} {n(-h / 2)}) scale({n(s)})"
    paint = f'fill="{fill}"'
    if stroke:
        paint += f' stroke="{stroke}" stroke-width="{n(sw / s)}"'
    return f'<path d="{HEART_D}" transform="{t}" {paint}/>'


SPARK_D = "M0 -50 C3.5 -14 14 -3.5 50 0 C14 3.5 3.5 14 0 50 C-3.5 14 -14 3.5 -50 0 C-14 -3.5 -3.5 -14 0 -50 Z"


def spark(cx, cy, size, fill, rot=0):
    return f'<path d="{SPARK_D}" transform="translate({n(cx)} {n(cy)}) rotate({n(rot)}) scale({n(size / 100)})" fill="{fill}"/>'


def daisy(cx, cy, r, petal=CREAM, centre=MUSTARD, rot=0, petals=8):
    out = f'<g transform="translate({n(cx)} {n(cy)}) rotate({n(rot)})">'
    for k in range(petals):
        out += (f'<ellipse cx="0" cy="{n(-0.52 * r)}" rx="{n(0.25 * r)}" ry="{n(0.47 * r)}" '
                f'fill="{petal}" transform="rotate({n(k * 360 / petals)})"/>')
    return out + f'<circle cx="0" cy="0" r="{n(0.3 * r)}" fill="{centre}"/></g>'


def sun(cx, cy, r=2.9, ray_in=4.1, ray_out=5.7, rays=12):
    out = f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{MUSTARD}"/>'
    for k in range(rays):
        a = math.radians(k * 360 / rays - 90)
        out += (f'<line x1="{n(cx + ray_in * math.cos(a))}" y1="{n(cy + ray_in * math.sin(a))}" '
                f'x2="{n(cx + ray_out * math.cos(a))}" y2="{n(cy + ray_out * math.sin(a))}" '
                f'stroke="{CORAL}" stroke-width="0.75" stroke-linecap="round"/>')
    return out


def stripes(yc, top=TAN, bottom=CORAL, star=CORAL):
    h, gap = 0.9, 0.55
    out = ""
    for x0, x1 in ((7.5, 21.9), (29.1, 43.5)):
        out += f'<rect x="{n(x0)}" y="{n(yc - gap / 2 - h)}" width="{n(x1 - x0)}" height="{n(h)}" fill="{top}"/>'
        out += f'<rect x="{n(x0)}" y="{n(yc + gap / 2)}" width="{n(x1 - x0)}" height="{n(h)}" fill="{bottom}"/>'
    return out + spark(25.5, yc, 4.8, star)


def checker(dark=COCOA, light=CREAM, rows=2, across=18):
    sq = LABEL / across
    out = f'<rect x="{n(-BLEED)}" y="{n(-BLEED)}" width="{n(LABEL + 2 * BLEED)}" height="{n(BLEED + rows * sq)}" fill="{light}"/>'
    for r in range(rows):
        y0, h = (r * sq, sq) if r else (-BLEED, sq + BLEED)
        for k in range(-1, across + 1):
            if (k + r) % 2 == 0:
                out += f'<rect x="{n(k * sq)}" y="{n(y0)}" width="{n(sq)}" height="{n(h)}" fill="{dark}"/>'
    return out


def bubble(cx, cy, r, color=PINK, sw=0.5):
    rh = r * 0.62
    a1, a2 = math.radians(195), math.radians(250)
    return (
        f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="none" stroke="{color}" stroke-width="{n(sw)}"/>'
        f'<path d="M {n(cx + rh * math.cos(a1))} {n(cy + rh * math.sin(a1))} A {n(rh)} {n(rh)} 0 0 1 '
        f'{n(cx + rh * math.cos(a2))} {n(cy + rh * math.sin(a2))}" fill="none" stroke="{color}" '
        f'stroke-width="{n(sw * 0.9)}" stroke-linecap="round"/>'
    )


_arc_ids = iter(range(1, 10_000))


def rainbow(cx=25.5, cy=57.0, bands=((26.5, 22.5, RED), (22.5, 18.5, CORAL), (18.5, 12.5, MUSTARD)),
            text_color=INK, size=1.5, track=0.14):
    out = ""
    for ro, ri, col in bands:
        r = (ro + ri) / 2
        out += (f'<path d="M {n(cx - r)} {n(cy)} A {n(r)} {n(r)} 0 0 1 {n(cx + r)} {n(cy)}" '
                f'fill="none" stroke="{col}" stroke-width="{n(ro - ri)}"/>')
    ro, ri, _ = bands[-1]
    rb = (ro + ri) / 2 - CAP_H * size / 2   # caps centred in the inner band
    uid = f"soul-arc-{next(_arc_ids)}"
    out += f'<path id="{uid}" d="M {n(cx - rb)} {n(cy)} A {n(rb)} {n(rb)} 0 0 1 {n(cx + rb)} {n(cy)}" fill="none"/>'
    out += (f'<text font-family="Montserrat, sans-serif" font-weight="600" font-size="{n(size)}" '
            f'letter-spacing="{n(size * track)}" fill="{text_color}">'
            f'<textPath href="#{uid}" startOffset="50%" text-anchor="middle">{BRAND}</textPath></text>')
    return out


# ---- The designs ------------------------------------------------------------
DESIGNS = {}


def design(key, ground, saying):
    def register(fn):
        DESIGNS[key] = {"ground": ground, "saying": saying, "draw": fn}
        return fn
    return register


@design("foamy-heart", COCOA, "My one and foamy")
def _():
    return [
        svg(heart(25.5, 3.6, 41, RED) + heart(25.5, 4.4, 39, "none", stroke=CREAM)
            + heart(25.5, 32.4, 3.2, CREAM)),
        line("my one", 16.2, 7.4, COOPER, CREAM, fit=34),
        line("and", 22.6, 7.4, COOPER, CREAM, fit=30),
        line("foamy", 29.2, 7.4, COOPER, CREAM, fit=26),
        brand(PINK),
    ]


@design("foamy-heart-groovy", COCOA, "My one and foamy")
def _():
    return [
        svg(heart(25.5, 3.8, 40, RED) + heart(7.6, 6.2, 3.6, CREAM, rot=-18)
            + heart(44.2, 34.6, 3.4, CREAM, rot=16)),
        line("my one", 16.0, 8.2, GROOVY, CREAM, fit=36),
        line("and", 22.8, 7.4, GROOVY, CREAM, fit=30),
        line("foamy", 31.0, 9.6, GROOVY, CREAM, fit=40),
        brand(CREAM),
    ]


@design("good-clean-stripes", CREAM, "If you can't be good, at least be clean!")
def _():
    return [
        line("IF YOU CAN’T BE", 8.6, 2.35, CAPS, INK, track=0.16),
        line("good,", 17.0, 9.0, GROOVY, RED, shadow=(MUSTARD, 0.5)),
        line("AT LEAST BE", 22.9, 2.35, CAPS, INK, track=0.16),
        line("clean!", 33.2, 11.0, GROOVY, RED, shadow=(MUSTARD, 0.6)),
        svg(stripes(37.4)),
        brand(INK),
    ]


@design("good-clean-rainbow", CREAM, "If you can't be good, at least be clean!")
def _():
    return [
        line("IF YOU CAN’T BE", 6.9, 2.2, CAPS, INK, track=0.16),
        line("good,", 14.4, 8.0, GROOVY, RED, shadow=(MUSTARD, 0.45)),
        line("AT LEAST BE", 19.4, 2.2, CAPS, INK, track=0.16),
        line("clean!", 27.8, 9.8, GROOVY, RED, shadow=(MUSTARD, 0.55)),
        svg(rainbow()),
    ]


@design("grubby", COCOA, "For when life gets a bit grubby")
def _():
    return [
        line("FOR WHEN LIFE", 15.6, 3.15, CAPSB, PINK, track=0.03),
        line("GETS A BIT", 19.7, 3.15, CAPSB, PINK, track=0.03),
        line("grubby", 32.2, 13.0, ROUND, PINK, track=-0.01),
        brand(PINK),
    ]


@design("soaper-star", RED, "You've got this, soap-er star!")
def _():
    return [
        svg(spark(9.0, 26.5, 3.4, CREAM) + spark(44.5, 29.0, 5.6, MUSTARD) + spark(44.6, 4.8, 2.6, MUSTARD)),
        line("YOU’VE GOT THIS,", 10.6, 2.6, CAPSB, CREAM, track=0.08),
        line("soap-er", 21.2, 9.6, COOPER, CREAM),
        line("star!", 33.4, 12.0, COOPER, MUSTARD, shadow=(COCOA, 0.5)),
        brand(CREAM),
    ]


@design("soaperb-sunshine", CREAM, "You're bloody soap-erb, sunshine!")
def _():
    return [
        svg(sun(25.5, 9.4)),
        line("YOU’RE BLOODY", 19.2, 2.5, CAPS, INK, track=0.14),
        line("soap-erb,", 29.4, 8.4, GROOVY, RED, shadow=(MUSTARD, 0.45)),
        line("SUNSHINE!", 36.4, 2.8, CAPSB, INK, track=0.14),
        brand(INK),
    ]


@design("glad-friends", PINK, "Soap glad we're friends")
def _():
    return [
        line("soap", 17.2, 12.5, COOPER, RED, shadow=(COCOA, 0.55)),
        line("glad", 29.6, 12.5, COOPER, RED, shadow=(COCOA, 0.55)),
        line("WE’RE FRIENDS", 37.4, 2.8, CAPSB, COCOA, track=0.1),
        svg(heart(8.4, 35.0, 2.8, RED, rot=-12) + heart(42.6, 35.0, 2.8, RED, rot=12)),
        brand(COCOA),
    ]


@design("proud", COCOA, "Soap proud of you")
def _():
    return [
        svg(spark(43.0, 8.5, 6.4, MUSTARD) + spark(8.0, 10.0, 3.2, MUSTARD) + spark(44.5, 33.0, 2.6, CREAM)),
        line("soap", 17.0, 12.5, COOPER, CREAM),
        line("proud", 29.6, 12.5, COOPER, CREAM),
        line("OF YOU", 37.6, 3.0, CAPSB, PINK, track=0.2),
        brand(PINK),
    ]


@design("thank-you", CREAM, "Thank you soap much")
def _():
    return [
        line("THANK YOU", 9.0, 2.6, CAPS, INK, track=0.18),
        line("soap", 19.8, 11.0, GROOVY, RED, shadow=(MUSTARD, 0.55)),
        line("much", 31.4, 11.0, GROOVY, RED, shadow=(MUSTARD, 0.55)),
        svg(stripes(37.0)),
        brand(INK),
    ]


@design("love-you-heart", PINK, "Love you soap much")
def _():
    return [
        svg(heart(25.5, 3.3, 42, RED) + heart(25.5, 4.1, 40, "none", stroke=CREAM)
            + heart(25.5, 31.8, 3.0, CREAM)),
        line("love you", 15.2, 6.8, COOPER, CREAM, fit=34),
        line("soap", 21.8, 6.8, COOPER, CREAM, fit=30),
        line("much", 29.0, 6.8, COOPER, CREAM, fit=26),
        brand(COCOA),
    ]


@design("much-love", RED, "Soap much love")
def _():
    return [
        svg(heart(6.8, 12.4, 3.2, CREAM, rot=-16) + heart(44.2, 16.0, 2.8, CREAM, rot=14)
            + heart(44.0, 36.4, 2.4, PINK, rot=18)),
        line("SOAP MUCH", 13.8, 3.4, CAPSB, CREAM, track=0.16),
        line("love", 33.0, 17.0, ROUND, PINK, shadow=(COCOA, 0.6), track=-0.01),
        brand(CREAM),
    ]


@design("sh-happens", RED, "Sh*t happens, have a soap")
def _():
    return [
        line("SH*T HAPPENS,", 11.4, 2.9, CAPSB, CREAM, track=0.12),
        line("have a", 22.4, 9.4, GROOVY, CREAM, shadow=(COCOA, 0.5)),
        line("soap", 34.0, 13.0, GROOVY, CREAM, shadow=(COCOA, 0.6)),
        svg(spark(44.0, 24.5, 3.6, MUSTARD) + spark(7.5, 31.0, 2.6, MUSTARD)),
        brand(CREAM),
    ]


@design("soap-mate", CREAM, "You're my soap mate")
def _():
    return [
        svg(checker()),
        line("YOU’RE MY", 14.6, 2.9, CAPSB, INK, track=0.18),
        line("soap", 26.0, 13.0, COOPER, RED),
        line("mate", 37.4, 13.0, COOPER, RED),
        brand(INK),
    ]


@design("glad-found-you", COCOA, "Soap glad I found you")
def _():
    return [
        svg(daisy(5.5, 5.5, 8.5, rot=10) + daisy(48.0, 29.5, 6.5, rot=-8) + daisy(4.0, 36.0, 3.4)),
        line("soap", 18.8, 12.0, COOPER, CREAM),
        line("glad", 31.0, 12.0, COOPER, CREAM),
        line("I FOUND YOU", 38.6, 2.8, CAPSB, PINK, track=0.14),
        brand(PINK),
    ]


@design("glad-mum", PINK, "Soap glad you're my mum")
def _():
    return [
        svg(daisy(45.5, 5.5, 8.5, rot=-6) + daisy(1.8, 25.0, 5.2, rot=12) + daisy(46.6, 38.6, 2.8, rot=20)),
        line("soap", 17.8, 12.0, COOPER, RED, shadow=(COCOA, 0.5)),
        line("glad", 30.0, 12.0, COOPER, RED, shadow=(COCOA, 0.5)),
        line("YOU’RE MY MUM", 37.8, 2.7, CAPSB, COCOA, track=0.1),
        brand(COCOA),
    ]


@design("love-you-mum", COCOA, "Love you soap much, Mum")
def _():
    return [
        svg(heart(25.5, 3.3, 42, RED) + heart(25.5, 4.1, 40, "none", stroke=CREAM)
            + heart(25.5, 32.6, 2.8, CREAM)),
        line("love you", 15.4, 6.2, COOPER, CREAM, fit=34),
        line("soap much,", 21.6, 5.5, COOPER, CREAM, fit=33),
        line("mum", 29.3, 8.4, COOPER, CREAM, fit=24),
        brand(PINK),
    ]


@design("me-time", CREAM, "Mum, you deserve a little me time")
def _():
    bubbles = [(44.0, 7.0, 4.2), (37.2, 4.6, 1.9), (48.6, 14.2, 2.3),
               (5.6, 38.8, 2.8), (10.6, 35.8, 1.3), (3.2, 33.8, 0.95)]
    return [
        svg("".join(bubble(*b) for b in bubbles)),
        line("MUM, YOU DESERVE", 17.0, 2.35, CAPS, INK, track=0.14),
        line("A LITTLE", 21.2, 2.35, CAPS, INK, track=0.14),
        line("me time", 32.6, 9.2, GROOVY, RED, shadow=(MUSTARD, 0.5)),
        brand(INK),
    ]


@design("mum-soaperb", RED, "Mum, you're soap-erb")
def _():
    return [
        svg(spark(7.4, 8.0, 4.0, MUSTARD) + spark(44.0, 9.6, 2.6, CREAM)
            + stripes(36.4, top=MUSTARD, bottom=CREAM, star=MUSTARD)),
        line("MUM, YOU’RE", 17.2, 3.0, CAPSB, CREAM, track=0.16),
        line("soap-erb", 29.2, 10.2, COOPER, CREAM, shadow=(COCOA, 0.5)),
        brand(CREAM),
    ]


@design("my-mess", COCOA, "Thank you for always cleaning up my mess")
def _():
    return [
        line("THANK YOU FOR ALWAYS", 16.6, 2.7, CAPSB, PINK, track=0.03),
        line("CLEANING UP", 20.4, 2.7, CAPSB, PINK, track=0.03),
        line("my mess", 31.6, 11.5, ROUND, PINK, track=-0.01),
        brand(PINK),
    ]


# ---- Sheets -----------------------------------------------------------------
SHEETS = [
    {
        "key": "everyday",
        "title": "Everyday sheet",
        "caption": "SOUL SOAP · EVERYDAY SHEET · LABEL PLANET LP15/51SQ · PRINT AT 100% / ACTUAL SIZE",
        "grid": [
            ["foamy-heart", "good-clean-stripes", "soaper-star"],
            ["soaperb-sunshine", "grubby", "glad-friends"],
            ["sh-happens", "soap-mate", "proud"],
            ["glad-found-you", "love-you-heart", "thank-you"],
            ["good-clean-rainbow", "much-love", "foamy-heart-groovy"],
        ],
    },
    {
        "key": "mum",
        "title": "Mum sheet",
        "caption": "SOUL SOAP · MUM SHEET · LABEL PLANET LP15/51SQ · PRINT AT 100% / ACTUAL SIZE",
        "grid": [[k] * 3 for k in ("glad-mum", "love-you-mum", "me-time", "mum-soaperb", "my-mess")],
    },
]


def label_origin(col, row):
    return MARGIN_X + col * PITCH, MARGIN_Y + row * PITCH


def label_html(key, col, row):
    """Design canvas: each label is one self-contained box (ground, shapes, text)."""
    d = DESIGNS[key]
    x, y = label_origin(col, row)
    ground = (f'<div style="position: absolute; left: {mm(-BLEED)}; top: {mm(-BLEED)}; '
              f'width: {mm(LABEL + 2 * BLEED)}; height: {mm(LABEL + 2 * BLEED)}; background: {d["ground"]}"></div>')
    body = "".join(d["draw"]())
    return (f'<div data-label="{key}" style="position: absolute; left: {mm(x)}; top: {mm(y)}; '
            f'width: {mm(LABEL)}; height: {mm(LABEL)}">{ground}{body}</div>')


def caption_html(text):
    return line(text, PAGE_H - 7.5, 1.9, CAPS, "#9A8F86", track=0.12, fit=PAGE_W, cx=PAGE_W / 2, width=PAGE_W)


def page_svg(inner, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(PAGE_W)} {n(PAGE_H)}" '
            f'style="position: absolute; left: 0; top: 0; width: {mm(PAGE_W)}; height: {mm(PAGE_H)}">'
            f"<defs>{defs}</defs>{inner}</svg>")


def sheet_body(sheet):
    """Design canvas sheet."""
    labels = "".join(label_html(k, c, r) for r, row in enumerate(sheet["grid"]) for c, k in enumerate(row))
    return labels + caption_html(sheet["caption"])


def print_sheet_body(sheet, cut=False):
    """Print sheet (cut=False, grounds bleed 0.95 mm) or peeled-sticker preview
    (cut=True, clipped to the label with rounded corners). Grounds and shapes
    sit in one page-wide SVG so they land exactly; text lines are HTML on top."""
    box = LABEL + 2 * BLEED
    clip_id = f"{sheet['key']}-{'cut' if cut else 'bleed'}"
    clip_rect = (f'<rect x="0" y="0" width="{n(LABEL)}" height="{n(LABEL)}" rx="2" ry="2"/>' if cut else
                 f'<rect x="{n(-BLEED)}" y="{n(-BLEED)}" width="{n(box)}" height="{n(box)}"/>')
    groups, texts = [], []
    for r, row in enumerate(sheet["grid"]):
        for c, key in enumerate(row):
            d = DESIGNS[key]
            x, y = label_origin(c, r)
            parts = d["draw"]()
            shapes = "".join(p.inner for p in parts if isinstance(p, Gfx))
            groups.append(f'<g transform="translate({n(x)} {n(y)})" clip-path="url(#{clip_id})">'
                          f'<rect x="{n(-BLEED)}" y="{n(-BLEED)}" width="{n(box)}" height="{n(box)}" fill="{d["ground"]}"/>'
                          f"{shapes}</g>")
            words = "".join(p for p in parts if not isinstance(p, Gfx))
            texts.append(f'<div data-label="{key}" style="position: absolute; left: {mm(x)}; top: {mm(y)}; '
                         f'width: {mm(LABEL)}; height: {mm(LABEL)}">{words}</div>')
    defs = f'<clipPath id="{clip_id}">{clip_rect}</clipPath>'
    return page_svg("".join(groups), defs) + "".join(texts) + caption_html(sheet["caption"])


FONT_FACES = """
@font-face { font-family: 'Caprasimo'; src: url(../fonts/Caprasimo-400.woff2) format('woff2'); font-weight: 400; }
@font-face { font-family: 'Shrikhand'; src: url(../fonts/Shrikhand-400.woff2) format('woff2'); font-weight: 400; }
@font-face { font-family: 'Fredoka'; src: url(../fonts/Fredoka-700.woff2) format('woff2'); font-weight: 700; }
@font-face { font-family: 'Montserrat'; src: url(../fonts/Montserrat-600.woff2) format('woff2'); font-weight: 600; }
@font-face { font-family: 'Montserrat'; src: url(../fonts/Montserrat-700.woff2) format('woff2'); font-weight: 700; }
"""

GOOGLE_FONTS = ("https://fonts.googleapis.com/css2?family=Caprasimo&family=Fredoka:wght@700"
                "&family=Montserrat:wght@600;700&family=Shrikhand&display=swap")


def print_html(cut=False):
    pages = []
    for i, sheet in enumerate(SHEETS):
        brk = "; break-after: page" if i < len(SHEETS) - 1 else ""
        pages.append(f'<section data-sheet="{sheet["key"]}" style="position: relative; width: {mm(PAGE_W)}; '
                     f'height: {mm(PAGE_H)}; overflow: hidden; background: #ffffff{brk}">{print_sheet_body(sheet, cut)}</section>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Soul Soap stickers · LP15/51SQ</title>
<style>{FONT_FACES}
@page {{ size: {mm(PAGE_W)} {mm(PAGE_H)}; margin: 0; }}
html, body {{ margin: 0; padding: 0; background: #ffffff; }}
</style>
</head>
<body>
{"".join(pages)}
</body>
</html>
"""


def alignment_html():
    grey, sw = "#8A8A8A", 0.25
    shapes = []
    for r in range(ROWS):
        for c in range(COLS):
            x, y = label_origin(c, r)
            # stroke centred sw/2 inside, so its outer edge is the label edge
            shapes.append(f'<rect x="{n(x + sw / 2)}" y="{n(y + sw / 2)}" width="{n(LABEL - sw)}" height="{n(LABEL - sw)}" '
                          f'rx="2" ry="2" fill="none" stroke="{grey}" stroke-width="{n(sw)}"/>')
            cx, cy = x + LABEL / 2, y + LABEL / 2
            shapes.append(f'<path d="M {n(cx - 4)} {n(cy)} H {n(cx + 4)} M {n(cx)} {n(cy - 4)} V {n(cy + 4)}" '
                          f'stroke="{grey}" stroke-width="0.2" fill="none"/>')
    # 100 mm bar, end ticks included
    shapes.append('<path d="M 55 287.55 H 155 M 55.15 286.4 V 288.7 M 154.85 286.4 V 288.7" stroke="#333333" stroke-width="0.3" fill="none"/>')
    marks, ruler = [page_svg("".join(shapes))], ""
    page = dict(fit=PAGE_W, cx=PAGE_W / 2, width=PAGE_W)
    head = (line("ALIGNMENT TEST · PRINT ON PLAIN PAPER AT 100% / ACTUAL SIZE", 8.2, 2.4, CAPSB, "#333333", track=0.08, **page)
            + line("Hold it behind a Label Planet LP15/51SQ sheet against a window: the outlines should sit on the label edges.",
                   12.6, 2.4, CAPS, "#555555", **page)
            + line("THIS BAR SHOULD MEASURE EXACTLY 100 MM", 293.6, 1.9, CAPS, "#555555", track=0.12, **page))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Soul Soap · alignment test</title>
<style>{FONT_FACES}
@page {{ size: {mm(PAGE_W)} {mm(PAGE_H)}; margin: 0; }}
html, body {{ margin: 0; padding: 0; background: #ffffff; }}
</style>
</head>
<body>
<section style="position: relative; width: {mm(PAGE_W)}; height: {mm(PAGE_H)}; overflow: hidden">{"".join(marks)}{ruler}{head}</section>
</body>
</html>
"""


# ---- Design canvas (claude.ai Design artboards) -------------------------------
def dc_html(sheet):
    # data-* attributes are only for the local fit check
    body = re.sub(r' data-(fit|label)="[^"]*"', "", sheet_body(sheet))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Soul Soap · {sheet["title"]}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="{GOOGLE_FONTS.replace("&", "&amp;")}">
<style>
body{{margin:0;background:#ffffff}}
</style>
</helmet>
<div style="position: relative; width: 794px; height: 1123px; overflow: hidden; background: #ffffff; font-family: 'Montserrat', sans-serif; color: {INK}">{body}</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":794,"height":1123}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
"""


def write_canvas(root):
    proj = pathlib.Path(root) / "project"
    proj.mkdir(parents=True, exist_ok=True)
    names = ["Main.dc.html", "Mum.dc.html"]
    boards = {}
    for i, (name, sheet) in enumerate(zip(names, SHEETS)):
        (proj / name).write_text(dc_html(sheet), encoding="utf-8")
        boards[name] = {"x": i * (794 + 80), "y": 0, "w": 794, "h": 1123, "title": sheet["title"]}
    index = {
        "v": 3,
        "createdOnFiles": {"v": 1, "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
        "title": "Soul Soap Sticker Sheet",
        "launch": {"view": "canvas"},
        "pages": [],
        "boards": boards,
        "order": names,
        "notes": {
            "title": {"x": 0, "y": -300, "text": "Soul Soap stickers · Label Planet LP15/51SQ (A4, 15 × 51 mm)",
                      "kind": "title1", "maxW": 794 * 2 + 80},
        },
        "designSystems": [],
    }
    (proj / "canvas.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")


def main():
    BUILD.mkdir(exist_ok=True)
    (BUILD / "print.html").write_text(print_html(), encoding="utf-8")
    (BUILD / "preview.html").write_text(print_html(cut=True), encoding="utf-8")
    (BUILD / "alignment.html").write_text(alignment_html(), encoding="utf-8")
    (BUILD / "designs.json").write_text(json.dumps(
        {k: {"saying": d["saying"], "ground": d["ground"]} for k, d in DESIGNS.items()}, indent=1), encoding="utf-8")
    if "--canvas" in sys.argv:
        write_canvas(sys.argv[sys.argv.index("--canvas") + 1])
    print(f"{len(DESIGNS)} designs, {len(SHEETS)} sheets -> {BUILD}")


if __name__ == "__main__":
    main()
