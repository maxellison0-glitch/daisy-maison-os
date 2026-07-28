# build.py option matrix — verified 25 Jul 2026

All six rendered from the same canonical geometry (570 × 125 mm, 4.54:1, real
LightBurn contour, real Times New Roman, real mounting holes). Zero credits —
this stage is entirely local and deterministic.

| Variant | Heart | Lines | Colourway | Command |
|---|---|---|---|---|
| A wedding (default) | yes | 2 | black on white | `python3 build.py <id> "MR & MRS HALE" "WHEN TWO NAMES BECOME ONE · 15TH AUGUST 2026" 486 out.svg` |
| B no heart, 2 lines | no | 2 | black on white | `SIGN_HEART=0 python3 build.py …` |
| C no heart, 1 line | no | 1 | black on white | `SIGN_HEART=0 python3 build.py <id> "THE DOG LIVES HERE" "" 486 out.svg` |
| D colour | no | 2 | forest green on cream | `SIGN_HEART=0 SIGN_COLOR=#1F3B2C SIGN_PANEL=#F4F1E8 …` |
| E colour + heart | yes | 2 | navy on white | `SIGN_COLOR=#152742 …` |
| F colour | no | 2 | burgundy on ivory | `SIGN_HEART=0 SIGN_COLOR=#5B1A24 SIGN_PANEL=#F7F2EA …` |

`SIGN_COLOR` sets frame **and** lettering together, as on the real product.
`SIGN_PANEL` sets the inset panel. `SIGN_HEART=0` removes the wedding heart.
An empty line 2 renders a clean single-line sign.

## Two things needing Max's decision

1. **Single-line vertical placement.** `CAP_CENTER_Y` is tuned for the two-line
   layout, so a one-line sign sits at the same cap height and leaves the
   subtitle space empty beneath. Should single-line signs re-centre optically?
2. **Heart colour on coloured signs.** The heart is the fixed PSD raster and
   stays red on navy/green/burgundy. Correct as the signature unit, or should it
   take the sign colour?

## Reference images per variant — OUTSTANDING

Per `Creative Studio/REFERENCE_PACK.md`, every product render needs an approved
real photograph as reference 1. Today only **one** exists: white sign, black
printing (`01-approved-product.jpg`).

Coloured signs therefore have **no approved reference yet**. The print-edit
prompt currently says "preserve its broad black printed border", which is wrong
for a coloured sign — the border colour is itself printing. Producing the first
approved coloured reference needs that one line adapted, and Max's approval of
the result. Until then, colour is renderable as artwork but has no validated
product-photo route.
