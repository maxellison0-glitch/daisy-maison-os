# Theme changes: Christmas decoration builders + Mr & Mrs line 2 (24 Sep 2026)

**Status:** built and tested on the unpublished theme **"Claude – Xmas builders + Mr & Mrs (24 Sep)"** (id 207729066323), duplicated from the live theme "In construction 🚧" at 17:13 on 24 Sep. Not published. Max publishes.

Preview links:
- Family Festive star: https://daisymaison.co.uk/products/personalised-family-festive-christmas-pebble-star-hanging-decoration?preview_theme_id=207729066323
- Merry & Bright: https://daisymaison.co.uk/products/personalised-merry-bright-family-christmas-pebble-hanging-decoration?preview_theme_id=207729066323
- Mr & Mrs sign: https://daisymaison.co.uk/products/mr-mrs-personalised-street-sign-gift?preview_theme_id=207729066323

Three files differ from live. The full change is in `xmas-builders-and-mr-mrs-line2.diff`, and `build_xmas.py` regenerates the builder edit from the live files.

| File | Change |
|---|---|
| `layout/theme.liquid` | The two decoration handles join the list of pages that load the native heart builder (`dm-heart-builder` + `daisy-heart-builder.js`). |
| `snippets/dm-heart-builder.liquid` | Two new kinds, `merrybrightheart` and `festivestar`, each a config block cloned from Wonderland. |
| `assets/daisy-street-sign-options.js` | Mr & Mrs preview: the sample line 2 only shows while line 1 is still the example. |

## 1. Merry & Bright and Family Festive star: off Globo, onto the native builder

Both pages now use the same builder as the other Christmas decorations (Wonderland, Love at Christmas, Our 1st Christmas). The builder hides the Globo form itself. `dm-wrap-kits` automatically adds the Gift Wrap Kit with the Classic / Christmas choice to every heart-builder page, so both pages get the Christmas kit with no change to the wrap-kit code.

**Property keys are verbatim from each product's own Globo form** (read from the live pages on 24 Sep), because fulfilment reads them exactly:

| | Merry & Bright | Family Festive star |
|---|---|---|
| Pebble count key / values | `Number of pebbles`: `1`–`4`, `5 (Large heart +£3)`, `7 (Large heart +£5)` | `Number of pebbles`: `1`–`4`, `5 (Large heart)`, `7 (Large heart)` |
| Size key / values | `Size 1`: `Small 10 x 10cm (£15.95)` / `Large 15 x 15cm (£18.95)` | `Size`: same two values |
| Pebble types | Adult, Child, Dog, Cat | Adult, Teen, Child, Baby, Dog, Cat |
| Wording | `Text above`, `Text below` | `Text above`, `Text below` |
| Year question | `Add 2026?` (Globo still says 2025; Wonderland's native config moved to 2026) | none (Globo never asked) |
| Second item | `**INCREDIBLE OFFER**` YES Please / NO Thanks, then `(Offer) …` keys | same |
| Helpers | (+£3) Large Decoration, (+£5) 7/8 pebbles, (+£10.95) INCREDIBLE OFFER DECORATION | same |
| Gift boxes | the three Wonderland designs | **none**, see below |

The star's keys match its three most recent paid orders (Aug–Sep 2026): `Number of pebbles`, `Size`, `Pebble N`, `Text above`, `Text below`, `**INCREDIBLE OFFER**`, and the `(+£3) Large Decoration` line at 5 pebbles. Merry & Bright had no orders in the last 60 days, so its keys come from the live Globo form. They are identical to Wonderland's, whose native config has been live all season.

**No gift boxes on the star.** Its description says "small 12cm x 12cm, large 20cm x 20cm", but the gift boxes are 10 × 10 and 14 × 18, so a box might not fit. The Globo page never offered one either. Add the `giftBox` block (copy it from Wonderland) once the size is confirmed.

### Tested on the preview (390 px phone, headless)

- **Star, 5 pebbles (Adult, Adult, Teen, Baby, Dog) with the Christmas wrap kit:** the total showed £24.90, and the basket received exactly:
  - the star, £15.95, with `Number of pebbles: 5 (Large heart)`, `Size: Large 15 x 15cm (£18.95)`, `Pebble 1–5`, `Text above`, `Text below`, `**INCREDIBLE OFFER**: NO Thanks`;
  - `(+£3) Large Decoration`, £3.00;
  - `Christmas Gift Wrap Kit`, £5.95.
  No Globo blocks were visible.
- **Merry & Bright:** the page renders the heading, the four pebble types, the year question, the "Add A Second Heart +£10.95" offer and the wrap kit, with no Globo blocks visible. The 7-pebble + offer basket run is listed under "QA" below.

## 2. Mr & Mrs: line 1 only means a one-line sign

Before, an empty line 2 always previewed the sample "FROM THIS DAY FORWARD - 14.08.2027", even after the customer had typed their own line 1 and the caption said "Your sign". Now the sample subtitle belongs to the untouched example only:

| Customer has typed | Preview |
|---|---|
| nothing | example sign, both lines, "Example — fill in the lines below" |
| line 1 only | their line 1 only, "Your sign", "Personalisation complete" badge |
| line 1 + line 2 | both of their lines |
| clears line 2 | line 1 only again |
| clears line 1 | the example returns |

Production already handles this: `production/run-batch.ps1` passes a blank line 2 as `--no-line2`, and `artwork/build.py` keeps line 1 in the same place whether or not there is a line 2. So the preview now matches what gets made. Adding to basket with only line 1 sends `Line 2: ""`, which was tested.

## Before publishing

1. Someone made **"Copy of In construction 🚧"** (id 207727198547) at 16:46 on 24 Sep. If the team is working in that theme, publishing one theme would overwrite the other's work. Merge the three files above into whichever theme goes live.
2. Re-check the live theme for changes made after 17:13 on 24 Sep, and copy any across first (as on 23 Sep, when a checkout wording change was nearly lost).
3. Confirm the star's real size (10 × 10 / 15 × 15 per its Globo form, or 12 × 12 / 20 × 20 per its description).
