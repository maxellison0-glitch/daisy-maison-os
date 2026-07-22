# Daisy Maison unified stock tracker — 2026-07-22

Run time: 2026-07-22 Europe/London  
Source of truth: Daisy Maison Shopify and the tracker context in this repository. Shopify and Gmail were read-only.

## Critical reorder actions

- **ORDER NOW / reconcile — Thermal Labels:** the 250-label manual baseline has been consumed by **274 Shopify orders from 2026-07-17 through 2026-07-21**, implying **-24 labels before receipt reconciliation**. Amazon delivered 500 labels on 2026-07-20, but current physical on-hand is unknown. Count and reconcile before relying on the receipt.
- **RECONCILE / supply check — Wooden Display Easel:** Shopify’s single-unit counter is **-83** after 12 sold yesterday and 41 in the seven-day window. A 32-easel pack was delivered on 2026-07-20 and a new one-pack order is due Friday, but current usable on-hand and reorder threshold are unknown.
- **RECONCILE / supply check — Mounting Strips (shared stock):** the primary Shopify counter is **-62**. Yesterday’s usage was 13 single orders plus 1 Two Sign Pack = **30 physical pads**. Amazon delivered one 48-pad pack on 2026-07-20; current physical balance is unknown.
- No East of India product has a confirmed run-out today.

## East of India/accessory stock

### East of India

**None today** — no included East of India product is confirmed out of stock or at a confirmed run-out after the state-file exclusions. Yesterday was **2026-07-21**; the seven-day velocity window was **2026-07-15 to 2026-07-21**. Etsy remains unconfirmed after **2026-07-07**, so missing Etsy sales are not treated as zero.

### Accessories

| Item / stock owner | Current Shopify/manual signal | Sold yesterday | 7-day signal | Status |
|---|---:|---:|---:|---|
| [Wooden Display Easel](https://daisymaison.co.uk/products/wooden-display-easel) | -83 single units | 12 | 41 (5.86/day) | ACTION — overselling enabled; physical receipts do not establish current on-hand |
| Mounting Strips (shared stock; primary SKU `ACC-MOUNT-SINGLE`) | -62 listing units | 13 singles + 1 Two Sign Pack | 59 singles + 3 Two Sign Packs | ACTION — shared physical balance unknown |
| [Gift Wrap Kit](https://daisymaison.co.uk/products/gift-wrapping) | -76 single-kit counter | 8 | 34 (4.86/day) | BLUE MADE TO ORDER — no reorder risk |
| Thermal Labels (manual) | Estimated -24 before receipt reconciliation | 60 orders | 274 orders since baseline | ACTION — physical count required |

## Packaging usage

- **Shopify activity:** analytics reports **60 orders on 2026-07-21** and **363 orders from 2026-07-15 through 2026-07-21**. Fifty recent paid orders were expanded for line-item classification; the connector page contained 61 paid orders for 21 July, so detailed review is a sample rather than a complete daily order audit.
- **Thermal labels:** 60 labels used yesterday. The corrected baseline is 250 labels from 2026-07-16, with tracking restarting 2026-07-17. The 274-order cumulative signal puts the pre-receipt estimate at -24; Amazon receipt evidence is 500 labels (2 rolls × 250), not confirmed current on-hand.
- **Custom pebble-picture boxes:** 23 pebble-picture units were present in the expanded paid sample. Exact order grouping was unavailable, so estimated usage is **12–23 boxes**, **24–46 Guardian strips**, and **2.4–4.6m fragile tape**.
- **Medium/large street-sign packaging:** 19 Medium/Large size upgrades in the expanded paid sample require **7 × 725 × 1135mm corrugated sheets** under the three-packages-per-sheet rule and approximately **19m fragile tape**.
- **Mounting-strip packaging:** 13 single-strip orders plus 1 Two Sign Pack used **30 physical pads** yesterday. The Amazon 48-pad delivery is receipt evidence only; current balance remains unknown.
- **Receipt counters already recorded:** Macfarlane delivery note `10073374` records 300 custom boxes, 150 corrugated sheets, and 1 Guardian roll delivered; one Guardian roll remained to follow. These are receipt counters, not total on-hand.
- **Exact packaging order needed:** cannot be calculated safely. Missing current on-hand, minimum reorder levels, supplier lead times, preferred case quantities, exact small-item envelope classifications, and post-delivery physical counts.

## Amazon stock watch

Amazon is supplier/order evidence only. Delivered state is recorded as receipt evidence, not current remaining stock. Canonical product links are used below.

| Item | ASIN / canonical link | Latest lifecycle evidence | Order / quantity | Owner treatment |
|---|---|---|---|---|
| 32 Pcs 9 inch Wood Easels | [B0FQTSHJ6D](https://www.amazon.co.uk/dp/B0FQTSHJ6D) | Dispatched 2026-07-22; arriving Friday | `206-8739896-8331514`, 1 pack / 32 easels | Easel accessory incoming evidence; do not count as current on-hand |
| 32 Pcs 9 inch Wood Easels | [B0FQTSHJ6D](https://www.amazon.co.uk/dp/B0FQTSHJ6D) | Separate order cancelled 2026-07-20 after payment verification | `206-3695011-7982722`, 2 packs | Blocked/cancelled; no stock |
| 32 Pcs 9 inch Wood Easels | [B0FQTSHJ6D](https://www.amazon.co.uk/dp/B0FQTSHJ6D) | Delivered 2026-07-20 | `206-3457020-8782768`, 1 pack / 32 easels | Easel receipt evidence; current on-hand unknown |
| L LIKED Direct Thermal Labels | [B07M834XD8](https://www.amazon.co.uk/dp/B07M834XD8) | Delivered 2026-07-20 | `206-3457020-8782768`, 1 pack / 2 rolls × 250 = 500 labels | Packaging receipt evidence; reconcile to physical count |
| Ormith mounting pads | [B0BRBS6VML](https://www.amazon.co.uk/dp/B0BRBS6VML) | Delivered 2026-07-20 | `206-3457020-8782768`, 1 pack / 48 pads | Mounting-strip receipt evidence; current balance unknown |
| JOLCEEY lobster clasps and split rings | [B0DXDPSM4F](https://www.amazon.co.uk/dp/B0DXDPSM4F) | Delivered 2026-07-20 | `206-0505064-1012353`, 1 pack / 60 clips + 60 split rings | Accessory receipt evidence; current on-hand unknown |
| HOMSFOU small art easel stands | [B0GLMQPND7](https://www.amazon.co.uk/dp/B0GLMQPND7) | Delivered 2026-07-16 | `206-0080348-4608363`, 1 pack / 10 stands | Easel substitute receipt evidence; current on-hand unknown |
| Evergreen Goods kraft labels | [B09MM95YGF](https://www.amazon.co.uk/dp/B09MM95YGF) | Delivered 2026-07-14 | `206-9914735-1984337`, 1 pack / 240 labels | Packaging receipt evidence; current on-hand unknown |

## Missing inputs for Max

- Physical post-delivery on-hand for easels, mounting pads, thermal labels, Evergreen labels, JOLCEEY hardware, HOMSFOU stands, and all packaging materials.
- Minimum reorder level, supplier lead time, and preferred reorder quantity/case size for each packaging/accessory owner.
- Confirmation that the 500-label and 48-pad Amazon receipts have been physically reconciled; no Shopify inventory was mutated.
- Exact envelope setting and tape usage for each smaller product/order type.
- Etsy sales quantities from 2026-07-08 through 2026-07-21; persistent Etsy coverage is only through 2026-07-07.
- Complete paid-order packaging review for 21 July if the 50-order sample is insufficient; analytics and connector order counts differ.

