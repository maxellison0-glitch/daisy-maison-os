# Daisy Maison unified stock tracker — 2026-07-21

Run time: 2026-07-21 06:36 Europe/London  
Source of truth: Daisy Maison Shopify and the tracker context in this repository. Gmail was read-only.

## Critical reorder actions

- **RECONCILE TODAY — Thermal Labels:** the corrected manual baseline gives an estimated **36 labels remaining** after 214 Shopify orders from 2026-07-17 through 2026-07-20; yesterday had 55 orders. Amazon order `206-3457020-8782768` also confirms delivery of one pack of two 250-label rolls (500 labels), but this receipt has not been treated as current on-hand. Physically count and reconcile before ordering.
- **RECONCILE / SUPPLY CHECK — Wooden Display Easel:** Shopify single-easel counter is **-71** after 4 sold yesterday and 38 in the last 7 days. Amazon has delivered one 32-easel pack and one separate 10-stand substitute pack, but current usable on-hand is unknown; do not infer a reorder quantity from the deliveries.
- **RECONCILE / SUPPLY CHECK — Mounting Strips (shared stock):** Shopify primary listing is **-51** after 9 single-strip orders yesterday. The shared physical usage is 18 pads yesterday and 126 pads over the last 7 days; Amazon confirms five 48-pad packs (240 pads) delivered under order `206-3457020-8782768`, but current physical on-hand is unknown.
- No East of India reorder quantity is confirmed today. The active East of India scan found no included product at a confirmed run-out after exclusions.

## East of India/accessory stock

### East of India

**None today** — no included East of India product is confirmed out of stock or at a confirmed run-out.

Yesterday was 2026-07-20; the seven-day velocity window was 2026-07-14 to 2026-07-20. Excluded/discontinued products and the Etsy gap were not silently treated as zero sales.

### Accessories

| Item / stock owner | Current Shopify counter | Sold yesterday | 7-day signal | Status |
|---|---:|---:|---:|---|
| [Wooden Display Easel](https://daisymaison.co.uk/products/wooden-display-easel) | -71 single units | 4 | 38 units (5.43/day) | ACTION — overselling is enabled; physical Amazon receipt is evidence only |
| Mounting Strips (shared stock; primary SKU `ACC-MOUNT-SINGLE`) | -51 listing units | 9 singles; 0 two-sign packs | 59 singles + 2 two-sign packs | ACTION — 18 pads used yesterday; physical balance unknown |
| [Gift Wrap Kit](https://daisymaison.co.uk/products/gift-wrapping) | -69 | 5 | 33 kits (4.71/day) | BLUE MADE TO ORDER — no reorder risk |
| Thermal Labels (manual) | Estimated 36 before 2026-07-20 receipt reconciliation | 55 labels | 379 orders (54.14/day) | ACTION — receipt and physical count need reconciling |

## Packaging usage

- **Shopify activity:** analytics reports 55 orders yesterday and 379 orders in the seven-day window. Fifty paid orders were expanded for line-item classification; the connector returned 57 matching order records while analytics reported 55, so the two sources do not reconcile perfectly.
- **Thermal labels:** 55 labels used yesterday. The corrected baseline was 250 labels from 2026-07-16, with tracking restarting 2026-07-17; 214 orders since then imply 36 labels before applying any new physical receipt. Amazon delivered 500 labels on 2026-07-20; current on-hand remains unknown.
- **Custom pebble-picture boxes:** 19 pebble-picture units in the daily sales aggregate. Seventeen single-picture orders were confirmed in the expanded paid-order sample; two units were in unexpanded orders, so exact box grouping is unknown. Estimated usage is **17–19 boxes**, **34–38 Guardian strips**, and **3.4–3.8m fragile tape**.
- **Medium/large street-sign packaging:** 24 medium/large size upgrades yesterday, requiring **8 × 725 x 1135mm corrugated sheets** under the three-sign-per-sheet rule and approximately **24m fragile tape**.
- **Mounting-strip packaging:** 9 primary single-strip orders yesterday used **18 physical pads**. No two-sign pack was recorded yesterday. The five Amazon Ormith packs delivered on 2026-07-20 represent 240 pads as receipt evidence, not confirmed remaining stock.
- **Receipt counters already recorded:** Macfarlane delivery note `10073374` recorded 300 custom boxes, 150 corrugated sheets, and 1 Guardian roll delivered; one Guardian roll remained to follow. These are receipt counters, not total on-hand.
- **Exact packaging order needed:** cannot be calculated safely today. Missing current on-hand, minimum reorder levels, lead times, preferred order quantities, exact envelope classifications, and the physical post-delivery counts for Amazon-sourced labels/pads/easels.

## Amazon stock watch

Amazon is supplier/order evidence only. Delivered state is recorded as a receipt, not as current remaining stock; order acknowledgements and cancelled orders are not treated as delivered stock.

| Item | ASIN / canonical link | Latest evidence | Order / quantity | Owner treatment |
|---|---|---|---|---|
| 32 Pcs 9 inch Wood Easels | [B0FQTSHJ6D](https://www.amazon.co.uk/dp/B0FQTSHJ6D) | Delivered 2026-07-20 | `206-3457020-8782768`, 1 pack / 32 easels; separate `206-3695011-7982722`, 2 packs cancelled after payment verification | Accessory receipt evidence; current on-hand unknown |
| L LIKED Direct Thermal Labels | [B07M834XD8](https://www.amazon.co.uk/dp/B07M834XD8) | Delivered 2026-07-20 | `206-3457020-8782768`, 1 pack / 2 rolls × 250 = 500 labels | Packaging receipt evidence; reconcile to thermal-label count |
| Ormith Double Sided Tape / mounting pads | [B0BRBS6VML](https://www.amazon.co.uk/dp/B0BRBS6VML) | Delivered 2026-07-20 | `206-3457020-8782768`, 5 packs / 48 pads each = 240 pads | Mounting-strip owner; current on-hand unknown |
| JOLCEEY lobster clasps and split rings | [B0DXDPSM4F](https://www.amazon.co.uk/dp/B0DXDPSM4F) | Delivered 2026-07-16 | `206-0080348-4608363`, 1 pack / 60 clips + 60 split rings | Accessory receipt evidence; no confirmed on-hand baseline |
| HOMSFOU small art easel stands | [B0GLMQPND7](https://www.amazon.co.uk/dp/B0GLMQPND7) | Delivered 2026-07-16 | `206-0080348-4608363`, 1 pack / 10 stands | Easel substitute receipt evidence; current on-hand unknown |
| Evergreen Goods 240 matte kraft labels | [B09MM95YGF](https://www.amazon.co.uk/dp/B09MM95YGF) | Delivered 2026-07-14 | Order number not exposed in the current Gmail result; 1 pack / 240 labels per reference | Packaging receipt evidence; current on-hand unknown |

## Missing inputs for Max

- Physical post-delivery on-hand for easels, mounting pads, thermal labels, Evergreen labels, JOLCEEY hardware, HOMSFOU stands, and all packaging materials.
- Minimum reorder level, supplier lead time, and preferred reorder quantity/case size for each packaging/accessory owner.
- Confirm whether the 500-label and 240-pad Amazon receipts have been physically received into the current counts; no Shopify inventory was mutated.
- Exact envelope setting and tape usage for each smaller product/order type.
- Etsy sales quantities from 2026-07-08 through 2026-07-20; the persistent Etsy log is confirmed only through 2026-07-07.
- Resolution of the Shopify connector mismatch: 55 analytics orders versus 57 matching order records, with only 50 detailed records returned in the current connector page.

