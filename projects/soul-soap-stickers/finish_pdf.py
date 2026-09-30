#!/usr/bin/env python3
"""Put Chrome's PDFs on exact A4 pages, then prove the labels land on the template.

Chrome can only make a 210.23 x 297.01 mm page, so each page is placed 1:1
on a true 210 x 297 mm page (only blank paper at the right edge is lost).
The check then measures the finished PDF: every label ground against Label
Planet's LP15/51SQ template, and every display line against where Chrome laid
it out on screen. It fails if a ground is more than 0.02 mm out, or a line of
text more than 0.15 mm (Chrome sets text on its 1/96 inch grid).

    python3 finish_pdf.py      # after node render.cjs
"""
import json
import pathlib
import sys

import pymupdf

from build import BLEED, COLS, DESIGNS, LABEL, PAGE_H, PAGE_W, ROWS, SHEETS, label_origin

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "output"
PT = 72 / 25.4           # points per mm
TOL = 0.02               # mm, label grounds (drawn in one page SVG, never snapped)
TEXT_TOL = 0.15          # mm, text: Chrome sets each line on its 1/96 in (0.26 mm) grid

GROUNDS = {d["ground"].lower() for d in DESIGNS.values()}


def hexcolour(c):
    return "#" + "".join(f"{round(v * 255):02x}" for v in c[:3]) if c else None


def ground_rects(page):
    """Label ground rectangles (mm, top-left origin), sorted row by row."""
    size = LABEL + 2 * BLEED
    found = []
    for d in page.get_drawings():
        r = d["rect"]
        if hexcolour(d.get("fill")) in GROUNDS and abs(r.width / PT - size) < 0.3 and abs(r.height / PT - size) < 0.3:
            found.append((r.y0 / PT, r.x0 / PT, r.x1 / PT, r.y1 / PT))
    found.sort(key=lambda t: (round(t[0]), t[1]))
    return found


def expected_rects():
    out = []
    for r in range(ROWS):
        for c in range(COLS):
            x, y = label_origin(c, r)
            out.append((y - BLEED, x - BLEED, x + LABEL + BLEED, y + LABEL + BLEED))
    return out


def text_error(doc):
    """Worst gap (mm) between each display line in the PDF and where Chrome laid
    it out on screen (build/layout.json, written by render.cjs): the PDF has to
    be the sheet that was reviewed, with no text shifted against the grounds."""
    layout = json.loads((HERE / "build" / "layout.json").read_text())
    spans = {}
    worst_base = worst_centre = 0.0
    for item in layout:
        page = item["sheet"]
        if page not in spans:
            spans[page] = [s for b in doc[page].get_text("dict")["blocks"] for ln in b.get("lines", [])
                           for s in ln["spans"]]
        matches = [s for s in spans[page] if s["text"].strip() == item["text"].strip()]
        if not matches:
            raise SystemExit(f"text check: {item['text']!r} not found on page {page + 1}")
        best = min(matches, key=lambda s: abs(s["origin"][1] / PT - item["baseline"])
                   + abs((s["bbox"][0] + s["bbox"][2]) / 2 / PT - item["centre"]))
        worst_base = max(worst_base, abs(best["origin"][1] / PT - item["baseline"]))
        worst_centre = max(worst_centre, abs((best["bbox"][0] + best["bbox"][2]) / 2 / PT - item["centre"]))
    return len(layout), worst_base, worst_centre


def worst_error(page):
    got, want = ground_rects(page), expected_rects()
    if len(got) != len(want):
        raise SystemExit(f"found {len(got)} label grounds, expected {len(want)}")
    return max(abs(g - w) for gr, wr in zip(got, want) for g, w in zip(gr, wr))


def finish(src_path):
    src = pymupdf.open(src_path)
    dst = pymupdf.open()
    for i in range(src.page_count):
        page = dst.new_page(width=PAGE_W * PT, height=PAGE_H * PT)
        page.show_pdf_page(pymupdf.Rect(0, 0, src[i].rect.width, src[i].rect.height), src, i, keep_proportion=False)
    dst.set_metadata({"title": src_path.stem, "creator": "Soul Soap sticker build"})
    tmp = src_path.with_suffix(".tmp.pdf")
    dst.save(tmp, garbage=3, deflate=True)
    src.close(); dst.close()
    tmp.replace(src_path)


def main():
    stickers = OUT / "soul-soap-stickers-LP15-51SQ.pdf"
    finish(stickers)
    finish(OUT / "alignment-test-LP15-51SQ.pdf")

    doc = pymupdf.open(stickers)
    bad = False
    for i, page in enumerate(doc):
        w, h = page.rect.width / PT, page.rect.height / PT
        err = worst_error(page)
        ok = err <= TOL and abs(w - PAGE_W) < 0.005 and abs(h - PAGE_H) < 0.005
        bad |= not ok
        print(f"{SHEETS[i]['key']:9s} page {w:.3f} x {h:.3f} mm, worst label edge error {err:.4f} mm {'ok' if ok else 'FAIL'}")
    lines, base_err, centre_err = text_error(doc)
    ok = base_err <= TEXT_TOL and centre_err <= TEXT_TOL
    bad |= not ok
    print(f"text: {lines} display lines, worst baseline error {base_err:.4f} mm, "
          f"worst centring error {centre_err:.4f} mm {'ok' if ok else 'FAIL'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
