# Daisy Maison Unified Stock Tracker — 2026-07-16

Run date: 2026-07-16 (Europe/London)

Shopify retry succeeded on 2026-07-16. After Max explicitly asked to apply the invoice, four Shopify counters were updated with compare-and-set checks and reason `received`. Gmail searches completed and returned no matching Amazon lifecycle messages in the searched 30-day window.

## Critical reorder actions

- **Thermal Labels — ACTION / reorder now.** Estimated stock is 30 labels: 500 baseline less 470 Shopify orders from 2026-07-09 through 2026-07-15. At 67.1 orders/day, stock is projected to run out on 2026-07-16. Reorder quantity is unknown.
- **Personalised Teacher Porcelain Tea Light Holder — now 67.** Invoice line 5706 added 70 units to the previous -3 counter; at 7.6/day, approximately 8.8 days remain and the projected stock-out is 2026-07-24.
- **Personalised Teacher Porcelain Matchbox Star — now 29.** Invoice line 5663 added 25 units to the previous 4 counter; at 1.4/day, approximately 20.3 days remain and the projected stock-out is 2026-08-05.
- Amazon watch items remain watch-only: no current Gmail evidence was found for the four candidate ASINs, and none has a confirmed on-hand baseline, threshold, lead time, or reorder quantity.

## East of India/accessory stock

| Product / shared stock owner | Stock | Sold yesterday | Shopify avg/day (7d) | Etsy avg/day | Combined avg/day | Days left | Stock-out | Alert |
|---|---:|---:|---:|---:|---:|---:|---|---|
| Porcelain Handled Tea Light Holder - Good friends | 53 | 0 | 0.0 | 0.0* | 0.0 | N/A | N/A | BLACK NO SALES |
| Porcelain Matchbox - Little Guardian Angel | 33 | 0 | 0.1 | 0.0* | 0.1 | 330 | 2027-06-11 | GREEN OK |
| Porcelain Matchbox Message Dog - Never walk alone | 5 | 0 | 0.0 | 0.0* | 0.0 | N/A | N/A | BLACK NO SALES |
| Porcelain Matchbox Message Penguin - Flipping love you | 39 | 0 | 0.1 | 0.0* | 0.1 | 273 | 2027-04-15 | GREEN OK |
| Personalised Teacher Porcelain Matchbox Star - Thanks Teacher | 29 | 0 | 1.4 | 0.0* | 1.4 | 20.3 | 2026-08-05 | GREEN OK |
| Porcelain Matchbox Message Seal - Sealed with a kiss | 6 | 0 | 0.0 | 0.0* | 0.0 | N/A | N/A | BLACK NO SALES |
| Porcelain Handled Tea Light Holder - You are my sunshine | 8 | 0 | 0.0 | 0.0* | 0.0 | N/A | N/A | BLACK NO SALES |
| Personalised Teacher Porcelain Tea Light Holder - Thank You for Being Amazing | 67 | 3 | 7.6 | 0.0* | 7.6 | 8.8 | 2026-07-24 | YELLOW ORDER SOON |
| Teacher Matchbox Message Incense Cone - You Are Amazing | 2 | 0 | 0.0 | 0.0* | 0.0 | N/A | N/A | BLACK NO SALES |
| Wooden Display Easel | -46 | 3 | 7.7 | 0.0* | 7.7 | N/A | N/A | WATCH — overselling enabled; physical count required |
| Mounting Strips (shared stock) | -14 primary listing | 8 | 13.1† | N/A | 13.1 | N/A | N/A | WATCH — overselling enabled; physical count required |
| Gift Wrap Kit | 0 baseline by design | 6 | 6.3 | N/A | N/A | N/A | N/A | BLUE MADE TO ORDER |
| Thermal Labels | 30 estimated | 47 orders | 67.1 orders/day | N/A | 67.1 | 0.4 | 2026-07-16 | RED REORDER NOW |

\* Etsy data is only confirmed through 2026-07-07, with one logged 2026-07-08 Seal sale; the gap through 2026-07-15 means these figures must not be read as complete channel coverage. Discontinued and not-yet-on-Etsy products remain excluded per the state file.

† Mounting Strips velocity combines 84 units of the £1.99 listing and 4 Two Sign Pack units counted as 8 physical pairs; the legacy £3.90 and £4.95 listings had no matching 7-day sales.

## Packaging usage

- Paid Shopify orders reviewed: **50 recent paid orders** (the connector returned 477 total matching orders; the report reviewed the latest 50 read-only).
- Packaging usage classified from the sample: 21 medium/large street-sign upgrade contexts, equivalent to approximately 7 corrugated sheets; 16+ pebble-picture units requiring order-level box allocation; 10 single mounting-strip units; 5 Gift Wrap Kits; and 4 Wooden Display Easels. Exact box count is uncertain because line items do not always preserve the complete product grouping needed for per-order recipes.
- Packaging consumed: known usage exists. Receipt counters now recorded are 300 custom boxes, 150 corrugated sheets, and 1 Guardian paper roll delivered; 1 further Guardian roll remains to follow. Total on-hand after prior stock and usage is still **Unknown**.
- Invoice receipt evidence applied to Shopify: Seal 1→6, Lucky Sixpence 36→56, Teacher Star 4→29, and Teacher Tea Light -3→67. No other counters were changed.
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

- Confirm the Thermal Label reorder quantity and replenish before the estimated 2026-07-16 depletion point.
- Etsy quantities for the uncovered period 2026-07-08 through 2026-07-15, if Max wants combined channel velocity.
- Current packaging on-hand counts for each tracked item.
- Packaging reorder thresholds, supplier lead times, preferred order/case quantities, and unresolved usage rules (small-item tape, street-sign envelope choice, and add-on handling).
- For Amazon candidates: confirmed stock owner, current on-hand, usage rule, reorder threshold, preferred order quantity, lead time, and substitute policy.
