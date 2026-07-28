#!/usr/bin/env python3
"""
Run every product gate on a generated held-sign image, before Max ever sees it.

    python3 qc.py image.png --sign x0,y0,x1,y1 --shoulders x0,x1 [--colourway BLACK]

Why this exists
---------------
Max has now caught four separate product faults by eye that my ad-hoc checks
missed, and each one measured out afterwards:

  crushed ink      "I can tell it was used from the SVG"   ink/panel ratio 0.034 vs 0.14-0.21 real
  oversized sign   "that looks massive"                    sign/shoulder 2.19 vs 1.21 true
  missing border   "what the fuck is that?"                border absent entirely
  wrong border     "the border is not the right size"      22.6% of sign height vs 9.9% canonical

Every one was cheap to measure and expensive to miss. Ad-hoc checking is the
problem: I measured whatever I happened to suspect, so a new fault class got
through each round. This runs all of them every time.

The boxes are passed in by hand on purpose. Automatic sign detection was tried
and abandoned — it latched onto walls, navy t-shirts and windows, and reported a
sign as "100% of frame width", which produced confidently wrong numbers. A wrong
measurement is worse than no measurement, so the operator supplies the box.
"""

import argparse
import json
import os
import sys

import numpy as np
from PIL import Image

# ---- canon, from build.py / the audited PSD -------------------------------
SIGN_MM_W, SIGN_MM_H = 570.0, 125.0
BORDER_MM = 12.4
BORDER_PCT = BORDER_MM / SIGN_MM_H * 100.0        # 9.92% of sign height

# ---- gates ---------------------------------------------------------------
# INK. Two corrections in one day, both because the gate contradicted Max's eye:
#
#   v1  a 0.12-0.24 window   -> would have failed the Freya blue master at 0.440,
#                               which he rated the best image in the whole audit.
#                               Pale colourways legitimately sit high. Made a floor.
#   v2  a 0.11 floor         -> failed W1 at 0.093, which he approved, and W2 at
#                               0.106. Both are dim exposures, and that is the flaw
#                               in a pure ratio: veiling glare lifts ink by an
#                               ABSOLUTE amount, so a dimly lit sign legitimately
#                               has a lower ratio than a brightly lit one. The ratio
#                               is not exposure-invariant, which I had assumed.
#
# v3 tests what actually distinguishes the failures: is the ink lifted off zero at
# all? Rejected "looks like an SVG" plate: ink luminance 7.8. Everything Max has
# passed: 18.7, 20.0, 34, 47, 96. An absolute floor separates them cleanly, and a
# very low ratio floor still catches a black panel that has gone flat.
INK_LUMA_MIN = 15.0
INK_RATIO_MIN = 0.07
INK_RATIO_BLACK_TYPICAL = (0.09, 0.24)

# sign width / shoulder width. Calibrated on a controlled pair Max judged by eye:
# the image he called right measured 1.33, the one he called "really off" 2.19,
# against a true flat-on 1.21 for a man. Women's shoulders are narrower, so the
# same sign reads larger; two passing images measured 1.60 and 1.64.
SHOULDER_RATIO = {"male": (1.20, 1.50), "female": (1.40, 1.75)}

BORDER_TOL = 3.5          # percentage points either side of canonical
BORDER_ASYMMETRY_MAX = 2.5  # top vs bottom, percentage points


def sign_metrics(img, box, shoulders, sex, colourway):
    a = np.asarray(img.convert("RGB"), dtype=float)
    H, W = a.shape[:2]
    x0, y0, x1, y1 = box
    results = []

    # --- ink / panel contrast, measured well inside the panel
    pad_x = int((x1 - x0) * 0.05)
    pad_y = int((y1 - y0) * 0.14)
    q = a[y0 + pad_y:y1 - pad_y, x0 + pad_x:x1 - pad_x].reshape(-1, 3)
    ink = np.percentile(q, 4, axis=0)
    panel = np.percentile(q, 90, axis=0)
    ratio = ink.mean() / max(panel.mean(), 1.0)
    luma = ink.mean()
    results.append(("ink lifted off black", "%.1f" % luma,
                    ">= %.0f" % INK_LUMA_MIN, luma >= INK_LUMA_MIN,
                    "" if luma >= INK_LUMA_MIN else "  <-- the vector-black signature"))
    note = ""
    if colourway == "BLACK":
        lo, hi = INK_RATIO_BLACK_TYPICAL
        if not (lo <= ratio <= hi):
            note = "  (unusual for black; check exposure)"
    results.append(("ink/panel contrast", "%.3f" % ratio,
                    ">= %.2f" % INK_RATIO_MIN, ratio >= INK_RATIO_MIN, note))
    results.append(("panel brightness", "%.0f" % panel.mean(), "context only", True,
                    "  (a dim panel legitimately lowers the contrast ratio)"))

    # --- blown highlights on the panel
    blown = int((a[y0:y1, x0:x1].max(2) > 253).sum())
    area = max((y1 - y0) * (x1 - x0), 1)
    pct = 100.0 * blown / area
    results.append(("panel highlight clipping", "%.2f%%" % pct, "< 0.50%",
                    pct < 0.5, ""))

    # --- scale against shoulders
    sg = x1 - x0
    shw = shoulders[1] - shoulders[0]
    sr = sg / max(shw, 1)
    lo, hi = SHOULDER_RATIO[sex]
    results.append(("sign / shoulder width", "%.2f" % sr,
                    "%.2f-%.2f (%s)" % (lo, hi, sex), lo <= sr <= hi, ""))

    # --- printed border: NOT AUTOMATED, and deliberately so.
    #
    # Three methods were tried and all three produced numbers that contradicted
    # Max's own verdicts:
    #   1. luminance column, searching beyond the box  -> same image gave 10.8%/7.6%
    #      and then 24.9%/6.2%, because a dim room and a dark jumper read as border
    #   2. luminance column, strictly inside the box    -> failed an image Max approved
    #   3. panel aspect ratio (background-independent)  -> ranked the image with NO
    #      border at all as the closest to canonical
    #
    # The root difficulty is that the printed border and a dark background are the
    # same thing to a luminance test, and the lettering breaks any row-coverage test
    # of the panel. Getting it right needs actual segmentation of the sign contour.
    #
    # So it stays a human check. Max has caught both border faults instantly by eye
    # ("what the fuck is that?" for a missing border, "the border is not the right
    # size" for a mis-sized one), and a gate that fires falsely is worse than no gate
    # because it trains everyone to ignore it.
    #
    # Reference for the eye: the printed border is a uniform 12.4mm inset on a 125mm
    # sign — 9.9% of the sign's height, the SAME on all four sides.

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--sign", required=True, help="x0,y0,x1,y1 of the sign's OUTER edge")
    ap.add_argument("--shoulders", required=True, help="x0,x1 of the shoulders")
    ap.add_argument("--sex", default="female", choices=["male", "female"])
    ap.add_argument("--colourway", default="BLACK")
    a = ap.parse_args()

    box = tuple(int(v) for v in a.sign.split(","))
    sh = tuple(int(v) for v in a.shoulders.split(","))
    img = Image.open(a.image)

    rows = sign_metrics(img, box, sh, a.sex, a.colourway)
    print("QC  %s" % os.path.basename(a.image))
    print("-" * 78)
    fails = 0
    for name, got, want, ok, note in rows:
        if not ok:
            fails += 1
        print("  %-26s %-10s want %-22s %s%s"
              % (name, got, want, "PASS" if ok else "FAIL", note))
    print("-" * 78)
    # Wording, heart and mounting holes are not measurable here — they need eyes.
    print("  MANUAL, still required — these are NOT measured above:")
    print("    * printed border: uniform 9.9% of sign height, same on all four sides")
    print("      (three automation attempts all disagreed with Max's eye — see source)")
    print("    * wording character-exact, both lines")
    print("    * no mounting holes anywhere on the panel")
    print("    * heart present if and only if it is a wedding sign, and only one")
    print("    * hands gripping only the extreme ends, no wording obscured")
    print()
    print("RESULT: %s" % ("ALL GATES PASS" if not fails else "%d GATE(S) FAILED" % fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
