# Daisy Maison Unified Stock Tracker — 2026-07-16

Run date: 2026-07-16 (Europe/London)

Data was requested read-only. Shopify live checks were blocked because the connected Shopify app requires reauthentication. Gmail searches completed and returned no matching Amazon lifecycle messages in the searched 30-day window.

## Critical reorder actions

- **No reorder quantity can be confirmed today.** Shopify inventory, sales, 7-day velocity, paid orders, and packaging usage inputs are unavailable until Shopify is reauthenticated.
- Do not treat the missing Shopify response as zero stock or zero sales.
- Amazon watch items remain watch-only: no current Gmail evidence was found for the four candidate ASINs, and none has a confirmed on-hand baseline, threshold, lead time, or reorder quantity.

## East of India/accessory stock

| Product / shared stock owner | Stock | Sold yesterday | Shopify avg/day (7d) | Etsy avg/day | Combined avg/day | Days left | Stock-out | Alert |
|---|---:|---:|---:|---:|---:|---:|---|---|
| East of India active range | Unknown | Unknown | Unknown | Unknown* | Unknown | Unknown | Unknown | UNKNOWN — Shopify reauth required |
| Wooden Display Easel | Unknown | Unknown | Unknown | 0.0* | Unknown | Unknown | Unknown | UNKNOWN — Shopify reauth required |
| Mounting Strips (shared stock) | Unknown | Unknown | Unknown | 0.0* | Unknown | Unknown | Unknown | UNKNOWN — Shopify reauth required |
| Gift Wrap Kit | 0 baseline by design | Unknown | Unknown | 0.0* | Unknown | N/A | N/A | BLUE MADE TO ORDER |
| Thermal Labels | Unknown | Unknown | Unknown | N/A | Unknown | Unknown | Unknown | UNKNOWN — Shopify reauth required |

\* Etsy data is only confirmed through 2026-07-07, with one logged 2026-07-08 Seal sale; the gap through 2026-07-15 means these figures must not be read as complete channel coverage. Discontinued products remain excluded per the state file.

## Packaging usage

- Paid Shopify orders reviewed: **Unknown** — Shopify reauthentication required.
- Packaging consumed: **Unknown**, not zero.
- Packaging stock/reorder status: **Unknown** because current on-hand, thresholds, lead times, and preferred order quantities are not recorded in the shared packaging references.
- Classification rules retained for the next successful run: pebble boxes and Guardian strips, small/medium/large envelope rules, corrugated sheets for medium/large street signs, and fragile-tape usage.

## Amazon stock watch

Gmail searches were read-only and covered the four reference ASINs over the recent 30-day window. No matching messages were returned, so current order state, quantity, order number, and delivery estimate/state are **unknown**.

| Item | ASIN | Canonical link | State |
|---|---|---|---|
| 32 Pcs 9 inch Wood Easels | B0FQTSHJ6D | [Amazon product](https://www.amazon.co.uk/dp/B0FQTSHJ6D) | WATCH — no current Gmail evidence |
| JOLCEEY 120pcs Swivel Lobster Clasps and Split Rings | B0DXDPSM4F | [Amazon product](https://www.amazon.co.uk/dp/B0DXDPSM4F) | WATCH — no current Gmail evidence |
| HOMSFOU 10pcs Small White Plastic Art Easel Display Stand | B0GLMQPND7 | [Amazon product](https://www.amazon.co.uk/dp/B0GLMQPND7) | WATCH — no current Gmail evidence |
| Evergreen Goods 240 Matte Kraft Sticker Paper Labels | B09MM95YGF | [Amazon product](https://www.amazon.co.uk/dp/B09MM95YGF) | WATCH — no current Gmail evidence |

Amazon evidence does not establish current on-hand stock. No item is promoted to a reorder action.

## Missing inputs for Max

- Reauthenticate the Daisy Maison Shopify connector, then rerun inventory, explicit-date sales/velocity, order-count, and recent paid-order checks.
- Etsy quantities for the uncovered period 2026-07-08 through 2026-07-15, if Max wants combined channel velocity.
- Current packaging on-hand counts for each tracked item.
- Packaging reorder thresholds, supplier lead times, preferred order/case quantities, and unresolved usage rules (small-item tape, street-sign envelope choice, and add-on handling).
- For Amazon candidates: confirmed stock owner, current on-hand, usage rule, reorder threshold, preferred order quantity, lead time, and substitute policy.
