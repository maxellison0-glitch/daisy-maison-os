#!/usr/bin/env python3
"""
sign-reprint — put ANY wording onto an APPROVED photographic plate, for free.

Why this exists
---------------
Every wording variant used to cost a credit-paid print-edit generation. That
capped us at a handful of designs and made a carousel as expensive as a film.
But the expensive part of the print-edit was never the printing — it was
establishing the *photograph*: real material, real border, real shaped ends,
real mounting holes, real contact shadow, real lens character.

Once a plate is approved, all of that is already solved and permanent. The only
thing that changes between designs is ink inside the panel. So we do that
locally, at zero credits, unlimited times.

The rule from REFERENCE_PACK.md is respected exactly, not bent:

    the approved product PHOTOGRAPH is the authority for the object
    the build.py SVG is the printing, and ONLY the printing

This script never touches the photographed border, the shaped ends, the
mounting holes, the edge highlights or the wall shadow. It replaces ink strictly
inside the panel, and it relights that ink from the plate's own light.

Relighting (the fix for "it looks a little bit fake / too perfect")
------------------------------------------------------------------
A generated panel comes back optically flat. Measured on the approved cat plate:
cream held 239/231/222 across all 880px of the sign's width, under 1.5 levels of
variation, while the wall behind it swung hard warm in the same daylight. Real
matte cream in that room picks up 8-15 levels of falloff plus a colour-temp
shift toward the window. Flatness is what the eye reads as CGI.

So we do two things:
  1. TRANSFER the plate's own low-frequency field onto the new ink, so the new
     print inherits whatever incident the photograph did have.
  2. SYNTHESISE the incident the plate is missing, sampled from the wall
     immediately above the sign. The wall is lit by the same light, so its
     across-width gradient is ground truth for direction and strength. Damped,
     because matte board picks up less range than emulsion paint.

Then matched grain and a matched focus fall-off, so the reprinted panel sits in
the same optical layer as the rest of the frame.

Usage
-----
    python3 reprint.py --plate cat --line1 "THE CAT'S HOUSE" \
                       --line2 "YOU JUST PAY THE MORTGAGE" --out out.png

    python3 reprint.py --plate cat --batch designs.txt --outdir carousel/
"""

import argparse, base64, json, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BUILD = os.path.join(REPO, "projects", "daisy-street-sign", "artwork", "build.py")
PLATES = os.path.join(HERE, "plates.json")

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# canonical product geometry, from build.py / the audited PSD
SIGN_MM_W, SIGN_MM_H = 570.0, 125.0
BORDER_MM = 12.4
# mounting holes, from the same LightBurn source build.py reads
HOLES_MM = ((23.31, 63.735, 2.0), (546.0, 61.5, 2.0))


# ----------------------------------------------------------------- rasterise
def rasterise_svg(svg_path, w, h):
    """SVG -> RGBA PNG at an exact pixel size, transparent background.

    Anisotropic on purpose. A wall-mounted sign is foreshortened, so the
    plate's sign is not 4.56:1 on screen; scaling to the measured box is what
    lands the new print exactly on the photographed silhouette.
    """
    svg = open(svg_path, "rb").read()

    # Rasterise at the sign's TRUE 570:125 ratio, then squeeze to the target box
    # in PIL. Two earlier attempts went through Chromium's aspect handling and
    # both misregistered: 'xMidYMid meet' letterboxed the sign inside the box,
    # and 'none' silently rendered to only 86% of the height, which then got
    # stretched and pushed line 2 out through the bottom border. PIL's resize is
    # exact and fully under our control, so the anisotropy belongs here, not
    # there. Supersampled for clean glyph edges.
    ss = max(2, int(math.ceil(2600.0 / w)))
    rw = w * ss
    rh = int(round(rw * SIGN_MM_H / SIGN_MM_W))

    src = "data:image/svg+xml;base64," + base64.b64encode(svg).decode()
    html = (
        "<!doctype html><meta charset=utf8>"
        "<style>*{margin:0;padding:0}html,body{background:transparent;"
        f"width:{rw}px;height:{rh}px;overflow:hidden}}"
        f"img{{display:block;width:{rw}px;height:{rh}px}}</style>"
        f"<img src='{src}'>"
    )
    # Headless Chromium's usable viewport is ~87px shorter than the window it is
    # given, and it pads the screenshot back out to the window size with
    # transparency. That silently amputated the bottom of every sign — a 211px
    # window painted only ~120px, a 579px window only 492px. Ask for extra
    # height, then take the region we actually wanted.
    VIEWPORT_SLACK = 240

    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, "p.html")
        op = os.path.join(td, "o.png")
        open(hp, "w").write(html)
        subprocess.run(
            [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
             "--hide-scrollbars", "--default-background-color=00000000",
             f"--window-size={rw},{rh + VIEWPORT_SLACK}",
             f"--screenshot={op}", "file://" + hp],
            check=True, capture_output=True,
        )
        img = Image.open(op).convert("RGBA")
        if img.size[0] != rw or img.size[1] < rh:
            raise RuntimeError("chromium returned %s, wanted >=%s" % (img.size, (rw, rh)))
        img = img.crop((0, 0, rw, rh))

    # Gate the raster before it can misregister anything downstream. The 409-vertex
    # contour fills its 570x125 viewBox exactly, so the sign must fill this render
    # edge to edge. Anything less means the aspect handling has moved again, and a
    # silent 14% shortfall is precisely the bug this replaced.
    bbox = img.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox is None:
        raise RuntimeError("empty SVG render")
    fill_x = (bbox[2] - bbox[0]) / rw
    fill_y = (bbox[3] - bbox[1]) / rh
    if fill_x < 0.99 or fill_y < 0.99:
        raise RuntimeError(
            "sign does not fill its raster (x %.3f, y %.3f) — aspect handling "
            "has changed; registration would be wrong" % (fill_x, fill_y))

    return img.resize((w, h), Image.LANCZOS)


def render_face(line1, line2, w, h, colourway=None, heart=False, fit=486):
    env = dict(os.environ)
    if colourway:
        env["SIGN_COLOURWAY"] = colourway
    env["SIGN_HEART"] = "1" if heart else "0"
    with tempfile.TemporaryDirectory() as td:
        svg = os.path.join(td, "face.svg")
        subprocess.run(
            [sys.executable, BUILD, "REPRINT", line1, line2, str(fit), svg],
            check=True, capture_output=True, env=env,
        )
        return rasterise_svg(svg, w, h)


# ------------------------------------------------------------------- masking
def panel_mask(face_rgba, w, h, safety=3.0):
    """Mask of the PANEL INTERIOR only — never the border or the shaped ends.

    Eroded from the render's own alpha by the true border width, scaled
    separately in x and y because the paste box is anisotropic.
    """
    ex = BORDER_MM * (w / SIGN_MM_W) + safety
    ey = BORDER_MM * (h / SIGN_MM_H) + safety
    r = int(round(max(ex, ey)))

    m = face_rgba.split()[3].point(lambda v: 255 if v > 128 else 0)

    # PIL's rank filters replicate the edge pixel at the image boundary, so a
    # silhouette touching the frame does not erode inward from that side at all
    # — the first build left the mask running to x=0 and x=w-1, straight over the
    # photographed border. Pad with transparency first so every side has
    # somewhere to erode from, then crop back.
    pad = r + 4
    canvas = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    canvas.paste(m, (pad, pad))
    m = canvas

    step = 9                                   # MinFilter only takes small odd k
    n, rem = divmod(r, (step - 1) // 2)
    for _ in range(n):
        m = m.filter(ImageFilter.MinFilter(step))
    if rem:
        m = m.filter(ImageFilter.MinFilter(2 * rem + 1))

    m = m.crop((pad, pad, pad + w, pad + h))

    # Punch the mounting holes back OUT of the mask. The holes fall ~11mm inside
    # the panel boundary, so they were being overwritten — and build.py draws them
    # as a hairline ring (correct for a cut file) while the photograph has real
    # drilled holes with real shadow in them. The holes are part of the
    # manufactured object, not the printing, so the photograph keeps them.
    d = ImageDraw.Draw(m)
    for hx, hy, hr in HOLES_MM:
        cx, cy = hx * w / SIGN_MM_W, hy * h / SIGN_MM_H
        rx, ry = hr * w / SIGN_MM_W + 2.5, hr * h / SIGN_MM_H + 2.5
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=0)

    return m.filter(ImageFilter.GaussianBlur(1.1))   # 1px feather, no seam


# ---------------------------------------------------------------- relighting
def _blur1d(a, radius, axis):
    """Separable moving-average pass with edge clamping, on floats."""
    if radius < 1:
        return a
    a = np.moveaxis(a, axis, 0)
    n = a.shape[0]
    pad = np.concatenate([np.repeat(a[:1], radius, 0), a,
                          np.repeat(a[-1:], radius, 0)], axis=0)
    c = np.cumsum(pad, axis=0)
    c = np.concatenate([np.zeros_like(c[:1]), c], axis=0)
    out = (c[2 * radius + 1: 2 * radius + 1 + n] - c[0:n]) / (2 * radius + 1)
    return np.moveaxis(out, 0, axis)


def _blur(a, sigma):
    """Gaussian-equivalent blur on a float array, in float throughout.

    PIL's GaussianBlur refuses mode 'F' and there is no scipy here, so this is
    three box passes — the standard approximation, and indistinguishable at the
    radii we use. Staying in float matters: the field is a RATIO, so quantising
    to 8-bit first throws away exactly the precision we need.
    """
    squeeze = a.ndim == 2
    if squeeze:
        a = a[:, :, None]
    r = max(1, int(round(sigma * 0.79)))     # 3 box passes ~= gaussian(sigma)
    out = a.astype(float)
    for _ in range(3):
        out = _blur1d(_blur1d(out, r, 0), r, 1)
    return out[:, :, 0] if squeeze else out


def panel_illumination(plate_np, sigma=90.0):
    """Estimate the panel's TRUE illumination, immune to ink coverage.

    A plain blur is not good enough here and the first build proved it: blurring
    an inked panel drags the field down wherever the letters are, so the ratio
    against a fresh render spikes across the caps and blows the cream to 255.

    Instead: normalised convolution over the cream pixels only. Weight = 1 on
    unlit-by-ink panel, 0 on ink; blur numerator and weight together and divide.
    That reconstructs the illumination *underneath* the old letters, which is
    exactly the surface the new letters will sit on.
    """
    lum = plate_np.mean(2)

    # Adaptive cream threshold. A fixed cut at 140 works for black ink but not
    # for the pale colourways: sage lettering sits around 185, well above 140, so
    # it would be sampled as if it were panel and flatten the field it is meant
    # to measure. The 70th percentile of the sign region lands in cream on every
    # colourway, because the panel always outweighs the ink.
    thr = max(120.0, float(np.percentile(lum, 70)) - 6.0)
    w = (lum > thr).astype(float)[:, :, None]
    num = _blur(plate_np * w, sigma)
    den = _blur(np.repeat(w, 3, axis=2), sigma)
    return num / np.maximum(den, 1e-3)


def shading_field(plate_np, face_np, panel_rgb, wall_band, damp=0.55, sigma=90.0):
    """Light field to multiply onto the new ink.

    Two components:
      transfer  — the plate's reconstructed panel illumination over the render's
                  flat panel colour, so the new print inherits the photograph's
                  exposure and colour temperature exactly.
      synth     — the across-width gradient of the wall above the sign,
                  normalised and damped, supplying the falloff the flat
                  generated panel is missing.
    """
    h, w = face_np.shape[:2]

    illum = panel_illumination(plate_np, sigma)
    transfer = illum / np.maximum(np.asarray(panel_rgb, dtype=float), 1.0)
    transfer = np.clip(transfer, 0.80, 1.10)

    # --- synthesised incident, from the wall's own gradient
    band = wall_band.astype(float)                      # (bh, w, 3)
    col = band.mean(axis=0)                             # (w, 3) per-column
    col = _blur(col[None, :, :], 28)[0]
    ratio = col / np.maximum(col.mean(axis=0, keepdims=True), 1.0)
    ratio = 1.0 + (ratio - 1.0) * damp                  # matte board, damped
    ratio = np.clip(ratio, 0.86, 1.16)
    synth = np.repeat(ratio[None, :, :], h, axis=0)

    return transfer * synth


def match_grain(out_np, plate_np, mask_np, seed=7):
    """Add grain matched to the plate's own noise inside the panel."""
    g = plate_np.mean(2)
    hp = g - _blur(g, 1.6)
    sel = hp[mask_np > 0.5]

    # Robust estimate, via median absolute deviation. A plain std over the panel
    # is measuring the LETTER EDGES, not the grain — it came back at 10 on the
    # dog plate and 24 on the cat plate, both of which just pinned the cap and
    # dumped visible mottle over the reprint. MAD ignores the sparse high-contrast
    # edges and reports the actual film-grain floor, which is around 1.
    if sel.size:
        sigma = 1.4826 * float(np.median(np.abs(sel - np.median(sel))))
    else:
        sigma = 1.0
    sigma = min(max(sigma, 0.4), 2.2)
    rng = np.random.default_rng(seed)
    n = rng.normal(0.0, sigma, out_np.shape[:2])[:, :, None]
    return out_np + n * mask_np[:, :, None]


# --------------------------------------------------------------- ink realism
def ink_grade(region, sign_mask, target_ratio, tint=(1.00, 0.92, 0.97)):
    """Lift the sign's blacks to a real photograph's measured response.

    THIS IS THE STEP THAT KILLS THE "I can tell it came from the SVG" TELL.

    Max could see it and could not name it; it measures out unambiguously. Ink
    luminance and ink/panel contrast ratio, same product, same colourway:

        real photograph, real sign, real room ....  38.5   ratio 0.213
        real photograph, border sample ..........  27.3   ratio 0.140
        the generated plate .....................   7.8   ratio 0.034
        a reprint on that plate .................  11.6   ratio 0.050

    The generated sign is four to six times more contrasty than the real object
    ever photographs. Vector black is #000 and renders as #000; real black ink in
    a real room never comes back below roughly 25-45, because ambient light
    scatters off the panel into the ink, the lens adds veiling glare, and the ink
    is a satin surface rather than a void. Absolute blacks in a lit interior are
    a rendering signature, and the eye reads them instantly as synthetic even
    when it cannot say why.

    The correction is the physics in reverse: glare ADDS a roughly constant
    amount of light, then exposure renormalises. So this is an affine map chosen
    so the panel level is left exactly where it is and the ink lands on the
    target ratio — geometry, edges and texture all untouched.

    Applied across the WHOLE sign silhouette, letters and printed border alike.
    Grading only the panel would leave the reprinted letters lighter than the
    photographed border around them, which is a worse artefact than the one it
    fixes. This is a grade, not a redraw: no pixel moves.
    """
    a = region.astype(float)
    lum = a.mean(2)
    inside = sign_mask > 0.5
    if not inside.any():
        return a

    panel = np.percentile(a[inside], 88, axis=0)
    ink = np.percentile(a[inside], 4, axis=0)

    target = panel * target_ratio * np.asarray(tint, dtype=float)
    denom = np.maximum(panel - ink, 1.0)
    alpha = panel * (1.0 - target / np.maximum(panel, 1.0)) / denom
    alpha = np.clip(alpha, 0.55, 1.0)
    beta = panel - alpha * panel

    graded = a * alpha + beta
    m = sign_mask[:, :, None]
    return a * (1 - m) + graded * m


# ------------------------------------------------------------------ the swap
def reprint(plate_cfg, line1, line2, heart=False, fit=486, focus=0.45):
    plate = Image.open(os.path.join(HERE, plate_cfg["image"])).convert("RGB")
    x0, y0, x1, y1 = plate_cfg["box"]
    w, h = x1 - x0, y1 - y0

    face = render_face(line1, line2, w, h,
                       colourway=plate_cfg.get("colourway"), heart=heart, fit=fit)
    mask = panel_mask(face, w, h)

    region = plate.crop((x0, y0, x1, y1))
    plate_np = np.asarray(region, dtype=float)
    face_np = np.asarray(face, dtype=float)

    # wall band immediately above the sign — same light, honest gradient
    bh = plate_cfg.get("wall_band", 90)
    wall = np.asarray(plate.crop((x0, max(0, y0 - bh), x1, y0)), dtype=float)

    # The render's flat panel colour, read off the render itself rather than
    # hard-coded, so a colourway change stays correct.
    #
    # By percentile, not by mean over a brightness mask. Sage lettering sits at
    # luminance 184, so a mask-and-mean pulled the "panel" colour down toward the
    # ink, the field divided by too small a number, and the whole sage panel blew
    # out to near-white with washed-out letters. The panel is both the majority of
    # the sign area and the brightest part of it on every colourway, so a high
    # percentile lands in clean panel every time.
    fa = face_np[:, :, 3]
    sel = fa > 200
    panel_rgb = (np.percentile(face_np[:, :, :3][sel], 85, axis=0) if sel.any()
                 else np.array([242.0, 238.0, 227.0]))

    field = shading_field(plate_np, face_np, panel_rgb, wall,
                          damp=plate_cfg.get("damp", 0.55))
    lit = face_np[:, :, :3] * field

    m = np.asarray(mask, dtype=float) / 255.0
    out = plate_np * (1 - m[:, :, None]) + lit * m[:, :, None]
    out = match_grain(out, plate_np, m)

    patch = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    if focus:                                   # match the plate's focus layer
        soft = patch.filter(ImageFilter.GaussianBlur(focus))
        patch = Image.composite(soft, patch, mask)

    # Ink realism grade over the whole sign silhouette. Off unless the plate
    # declares a target ratio, so existing behaviour is unchanged without opt-in.
    ratio = plate_cfg.get("ink_ratio")
    if ratio:
        sign_alpha = np.asarray(
            face.split()[3].point(lambda v: 255 if v > 128 else 0)
            .filter(ImageFilter.GaussianBlur(0.8)), dtype=float) / 255.0
        graded = ink_grade(np.asarray(patch, dtype=float), sign_alpha, ratio,
                           tuple(plate_cfg.get("ink_tint", (1.00, 0.92, 0.97))))
        patch = Image.fromarray(np.clip(graded, 0, 255).astype(np.uint8))

    final = plate.copy()
    final.paste(patch, (x0, y0))
    return final


# ----------------------------------------------------------------------- cli
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", required=True)
    ap.add_argument("--line1")
    ap.add_argument("--line2", default="")
    ap.add_argument("--heart", action="store_true")
    ap.add_argument("--fit", type=int, default=486)
    ap.add_argument("--out")
    ap.add_argument("--batch", help="TSV: line1<TAB>line2 per row")
    ap.add_argument("--outdir")
    a = ap.parse_args()

    cfg = json.load(open(PLATES))[a.plate]

    if a.batch:
        os.makedirs(a.outdir, exist_ok=True)
        rows = [r.rstrip("\n") for r in open(a.batch) if r.strip()]
        for i, row in enumerate(rows, 1):
            parts = (row.split("\t") + [""])[:2]
            img = reprint(cfg, parts[0], parts[1], heart=a.heart, fit=a.fit)
            p = os.path.join(a.outdir, "%02d.png" % i)
            img.save(p)
            print("%2d  %-28s %s" % (i, parts[0], p))
    else:
        img = reprint(cfg, a.line1, a.line2, heart=a.heart, fit=a.fit)
        img.save(a.out)
        print("wrote", a.out)


if __name__ == "__main__":
    main()
