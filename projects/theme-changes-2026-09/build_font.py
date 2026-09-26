"""Rebuild the light street-sign preview font used on the sign product pages.

The theme's assets/daisy-street-sign-times.ttf is 1.2 MB because it carries every
alphabet. The sign preview only needs Latin, so this makes a 27 KB WOFF2 with the
same glyphs and spacing, and prints the two unicode-range lists that
layout/theme.liquid uses: the WOFF2 covers the Latin list, and the full TTF stays
as a fallback for any other character (the browser only downloads it if a
customer types one).

Usage: pip install fonttools brotli
       python build_font.py daisy-street-sign-times.ttf
"""
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

LATIN = ("U+0020-007E,U+00A0-017F,U+0218-021B,U+02C6-02C7,U+02D8-02DD,U+2010-2027,"
         "U+2030-203A,U+2044,U+20AC,U+2116,U+2122,U+2153-215E,U+2212,U+2665,U+FB01-FB02")


def ranges(codepoints):
    out, start, prev = [], None, None
    for c in sorted(codepoints):
        if start is None:
            start = prev = c
        elif c == prev + 1:
            prev = c
        else:
            out.append((start, prev))
            start = prev = c
    if start is not None:
        out.append((start, prev))
    return ",".join("U+%04X" % a if a == b else "U+%04X-%04X" % (a, b) for a, b in out)


def main(src):
    cmap = TTFont(src).getBestCmap()
    keep = [c for c in subset.parse_unicodes(LATIN) if c in cmap]
    rest = [c for c in cmap if c not in set(keep)]

    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.hinting = False
    opts.legacy_kern = True
    opts.drop_tables += ["DSIG", "JSTF", "PCLT", "VDMX", "hdmx", "LTSH", "meta"]
    subsetter = subset.Subsetter(opts)
    subsetter.populate(unicodes=keep)
    font = TTFont(src)
    subsetter.subset(font)
    font.flavor = "woff2"
    font.save("daisy-street-sign-times-latin.woff2")

    full, light = TTFont(src), TTFont("daisy-street-sign-times-latin.woff2")
    fc, lc = full.getBestCmap(), light.getBestCmap()
    mismatches = [c for c in keep if full["hmtx"][fc[c]][0] != light["hmtx"][lc[c]][0]]
    assert not mismatches, "character widths changed"

    print("WOFF2 unicode-range:", ranges(keep))
    print("TTF fallback unicode-range:", ranges(rest))


if __name__ == "__main__":
    main(sys.argv[1])
