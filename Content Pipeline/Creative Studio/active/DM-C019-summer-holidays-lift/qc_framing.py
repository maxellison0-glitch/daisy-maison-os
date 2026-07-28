#!/usr/bin/env python3
"""Reject a sign video whose wording runs off the side of the frame.

Take 01 of DM-C019 failed exactly this way and nothing caught it but an eye on a
filmstrip. The sign was fully inside the frame for the first 2.0 seconds and then
ran edge to edge for the remaining 4.0 - so the hold, the part a viewer actually
reads, had letters missing off both sides. A product reel whose product cannot be
read is worthless no matter how good the motion is, so this is a hard gate.

    python3 qc_framing.py delivery/DM-C019-native-raw.mp4

Exit 0 = every frame passes. Exit 1 = at least one frame is clipped.

How the sign is found
---------------------
Not by "darkest pixels" - the coat, the doorway and the shadows under the console
are all dark, and a naive dark-pixel extent returns the full frame width on every
frame regardless of the sign. That was the first attempt and it silently reported
a pass-shaped answer to the wrong question.

Instead: the sign's printed border is a long unbroken horizontal dark line, and
nothing else in a hallway is. So take the row with the most dark pixels and
measure the longest CONTIGUOUS run in it. That run is the border.

A frame fails when the run reaches within MARGIN_PX of either side, because the
shaped end - and usually a letter - is then outside the picture.
"""
import subprocess
import sys
import tempfile
import os
import glob

import numpy as np
from PIL import Image

MARGIN_PX = 24      # background that must stay visible beyond each end
DARK = 90           # 0-255 luma below which a pixel counts as printed border


def longest_dark_run(row):
    runs, start = [], None
    for x, v in enumerate(row):
        if v and start is None:
            start = x
        elif not v and start is not None:
            runs.append((x - start, start, x - 1))
            start = None
    if start is not None:
        runs.append((len(row) - start, start, len(row) - 1))
    return max(runs) if runs else (0, 0, 0)


def check(video):
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-v", "error", "-i", video,
                        os.path.join(td, "f%04d.png")], check=True)
        frames = sorted(glob.glob(os.path.join(td, "f*.png")))
        if not frames:
            print("No frames decoded from %s" % video)
            return 1

        bad = []
        for i, f in enumerate(frames):
            a = np.asarray(Image.open(f).convert("L"))
            dark = a < DARK
            r = int(dark.sum(1).argmax())
            w, L, R = longest_dark_run(dark[r])
            if L < MARGIN_PX or R > a.shape[1] - 1 - MARGIN_PX:
                bad.append((i + 1, i / 24.0, L, R, w))

        n = len(frames)
        if bad:
            print("FAIL - %d of %d frames clip the sign at a frame edge." % (len(bad), n))
            print("frame   t(s)     L      R   width")
            for fr, t, L, R, w in bad[:12]:
                print("%5d %6.2f %6d %6d %7d" % (fr, t, L, R, w))
            if len(bad) > 12:
                print("... and %d more" % (len(bad) - 12))
            print("\nThe sign must stay inside the frame with at least %dpx of "
                  "background beyond each end." % MARGIN_PX)
            return 1

        print("PASS - all %d frames keep the whole sign inside the frame." % n)
        return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: qc_framing.py <video.mp4>")
    sys.exit(check(sys.argv[1]))
