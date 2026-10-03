# Daisy Maison Site Change Log

Compact, dated confirmation of website and Shopify changes. Planned work does
not belong here until Max confirms it happened.

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

