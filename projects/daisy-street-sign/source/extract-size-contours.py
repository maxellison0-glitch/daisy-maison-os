"""Extract the Large, Medium and Small cut contours into ONE portable JSON file.

RUN THIS ONCE, ON THE PC THAT HAS THE USB CUT FILES. Its output,
source/size-contours.json, is committed and is the source of truth from then on.
No other script in this project touches a USB drive, so the whole pipeline runs
on any machine that has only the git checkout.

Three things the naive reader gets wrong, all of which cost real time:

  * XForm is a CHILD element, not an attribute, and shapes reference a shared
    <VertList> by VertID - later shapes carry only an XForm. Miss that and most
    shapes parse as empty.
  * PrimList has TWO encodings. Usually "B0 1L1 2..." triples, but it can also be
    the bare sentinel "LineClosed", meaning join every vertex in order and close.
    Requiring triples makes every LineClosed path look empty - that is what hid
    the Large outline and made the Street Signs files appear to contain nothing.
  * Medium and Small are 8 vertices with 4 CUBIC corners, unlike Large's 409 flat
    vertices. Keeping vertices only turns the swept corners into straight
    chamfers, an error of up to 5.99 mm on Medium. The Beziers must be flattened.

WHERE SMALL COMES FROM
----------------------
There is no Small cut file. There does not need to be one: the Medium file's
XForm is a NON-UNIFORM scale (a=-1.55172, d=-1.41176) applied to local geometry
that spans exactly 290.000 x 85.000 mm - and 290*1.55172 = 450.0, 85*1.41176 =
120.0. Medium was authored by scaling the Small shape up, so the Small contour is
that same geometry at unit scale. It is read, not invented.

Validated against real production artwork
(E:\\Jigs\\Street Sign Jigs\\MINI\\MEDIUM ALL COLOUR 2023.psd, the 8-up bed at 300
dpi): buffering the 290x85 master outward by 1.00 mm reproduces the printed
silhouette to mean 0.182 mm, 100% of 2750 sampled edge points within 1.0 mm. That
1.00 mm also matches the 1.018 mm/edge bleed measured independently on the Medium
production PSD.

Do NOT use "MINI TRADITIONAL ROAD SIGN SHAPE.lbrn2" - that is the Personalised
Traditional Road Sign, a different product whose corners are deliberately not
scalloped (convex, area/hull 1.0000, against 0.9927 here).

    python extract-size-contours.py [--cut-files <dir>]
"""

import argparse
import glob
import json
import os
import re
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))

# Searched in order. The USB drive letter changes between machines, so the
# directory is looked up rather than hard-coded; --cut-files overrides.
SEARCH_HINTS = [
    r"{d}:\sean\max\cutting files street signs",
    r"{d}:\Daisy-Production\Street-Sign\Templates",
    r"{d}:\sean\max",
    r"{d}:\sean",
]

VERT_RE = re.compile(
    r"V(-?[\d.eE+-]+)\s+(-?[\d.eE+-]+)"
    r"(?:c0x(-?[\d.eE+-]+))?(?:c0y(-?[\d.eE+-]+))?"
    r"(?:c1x(-?[\d.eE+-]+))?(?:c1y(-?[\d.eE+-]+))?"
)
PRIM_RE = re.compile(r"([LB])\s*(\d+)\s+(\d+)")
STEPS = 48  # ~0.02 mm chord error on a 13 mm corner

# file, expected blank size, and whether to read the shape BEFORE its XForm.
# Small uses Medium's file at unit scale - see the module docstring.
SOURCES = {
    "large":  {"file": "LARGE SIGN.lbrn2",               "blank": (570.0, 125.0), "local": False},
    "medium": {"file": "MIDDLE size  halfbed JUN26.lbrn2", "blank": (450.0, 120.0), "local": False},
    "small":  {"file": "MIDDLE size  halfbed JUN26.lbrn2", "blank": (290.0,  85.0), "local": True},
}


def fnum(v):
    return float(v) if v not in (None, "") else None


def cubic(p0, c0, c1, p1):
    out = []
    for i in range(1, STEPS + 1):
        t = i / STEPS
        m = 1 - t
        out.append((
            m**3*p0[0] + 3*m*m*t*c0[0] + 3*m*t*t*c1[0] + t**3*p1[0],
            m**3*p0[1] + 3*m*m*t*c0[1] + 3*m*t*t*c1[1] + t**3*p1[1],
        ))
    return out


def find_cut_dir(explicit):
    if explicit:
        if not os.path.isdir(explicit):
            raise SystemExit(f"--cut-files directory not found: {explicit}")
        return explicit
    for drive in "FEGDHIJ":
        for hint in SEARCH_HINTS:
            d = hint.format(d=drive)
            if os.path.isdir(d):
                return d
    raise SystemExit(
        "Could not find the cut files. Attach the USB drive and pass its path:\n"
        "    python extract-size-contours.py --cut-files \"F:\\sean\\max\\cutting files street signs\"\n"
        "You do NOT need this script to run the pipeline - source/size-contours.json\n"
        "is committed and is the source of truth."
    )


def locate(cut_dir, name):
    """Find a cut file by name anywhere under cut_dir, tolerating '- Copy' suffixes."""
    stem = os.path.splitext(name)[0]
    for pattern in (name, stem + "*.lbrn2"):
        for root, _, _ in os.walk(cut_dir):
            hits = sorted(glob.glob(os.path.join(root, pattern)))
            if hits:
                return hits[0]
    # also try the drive root, one level up from a Templates-style layout
    parent = os.path.dirname(cut_dir.rstrip("\\/"))
    for root, _, _ in os.walk(parent):
        hits = sorted(glob.glob(os.path.join(root, stem + "*.lbrn2")))
        if hits:
            return hits[0]
    return None


def outlines(path, local):
    """Yield flattened point lists for every path shape in the file.

    local=True returns the shape BEFORE its XForm, i.e. the authored master
    geometry; local=False returns it placed on the laser bed.
    """
    root = ET.parse(path).getroot()
    vcache, pcache = {}, {}
    for sh in root.iter("Shape"):
        if sh.get("Type") == "Ellipse":
            continue
        xf_el = sh.find("XForm")
        xf = [float(v) for v in xf_el.text.split()] if xf_el is not None else [1, 0, 0, 1, 0, 0]
        a, b, c, d, e, f = ([1, 0, 0, 1, 0, 0] if local else xf)

        vid, pid = sh.get("VertID"), sh.get("PrimID")
        vl, pl = sh.find("VertList"), sh.find("PrimList")
        if vl is not None:
            vcache[vid] = [
                {"p": (float(m.group(1)), float(m.group(2))),
                 "c0": (fnum(m.group(3)), fnum(m.group(4))),
                 "c1": (fnum(m.group(5)), fnum(m.group(6)))}
                for m in VERT_RE.finditer(vl.text or "")
            ]
        if pl is not None:
            txt = (pl.text or "").strip()
            pcache[pid] = "LineClosed" if txt == "LineClosed" else PRIM_RE.findall(txt)
        verts, prims = vcache.get(vid), pcache.get(pid)
        if not verts or not prims:
            continue

        if prims == "LineClosed":
            pts = [v["p"] for v in verts]
            nbez = 0
        else:
            pts = []
            for kind, ia, ib in prims:
                va, vb = verts[int(ia)], verts[int(ib)]
                pts.append(va["p"])
                if kind == "B" and va["c0"][0] is not None and vb["c1"][0] is not None:
                    pts.extend(cubic(va["p"], va["c0"], vb["c1"], vb["p"]))
            nbez = sum(1 for k, _, _ in prims if k == "B")
        if len(pts) < 3:
            continue
        yield [(a*x + c*y + e, b*x + d*y + f) for x, y in pts], len(verts), nbez


def area(pts):
    s = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        s += x0*y1 - x1*y0
    return abs(s) / 2.0


def hull(pts):
    p = sorted(set(pts))
    if len(p) < 3:
        return p
    def half(seq):
        out = []
        for q in seq:
            while len(out) >= 2:
                (ax, ay), (bx, by) = out[-2], out[-1]
                if (bx-ax)*(q[1]-ay) - (by-ay)*(q[0]-ax) <= 0:
                    out.pop()
                else:
                    break
            out.append(q)
        return out
    return half(p)[:-1] + half(list(reversed(p)))[:-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cut-files", help="directory holding the .lbrn2 cut files")
    args = ap.parse_args()
    cut_dir = find_cut_dir(args.cut_files)
    print(f"cut files: {cut_dir}\n")

    result = {
        "_note": "Generated by source/extract-size-contours.py. COMMITTED - this is the "
                 "source of truth for all three blank contours. No USB needed to use it.",
        "_shapeFamily": "All three are the same scalloped design: four CONCAVE corners, "
                        "area/convex-hull ratio ~0.993. A convex 1.0000 outline is the "
                        "Traditional Road Sign, a different product.",
        "sizes": {},
    }

    for name, cfg in SOURCES.items():
        path = locate(cut_dir, cfg["file"])
        if not path:
            raise SystemExit(f"{name}: cut file not found under {cut_dir}: {cfg['file']}")

        bw, bh = cfg["blank"]
        chosen = None
        for pts, nverts, nbez in outlines(path, cfg["local"]):
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            w, h = max(xs) - min(xs), max(ys) - min(ys)
            if abs(w - bw) <= 0.05 and abs(h - bh) <= 0.05:
                chosen = (pts, nverts, nbez, w, h)
                break
        if not chosen:
            raise SystemExit(f"{name}: no {bw}x{bh} mm outline in {os.path.basename(path)} - refusing to guess.")
        pts, nverts, nbez, w, h = chosen

        ratio = area(pts) / area(hull(pts))
        if not (0.985 < ratio < 0.9985):
            raise SystemExit(
                f"{name}: area/convex-hull ratio {ratio:.4f} is not the scalloped street-sign "
                f"family (expected ~0.993). A convex 1.0000 outline is a different product."
            )

        # Normalise to a 0,0 top-left origin.
        #
        # Y IS NOT FLIPPED, and that is deliberate. The obvious reading -
        # LightBurn Y goes up, SVG Y goes down, so flip - produces a contour that
        # is 0.31 mm Hausdorff away from the audited source-data.js Large, i.e.
        # the sign upside down. The blank is very nearly symmetric top-to-bottom,
        # so the error is easy to introduce and almost impossible to see. Matching
        # the audited original is what matters: it is the file the Max-approved
        # Large artwork was produced from. With this convention the extracted
        # Large reproduces it to 0.0006 mm.
        x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
        norm = [{"x": round(px - x0, 4), "y": round(py - y0, 4)} for px, py in pts]

        result["sizes"][name] = {
            "blankWidthMm": round(w, 3),
            "blankHeightMm": round(h, 3),
            "sourceFile": os.path.basename(path),
            "sourceGeometry": "local (pre-XForm) master" if cfg["local"] else "placed on bed",
            "sourceVertices": nverts,
            "cubicCorners": nbez,
            "areaOverHull": round(ratio, 4),
            "contour": {"points": norm},
            "mountingHoles": [],   # holes are drilled, never printed - see CLAUDE/workflow notes
        }
        print(f"{name:7s} {w:8.3f} x {h:7.3f} mm | {nverts:3d} verts + {nbez} cubics "
              f"-> {len(norm):4d} pts | a/hull {ratio:.4f} | {os.path.basename(path)}")

    # source-data.js is the audited original that produced the Max-approved Large
    # artwork. Its exact numbers are ADOPTED for Large rather than merely compared
    # against, for a reason worth knowing:
    #
    # This script and the older build-source-data.ps1 read the same cut file and
    # agree to 0.001 mm - pure rounding ties, 36 of 409 points. But build.py insets
    # the plate by 12.4 mm to make the frame, and that inward offset is badly
    # conditioned at the four scalloped corners, where adjacent segments are nearly
    # collinear. One micron of vertex noise moves the offset intersection ~127
    # microns. Re-deriving Large would therefore shift the approved frame by
    # 0.127 mm for no benefit. Adopting the audited points makes Large bit-identical
    # while still keeping ONE file that build.py reads.
    audit = os.path.join(HERE, "source-data.js")
    if os.path.exists(audit):
        raw = open(audit, encoding="utf-8").read().split("=", 1)[1].strip().rstrip(";")
        want = [(p["x"], p["y"]) for p in json.loads(raw)["lightBurn"]["contour"]["points"]]
        got = [(p["x"], p["y"]) for p in result["sizes"]["large"]["contour"]["points"]]
        if len(want) != len(got):
            raise SystemExit(f"AUDIT FAILED: Large has {len(got)} points, source-data.js has {len(want)}.")
        worst = max(((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5 for a, b in zip(want, got))
        if worst > 0.01:
            raise SystemExit(
                f"AUDIT FAILED: the cut file's Large outline differs from the audited "
                f"source-data.js by {worst:.4f} mm. Refusing to write. If the Y convention "
                f"flipped, the shape is upside down - the blank is nearly symmetric so it "
                f"looks fine but is not."
            )
        result["sizes"]["large"]["contour"]["points"] = [{"x": x, "y": y} for x, y in want]
        result["sizes"]["large"]["_largePoints"] = (
            "Adopted verbatim from the audited source-data.js. The cut file agrees to "
            f"{worst:.4f} mm; the audited numbers are used so the approved Large frame is "
            "bit-identical - the 12.4 mm inset amplifies micron noise ~100x at the scallops."
        )
        print(f"\naudit    cut file matches source-data.js to {worst:.6f} mm; adopted audited Large points")

    out = os.path.join(HERE, "size-contours.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    print(f"wrote {out} ({os.path.getsize(out):,} bytes)")


if __name__ == "__main__":
    main()
