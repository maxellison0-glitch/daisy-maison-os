# Daisy Maison Unified Stock Tracker — 2026-07-19

Run time: 2026-07-19 07:30 Europe/London (scheduled read-only run)

Coverage: Shopify yesterday = 2026-07-18; Shopify velocity = 2026-07-12 to 2026-07-18; paid-order packaging review used recent paid orders returned by Shopify; Amazon/Gmail lifecycle search covered the last 30 days.

## Critical reorder actions

- **ORDER NOW — Wooden Display Easel (Shopify accessory owner):** primary single variant is **-57** available (`ACC-EASEL`); the three-pack is 0. Overselling is enabled, but the counter is materially negative. Exact order quantity is not calculated because the preferred pack quantity, reorder threshold, and lead time are missing. Amazon supplier evidence includes a separate **2-pack** order that is payment-blocked and must not be treated as incoming stock.
- **ORDER NOW — Mounting Strips (shared Shopify accessory owner):** primary physical-stock listing is **-35** (`ACC-MOUNT-SINGLE`); other shared listings are -407, -12, and the two-sign pack is -14. Reported as one physical stock owner. Exact order quantity is not calculated because physical on-hand baseline, reorder threshold, preferred quantity, and lead time are missing.
- **WATCH — packaging materials:** usage is confirmed, but total on-hand and reorder thresholds are not. No quantity can be safely ordered from this run.
- **WATCH — JOLCEEY keyring hardware:** Amazon order is delayed to 2026-07-19; it is incoming supplier evidence only, not current stock.

## East of India/accessory stock

### East of India

No confirmed East of India run-out today. The zero `totalInventory` values returned for some products conflicted with positive variant-level quantities, so variant inventory was used as the live stock figure. Discontinued and excluded products remain omitted.

Shopify sales: **104 net items** and **52 orders** on 2026-07-18; **851 net items** over 2026-07-12 to 2026-07-18. Etsy remains uncovered after 2026-07-07, so these are Shopify-only signals.

### Accessories

| Item / stock owner | Current Shopify available | 2026-07-18 sales | 7-day sales | Alert |
|---|---:|---:|---:|---|
| Wooden Display Easel (`ACC-EASEL`, single; set of three is separate listing) | -57; set of three 0 | 4 | 40 | **RED REORDER NOW**; overselling enabled |
| Mounting Strips (shared stock; primary `ACC-MOUNT-SINGLE`) | -35 primary; other shared listings -407 / -12 / -14 | 10 single listings | 73 single listings + 3 two-sign packs | **RED REORDER NOW**; overselling enabled; two-sign packs consume 2 pairs each |
| Gift Wrap Kit (`ACC-GIFTWRAP`) | -58 single; two-kit 0 | 4 | 32 | **BLUE MADE TO ORDER**; do not reorder as held stock |
| Thermal Labels (manual baseline) | 154 labels estimated remaining | 52 labels used | 96 labels used since 2026-07-17 baseline | **WATCH**; 250-label baseline less Shopify order count; no reorder threshold |

## Packaging usage

Paid Shopify order review covered **50 recent paid orders** returned by the connector; Shopify analytics recorded **52 orders** for 2026-07-18. Order-level classifications found 16 pebble-picture orders, 27 medium/large street-sign upgrades, 10 mounting-strip add-ons, 4 easel add-ons, and 4 gift-wrap kits. The two-order connector difference is retained as a coverage limitation, not treated as zero usage.

| Packaging item | Estimated 2026-07-18 usage | Receipt / stock position | Reorder status |
|---|---:|---|---|
| Custom pebble-picture boxes | 16 boxes (1 box per reviewed picture order) | 300 delivered on delivery note 10073374; total on-hand unknown | **WATCH** — need current on-hand, threshold, lead time, preferred quantity |
| Guardian paper strips | 32 strips (2 per pebble box) | 1 roll delivered on delivery note 10073374, about 180 strips; 1 further roll to follow; total on-hand unknown | **WATCH** — need current on-hand, threshold, lead time, preferred quantity |
| 725 × 1135 mm corrugated sheets | 9 sheets allocated to 27 medium/large street-sign packages (3 packages per sheet) | 150 delivered on delivery note 10073374; total on-hand unknown | **WATCH** — need current on-hand, threshold, lead time, preferred quantity |
| Fragile tape | Approximately 30.2m: 27m street-sign usage + 3.2m pebble-box usage | Roll stock unknown | **WATCH** — need current on-hand, threshold, lead time, preferred quantity |
| Small / medium / large Mail Lite envelopes | At least 52 order packages, but exact size split is not reliable from current order data | Stock unknown | **WATCH** — need size-by-product mapping and current counts |

Packaging receipt evidence: Macfarlane delivery note **10073374**, order **6277938**, dated 2026-07-16. The receipt counters above are not total on-hand counts.

## Amazon stock watch

Amazon evidence is supplier/order-state evidence only. No delivered item has been added to current on-hand because consumption and Shopify ownership may already apply.

| Item | Qty / order | Latest state | Owner / treatment | Canonical link |
|---|---:|---|---|---|
| 32 Pcs 9 inch Wood Easels | 2 packs; order `206-3695011-7982722` is payment-blocked | **BLOCKED — pending payment verification** | Shopify accessory owner; do not count as incoming | [Amazon](https://www.amazon.co.uk/dp/B0FQTSHJ6D) |
| JOLCEEY 120pcs Swivel Lobster Clasps and Split Rings | 1 pack; order `206-0505064-1012353` | **DELAYED — estimated 2026-07-19** | Amazon watch; not current stock | [Amazon](https://www.amazon.co.uk/dp/B0DXDPSM4F) |
| HOMSFOU 10pcs Small White Plastic Art Easel Display Stand | 1 pack; order `206-0080348-4608363` | **DELIVERED 2026-07-16** | Accessory owner; delivery evidence only, current on-hand unknown | [Amazon](https://www.amazon.co.uk/dp/B0GLMQPND7) |
| Evergreen Goods 240 Matte Kraft Sticker Paper Labels | 1 pack; order `206-9914735-1984337` | **DELIVERED 2026-07-14** | Packaging/label supplier evidence; not added to thermal-label count | [Amazon](https://www.amazon.co.uk/dp/B09MM95YGF) |

## Missing inputs for Max

- Current physical on-hand for packaging items, including envelopes, boxes, Guardian rolls/strips, corrugated sheets, and fragile-tape rolls.
- Packaging reorder thresholds, supplier lead times, and preferred order/case quantities.
- Current physical on-hand and reorder policy for Amazon-sourced easel/keyring items; confirm whether delivered HOMSFOU easels are an accepted substitute for the Shopify easel.
- Confirmed Etsy sales or a catch-up through at least 2026-07-18; current Etsy coverage stops at 2026-07-07.
- Confirmed small-item envelope size mapping and a fixed tape-use assumption for Mail Lite packages.

No Shopify, Gmail, Amazon, or other external system was mutated during this run.
