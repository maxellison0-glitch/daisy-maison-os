"""One colour path for content and for the laser. Read from the sign maker.

Max, 28 Jul 2026: "take colour paths from the sign maker workflow so we are all
in sync and on the same team."

The single source of truth is the production rules file:

    projects/daisy-street-sign/production/product-rules.json

which is the same file `production/recolour-sign.ps1` reads before a real order
goes to the laser. Nothing here defines a colour. If a colourway is added,
renamed or retired for the product, content picks it up on the next run without
anyone editing this file — which is the whole point.

Why content needed its own copy of the logic
--------------------------------------------
Production applies colour in PowerShell, after build.py, on the finished SVG.
Content runs on Linux and cannot call the .ps1, so this is a faithful port of
`recolour-sign.ps1`'s DOM pass — deliberately the same rules, not a second
opinion:

  - Edit by ELEMENT ID via the XML tree, never by string-replacing "#010101".
    A blind replace would also hit the mounting-hole strokes, the metadata
    block, and anything that later happens to share the colour. That warning is
    quoted from the production script and it is the reason this is not four
    lines of regex.
  - Border and every text run take the colourway colour; they must stay one
    visual colour, ampersand included.
  - The heart is never recoloured. It is a raster and part of the locked
    signature unit — the red heart is the same on every colourway.
  - Mounting holes are removed, not painted. They are physical holes in the
    acrylic, so ink there is ink on absent material.

What this replaced, and the bug that made it necessary
------------------------------------------------------
`reprint.py` used to set SIGN_COLOURWAY, SIGN_HEART and SIGN_HOLES and let
build.py act on them. Merging main's build.py removed all three — main handles
colour, heart and holes downstream instead. The env vars kept being set and
kept being ignored, so content would have silently rendered every sign black,
hearted and holed, with no error anywhere. Found 28 Jul 2026 while checking
that the merge had not touched the production path.
"""
import json
import os
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
RULES_PATH = os.path.join(_REPO, "projects", "daisy-street-sign",
                          "production", "product-rules.json")


def load_rules():
    if not os.path.exists(RULES_PATH):
        raise SystemExit(
            "Missing %s. It holds the colourways the laser actually prints, and "
            "content must not invent its own." % RULES_PATH)
    return json.load(open(RULES_PATH, encoding="utf-8"))


def palette():
    """Colourway name -> hex, including production's aliases. Keys lowercased."""
    r = load_rules()
    p = {k.lower(): v for k, v in r.get("colourways", {}).items()}
    for alias, target in r.get("colourwayAliases", {}).items():
        if target.lower() in p:
            p[alias.lower()] = p[target.lower()]
    return p


def resolve(name):
    """'SAGE' or 'Light Sage' or '#68893C' -> hex. Hard fail on anything else.

    A fallback would be worse than a crash: a typo that quietly renders a
    plausible colour we do not sell reaches Max as an approved-looking image,
    and from there a customer.

    How exact to be about this, settled by Max on 28 Jul 2026: "for content,
    obviously colour is gonna differ based on lighting and stuff like that, so
    we don't need to be too strict. Just pick a template, and then we'll stick
    with it." So the name in plates.json is the template and it is authoritative
    - do not re-measure a photograph and relabel a plate because a sampled
    pixel landed nearer a neighbouring shade. Lighting moves colour further
    than two adjacent sages differ, so that measurement can never settle it and
    chasing it just makes old content stop matching new content.
    """
    if not name:
        return None
    p = palette()
    key = "".join(ch for ch in str(name).lower() if ch.isalnum())
    if key in p:
        return p[key]
    s = str(name).strip()
    if s.startswith("#") and len(s) == 7:
        return s.upper()
    raise SystemExit(
        "Colourway %r is not one the product is sold in. The laser knows: %s\n"
        "(from %s — add it there, not here.)"
        % (name, ", ".join(sorted(p)), RULES_PATH))


def recolour_svg(path, colourway=None, panel=None,
                 keep_heart=False, keep_holes=False):
    """Recolour a build.py SVG in place. Port of recolour-sign.ps1's DOM pass."""
    ink = resolve(colourway) if colourway else None
    panel_hex = resolve(panel) if panel else None

    tree = ET.parse(path)
    root = tree.getroot()

    def q(tag):
        return "{%s}%s" % (SVG_NS, tag)

    changed = 0
    by_id = {}
    for el in root.iter():
        i = el.get("id")
        if i:
            by_id.setdefault(i, el)

    if ink:
        el = by_id.get("outer-plate")
        if el is not None and el.get("fill") not in (None, "none"):
            el.set("fill", ink); changed += 1
        # Every text run, the ampersand included - one visual colour.
        for t in root.iter(q("text")):
            for attr in ("fill", "stroke"):
                if t.get(attr) not in (None, "none"):
                    t.set(attr, ink); changed += 1

    if panel_hex:
        el = by_id.get("inset-panel")
        if el is not None and el.get("fill") not in (None, "none"):
            el.set("fill", panel_hex); changed += 1

    # Holes and heart need the parent to remove a child, which ElementTree
    # cannot do from the node itself.
    for parent in root.iter():
        for child in list(parent):
            cid = child.get("id")
            if cid in ("mounting-hole-left", "mounting-hole-right") and not keep_holes:
                parent.remove(child); changed += 1
            elif cid == "signature-heart" and not keep_heart:
                parent.remove(child); changed += 1

    tree.write(path, encoding="utf-8", xml_declaration=True)
    return changed


if __name__ == "__main__":
    p = palette()
    print("Colourways the laser prints (%s):" % RULES_PATH)
    for k in sorted(p):
        print("  %-12s %s" % (k, p[k]))
