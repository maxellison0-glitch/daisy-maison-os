#!/usr/bin/env python3
"""
Build a carousel from ONE approved plate and N wordings — at zero credits.

The economics, which are the whole point
----------------------------------------
Before: every wording variant needed its own paid print-edit generation, so ten
designs cost roughly what a film costs, and a film is one idea.

Now: the plate is paid for once. Every wording after that is free and instant.
Ten designs, fifty designs, a seasonal set — same cost as one. That inverts the
content plan: stills become the volume format and video becomes the rare one.

It also collapses the error surface. A film has motion, drift, occlusion, audio
and pacing to get wrong. A reprint has one thing to get wrong — the printing —
and that is rendered from the audited PSD, so it cannot drift.

Output: 4:5 slides (1080x1350 after downscale) for feed carousels, plus the
wordmark end-slide.
"""

import json, os, sys
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reprint import reprint            # noqa: E402
import wordmark                        # noqa: E402

FEED_W, FEED_H = 1080, 1350            # Instagram 4:5


def crop_45(img, cfg):
    """Crop the portrait plate to 4:5.

    The window is an explicit box in plates.json, not a derived one, because
    'where the charm is' is a composition judgement per plate. Two things it has
    to buy: the sign large enough that line 2 is legible on a phone, and some
    wall above the sign so it is not jammed against the frame edge. The first
    pass took full width from a y offset and got neither.
    """
    x0, y0, x1, y1 = cfg["crop45"]
    return img.crop((x0, y0, x1, y1))


def place_wordmark(slide, scale=0.62, y_frac=0.30):
    """Drop the lockup into the wall gap BELOW the sign.

    Placement has now been wrong twice in opposite directions: the advert put it
    over the cat house, and the first carousel put it straight over the sign. The
    only free real estate is the band of wall between the sign's bottom edge and
    the roofline, so that is where it goes — it covers neither the product nor
    the animal, and it stays clear of Instagram's own UI chrome.
    """
    wm_path = os.path.join(HERE, "wordmark.png")
    if not os.path.exists(wm_path):
        wordmark.render(wm_path)
    wm = Image.open(wm_path).convert("RGBA")
    w = int(slide.width * scale)
    h = int(wm.height * w / wm.width)
    wm = wm.resize((w, h), Image.LANCZOS)
    out = slide.convert("RGBA")
    out.alpha_composite(wm, ((slide.width - w) // 2, int(slide.height * y_frac)))
    return out.convert("RGB")


def main():
    plate = sys.argv[1]
    designs_file = sys.argv[2]
    outdir = sys.argv[3]
    cfg = json.load(open(os.path.join(HERE, "plates.json")))[plate]
    os.makedirs(outdir, exist_ok=True)

    rows = [r.rstrip("\n") for r in open(designs_file) if r.strip()
            and not r.startswith("#")]
    slides = []
    for i, row in enumerate(rows, 1):
        l1, l2 = (row.split("\t") + [""])[:2]
        full = reprint(cfg, l1, l2)
        slide = crop_45(full, cfg).resize((FEED_W, FEED_H), Image.LANCZOS)
        p = os.path.join(outdir, "slide-%02d.jpg" % i)
        slide.save(p, quality=94, subsampling=0)
        slides.append((l1, l2, p, slide))
        print("%2d  %-22s %s" % (i, l1, os.path.basename(p)))

    # end slide: the hero wording, with the lockup
    end = place_wordmark(slides[0][3].copy(),
                         y_frac=cfg.get("wordmark_y", 0.30))
    ep = os.path.join(outdir, "slide-%02d-END.jpg" % (len(slides) + 1))
    end.save(ep, quality=94, subsampling=0)
    print("%2d  %-22s %s" % (len(slides) + 1, "[wordmark]", os.path.basename(ep)))

    # contact sheet for review
    cols, pad = 5, 12
    rowsn = (len(slides) + 1 + cols - 1) // cols
    tw = FEED_W // 4
    th = FEED_H // 4
    sheet = Image.new("RGB", (cols * (tw + pad) + pad,
                             rowsn * (th + pad) + pad), "#141414")
    allsl = [s[3] for s in slides] + [end]
    for i, s in enumerate(allsl):
        r, c = divmod(i, cols)
        sheet.paste(s.resize((tw, th), Image.LANCZOS),
                    (pad + c * (tw + pad), pad + r * (th + pad)))
    sheet.save(os.path.join(outdir, "CONTACT-SHEET.jpg"), quality=93)
    print("contact sheet ->", os.path.join(outdir, "CONTACT-SHEET.jpg"))


if __name__ == "__main__":
    main()
