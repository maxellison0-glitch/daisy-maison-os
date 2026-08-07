"""Add a printed bleed around an approved Daisy street-sign SVG.

WHY THIS EXISTS
---------------
Printing the artwork at exactly the blank size leaves white acrylic showing on any
edge where the blank is a fraction out of position in the jig. Max reported visible
white edges on real prints (2026-07-26) and specified 4 mm of extra ink all round.

WHY DILATE RATHER THAN DRAW A RECTANGLE
---------------------------------------
The sign is not a rectangle - it has four concave scalloped corners. A backing
rectangle would flood those scallops with ink, putting a lot of unnecessary colour
on the paper jig and inking it up over repeated runs. Buffering the real 409-vertex
cut contour outward by 4 mm keeps the sign's actual silhouette and adds ink only
where it is needed.

The dilated shape is inserted BEHIND the existing artwork and the approved elements
are not modified, so this cannot alter the signed-off geometry. The canvas grows by
the bleed on every side, and the negative viewBox origin is what downstream tools
read to keep the BLANK (not the canvas) on its jig coordinate.

USAGE
    python add-bleed.py <in.svg> <out.svg> [bleed_mm]

Default bleed is 4.0 mm.
"""

import sys
import re
import xml.etree.ElementTree as ET

from shapely.geometry import Polygon

SVG_NS = "http://www.w3.org/2000/svg"
DAISY_NS = "https://daisymaison.co.uk/ns/production"
XLINK_NS = "http://www.w3.org/1999/xlink"

DEFAULT_BLEED_MM = 4.0


def parse_polyline(d):
    """These contours are pure M/L/Z. Anything else is a hard failure rather than
    a silent approximation of artwork that has already been approved."""
    tokens = re.findall(r"[MLZmlz]|-?\d*\.?\d+(?:[eE][-+]?\d+)?", d)
    pts, i, cmd = [], 0, None
    while i < len(tokens):
        t = tokens[i]
        if t in "MLZmlz":
            cmd = t.upper()
            i += 1
            continue
        if cmd in ("M", "L"):
            pts.append((float(tokens[i]), float(tokens[i + 1])))
            i += 2
            if cmd == "M":
                cmd = "L"
            continue
        raise SystemExit(f"Unsupported path command {cmd!r} - refusing to approximate.")
    return pts


def to_path_data(coords):
    head = "M {:.4f},{:.4f}".format(*coords[0])
    rest = " ".join("L {:.4f},{:.4f}".format(x, y) for x, y in coords[1:])
    return f"{head} {rest} Z"


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    bleed = float(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_BLEED_MM
    if bleed <= 0:
        raise SystemExit("Bleed must be positive.")

    ET.register_namespace("", SVG_NS)
    ET.register_namespace("daisy", DAISY_NS)
    ET.register_namespace("xlink", XLINK_NS)
    tree = ET.parse(src)
    root = tree.getroot()

    # refuse to double-apply
    existing = root.find(f".//{{{DAISY_NS}}}bleedMm")
    if existing is not None:
        raise SystemExit(f"{src} already has {existing.text} mm of bleed - refusing to stack another pass.")

    vb = [float(v) for v in root.get("viewBox").split()]
    if vb[0] != 0 or vb[1] != 0:
        raise SystemExit(f"Expected a 0-origin viewBox, got {vb} - already modified?")
    w_mm, h_mm = vb[2], vb[3]

    plate = None
    for p in root.iter(f"{{{SVG_NS}}}path"):
        if p.get("id") == "outer-plate":
            plate = p
            break
    if plate is None:
        raise SystemExit("No outer-plate contour found - is this an approved sign SVG?")

    pts = parse_polyline(plate.get("d"))
    poly = Polygon(pts)
    if not poly.is_valid:
        poly = poly.buffer(0)
    # round joins: mitre can throw long spikes at the scalloped corners, and the
    # exact silhouette outside the cut line does not matter - robustness does.
    grown = poly.buffer(bleed, join_style=1, resolution=16)
    if grown.geom_type != "Polygon":
        raise SystemExit(f"Buffer produced {grown.geom_type}, expected a single Polygon.")

    coords = list(grown.exterior.coords)
    border_colour = plate.get("fill") or "#010101"

    bleed_el = ET.Element(f"{{{SVG_NS}}}path")
    bleed_el.set("id", "print-bleed")
    bleed_el.set("d", to_path_data(coords))
    bleed_el.set("fill", border_colour)
    # first child = painted first = behind everything, including the white panel
    root.insert(0, bleed_el)

    # grow the canvas so the bleed is inside it; negative origin keeps the blank's
    # own coordinates unchanged, which is what the imposition step relies on.
    root.set("viewBox", f"{-bleed:g} {-bleed:g} {w_mm + 2 * bleed:g} {h_mm + 2 * bleed:g}")
    root.set("width", f"{w_mm + 2 * bleed:g}mm")
    root.set("height", f"{h_mm + 2 * bleed:g}mm")

    prod = root.find(f".//{{{DAISY_NS}}}production")
    if prod is not None:
        for k, v in (("bleedMm", f"{bleed:g}"),
                     ("bleedColour", border_colour),
                     ("blankSizeMm", f"{w_mm:g} x {h_mm:g}"),
                     ("bleedAddedBy", "production/add-bleed.py")):
            el = ET.SubElement(prod, f"{{{DAISY_NS}}}{k}")
            el.text = v
    else:
        print("WARNING: no daisy:production block - bleed provenance not recorded")

    tree.write(dst, encoding="utf-8", xml_declaration=True)
    print(f"{src}")
    print(f"  blank      {w_mm:g} x {h_mm:g} mm")
    print(f"  bleed      {bleed:g} mm all round, colour {border_colour}")
    print(f"  canvas     {w_mm + 2*bleed:g} x {h_mm + 2*bleed:g} mm, viewBox origin {-bleed:g},{-bleed:g}")
    print(f"  contour    {len(pts)} verts in -> {len(coords)} verts out")
    print(f"  wrote      {dst}")


if __name__ == "__main__":
    main()
