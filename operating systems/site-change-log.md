# Daisy Maison Site Change Log

Compact, dated confirmation of website and Shopify changes. Planned work does
not belong here until Max confirms it happened.

## 2026-10-23 ~15:20 BST — Family Christmas Walk landing page built like Wonderland (DRAFT theme, Max publishes)

**Product** `personalised-family-christmas-walk-decoration-the-storybook-collection-personalised-pebble-christmas-tree-keepsake-unique-christmas-gift` (id 11016863973715, still DRAFT). Copied from Wonderland (9436262629715): price £15.95, compare-at £19.95, weight 0.072 kg, taxable, inventory not tracked. Description and SEO title/description copied with the product name swapped, and the "-¬£50" encoding glitch fixed to "£50". Joined the same 6 manual collections: Christmas, Christmas Gifts Top Picks, Christmas Hanging Decorations, Occasions, Pebble Hanging Hearts, Pebble People. No SKU set; Wonderland's is XT-537-WFC, so the new SKU is Max's call.

**Theme** draft **210012406099** "Christmas Walk builder – 23 Oct (draft)", duplicated from live 209801642323. UNPUBLISHED; Max publishes. 3 files:
- `layout/theme.liquid`: added the new handle to the line-412 heart-builder handle list, straight after Wonderland's.
- `snippets/dm-heart-builder.liquid`: new handle → kind `xmaswalkheart`, plus `{%- when 'xmaswalkheart' -%}{%- render 'dm-heart-xmaswalk-config' -%}`.
- `snippets/dm-heart-xmaswalk-config.liquid` (new): a copy of the `wonderlandheart` config. Three differences only: heading "Create your Family Christmas Walk heart", offer note "Personalise another Family Christmas Walk heart at a special price", and a gift box list holding ONLY Christmas 2026 (small 54335779570003 / large 54335779602771, same image). Cart property keys and values are unchanged, so fulfilment reads them the same way.
- Why a separate snippet: dm-heart-builder.liquid is 255KB, against Shopify's 256KB per-file limit, and an inline copy was silently rejected. **Any future kind must go in its own snippet the same way.**
- Upload method that works: stagedUploadsCreate PUT, then themeFilesUpsert `type: URL` pointing at the staged resourceUrl. A cdn.shopify.com Files URL silently fails.
- Checks: all 3 file checksums match the local edited copies. Wonderland's rendered config on the draft theme is byte-identical to live.
- Leftovers: two harmless comment-only test snippets on the draft (`snippets/zz-upsert-test.liquid`, `snippets/zz-url-staged.liquid`), never rendered. Delete them in admin; the API blocks theme-file deletes.

**Before publishing:** the draft was duplicated at ~15:10 BST on 23 Oct. Any change made to live after that is missing from the draft.

CORRECTION 2026-10-23 ~15:30 BST (Max): "build like Wonderland" did not mean copying Wonderland's customer wording. This product has the wording at the TOP and the names at the BOTTOM. Updated `dm-heart-xmaswalk-config.liquid` (draft theme only):
- Field labels: "Wording at the top" (e.g. The Harrison Family at Christmas) and "Names at the bottom" (e.g. Dad, Mum, George, Charlie, Poppy, Lily, Milo, Buddy). The offer fields use the same wording.
- `itemNoun: "decoration"` and `companionName: "Second decoration"`, because it's round, not a heart. This is the same pattern as the diffusers.
- Large-size suffixes now say "decoration".
- Property KEYS are still Wonderland's ("Text above", "Text below", "Add 2026?", "Size 1", "**INCREDIBLE OFFER**"), so fulfilment reads orders the same way. Visible differences on order lines: "Gift box for: Decoration 1" and "Add-on: Second decoration".

CORRECTION 2026-10-23 ~15:35 BST (Max): removed the "Add 2026?" field from the main and the offer decoration, because this design has no year. Gift box switched to `style: "cards"`: picture cards visible from the start ("No gift box, thanks" / "Christmas 2026 gift box" / "2 Christmas 2026 gift boxes"), the same card look as the Gift Wrap Kit, with a 400px image. Same variants and prices (small £3.95 / large £4.95). No badge was added, because there's no data behind a "Most popular" claim. Draft theme only.

2026-10-23 ~15:50 BST (Max: "implement and we see how it looks"): the builder intro line now shows the pebble price ladder on BOTH Christmas Walk and Wonderland (draft theme only): "1–4 pebbles: small £15.95 or large £18.95 · 5–6 pebbles: large £18.95 · 7–8 pebbles: large £20.95." Reason: at 7–8 pebbles the total jumps £5 while the Large card still says +£3, and nothing on the page explained it. Wonderland change is inside the `wonderlandheart` block only; other kinds sharing the old sentence are untouched. Checked: the draft renders the new Wonderland copy, and nothing else in its config changed. **The prices are typed into the copy, so update the line if a price changes.**

CORRECTION 2026-10-23 ~16:00 BST (Max: "overwhelming and clunky on mobile, get rid"): the price ladder copy is REVERTED on both pages. Replaced, on **Christmas Walk only** (Max: leave Wonderland unless told), by a note under the pebble counter that appears only when it applies:
- 5–6 pebbles: "5 or more pebbles need our large size (15 × 15cm): +£3."
- 7–8 pebbles: "7 or 8 pebbles need the large size plus extra pebbles: +£5 in total."
- 1–4 pebbles: hidden.
The second-decoration counter works the same way.
- `assets/daisy-heart-builder.js` (draft): new opt-in `pebbles.stepNotes` support. Without it, products render exactly as before. The offer counter title "Second heart pebbles" now uses `noun(config)`, which still renders "heart" everywhere except Christmas Walk ("decoration").
- Tested in headless Chromium at 390px on a local harness: the note shows and hides at 3/5/6/7/8/4, totals £15.95/£18.95/£20.95, no JS errors. Live Wonderland on the draft theme with the new JS: no note, 7 pebbles = £20.95, no errors.

2026-10-23 ~16:05 BST (Max: "1 box does not need a dropdown"): the theme's add-on accordion folded the gift box cards behind a closed header. Christmas Walk now opts out with `giftBox.open: true`; daisy-heart-builder.js adds `dm-acc-off`, the same opt-out the diffusers use. The cards show straight away: "No gift box, thanks", then the Christmas 2026 box picture, price and Select button. Tested at 390px with the theme's real accordion script: without the flag the cards are hidden (closed); with it, 2 cards are visible. One tap = single box, total £15.95 → £19.90. Other products are unchanged (no flag).

## 2026-10-12 ~16:50 BST — Incredible Offer back on landing pages (theme "working copy - Max" published by Max)

Live theme **209047290195** "working copy - Max" (previous live 208785637715 kept for rollback). Changed files: `snippets/dm-clean-product.liquid`, `assets/dm-clean-product.css`, `assets/dm-clean-product.js`, `snippets/dm-heart-builder.liquid`.

- **Second-item offer switched back on** for the 5 pages hidden on 3 Oct (Mr & Mrs, Family, Create Your Own signs; Engagement Love Tree, Wedding Flower Arch pebbles). Second item has its own size/wording; add-ons offer "one / both".
- **One add-on per page** on Max's Google Ads list (8 signs, 17 pebble pictures, 5 hearts/decorations): signs = mounting strips, pebbles = easel, hearts = gift box. Removed from those pages: matching heart, gift wrap kit, Lucky Sixpence, easel on signs. All removed add-ons default to off.
- **New second-heart offer** on Family and Christening pebble hearts: Small £10.95 / Large £13.95 (same as other hearts), mirrors pebbles + both wording lines, 5 pebbles forces Large.
- Basket-tested (no orders placed): 8 signs, 5 pebble pages, Family + Christening hearts, Festive star, Good Friends tea light (no offer). Wedding heart second-heart fields confirmed; its basket test was blocked by Cloudflare.
- **Known issue not fixed:** New Home pebble — second picture's Frame Colour dropdown is empty (pre-existing config gap), so the offer can't be completed there. One-line fix given to Max.
- **Not on site:** Mum Flutterby Blossom Tree, Grandparent Pebble Sketch, Engagement Pebble Artwork (on Max's Google Ads list) return 404 — products deleted.
- Tea light second-item discount not built — waiting on Max's 10% / 20% decision.

**Measurement start:** compare upsell take rate, AOV, conversion and checkout abandonment from the publish time against 3–11 Oct.

## 2026-10-03 at 16:37:26 BST — reviewed landing-page theme published

Max approved publication after reviewing the layout and the base-upsell placement. Codex published theme **208326623571**, “Codex – price clarity & clean pages – 3 Oct”, using Shopify admin. Shopify confirms MAIN; previous theme **208291496275** is UNPUBLISHED and retained for rollback. Preflight confirmed all 14 reviewed file bodies matched and no intervening changes to the previous live theme. No additional theme code or selling-price changes were made during publication.

**Measurement start:** 2026-10-03 16:37:26 BST / 15:37:26 UTC. Compare complete equal-length pre/post windows for the five scoped landing pages and track conversion, accessory take rate, checkout abandonment and AOV. Account for Aftersell's existing 50/50 test and traffic mix; this release has no measured conversion lift yet.

## 2026-10-03 — price corrections and pre-publication audit

Executed by Codex under `codex-handoff-2026-10-03-prices-landing-pages.md`. [Full audit and decisions](price-audit-2026-10-03.md). Final catalogue check: 783 active products / 959 variants; all selling prices and compare-at values match the starting snapshot. The Globo incident below was a transient exception, restored before completion.

- **Live catalogue labels:** corrected 14 product titles and 9 variant option labels to describe existing charges. Includes the second-sign size ladder (£9.95 / £15.94 / £18.94), x3 easels (£11.85), and legacy helper labels. Exact product IDs and original/new wording: `price-audit-2026-10-03/title-corrections.json` and `variant-label-corrections.json`. These broad audit fixes are not claimed landing-page conversion improvements.
- **Live SEO labels:** removed 146 stale “Just £…” price phrases from global SEO fields using verified compare-and-set writes; retained the rest of the copy. Per-field rollback record: `price-audit-2026-10-03/seo-label-corrections.json`.
- **Live Globo labels:** Minifigure Keyring set 772537/select-2 now says £8.95; Robin remembrance set 772528/select-13 now says £11.95. Refreshed the same linked existing variants. Keyring's native storefront was already correct; Robin's storefront previously said £4.95 in the heading and £11.95 in the option.
- **Globo side effect caught/restored:** saving Robin unexpectedly reset variant 49588707623251 to stale £4.95. Restored its original £11.95 immediately. Final live heading and option both show £11.95; whole-catalogue recheck found no remaining selling-price/compare-at differences. Record: `price-audit-2026-10-03/globo-save-side-effect.json`.
- **Draft created:** theme 208326623571, “Codex – price clarity & clean pages – 3 Oct”, duplicated from live 208291496275. 14 changed files, actual source diff +281/−16. **UNPUBLISHED; Max publishes.**
- **Draft Mr & Mrs Street Sign:** 190 landing sessions → 17 orders in the handoff's 1–2 Oct window. Five optional upsell groups reduced to mounting strips only. Selected-size compare-at calculation corrected. Large + strips tested at £22.23.
- **Draft Engagement Love Tree:** 52 → 5. Four optional groups reduced to easel only. Picture + easel tested at £30.90; second picture available in basket, combined test £50.90.
- **Draft Family Street Sign:** 65 → 3. Four optional groups reduced to strips only. Full size prices and selected total made explicit. Medium + strips tested at £22.93.
- **Draft Create Your Own Street Sign:** 34 → 2. Four optional groups reduced to strips only. Current Medium £22.94 / Large £25.94 displayed consistently; Large without extras tested at £25.94. Previous Medium £24.94 sale confirmed; intended selling prices remain Max's decision.
- **Draft Wedding Flower Arch:** 66 → 3. Four optional groups reduced to easel only. Deselecting easel restored one £22.95 picture. Reviews and delivery information retained on all five pages.
- **Draft basket:** added collapsed, personalised second-sign/picture offers with current variant prices, actual parent line linkage and existing cart-response reconciliation. Large second sign tested at £18.94. Existing accessory offer and 10% discount retained; gift wrap reached checkout at £5.36. No order placed.
- **Aftersell read-only finding:** existing Street sign ppu funnel splits traffic 50/50 between strips and easel/wrap, each with 10% off. Editor confirms easel/wrap £5.36 from £5.95. No funnel or discount changed. This is a measurement confounder, not a new rollout.

The draft status in the audit entries above records the original handoff state. Publication and its measurement start are recorded in the later entry at the top. Do not track Large as a separate upsell (it is a main variant).

## 2026-07-12

- New products added to the Daisy Maison website. Product names, count,
  handles, and publication state were not specified.
- Cleaning-kit upsell completed/ticked off. Exact storefront placement,
  eligible products, price, and live test status remain unconfirmed.

