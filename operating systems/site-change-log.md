# Daisy Maison Site Change Log

Compact, dated confirmation of website and Shopify changes. Planned work does
not belong here until Max confirms it happened.

## 2026-10-09 — Storybook range: engagement, christening, new baby (theme 208801857875)

- **Christening** 10927915991379 (was The Good Life) → `storybook-christening-pebble-picture`; **New Baby** 10927918973267 (was Friends) → `storybook-new-baby-pebble-picture`. Team changed titles/photos; descriptions, SEO, alt text rewritten; collections Framed Pebble Art + Personalised Christening & New Baby Gifts (left Pebble People).
- **Builders follow image 1, examples = image 1 wording:** christening = pebbles 1–8 (+£3 over 6), keep/own "On Your Christening Day", Name(s) "Lily Blossom Walker", Church or venue (optional) "St Christopher’s Church, Springfield", Date "9th November 2026". New baby = pebbles 1–8, keep/own "How Wonderful Life Is Now You’re In The World", Baby’s name "Beau Wren". Engagement examples already image 1 (Yazmin + Luke, 14th October 2026).
- Same theme 208801857875, renamed "Claude – Storybook range (3) – 9 Oct"; md5s verified. Phone test on preview, all 3: builder, no Globo, add to basket with all properties, checkout opens, 0 errors. All 3 UNLISTED until the theme is published, then ACTIVE.

- **Fence range collapsed:** the 4 fence products were one design, so all 16 fence photos now sit on Our Little Family (ACTIVE, 10927920578899), and The Good Life (10927915991379) + Friends (10927918973267) stay DRAFT until the team swaps in new designs/titles.
- **Product 10927937290579** (was Together Always) re-titled by the team to "Personalised Engagement Pebble Picture Gift — The Storybook Collection" with 2 new photos. Handle → `storybook-engagement-pebble-picture`; description/SEO rewritten for the proposal picnic design ("The Beginning of Always", names, date); alt text added; collections Framed Pebble Art + Personalised Engagement Gifts (left Pebble People).
- **Theme 208801857875** "Claude – Storybook engagement – 9 Oct" (from live 208785637715, uploaded after processing finished, md5s verified): old Together Always handle replaced by kind `storybookengagement` — Frame Colour, wording keep/own (default "The Beginning of Always"), Names, Date; review line "Loved for engagements and proposals". Phone test on preview: builder, no Globo, add to basket with all properties, checkout opens, 0 errors.
- **Process for the next two:** team changes photos + title → handle/description/SEO/collections (Framed Pebble Art + category) + builder per the new artwork → theme copy → publish → ACTIVE.

## 2026-10-09 — Fence pebble picture range: 4 products + landers (theme 208785637715, live 9 Oct)

- **LIVE 9 Oct:** Max published theme 208785637715; all 4 products set ACTIVE straight after (still not on Shop). Pre-publish checks on the preview, phone: builder + default wording + review line, no Globo (none of the 4 IDs are in Globo's option-set map), add to basket with all personalisation properties, checkout opens, 0 page errors. Extra pebbles on Together Always: 8 pebbles → £3 "7/8 Pebbles" add-on line, basket £32.95, all 8 pebbles + names carried. Desktop: arrows gallery, centred price, 0 errors. Post-publish: all 4 return 200 on the live theme with builder + review line.
- **Products (UNLISTED until the theme is live; set ACTIVE after publish):** The Good Life `the-good-life-pebble-picture` (10927915991379), Friends Make the World Beautiful `friends-make-the-world-beautiful-pebble-picture` (10927918973267), Our Little Family `our-little-family-pebble-picture` (10927920578899), Together Always `together-always-family-pebble-picture` (10927937290579). Same settings as Together/Home: £29.95 / compare-at £34.95, untracked + CONTINUE, 1.1 kg, Daisy Maison vendor, Framed Pebble Art + Pebble People, description/SEO in the house pattern (SEO line says "Free UK Delivery Over £50", not "FAST FREE DELIVERY"). Published to Online Store, POS, Facebook & Instagram, Google & YouTube, TikTok — **not Shop** (Shop-app orders skip personalisation).
- **Images:** Higgsfield Nano Banana Pro 2K square from Max's photos (photos themselves not used on the products): close hero first, modern take, pebble close-up, room shot, then the shared white gift-wrap image. The gift-wrap image is the existing shared file (MediaImage 62448711139667), not a copy — never productSet these products' files without it.
- **Theme draft 208785637715** "Claude – Fence range landers – 9 Oct" (from live 208648110419): builder kinds `goodlife` / `friendsworld` / `littlefamily` / `togetheralways` cloned from `together` (default wording = the print's wording), handles in the JS list, grey + spray lists, fast gallery; proof quotes reuse existing verbatim reviews that had been used once (Always Forever, True Friends, To the Moon, Engagement artwork). Also restores Home to the fast-gallery list — live had lost it because the Home theme copy was still processing when the file was uploaded and the copy overwrote it. **Rule: upload only after `processing: false`, then re-verify.**
- Flagged, not changed: Family Blossom Tree SEO title/description contain "¬£" mojibake.

## 2026-10-07 — Desktop gallery + builder readability (same draft 208648110419)

- **Desktop/tablet gallery bug:** from 768px the theme stacked every image (Mr & Mrs: 14 images = 8,650px) beside a sticky details column taller than the screen, so Add to cart was unreachable until all images were scrolled past. New `snippets/dm-desktop-gallery.liquid`: one image at a time, arrows, "n / N" counter, thumbnails switch the image. Phones unchanged.
- **Pebble builder wording:** "Number of pebbles (including pets)" with 1–8 ("(+£3)" on 7/8), each pebble "Select pebble" + "Fill in name for pebble N", selects "Select frame colour". Cart values unchanged ("4 (Inc dog/cat)" etc.).
- **Readability pass** `snippets/dm-builder-polish.liquid` (pebble + street-sign builders): measured vs Globo (109px/field, 14px labels) ours used ~250–300px/field with 10–12px text. Now 16px sentence-case labels, small print ≥14px, 16px/48px inputs (no iOS zoom), eyebrow pills and the pebble intro sentence removed. Selectors use `html:root body[class]` to outrank `daisy-product-poc.css`.
- Extended to hanging-heart (wedding/teacher), family / create-your-own and native sign builders (labels 16px, small print 13–15px, 16px inputs, eyebrow pills removed). Price row on family / create-your-own signs (`.dm-clean-price`, flex) was left-aligned under a centred title; now centred like every other page.
- Tested on the draft: pebble (Home) and Mr & Mrs add to basket with all properties → checkout.
- Known, not ours: theme header script logs a caught TypeError (sticky-header missing); theme.js logs a JSON parse error from a background request.

## 2026-10-07 — Globo off all 142 builder products (draft 208648110419)

- Max published the Home lander theme (now "Live -- tested 07/10", 208643621203).
- Globo's `productOptionSetMap` lists 526 products (338 public). Checking each public page for our builder markers: **142** have our own builder (68 hearts, 35 pebble pictures, 39 signs/other), **196** rely on Globo only and are untouched. The 142 product IDs are now in the Globo-off list in `snippets/dm-mobile-fixes.liquid`; list with option-set IDs in `landing-pages-2026-10-05/globo-off-products.csv` (134 option sets; 11 are shared with Globo-only products — remove products, don't delete those sets).
- Draft **208648110419** "Claude – Globo off all builder products – 7 Oct". Phone check on the draft: all 142 load with no Globo and our form present; two Globo-only controls still show Globo. (Bulk checking triggers Shopify 429 rate limits — re-check slowly.)

## 2026-10-07 — 'Home' modern pebble lander (draft 208643621203)

- **Product** `personalised-family-pebble-picture-gift-same-stars-unique-mothers-day-christmas-birthday-gift` (10919278969171, live, created by the team): added description + SEO in the Together pattern, compare-at £34.95, sell when out of stock (untracked), 1.1 kg, Pebble People + Modern Pebble Pictures, Framed Pebble Art after Together. No Globo on it (checked live).
- **Theme draft 208643621203** "Claude – Home lander – 7 Oct" = live 208556032339 + builder kind `modernhome` (Together clone, default wording "Our Family") with an optional **Second line** field (design has a second line, e.g. "Est. 2010"), in the four handle-keyed files; the four modern landers added to the Globo-off list. Phone test on the draft: 4 named pebbles + second line → `/cart` with every property → checkout.
- Still on the Shop app channel (can't unpublish via API) — Shop-app orders skip personalisation (order DM41567).
- Unused leftover: unlisted placeholder product 10919279690067 `modern-family-pebble-picture` (created 6 Oct, awaiting Max's keep/delete).

## 2026-10-06 — Globo off the top-10 revenue pages (draft 208556032339)

- `snippets/dm-mobile-fixes.liquid`: on 10 product IDs (Mr & Mrs sign, Wedding pebble, Engagement love tree, Family sign, Christening, Create-your-own sign, Family Blossom Tree, Wedding hanging heart, Mum Flutterby, New Home — top 60-day net sales, add-ons excluded, Tea Light Holder skipped as it has no Globo) the theme makes `GPOConfigs.options` ignore writes, so Globo renders nothing and adds no Add to cart guard. Our builders already handled all ten; none depend on Globo. Globo's own admin still lists the option sets; remove them there later if wanted.
- Same draft removes three basket upsells (Max, 6 Oct: too few takes): diffuser offer (`dm-matching-gift`), "Finish your gift" checkout pop-up (`dm-cart-upsells`) and "Add another personalised gift" box (`dm-cart-extra-gifts`). Only their renders in `sections/main-cart.liquid` are commented out; snippets kept. Since 3 Oct: ~2 extra-gift orders, 1–2 diffuser orders, a handful of discounted easels/wraps. Checkout button now goes straight to checkout.
- Same draft carries the basket gift-box fix. Phone test on the draft: all ten reach basket via the main button; checkout reached through the Aftersell "Finish your gift" pop-up.

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

