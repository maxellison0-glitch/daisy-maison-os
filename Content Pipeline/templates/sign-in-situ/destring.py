"""Paint the feather-toy string out of every frame.

Max: "The string: I don't like that we've overlaid it."

It is a taut line, so its position is linear in y — fit a line rather than
tracking per-row, which makes the result stable frame to frame instead of
wobbling. Then inpaint horizontally across it: the wall is smooth, so a linear
blend between the pixels either side is exact to within grain.
"""
import numpy as np


def _hblur(row, k=41):
    pad = np.pad(row, (k // 2, k // 2), mode="edge")
    c = np.cumsum(np.insert(pad, 0, 0))
    return (c[k:] - c[:-k]) / k


def find_string(a, y0, y1, xlo, xhi, step=6):
    """Robust straight-line fit to the string's x position over rows y0..y1."""
    lum = a.mean(2)
    ys, xs = [], []
    for y in range(y0, y1, step):
        row = lum[y, xlo:xhi]
        hp = row - _hblur(row)
        j = int(np.argmax(hp))
        if hp[j] > 1.5:                      # a real ridge, not just grain
            ys.append(y)
            xs.append(xlo + j)
    if len(ys) < 12:
        return None
    ys = np.asarray(ys, float)
    xs = np.asarray(xs, float)
    for _ in range(3):                       # least squares, drop outliers, refit
        A = np.stack([ys, np.ones_like(ys)], 1)
        coef, *_ = np.linalg.lstsq(A, xs, rcond=None)
        resid = xs - A @ coef
        keep = np.abs(resid) < max(2.5 * resid.std(), 1.5)
        if keep.sum() < 10:
            break
        ys, xs = ys[keep], xs[keep]
    return coef                              # x = coef[0]*y + coef[1]


def erase(a, coef, y0, y1, half=5, feather=7):
    """Replace a band centred on the line with a horizontal linear blend."""
    out = a.copy()
    H, W = a.shape[:2]
    for y in range(max(0, y0), min(H, y1)):
        xc = coef[0] * y + coef[1]
        lo = int(round(xc - half))
        hi = int(round(xc + half))
        a0, a1 = lo - feather, hi + feather
        if a0 < 1 or a1 > W - 2:
            continue
        left = a[y, a0 - 1:a0 + 1].mean(0)
        right = a[y, a1:a1 + 2].mean(0)
        n = a1 - a0
        t = np.linspace(0.0, 1.0, n)[:, None]
        out[y, a0:a1] = left[None, :] * (1 - t) + right[None, :] * t
    return out
