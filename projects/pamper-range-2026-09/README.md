# Pamper range (AW Aromatics stock), 28 Sep 2026

Brief with setup, packaging and ChatGPT prompts: `pamper-range-brief.html`
(published at https://claude.ai/artifact/8VeVo8Wmy7ExLHbsWN2RDV).

## Built so far (duplicate theme "Copy of constructed 🚧", 207968960851)

**Products** (live data, published to Online Store, not linked from any menu yet):

| Product | Handle | Price | SKU | Stock |
|---|---|---|---|---|
| Emerald Truffle Soap | `emerald-truffle-soap` | £4.95 | DM-SOAP-ET-100 | not tracked (stock is managed by the team) |
| Slice of Sunshine Soap | `slice-of-sunshine-soap` | £4.95 | DM-SOAP-SS-100 | not tracked (stock is managed by the team) |
| Rose & Rose Petals Soap | `rose-and-rose-petals-soap` | £4.95 | DM-SOAP-RP-100 | not tracked (stock is managed by the team) |
| Mojito Bath Bomb Set | `mojito-bath-bomb-set` | £12.95 | DM-BB-MOJITO (EAN 5056422901079) | not tracked |
| Piña Colada Bath Bomb Set | `pina-colada-bath-bomb-set` | £12.95 | DM-BB-PINACOLADA (EAN 5056422901086) | not tracked |
| Gin & Tonic Bath Bomb Set | `gin-and-tonic-bath-bomb-set` | £12.95 | DM-BB-GINTONIC (EAN 5056422901048) | not tracked |
| Martini Bath Bomb Set | `martini-bath-bomb-set` | £12.95 | DM-BB-MARTINI (EAN 5056422901062) | not tracked |
| Muscle Ease Massage Oil | `muscle-ease-massage-oil` | £12.95 | DM-OIL-ME-100 | not tracked. ACTIVE (Max's call, 28 Sep) |

- Soaps: 4 images each (kraft pouch hero, stack, in hand, ruler), matched by colour: pink = Rose, brown swirl = Emerald Truffle, yellow = Slice of Sunshine.
- Ingredients in the descriptions come from the AW labels. Emerald Truffle's label was cut off in the photo, so its page says the list is on the pack until Max sends a clear photo.
- Product type drives everything: `Soap` or `Bath Bomb`.

**Collections** (smart, by product type; published, not in the menu):
- `handmade-soap` (Handmade Soap), template `collection.soap`.
- `bath-bombs` (Cocktail Bath Bombs), template `collection.pamper`.

**Deal:** automatic discount "Soap: any 3 for £12" (DiscountAutomaticNode/1841638375763). It applies 19.2% off every item in Handmade Soap once 3 or more are in the basket, which makes each soap £4.00 (3 = £12.00, 4 = £16.00). At 19.19% Shopify's per-line rounding gave £12.03, so keep 19.2%. It combines with other discounts.
Bath bombs: automatic discount "Bath bombs: any 2 sets for £22" (DiscountAutomaticNode/1841685692755), approved by Max. It applies 15.06% off every set in Cocktail Bath Bombs once 2 or more are in the basket, which makes each set £11.00 (2 = £22.00, 3 = £33.00). Tested: Piña Colada + Gin & Tonic come to £22.00.

**Theme files** (copies in `theme/`):
- `snippets/dm-soap-range.liquid`: one snippet, three modes (reworked after Max's feedback that the upsell sat under Add to Cart).
  - `picker`: sits ABOVE Add to Cart. It shows one row per product in the range: image, name, a plain colour/scent line, price, and a − / + stepper.
    - Soaps: a "3 for £12" badge, "Mix & match any 3 soaps", one of each pre-picked, a 3-step bar, and a live button ("Add 3 soaps · £12.00"). Soaps already in the basket count towards the deal.
    - Bath bombs: a "2 for £22" badge, "Mix & match any 2 cocktail sets", the viewed set pre-picked (so it reads "Add 1 more for 2 for £22"), and a 2-step bar.
    - Under the button: "Just want this one? Use Add to Cart below."
  - `wrap`: the gift wrap picker, after Add to Cart.
  - `collection`: heading, intro and (soap) offer steps at the top of the collection page.
  - The colour/scent lines live in a `case` on the product handle. Add a line there for each new scent or set.
- `templates/product.soap.json` and `product.pamper.json`: identical. They are a copy of `product.json` without the Globo block, the dm-gc builder, the handle-specific gift box block, the personalisation FAQ tab or any disabled blocks, plus the two snippet blocks.
- `templates/collection.soap.json` and `collection.pamper.json`: breadcrumb, snippet intro and product grid.

**Tested on the duplicate theme (phone, headless), picker version:**
- Slice of Sunshine: the picker is above Add to Cart, with the trio pre-picked and "Add 3 soaps · £12.00". Tapping + on Rose makes it "Add 4 soaps · £16.00". Adding the trio gives a basket of exactly £12.00.
- Martini: "Choose your cocktail" lists all four sets, with Martini pre-picked, "Add 1 set · £12.95" and the gift wrap picker below.

**Tested earlier (strip version):**
- Soap pages: the three one-tap adds step the progress bar through 1/3, 2/3 and "3 for £12 unlocked", and the basket comes to exactly £12.00.
- The Piña Colada page shows £12.95 and "Choose your cocktail" (Piña Colada, Mojito).
- The soap collection opens with the heading and offer.
- No page errors and no sideways scroll.

## Still to do
- Massage oil: the product is built as a draft, using Max's ASA-safe copy (scent, glide and soft skin; no muscle or pain claims). Set it to Active once AW confirms the safety report. The ingredients line says the full list is on the bottle until AW sends the complete list. Its page (pamper template) shows no picker, only gift wrap; a "pamper night" cross-sell can come with the bundle.
- Bath bomb stock counts, so inventory can be tracked.
- When Max approves:
  - add both collections to the menu and the items to Gifts UNDER £15
  - publish the duplicate theme (the new templates only exist there)

## Layout rebuild (after Max's review, 28 Sep)
All 3 soaps and all 4 bath bomb sets now use `templates/product.mixmatch.json`:
1. Photos
2. Name and price
3. Intro (`mode: 'intro'`): the description's first paragraph and its facts as chips
4. Picker: the only add-to-basket on the page. Soaps also get "Or just this soap · £4.95".
5. Review stars and trust image
6. Details (`mode: 'details'`): How to use, Good to know and Ingredients as drop-downs, then the Delivery tab

Removed from these pages:
- the theme quantity box and Add to Cart (two add buttons confused things)
- gift wrap (bath bombs come boxed; nobody wraps a soap)
- the "Free Personalisation" badge
- the empty Related / Recently Viewed sections

The massage oil keeps `product.pamper.json`: a normal Add to Cart, no picker, no gift wrap, no personalisation badge.
Tested: on the Emerald Truffle page the trio gives £12.00, "just this soap" then takes it to £16.00, and there are no page errors.
Emerald Truffle ingredients: not on AW's product page either (it lists only the scent from perfume and patchouli). Its label shows a different recipe from the other two soaps (sucrose, SLS), so the page keeps "full list printed on the pack" rather than copying theirs.

## 28 Sep, later
- Emerald Truffle ingredients were read from Max's label photo and are now on the product page. "Sodium La…" at the photo's cut-off edge is taken as Sodium Laurate. One colour code after CI 42090 is cut off by the photo edge and is left out until someone reads the end of that line on the pack.
- Muscle Ease Massage Oil set to Active on Max's instruction.
- Launch (Max: "go"):
  - `main-nav` now has "Handmade Soap" and "Cocktail Bath Bombs" after Gift Bundles. The previous menu is backed up in the session scratchpad.
  - All 8 products are in Gifts UNDER £15 (`east-of-india`) and moved to the top in this order: Gin & Tonic, Rose, Mojito, Slice of Sunshine, Piña Colada, Emerald Truffle, Martini, massage oil.
  - The live theme hadn't changed since the duplicate was made (last live edit 13:20, copy made at 14:29), so publishing the duplicate loses nothing.
