# The real colourways — sampled from the live listing swatch

Source: `Mow-It-Swatch-Final-copy.jpg`, a product image on the live Family
Street Sign listing (SKU 36965). Saved to
`Creative Studio/reference-masters/street-sign-COLOURWAY-SWATCH.jpg`.

**These five are the only colours the product is sold in.**

| Colourway | Ink (frame + lettering) | Panel |
|---|---|---|
| BLACK | `#000000` | `#F2EEE3` |
| GREY  | `#7C7C7E` | `#F2EEE3` |
| SAGE  | `#BEC0AA` | `#F2EEE3` |
| GRASS | `#6E8F40` | `#F2EEE3` |
| BLUE  | `#7A9EAA` | `#F2EEE3` |

The panel is the same warm cream on all five — **not** pure white. The
black-on-pure-white master remains a separate legacy case.

## Use it by name

```
SIGN_COLOURWAY=GREY SIGN_HEART=0 python3 build.py <id> "LINE 1" "LINE 2" 486 out.svg
```

An unknown name hard-fails and prints the real options. Colours previously used
in this repo — navy, burgundy, forest green, slate — were **invented and are not
products**. That is why the guard exists.

## Legibility finding (matters for video)

At phone size, ink contrast against the cream panel varies a lot:
- **BLACK** — strongest; subtitle line fully legible.
- **GREY** — good; subtitle legible.
- **SAGE** — weakest. The subtitle line nearly disappears when the sign is small
  in frame. Fine on a product page or a large still; **avoid for the small-in-frame
  in-situ video shots** unless the sign fills a lot of the frame.
- GRASS / BLUE — untested at small size; assume between GREY and SAGE.
