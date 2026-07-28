#!/usr/bin/env python3
"""
Correct a plate whose sign was generated at the wrong physical size.

Why this is needed
------------------
Max: "the sizing isn't right for the sage sign. It just looks like a Chinese AI
photo."

He was right and it measures out. The real sign is 570mm wide. Read against
three independent anchors in the dog plate's own room:

    panelling dado (floor->rail, 680px @ ~1050mm)  sign should be 369px  (2.08x over)
    golden retriever lying, nose to rump (800px)   sign should be 480px  (1.60x over)
    ceramic dog bowl diameter (174px @ ~180mm)     sign should be 551px  (1.39x over)

It measures 768px. So it is roughly 1.6x too big — a 90cm plaque instead of a
57cm one. And note the anchors disagree with each other by 1.5x, which means the
generated ROOM is not internally consistent on scale either. That inconsistency
is its own tell, and it is not fixable by resizing the sign.

What this does
--------------
Shrinks the PHOTOGRAPHED sign rather than redrawing it, so all the realism the
plate paid for survives — material, border, shaped ends, drilled holes, edge
highlights, and the contact shadow, which scales with it.

The move that makes it clean is working in RATIO space, not pixel space:

  1. Estimate the wall behind the sign by fitting a robust 2D quadratic to a ring
     of wall pixels around it. The wall is plain emulsion with a soft gradient, so
     a quadratic fits it to within grain.
  2. ratio = patch / wall_estimate. The sign reads far from 1, the contact shadow
     reads slightly under 1, and clean wall reads exactly 1.
  3. Scale that RATIO map, not the pixels, and multiply it back onto the wall.

Scaling pixels would drag the old wall tone along with the sign and leave a
visible rectangle. Scaling the ratio means sign and shadow shrink together and
anything that was wall stays wall, automatically.

Usage
-----
    python3 rescale_plate.py --plate dog --scale 0.625 --out plate-dog-rescaled.png
"""

import argparse, json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
from reprint import _blur                       # noqa: E402


def fit_wall(plate_np, box, ring=110, iters=3):
    """Robust 2D quadratic fit to the wall around `box`, evaluated inside it."""
    x0, y0, x1, y1 = box
    H, W = plate_np.shape[:2]
    rx0, ry0 = max(0, x0 - ring), max(0, y0 - ring)
    rx1, ry1 = min(W, x1 + ring), min(H, y1 + ring)

    yy, xx = np.mgrid[ry0:ry1, rx0:rx1]
    outside = ~((xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1))

    sx = (xx - x0) / max(1, x1 - x0)
    sy = (yy - y0) / max(1, y1 - y0)
    A = np.stack([np.ones_like(sx), sx, sy, sx * sx, sx * sy, sy * sy], -1)

    out = np.empty((y1 - y0, x1 - x0, 3), float)
    gy, gx = np.mgrid[0:y1 - y0, 0:x1 - x0]
    gsx = gx / max(1, x1 - x0)
    gsy = gy / max(1, y1 - y0)
    G = np.stack([np.ones_like(gsx), gsx, gsy, gsx * gsx, gsx * gsy, gsy * gsy], -1)

    for c in range(3):
        vals = plate_np[ry0:ry1, rx0:rx1, c]
        keep = outside.copy()
        coef = None
        for _ in range(iters):
            # Robust: the ring can clip a coat or a hook, and one dark outlier
            # tilts a least-squares plane badly. Refit after dropping >2 sigma.
            M = A[keep]
            coef, *_ = np.linalg.lstsq(M, vals[keep], rcond=None)
            resid = vals - A @ coef
            s = resid[keep].std()
            keep = outside & (np.abs(resid) < 2.0 * max(s, 1.0))
        out[:, :, c] = G @ coef
    return out


def rescale_sign(plate, cfg, scale, dy=0):
    """Shrink the photographed sign (and its shadow) about its own centre."""
    a = np.asarray(plate.convert("RGB"), dtype=float)
    sx0, sy0, sx1, sy1 = cfg["box"]

    # Work on a margin around the sign so the contact shadow travels with it.
    mw = int(round((sx1 - sx0) * 0.10))
    mh = int(round((sy1 - sy0) * 0.55))          # shadow falls mostly below
    bx0, by0 = max(0, sx0 - mw), max(0, sy0 - mh)
    bx1, by1 = min(a.shape[1], sx1 + mw), min(a.shape[0], sy1 + mh)
    box = (bx0, by0, bx1, by1)

    wall = fit_wall(a, box)
    patch = a[by0:by1, bx0:bx1]

    # Harmonise the fit against the REAL wall. A quadratic gets the shape right but
    # can sit a couple of levels off, and that showed up as a faint rectangular
    # ghost exactly where the old sign had been — the eye finds a flat tonal patch
    # even at 2 levels. So: measure the residual wherever the patch IS clean wall,
    # fill that residual across the sign by normalised convolution, and add it
    # back. The estimate now agrees with the real wall at every boundary and only
    # interpolates where it has to.
    rough = patch / np.maximum(wall, 1.0)
    cleanw = ((np.abs(rough.mean(2) - 1.0) < 0.012).astype(float))[:, :, None]
    resid = (patch - wall) * cleanw
    num = _blur(resid, 60.0)
    den = _blur(np.repeat(cleanw, 3, axis=2), 60.0)
    wall = wall + num / np.maximum(den, 1e-3)

    ratio = patch / np.maximum(wall, 1.0)

    # Scale the ratio map about the sign's centre, padding with 1.0 (= clean wall)
    ph, pw = ratio.shape[:2]
    nw, nh = max(1, int(round(pw * scale))), max(1, int(round(ph * scale)))
    r_img = Image.fromarray(np.clip(ratio * 128.0, 0, 255).astype(np.uint8))
    r_small = np.asarray(r_img.resize((nw, nh), Image.LANCZOS), dtype=float) / 128.0

    new_ratio = np.ones_like(ratio)
    cx = (sx0 + sx1) / 2.0 - bx0
    cy = (sy0 + sy1) / 2.0 - by0
    # keep the sign's own centre fixed, then allow a deliberate vertical nudge
    ox = int(round(cx - (cx * scale)))
    oy = int(round(cy - (cy * scale))) + dy
    ox = max(0, min(pw - nw, ox))
    oy = max(0, min(ph - nh, oy))
    new_ratio[oy:oy + nh, ox:ox + nw] = r_small

    # Touch ONLY what has to change: where the old sign/shadow must be erased, and
    # where the new one must be drawn. Replacing the whole patch with
    # wall * new_ratio left a faint rectangle, because a quadratic fit of the wall
    # is close but not equal to the real wall, and the eye finds a straight tonal
    # seam instantly. Outside those two areas the original pixels survive
    # untouched, so there is no seam to find.
    def active(r, grow=9):
        d = np.abs(r.mean(2) - 1.0)
        m = (d > 0.012).astype(float)
        m = _blur(m, grow)
        return np.clip(m * 3.0, 0.0, 1.0)

    w = np.clip(active(ratio) + active(new_ratio), 0.0, 1.0)
    w = _blur(w, 3.0)[:, :, None]

    rebuilt = wall * new_ratio

    # the fitted wall is perfectly smooth; give the erased area back the plate's grain
    g = a[by0:by1, bx0:bx1].mean(2)
    hp = g - _blur(g, 1.6)
    sd = 1.4826 * float(np.median(np.abs(hp - np.median(hp))))
    rng = np.random.default_rng(11)
    clean = ((new_ratio.mean(2) > 0.995) & (new_ratio.mean(2) < 1.005)).astype(float)
    n = rng.normal(0.0, min(max(sd, 0.4), 2.5), (by1 - by0, bx1 - bx0))
    rebuilt = rebuilt + (n * clean)[:, :, None]

    out = a.copy()
    out[by0:by1, bx0:bx1] = patch * (1 - w) + rebuilt * w

    new_box = [int(round(bx0 + ox + (sx0 - bx0) * scale)),
               int(round(by0 + oy + (sy0 - by0) * scale)),
               int(round(bx0 + ox + (sx1 - bx0) * scale)),
               int(round(by0 + oy + (sy1 - by0) * scale))]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), new_box


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", required=True)
    ap.add_argument("--scale", type=float, required=True)
    ap.add_argument("--dy", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(HERE, "plates.json")))[a.plate]
    plate = Image.open(os.path.join(HERE, cfg["image"]))
    img, new_box = rescale_sign(plate, cfg, a.scale, a.dy)
    img.save(a.out)
    print("wrote %s\nnew sign box: %s  (%dpx wide)"
          % (a.out, new_box, new_box[2] - new_box[0]))


if __name__ == "__main__":
    main()
