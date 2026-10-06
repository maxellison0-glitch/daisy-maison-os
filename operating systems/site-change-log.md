# Daisy Maison Site Change Log

Compact, dated confirmation of website and Shopify changes. Planned work does
not belong here until Max confirms it happened.

## 2026-10-06 — Together theme published; basket gift-box fix in draft

- Max published **208538960211** (Together lander + cookie fix + Globo add-to-cart fix). Together product set ACTIVE, on all six channels, added to Framed Pebble Art (5th, after Same Stars) and Pebble People.
- **Basket:** `snippets/dm-cart-extra-gifts.liquid` (3 Oct) showed one "Add another personalised gift (optional)" box per qualifying basket line (6 signs → 6 boxes). Now once per product. In draft **208556032339** "Claude – basket gift box fix – 6 Oct"; Max publishes.

## 2026-10-06 — Main "Add to cart" blocked by hidden Globo (fix in draft 208538960211)

- **Bug:** on products where our own builder replaces Globo (street signs, pebble landers), the big Add to cart button did nothing; the sticky button worked. Cause: a Globo Product Options update (extension `globo-product-options-472`) now cancels ATC clicks from a window capture listener when its hidden option set's required fields are empty, before our builders see the tap. Not caused by the 5–6 Oct theme work; it reproduced on the 3 Oct and 2 Oct themes too.
- **Fix:** `snippets/dm-mobile-fixes.liquid` (product pages) marks the tapped button with Globo's own opt-out (`.gpo-exclude` / `egw-atc-override`) when Globo's form is hidden. Products with visible Globo options are untouched. Tested on the draft: Mr & Mrs (main and sticky), Blossom, Golden Skies and Together all reach `/cart`.
- **Longer term:** unassign the old Globo option sets from products that use our builders (or turn off the Globo app embed once nothing uses it).

## 2026-10-06 — Together pebble-picture lander (draft, awaiting publish)

- **Product:** Together Family Pebble Picture (`together-family-pebble-picture`, 10917497110867), created UNLISTED on Online Store only. Same price/settings/description pattern as Same Stars. Images: 4 Nano Banana 2 heroes (2k, 1:1, 10 credits incl. one redo where the A4 frame came out square) then Max's 4 real photos.
- **Theme draft 208538960211** “Claude – Together lander + cookie fix – 6 Oct” = live theme + builder kind `together` (default wording “Together side by side”) in the four handle-keyed files + the cookie-banner fix in `dm-mobile-fixes`. Files in `landing-pages-2026-10-05/theme-files/`.
- **On publish:** set product ACTIVE, publish to the other five channels, add to Framed Pebble Art (after Same Stars) and Pebble People.
- **Upload route that works:** Shopify-CDN (`cdn.shopify.com/.../files/`) URLs as `themeFilesUpsert` bodies silently fail; `raw.githubusercontent.com` URLs from this (public) repo save immediately, overwrites included. Supersedes the 5 Oct tooling note. Drafts 208489152851 (cookie fix only) is superseded.

## 2026-10-05 — Golden Skies and Same Stars pebble-picture landers live

Max published theme **208484598099** “Claude – Same Stars landing + extra-pebble price – 5 Oct” in Shopify admin (previous: 208480764243 Golden Skies, before that 208326623571 Codex 3 Oct, both retained for rollback). Theme diff against the 3 Oct theme: `landing-pages-2026-10-05/live-theme-208484598099.patch`.

- **Golden Skies Family Pebble Picture** (`golden-skies-family-pebble-picture`, 10914052637011) and **Same Stars Family Pebble Picture** (`same-stars-family-pebble-picture`, 10914092253523) are exact copies of the Family Blossom Tree lander: builder kinds `goldenskies` / `samestars` cloned from `blossom` (frame incl. grey, 1–8 pebbles with names, wording keep/change, second picture, easel, gift wrap), same proof quote, fast gallery, grey-frame and spray lists. Only wording differs (defaults “Always under golden skies” / “Always under the same stars”). Cart property keys match Blossom. New landers: add the handle in the same four files (builder snippet, `assets/daisy-pebble-picture.js` handle list, `dm-proof`, `product-page-right-thumbs`).
- **Product data (live):** £29.95 with £34.95 compare-at, sell when out of stock, 1.1 kg, Blossom-structure description and SEO. Both in Framed Pebble Art (manual sort: Golden Skies 3rd, Same Stars 4th) and Pebble People.
- **All pebble builders:** the 7/8-pebble options now say “+£3” with the line “Up to 6 pebble characters included. Choose 7 or 8 for +£3.” (price read from `3-7-8-pebbles-1`, one flat add-on). Inputs 16px (no iOS zoom), Return = “Done” and closes the keyboard, theme capitalisation removed from that note and the wording preview.
- **“New” badge off site-wide** (`snippets/product-badge.liquid`, `if false`).
- **Cookie banner:** heading and Privacy Policy link were white on cream since the 2 Oct `custom.css` restyle. Fix is in draft **208489152851** “Claude – cookie banner text fix – 5 Oct” (`landing-pages-2026-10-05/cookie-fix-draft-208489152851.patch`) — **not yet published** as of 6 Oct.
- Leftovers, harmless: unused theme files `assets/daisy-pebble-picture-v2.js`, `snippets/dm-product-badge-src.liquid` (live) and `assets/dm-write-test.css` (cookie draft). Temporary upload files removed from Shopify Files.
- Tooling note: URL-based `themeFilesUpsert` overwrites silently drop at random; new files and `themeFilesCopy` (new file → copy over) or TEXT bodies are reliable.

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

