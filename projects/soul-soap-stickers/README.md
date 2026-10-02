# Soul Soap by Daisy Maison: saying stickers

Print-ready sticker sheets for the Soul Soap bars, in the 70s retro look from
the approved mockups (cocoa, cream, red and pink grounds; hearts, daisies,
rainbow, sparkles).

## What to print

| File | What it is |
|---|---|
| `output/soul-soap-stickers-LP15-51SQ.pdf` | Page 1: Everyday sheet (15 designs). Page 2: Mum sheet (5 designs, three of each, one per row). |
| `output/alignment-test-LP15-51SQ.pdf` | Label outlines and a 100 mm bar. Print it on plain paper first. |
| `output/preview-everyday.png`, `output/preview-mum.png` | What the peeled stickers look like (not for printing). |

Design canvas (claude.ai Design, private to Max until shared):
https://claude.ai/artifact/5ZTWifKwjRC1yomjbSPJPA

### Printing

1. Print `alignment-test-LP15-51SQ.pdf` on plain A4 at **100% / Actual size**
   (never "Fit to page"). The bar at the bottom should measure exactly 100 mm.
2. Hold it behind a label sheet against a window. The outlines should sit on the
   label edges. If they are off, fix the printer's alignment or offset setting
   before using label sheets.
3. Print the page you need from `soul-soap-stickers-LP15-51SQ.pdf`, again at
   100%, printing only that page (page 1 Everyday, page 2 Mum).

These are matt paper labels. Laser is safest: inkjet ink on matt paper can
smudge if the sticker gets wet.

## The sheet

Label Planet LP15/51SQ, from Label Planet's template page: A4 portrait, 3
across x 5 down, 51 x 51 mm labels with rounded corners, 52.9 mm pitch both
ways (1.9 mm gaps), top/bottom margin 17.2 mm, left/right margin 26.6 mm.

- Colour grounds bleed 0.95 mm past every label edge (half the gap).
- Text stays at least 3 mm inside every label edge (`render.cjs` checks this).
- The PDF is checked after every build: exact 210 x 297 mm pages, every
  label ground within 0.02 mm of the template, and every display line within
  0.15 mm of the on-screen layout.

## The look

| Token | Hex | Use |
|---|---|---|
| Cocoa | `#5A2D1E` | ground |
| Cream | `#F7EBD6` | ground, text on dark |
| Red | `#CF2A27` | ground, hearts, italic words |
| Pink | `#F7A1BC` | ground, bubbly words, brand line on cocoa |
| Mustard | `#F1B33E` | shadows, sparkles, daisy centres, rainbow |
| Coral | `#EB6443` | stripes, rainbow, sun rays |
| Tan | `#C28453` | stripes |
| Ink | `#2B1A12` | small caps on cream |

Type (all SIL Open Font License, from Google Fonts): Caprasimo (soft
Cooper-style words), Shrikhand (70s italic words with a stepped mustard or
cocoa shadow), Fredoka Bold (bubbly words such as "grubby"), Montserrat
SemiBold/Bold (spaced small caps and the `SOUL SOAP · DAISY MAISON` line on
every sticker). Montserrat replaced Poppins because Poppins has no kerning and
its spaced capitals looked gappy.

## Sayings

Everyday sheet: My one and foamy (heart, and a groovy heart alternate) · If you
can't be good, at least be clean! (stripes, and a rainbow alternate) · You've
got this, soap-er star! · You're bloody soap-erb, sunshine! · For when life gets
a bit grubby · Soap glad we're friends · Sh*t happens, have a soap · You're my
soap mate · Soap proud of you · Soap glad I found you · Love you soap much ·
Thank you soap much · Soap much love.

Mum sheet: Soap glad you're my mum · Love you soap much, Mum · Mum, you
deserve a little me time · Mum, you're soap-erb · Thank you for always cleaning
up my mess.

## Rebuilding

Every design is a function in `build.py` (coordinates in mm from the label's
top-left, text placed by baseline). The sheet layouts are `SHEETS` at the
bottom of the design list.

```sh
python3 build.py            # build/*.html (add --canvas DIR for the Design canvas files)
node render.cjs             # PDFs, previews and the fit check (--review: large crops in build/review)
python3 finish_pdf.py       # exact A4 pages and the registration check
```

Needs Python 3 with `pymupdf`, and Node with Playwright's Chromium.
