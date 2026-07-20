# Daisy Maison Unified Stock Tracker — 2026-07-20

Run time: 2026-07-20 06:34:31 +01:00 Europe/London (read-only run)

Coverage: Shopify yesterday = 2026-07-19; Shopify velocity = 2026-07-13 to 2026-07-19; Shopify analytics recorded 63 orders yesterday and 813 net items in the 7-day window. Gmail/Amazon lifecycle searches covered the last 30 days.

## Critical reorder actions

- **ORDER NOW — Wooden Display Easel (Shopify accessory owner):** primary single variant is **-67** available (`ACC-EASEL`); the set of three is 0. Overselling is enabled, but the counter is materially negative. Exact order quantity cannot be calculated because preferred pack quantity, reorder threshold, and lead time are missing. Amazon evidence includes a separate payment-blocked 2-pack and a newer dispatched 1-pack; neither is counted as current stock.
- **ORDER NOW — Mounting Strips (shared Shopify accessory owner):** primary physical-stock listing is **-40** (`ACC-MOUNT-SINGLE`); other shared listings are -407, -12, and the two-sign pack is -14. The 13–19 July signal is 64 primary-listing units plus 2 two-sign packs, with each two-sign pack consuming 2 pairs. Exact order quantity cannot be calculated because physical on-hand baseline, reorder threshold, preferred quantity, and lead time are missing.
- **WATCH — Thermal Labels:** estimated **91 labels remaining** from the corrected 250-label baseline on 2026-07-16 less 159 Shopify orders since 2026-07-17. Reorder threshold and replacement quantity are missing; Amazon thermal-label evidence in a combined order is supplier evidence only.
- **WATCH — packaging materials:** usage is confirmed, but total on-hand and reorder thresholds are not. No safe order quantity can be calculated.

## East of India/accessory stock

### East of India

**None today** — no confirmed East of India run-out. Variant-level inventory was used because some Shopify `totalInventory` values conflicted with positive variant quantities. Discontinued and excluded products remain omitted. Shopify sales were 0 East of India net items on 2026-07-19; the broader store totals were 112 net items yesterday and 813 over the 7-day window. Etsy remains uncovered after 2026-07-07, so these are Shopify-only signals.

### Accessories

| Item / stock owner | Current Shopify available | 2026-07-19 sales | 13–19 Jul sales | Alert |
|---|---:|---:|---:|---|
| Wooden Display Easel (`ACC-EASEL`, single; set of three separate) | -67; set of three 0 | 10 | 43 | **RED REORDER NOW**; overselling enabled |
| Mounting Strips (shared stock; primary `ACC-MOUNT-SINGLE`) | -40 primary; other shared listings -407 / -12 / -14 | 5 primary listing units | 64 primary listing units + 2 two-sign packs | **RED REORDER NOW**; two-sign packs consume 2 pairs each |
| Gift Wrap Kit (`ACC-GIFTWRAP`) | -63 single; two-kit 0 | 5 | 33 | **BLUE MADE TO ORDER**; do not reorder as held stock |
| Thermal Labels (manual baseline) | 91 labels estimated remaining | 63 labels used | 159 labels used since 2026-07-17 baseline | **WATCH**; threshold missing |

## Packaging usage

Shopify analytics recorded **63 orders** on 2026-07-19. Product-level analytics show **28 pebble-picture units**, **22 medium/large street-sign upgrades**, 5 primary mounting-strip units, 10 easel units, and 5 gift-wrap kits. Exact order-level pebble grouping was not available in the connector response, so box and Guardian usage is shown as a range rather than treating aggregate units as order count.

| Packaging item | Estimated 2026-07-19 usage | Receipt / stock position | Reorder status |
|---|---:|---|---|
| Custom pebble-picture boxes | **14–28 boxes** for 28 pictures (exact grouping missing; up to 2 pictures per box) | 300 delivered on delivery note 10073374; total on-hand unknown | **WATCH** — need current on-hand, threshold, lead time, preferred quantity |
| Guardian paper strips | **28–56 strips** (2 per pebble box) | 1 roll delivered on delivery note 10073374, about 180 strips; 1 further roll to follow; total on-hand unknown | **WATCH** — need current on-hand, threshold, lead time, preferred quantity |
| 725 × 1135 mm corrugated sheets | **8 sheets** allocated to 22 medium/large street-sign packages (3 packages per sheet) | 150 delivered on delivery note 10073374; total on-hand unknown | **WATCH** — need current on-hand, threshold, lead time, preferred quantity |
| Fragile tape | **Approximately 24.8–27.6m**: 22m street-sign usage + 2.8–5.6m pebble-box usage | Roll stock unknown | **WATCH** — need current on-hand, threshold, lead time, preferred quantity |
| Small / medium / large Mail Lite envelopes | Exact size split unknown; 63 order packages reviewed by analytics | Stock unknown | **WATCH** — need size-by-product mapping and current counts |

Packaging receipt evidence: Macfarlane delivery note **10073374**, order **6277938**, dated 2026-07-16. Receipt counters are not total on-hand counts. The 900 × 1140 mm sheet remains discontinued for future costing.

## Amazon stock watch

Amazon evidence is supplier/order-state evidence only. Delivered state does not prove current on-hand where stock may already have been consumed, and no Amazon item has been added to Shopify or packaging counters.

| Item | Qty / order | Latest state | Owner / treatment | Canonical link |
|---|---:|---|---|---|
| 32 Pcs 9 inch Wood Easels | 2 packs; order `206-3695011-7982722` | **BLOCKED — pending payment verification** | Shopify accessory owner; do not count as incoming | [Amazon](https://www.amazon.co.uk/dp/B0FQTSHJ6D) |
| 32 Pcs 9 inch Wood Easels | 1 pack; order `206-3457020-8782768` | **DISPATCHED — arrival status not confirmed** | Shopify accessory owner; supplier evidence only | [Amazon](https://www.amazon.co.uk/dp/B0FQTSHJ6D) |
| JOLCEEY 120pcs Swivel Lobster Clasps and Split Rings | 1 pack; order `206-0505064-1012353` | **DISPATCHED / delivery not confirmed**; prior estimate was 2026-07-19 | Shopify mounting/keyring evidence; not current stock | [Amazon](https://www.amazon.co.uk/dp/B0DXDPSM4F) |
| HOMSFOU 10pcs Small White Plastic Art Easel Display Stand | 1 pack; order `206-0080348-4608363` | **DELIVERED 2026-07-16** | Accessory supplier evidence; current on-hand unknown | [Amazon](https://www.amazon.co.uk/dp/B0GLMQPND7) |
| Evergreen Goods 240 Matte Kraft Sticker Paper Labels | 1 pack; order `206-9914735-1984337` | **DELIVERED 2026-07-14** | Packaging/label supplier evidence; not added to thermal-label count | [Amazon](https://www.amazon.co.uk/dp/B09MM95YGF) |

## Missing inputs for Max

- Current physical on-hand for packaging items, including envelopes, boxes, Guardian rolls/strips, corrugated sheets, and fragile-tape rolls.
- Packaging reorder thresholds, supplier lead times, and preferred order/case quantities.
- Exact paid-order grouping for the 28 pebble-picture units, or confirmation that the 14–28 box range is acceptable for planning.
- Current physical on-hand and reorder policy for Amazon-sourced easel/keyring items; confirm whether delivered HOMSFOU easels are an accepted substitute for the Shopify easel.
- Confirmed Etsy sales or a catch-up through at least 2026-07-19; current Etsy coverage stops at 2026-07-07.
- Confirmed small-item envelope size mapping and a fixed tape-use assumption for Mail Lite packages.

No Shopify, Gmail, Amazon, or other external system was mutated during this run.
