# Daisy Maison unified stock tracker - 18 July 2026

Run timestamp: 18 July 2026, 06:35 Europe/London  
Shopify sales windows: yesterday **17 July 2026**; 7-day velocity **11-17 July 2026**.  
Shopify and Gmail checks were read-only. Etsy data remains confirmed only through 7 July 2026.

## Critical reorder actions

| Priority | Item / stock owner | Evidence | Action and quantity basis |
|---|---|---|---|
| **RED** | Wooden Display Easel - Accessories / Shopify | Available **-53** on `ACC-EASEL`; 3 sold yesterday and 51 in the 7-day window. | Resolve the shortage now. The Amazon 2-pack is payment-blocked and is not counted as incoming stock. Exact order quantity is missing because the reorder level, lead time and preferred pack quantity are not recorded. |
| **RED** | Mounting Strips (shared stock) - Accessories / Shopify | Primary counter available **-26**; 7-day usage is **85 pairs** (77 single listings plus 4 Two Sign Packs x 2). | Replenishment is urgent. Do not sum the duplicate listing counters. Exact quantity is missing because the reorder level, lead time and preferred order quantity are not recorded. |
| **RED / WATCH** | Thermal Labels - manual packaging consumable | Baseline 250 labels on 16 July; **44 paid orders** on 17 July; inferred balance **206 labels**. Seven-day order velocity is **59.4 labels/day**, or about **3.5 days**. | Confirm the physical roll and reorder settings. A reliable order quantity cannot be calculated without the minimum level, supplier lead time and preferred roll quantity. |

## East of India/accessory stock

### East of India

Only out-of-stock or confirmed run-out signals are shown here.

**None today.** No included East of India item is at zero/negative available stock or has a confirmed 7-day velocity-based run-out. Discontinued products remain excluded.

### Accessories

| Accessory | SKU / stock basis | Available stock | Sold yesterday | 7-day velocity | Alert |
|---|---|---:|---:|---:|---|
| [Wooden Display Easel](https://daisymaison.co.uk/products/wooden-display-easel) | `ACC-EASEL`, primary single listing | -53 | 3 | 51 / 7.29 per day | **RED REORDER NOW** - oversell-enabled negative counter |
| [Mounting Strips (shared stock)](https://daisymaison.co.uk/products/1-95-mounting-strips) | `ACC-MOUNT-SINGLE`; Two Sign Pack consumes 2 pairs | -26 primary counter | 7 single + 1 Two Sign Pack = 9 pairs | 77 single + 4 Two Sign Packs x 2 = 85 pairs / 12.14 per day | **RED REORDER NOW** - shared physical stock is negative; duplicate listing counters not summed |
| [Gift Wrap Kit](https://daisymaison.co.uk/products/gift-wrapping) | `ACC-GIFTWRAP`; made fresh daily | 0 by design | 6 | 40 / 5.71 per day | **BLUE MADE TO ORDER** - no reorder flag |
| Thermal Labels | Manual; one label per Shopify order | 206 inferred from 250 baseline less 44 orders | 44 | 416 / 59.43 per day | **RED / WATCH** - inferred balance only; physical count and reorder settings missing |

## Packaging usage

### 17 July paid-order review

- **44 paid Shopify orders reviewed**, using line-item detail for the Europe/London trading day.
- **Pebble pictures:** 18 pictures mapped to **16 custom boxes**, therefore **32 Guardian paper strips** and approximately **3.2m fragile tape**.
- **Medium/large-upgrade street signs:** 18 packages, consuming **6 corrugated sheets** under the 3-per-sheet rule and approximately **18m fragile tape**.
- **Default-size street signs:** 7 packages identified; exact Medium-vs-Large envelope treatment is not inferable without the sign-size context.
- Gift Wrap Kit usage was **6 kits**. Thermal-label usage was **44 labels** under the one-label-per-order rule.
- Small products and default-size mailers remain partly unclassified because the exact envelope and tape rules are not fixed for every item.

### Receipt counters

- Macfarlane delivery note `10073374` / order `6277938`: **300 custom boxes delivered**, **150 corrugated sheets delivered**, **1 Guardian roll delivered** (about 180 strips), with **1 Guardian roll still to follow**.
- These are receipt counters, not total on-hand. Prior stock and consumption remain unknown.

### Reorder list

- No exact packaging order quantity can be confirmed today. Missing inputs are current physical on-hand, minimum reorder levels, supplier lead times, preferred order/case quantities, and confirmed envelope/tape rules for default-size street signs and other small items.
- The 6-sheet corrugated usage and 32-strip Guardian usage are consumption signals only; they do not authorize an order.

## Amazon stock watch

Amazon evidence is supplier/order evidence only. Acknowledgement and delivery are not treated as current on-hand after possible consumption. Canonical product links only:

| Item | ASIN | Latest state | Quantity | Order number / delivery estimate | Owner |
|---|---|---|---:|---|---|
| 32 Pcs 9-inch Wood Easels | [B0FQTSHJ6D](https://www.amazon.co.uk/dp/B0FQTSHJ6D) | **BLOCKED / PENDING PAYMENT VERIFICATION** | 2 packs | `206-3695011-7982722`; no delivery estimate while blocked | Accessories / Shopify remains authoritative |
| JOLCEEY 120pcs swivel lobster clasps and split rings | [B0DXDPSM4F](https://www.amazon.co.uk/dp/B0DXDPSM4F) | **IN TRANSIT / DELAYED** | 1 pack | `206-0505064-1012353`; estimated by 19 July | Accessory supplier evidence; not current on-hand |
| HOMSFOU 10pcs small white plastic easel stands | [B0GLMQPND7](https://www.amazon.co.uk/dp/B0GLMQPND7) | **DELIVERED** | 1 pack | `206-3571145-3499556`; delivered 16 July | Accessory evidence; current remaining stock unknown |
| Evergreen Goods 240 matte kraft sticker labels | [B09MM95YGF](https://www.amazon.co.uk/dp/B09MM95YGF) | **DELIVERED** | 1 pack / 240 labels | `206-9914735-1984337`; delivered 14 July | Packaging/label evidence; current remaining stock unknown |

The delivered HOMSFOU pack and Evergreen labels were not added to on-hand counts. No Amazon order was placed.

## Missing inputs for Max

- Etsy quantities for **8-17 July 2026**; Shopify velocity is not yet combined-channel velocity.
- Physical on-hand, minimum reorder level, supplier lead time and preferred order quantity for easels, mounting strips, thermal labels and each packaging item.
- Confirm whether the delivered HOMSFOU pack and Evergreen label pack are physically received and how much remains.
- Resolve the blocked Wood Easel Amazon payment verification before treating that order as incoming stock.
- Confirm Medium-versus-Large envelope treatment for the 7 default-size street signs and the tape length for small-item mailers.
