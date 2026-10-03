# Price audit and landing-page review — 3 October 2026

## Outcome and publication state

Audited all **783 active products / 959 variants**, the live theme's **1,023 files (997 text files)**, accessible product/variant metafields, **410 Globo option sets**, and the installed-app inventory. Corrected **14 product titles, 9 variant labels, 146 SEO price claims and 2 Globo offer labels**. Final full-catalogue verification confirms all 959 selling prices and compare-at values match the starting values. One transient Globo side effect was caught and restored, detailed below.

The conversion work is deliberately scoped to the five landing pages in Max's handoff: **407 landing sessions and 30 orders** across 1–2 October (handoff figures, not re-attributed here). Broader catalogue label corrections are audit maintenance, not claimed conversion improvements. The actual theme difference is **281 lines added / 16 removed across 14 files**. Full downloaded theme copies and raw working data are excluded from the source commit.

**Published with Max's approval on 3 October 2026 at 16:37:26 BST (15:37:26 UTC).** Theme **208326623571**, **Codex – price clarity & clean pages – 3 Oct**, is now live. The previous theme **208291496275** (Claude – cart split fix (2 Oct)) remains unpublished and available for rollback. Immediately before publication all 14 reviewed file bodies matched, and the previous live theme had not changed since the audited baseline. References to “draft” below describe the reviewed implementation and its pre-publication tests; that implementation is now published.

[Preview Mr & Mrs](https://daisymaison.co.uk/products/mr-mrs-personalised-street-sign-gift?preview_theme_id=208326623571) · [All five screenshot pairs](../projects/price-landing-audit-2026-10-03/screenshots/index.html) · [Draft source patch](../projects/price-landing-audit-2026-10-03/draft-theme.patch)

## The four reported problems

| Product | Where | Shows / observed | Actual | Fixed? |
|---|---|---|---|---|
| Grandparent Garden sign | Catalogue variants | Small £11.25 looks unusual | £11.25 / £17.24 / £20.24; Mr & Mrs currently has the same selling-price ladder | **Decision required.** No evidence establishes an accidental discount. Selling prices untouched. |
| Family / Create Your Own | Compare-at values | Only Small has a “was” value | Family Small £14.95 was £28.95; Medium £20.94 and Large £23.94 have none. Create Small £16.95 was £24.95; Medium £22.94 and Large £25.94 have none | Draft displays only the selected variant's valid compare-at. No invented Medium/Large “was” price. Policy question below. |
| Create Your Own | Catalogue vs 2 Oct sales | Medium sold at £24.94 yesterday | Current Medium £22.94; Large £25.94. Aggregated 2 Oct sales confirm Medium £24.94 and Large £25.94 | **Decision required** on intended price. Draft size buttons and total use current variant data. Exact change time/actor unavailable. |
| Second personalised sign | Product title / offer | “2nd sign for £9.95” implies one price | Small £9.95 / Medium £15.94 / Large £18.94 | **Title fixed live.** Draft cart offer lists each size's actual price; Large tested at £18.94. |

The 2 Oct Large second-sign aggregate includes reversals: gross £37.88, net £18.94, net quantity 1. It is not evidence of a £37.88 unit price. No customer-level order data was needed.

## Confirmed label and display corrections

| Product | Where | Shows (before) | Actual / corrected display | Fixed? |
|---|---|---|---|---|
| option-set-728788-select-1 | Product title | **INCREDIBLE OFFER** Buy a second one for just £10.95 | **INCREDIBLE OFFER** Buy a second one for just £4.95 | Yes — live label only |
| option-set-767521-select-1 | Product title | **INCREDIBLE OFFER** Buy a second one for just £15 | **INCREDIBLE OFFER** Buy a second one for just £10.00 | Yes — live label only |
| option-set-767526-select-1 | Product title | **INCREDIBLE OFFER** Buy a second one for just £15 | **INCREDIBLE OFFER** Buy a second one for just £15.60 | Yes — live label only |
| option-set-769814-select-1 | Product title | **INCREDIBLE OFFER** Buy a second laser cut sign for just £24.95 | Second Laser Cut Sign — Greenhouse £9.95 / Other Sign £24.95 | Yes — live label only |
| 6-99-incredible-offer | Product title | (+£6.95) **INCREDIBLE OFFER** FESTIVE SIGN | (from £6.95) **INCREDIBLE OFFER** FESTIVE SIGN | Yes — live label only |
| option-set-769051-select-1 | Product title | **INCREDIBLE OFFER** Buy a second one for just £12.95 | **INCREDIBLE OFFER** Buy a second one for just £13.95 | Yes — live label only |
| option-set-769063-select-1 | Product title | **INCREDIBLE OFFER** Buy a second one for just £12.95 | **INCREDIBLE OFFER** Buy a second one for just £13.95 | Yes — live label only |
| option-set-769038-select-1 | Product title | **INCREDIBLE OFFER** Buy a second keyring for just £3.95 | **INCREDIBLE OFFER** Buy a second keyring for just £4.95 | Yes — live label only |
| option-set-769976-select-1 | Product title | **INCREDIBLE OFFER** Buy a second coaster for just £4.95 | **INCREDIBLE OFFER** Buy a second coaster from £4.95 | Yes — live label only |
| 11-89-x3-easels | Product title | (+£11.89) x3 Easels | (+£11.85) x3 Easels | Yes — live label only |
| 9-95-incredible-offer-spooky-kooky-sign | Product title | (+£9.95) **INCREDIBLE OFFER** Spooky Kooky Sign | (from £9.95) **INCREDIBLE OFFER** Spooky Kooky Sign | Yes — live label only |
| 9-small-street-sign | Product title | (£7.45) Small Street Sign | Street Sign Size Options — from £7.45 | Yes — live label only |
| incredible-offer-get-a-2nd-sign-for-9-95 | Product title | **INCREDIBLE OFFER - GET A 2ND SIGN FOR £9.95 | Second Personalised Sign — Small £9.95 / Medium £15.94 / Large £18.94 | Yes — live label only |
| 7-95-plush-elf-friend | Product title | (£7.95) Plush Elf Friend | Plush Elf Friends — Twin Pack £13.95 | Yes — live label only |
| Seven helper products / nine option values | Variant names | Pebble count +£3, second-item £12.95, large-heart +£3, keyring £3.95, and two +£2 labels | Matched existing variant charges: £4 / £9.95 / £13.95 / £5 / £4.95 / £0.00 as applicable | Yes — see variant-label-corrections.json; no variant IDs or prices changed |
| 146 SEO fields | global.title_tag / description_tag | Stale “Just £…” amount did not equal current minimum | Removed only the stale price phrase, preserving the rest of the SEO copy | Yes — live, compare-and-set writes after verifying original values |
| Minifigure Keyring | Globo set 772537, select-2 | Second keyring £7.95 | £8.95 | Yes — saved label and refreshed the same existing variant link; native storefront was already correct |
| Robin remembrance | Globo set 772528, select-13 | Heading £4.95 beside an option charging £11.95 | £11.95 | Yes — saved label and refreshed the same existing variant link |
| Family / Create Your Own | Main-price header, size buttons and total | Header could remain at starting price; total represented an increment | Full selected variant price, plus chosen strips in the total | Yes — draft |
| Mr & Mrs | Selected-size “was” calculation | Base compare-at plus upgrade could produce an invented comparison | The selected variant's own compare-at, plus actual chosen add-ons when displaying a basket total | Yes — draft |
| Five scoped pages | Product sale presentation | Unqualified “from” / sale state could survive a size change | Selected price and valid compare-at only in the price header | Yes — draft |

Exact original and new strings, product IDs and variant IDs are in the correction JSON files. They form the rollback record; restoring labels does not require touching prices.

## Full inventory and review flags

- [active-variants.csv](price-audit-2026-10-03/active-variants.csv): all 959 variants, selling price, compare-at, title amounts, invalid comparisons and unusual pence. “Nonstandard pence” is a screening flag, not proof of a mistake: £5.99 size increments legitimately produce .94 and .24 prices.
- [theme-price-references.csv](price-audit-2026-10-03/theme-price-references.csv): **403** currency literals across Liquid/JS/JSON/CSS, with file and line. Includes comments, old fallbacks, product-specific examples, shipping thresholds and inactive code; not 403 confirmed storefront errors.
- [globo-price-inventory.csv](price-audit-2026-10-03/globo-price-inventory.csv): **2,419** price-linked or price-text rows from 410 sets, with option/set IDs and linked variant prices. Export examined 21,977 rows. Customer rules and other unrelated settings were excluded from saved evidence.
- The Globo inventory flags 225 cached-price differences, 157 label/increment screening flags, and 92 references not found in the **active** catalogue. These overlap. 178 cached differences are assigned to at least one active parent product. Missing active variants may be archived; they are not automatically broken links.
- [Compressed catalogue and metadata evidence](price-audit-2026-10-03/catalogue-metadata-evidence.zip) contains the before/after catalogues, theme manifests, accessible active-product/variant metafield keys, SEO values and detailed Globo flags. 618 SEO fields carried price amounts, 146 stale claims corrected. These are audit snapshots, not source-code changes.
- [price-verification.json](price-audit-2026-10-03/price-verification.json): before/after catalogue reconciliation. This is a point-in-time audit, not a permanent price monitor.

**Globo interpretation matters.** The Robin storefront already fetched £11.95 for its option while its manually written heading remained £4.95. The app editor still cached £4.95. Consequently a stale exported cache is not itself proof that customers see or pay that value. “Large £17.95” can be a valid full product total with a £3 upgrade. Per-unit easel labels can legitimately differ from a pack's total. These were not blindly rewritten to the increment. Two wedding-bundle sets even associate the six-easel choice with a **6x Magnets** helper; this requires a product-mapping decision, not a guessed price edit.

Globo's official [import documentation](https://docs.globo.io/options/option-sets/import-and-export) explicitly says imports create new sets rather than update existing ones. No bulk re-import was performed. The two clear active offer errors were edited in the app and their existing variant links refreshed.

**Observed app side effect, corrected:** saving the Robin set reset its linked Shopify variant from the original £11.95 to the stale £4.95 despite the refreshed link showing £11.95. Final storefront verification caught this. The original £11.95 was restored immediately via Shopify and a fresh complete 783-product/959-variant query confirmed no remaining selling-price or compare-at differences. This transient change is recorded in [globo-save-side-effect.json](price-audit-2026-10-03/globo-save-side-effect.json). Future Globo edits should compare linked Shopify prices immediately after saving; do not assume a label save is price-neutral.

### Invalid compare-at values (left for Max)

| Product | Where | Shows | Actual selling price | Fixed? |
|---|---|---|---|---|
| Personalised Acrylic Robin Family Tree Decoration / Default Title | Variant compare-at | £9.95 | £15.95 | No — price/promotion decision |
| Personalised Acrylic Robin Remembrance Tree Decoration / Default Title | Variant compare-at | £9.95 | £15.95 | No — price/promotion decision |
| Personalised Halloween Street Sign Gift — Spooky Kooky \| Funny Halloween Home Decoration / Small | Variant compare-at | £0.00 | £14.95 | No — price/promotion decision |
| 3D Framed Stag Artwork / Default Title | Variant compare-at | £34.95 | £34.95 | No — price/promotion decision |
| 3D Framed Bull Artwork / Default Title | Variant compare-at | £34.95 | £34.95 | No — price/promotion decision |
| 3D Framed Bull Artwork / Default Title | Variant compare-at | £34.95 | £34.95 | No — price/promotion decision |
| Friends are like stars pebble picture / Default Title | Variant compare-at | £34.95 | £34.95 | No — price/promotion decision |
| 3D Framed Horse Artwork / Default Title | Variant compare-at | £34.95 | £34.95 | No — price/promotion decision |

### App, checkout and collection coverage

33 installed apps were enumerated. **Candy Rack is not installed.** Globo and Aftersell are installed. Theme embeds: Globo, Instafeed, Klaviyo and Stape enabled; Feefo embeds, OptiMonk and Bevy disabled in the inspected configuration. App block and embed configuration matches across the retained 2 Oct themes; it does not establish when apps were first installed.

The existing native basket finishing offer uses current product data and a 10% accessory discount. A £5.95 gift-wrap kit displayed and reached checkout at **£5.36**; the tested total was **£27.59** with a £20.24 Large Mr & Mrs sign and £1.99 strips. The two-sign strips pack is a separate **£3.99** variant; the legacy £3.90 and £4.95 mounting products are different IDs, not evidence that one variant is charging three prices. Current Wooden Display Easel is £5.95; legacy wedding-bundle easels are £3.95 each.

Aftersell has three active post-purchase funnels. Street sign ppu runs a 50/50 test: mounting strips versus easels/gift wrap, both at 10% off; subsequent tea-light offers use 20% or 30%. Its editor preview confirms both Single Gift Wrap Kit – Ivory & Twine and Single Wooden Display Easel at £5.36, down from £5.95. No test, discount, eligibility rule or post-purchase selling price was changed. The relevant street-sign funnel was inspected; the two other heart funnels were enumerated, not exhaustively exercised. No paid order was placed to test post-purchase acceptance. The live A/B test is a confounder when evaluating accessory take rate.

Collection/card prices and badges derive from Shopify product/variant data in the theme, rather than a second collection-specific price table. Product-level sale badges may describe a Small-only promotion across a product with other full-price variants; Max should decide the comparison-price policy. The eight invalid compare-at records above remain in the catalogue. This is not a claim that all 959 variants, every conditional app branch or every market was transaction-tested.

## Landing-page changes

Counts refer to optional upsell groups before the main Add to Cart, not required personalisation/size controls. Mobile evidence is 390 CSS pixels wide; screenshots include the Shopify preview toolbar where Shopify displayed it.

| Product | Sessions → orders (1–2 Oct handoff) | Before | Draft | Remaining upfront add-on | Preview |
|---|---|---:|---:|---|---|
| Mr & Mrs Street Sign | 190 → 17 | 5 | 1 | Mounting strips | [Open](https://daisymaison.co.uk/products/mr-mrs-personalised-street-sign-gift?preview_theme_id=208326623571) |
| Engagement Love Tree | 52 → 5 | 4 | 1 | Easel | [Open](https://daisymaison.co.uk/products/engagement-proposal-love-tree-personalised-pebble-picture-copy?preview_theme_id=208326623571) |
| Family Street Sign | 65 → 3 | 4 | 1 | Mounting strips | [Open](https://daisymaison.co.uk/products/family-personalised-street-sign?preview_theme_id=208326623571) |
| Create Your Own Street Sign | 34 → 2 | 4 | 1 | Mounting strips | [Open](https://daisymaison.co.uk/products/kitchen-personalised-street-sign?preview_theme_id=208326623571) |
| Wedding Flower Arch | 66 → 3 | 4 | 1 | Easel | [Open](https://daisymaison.co.uk/products/wedding-flower-arch-personalised-pebble-picture?preview_theme_id=208326623571) |

Personalisation, size, price and the main action stay together. Extra offers default to “No thanks”; required blank personalisation still blocks submission. Reviews, delivery information and product descriptions remain. Hidden legacy offer controls cannot add unseen items. Second signs and pictures move to a collapsed basket section with editable wording and actual variant prices; matching hearts link to their personalisation page. Existing cart easel/wrap/strips offers and the cart diffuser offer remain.

The new second-sign basket line uses the actual parent line key. Its transport uses the existing DaisyCartSubmit reconciliation helper so an uncertain response asks the buyer to review the basket instead of encouraging a duplicate add. The 2 Oct cart-split fix is retained.

### Validation

- All five mobile pages inspected before/after; no horizontal overflow in the recorded 390px screenshots. Desktop Mr & Mrs inspected at the browser's effective 1309px CSS width with one mounting-strip block and no horizontal overflow.
- Eight recorded cart/checkout scenarios passed: Create Large £25.94; second Large £18.94; Mr & Mrs Large + strips £22.23; wrap checkout total £27.59; Family Medium + strips £22.93; Engagement + easel £30.90; second Engagement total £50.90; Wedding easel deselection restores one £22.95 item. Fake QA personalisation only; test baskets cleared and no order placed.
- Six price-model regression assertions pass, covering selected compare-at, no compare-at, quantities, independently changing prices and native parent linkage. A separate basket regression check covers parent-line linkage, retained personalisation, success navigation, and preventing duplicate retries after an uncertain response. Changed JS files pass syntax checks. The final transport integration was checked locally after the browser's isolated QA session closed; the recorded live-cart scenarios predate that transport-only substitution.
- Shopify Liquid validation passes for the 14 modified files **with inherited warnings**. The unmodified theme has three parser-blocking legacy scripts; the scoped validation explicitly disables that existing ParserBlockingScript check. Baseline and scoped output are saved. This is not a claim that the inherited theme is globally warning-free.
- The full automated safety suite is proportionate to this draft: no production payment, no traffic experiment, no assertion that conversion will improve.

## What changed between 28 Sep and 3 Oct

The retained theme versions and repo history do **not** provide a complete 28 Sep baseline. No exact all-week change list can be reconstructed honestly. The evidence available is:

| Retained theme | Created / updated on 2 Oct (UTC) | Differences from current live |
|---|---|---|
| 208250732883 — Claude – pet landing page (2 Oct) | 07:44 / 10:51 | daisy-cart-submit.js; daisy-street-sign-options.js; dm-pet-sign.js |
| 208260268371 — Claude – pet preview colours (2 Oct) | 10:11 / 18:20 | daisy-cart-submit.js; daisy-street-sign-options.js |
| 208280125779 — Claude – family beach pebble picture (2 Oct) | 15:06 / 15:57 | daisy-cart-submit.js; daisy-street-sign-options.js; daisy-pebble-picture.js; dm-pebble builder/proof snippets (exact paths in patch) |
| 208291496275 — current live cart split fix | 18:09 / 18:20 | Source of the duplicate created for this audit |

The live cart helper groups split lines before checking quantities and parent relationships; the Mr & Mrs error path releases the loading state. Pet-preview colour differences are present in retained history. Family-beach builder changes exist in that separate retained draft and are **not proven published**. Product templates and app/config checksums match across the retained 2 Oct versions. A source comment dates dm-upsell-accordion to 29 Sep; that is source evidence, not a publication timestamp. The exact [retained diffs](price-audit-2026-10-03/retained-theme-differences.patch) and manifests are saved.

The handoff's fall in upsell take rate is real task context, but timing alone does not establish that page clutter caused it. Aftersell's live offer split, traffic and product mix also matter.

## Competitor observations

Sampled comparable UK personalised-gift listings on 3 Oct, not a verified ranking of best performers:

| Listing | Optional accessory blocks before the initial purchase button | Placement |
|---|---:|---|
| [Oakdene Designs / NOTHS street sign](https://www.notonthehighstreet.com/oakdenedesigns/product/personalised-metal-street-sign) | 0 initially; 2 inside personalisation | Sticky tabs (£2.60) and gift card (£3) within the personalisation drawer |
| [Ladedaliving / Etsy wedding pebble picture](https://www.etsy.com/uk/listing/1732879333/personalised-wedding-pebble-picture) | 0 separate accessory blocks | Frame/size configuration and personalisation before Add to basket |
| [RSmyHandicraft / Etsy wedding gift](https://www.etsy.com/uk/listing/1082292106/personalised-wedding-gift-wedding-gift) | 0 separate accessory blocks | Frame configuration and personalisation before Add to basket |

The relevant design lesson is a short product-configuration path. These observations do not prove a conversion-rate advantage.

## Decisions for Max — no selling-price changes made

1. **Grandparent Small:** retain £11.25, or what should Small/Medium/Large be? The matching Mr & Mrs ladder may be intentional.
2. **Create Your Own:** are Medium £22.94 and Large £25.94 now intended, or should either return to the previous £24.94 / £27.94 ladder? The 2 Oct Medium sale supports £24.94 at that time, not the intent now.
3. **“Was” policy:** maintain Small-only promotions, remove them, or supply genuine per-size comparison prices? Also resolve the eight invalid comparisons above. Do not derive fictitious “was” prices from size increments.
4. **Legacy helper mapping/prices:** `9-small-street-sign` currently has Small £7.45 / Medium £13.44 / Large £10.45; confirm the inverted Medium/Large ladder. Confirm £0 large-decoration increments and whether old easel/mounting packs should stay distinct. The Tuscany/Riviera six-easel choices link to a six-magnet helper: which variant should those choices use?
5. **Publish the duplicate after preview.** Record the actual publication time. This audit's date is not the start of the landing-page experiment.

## Measurement and rollback

Use the actual publication timestamp to compare complete, equal-length windows. Track orders with strips/easel/wrap divided by eligible orders, per product and offer surface, alongside conversion, checkout abandonment and AOV. Keep the existing Aftersell A/B split visible in the analysis. Do not resume the obsolete “Large size upgrade take rate” metric; Large is a main variant.

Until publication, the current live layout remains unchanged. After publication, restoring theme 208291496275 rolls back the theme work; catalogue labels/SEO/Globo are separate shared data and have their own before/after records. Do not restore old wrong price labels merely to roll back layout.
