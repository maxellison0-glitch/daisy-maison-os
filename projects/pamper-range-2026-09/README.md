# Pamper range (AW Aromatics stock), 28 Sep 2026

Brief with setup, packaging and ChatGPT prompts: `pamper-range-brief.html`
(published at https://claude.ai/artifact/8VeVo8Wmy7ExLHbsWN2RDV).

## Built so far (duplicate theme "Copy of constructed 🚧", 207968960851)

**Products** (live data, published to Online Store, not linked from any menu yet):

| Product | Handle | Price | SKU | Stock |
|---|---|---|---|---|
| Emerald Truffle Soap | `emerald-truffle-soap` | £4.95 | DM-SOAP-ET-100 | tracked, 13 |
| Slice of Sunshine Soap | `slice-of-sunshine-soap` | £4.95 | DM-SOAP-SS-100 | tracked, 13 |
| Rose & Rose Petals Soap | `rose-and-rose-petals-soap` | £4.95 | DM-SOAP-RP-100 | tracked, 13 |
| Mojito Bath Bomb Set | `mojito-bath-bomb-set` | £12.95 | DM-BB-MOJITO (EAN 5056422901079) | not tracked yet |
| Piña Colada Bath Bomb Set | `pina-colada-bath-bomb-set` | £12.95 | DM-BB-PINACOLADA (EAN 5056422901086) | not tracked yet |
| Gin & Tonic Bath Bomb Set | `gin-and-tonic-bath-bomb-set` | £12.95 | DM-BB-GINTONIC (EAN 5056422901048) | not tracked yet |

- Soaps: 4 images each (kraft pouch hero, stack, in hand, ruler), matched by colour: pink = Rose, brown swirl = Emerald Truffle, yellow = Slice of Sunshine.
- Ingredients in the descriptions come from the AW labels. Emerald Truffle's label was cut off in the photo, so its page says the list is on the pack until Max sends a clear photo.
- Product type drives everything: `Soap` or `Bath Bomb`.

**Collections** (smart, by product type; published, not in the menu):
- `handmade-soap` (Handmade Soap), template `collection.soap`.
- `bath-bombs` (Cocktail Bath Bombs), template `collection.pamper`.

**Deal:** automatic discount "Soap: any 3 for £12" (DiscountAutomaticNode/1841638375763). It applies 19.2% off every item in Handmade Soap once 3 or more are in the basket, which makes each soap £4.00 (3 = £12.00, 4 = £16.00). At 19.19% Shopify's per-line rounding gave £12.03, so keep 19.2%. It combines with other discounts.

**Theme files** (copies in `theme/`):
- `snippets/dm-soap-range.liquid`: one snippet, three modes.
  - `deal`: the "Offer: Mix & match any 3 soaps for £12" line under the price (soap only).
  - `range`: the strip after Add to Cart. Soaps get "Mix & match any 3 for £12" with a 3-step progress bar read from the basket and one-tap Add cards. Bath bombs get "Choose your cocktail" cards (shown once there are 2+ sets). Both get the gift wrap picker (`[data-dm-wrap-instant]`).
  - `collection`: heading, intro and (soap) offer steps at the top of the collection page.
- `templates/product.soap.json` and `product.pamper.json`: identical. They are a copy of `product.json` without the Globo block, the dm-gc builder, the handle-specific gift box block, the personalisation FAQ tab or any disabled blocks, plus the two snippet blocks.
- `templates/collection.soap.json` and `collection.pamper.json`: breadcrumb, snippet intro and product grid.

**Tested on the duplicate theme (phone, headless):**
- Soap pages: the three one-tap adds step the progress bar through 1/3, 2/3 and "3 for £12 unlocked", and the basket comes to exactly £12.00.
- The Piña Colada page shows £12.95 and "Choose your cocktail" (Piña Colada, Mojito).
- The soap collection opens with the heading and offer.
- No page errors and no sideways scroll.

## Still to do
- Martini bath bomb set (waiting for its image). The massage oil waits on AW's safety report.
- Bath bomb deal: Max to pick (suggested: any 2 sets for £22).
- Bath bomb stock counts, so inventory can be tracked.
- When Max approves:
  - add both collections to the menu and the items to Gifts UNDER £15
  - publish the duplicate theme (the new templates only exist there)
