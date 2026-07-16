# Shared Stock Context

This is the source-of-truth context for the Daisy Maison stock tracker.

## Current Scope

The active direction is one daily stock tracker with multiple sections, not
separate automations per stock category.

Current data sources:

- Shopify Daisy Maison store.
- Supplier pricing from Macfarlane Packaging.
- Gmail Amazon.co.uk / Amazon Business purchase and delivery messages for
  Amazon-sourced operational supplies.
- Human corrections from Daisy Maison operations.

Future data sources:

- Etsy orders and stock usage, using the Etsy prompt once provided.

## Unified Stock Tracker

Control file:

- `../reports/daisymaison-stock-tracker-project.md`

The tracker should produce one daily report with sections for East of India and
accessory stock, packaging usage, and Amazon-sourced operational stock evidence.
It should also produce one combined reorder draft, deduplicated by stock owner.

### Physical Invoice / Delivery-Note Rule

- A clear physical invoice or delivery note shown in a photo is treated as
  confirmation that the goods were delivered just now.
- Automatically apply the legible delivered quantities to the relevant stock
  counter during that run; do not wait for a separate written confirmation.
- Record the document number, document/order date, delivery date if shown, and
  the exact Europe/London timestamp when the photo was processed.
- For Shopify-owned stock, read current inventory first and use a compare-and-set
  received update. For packaging or manual stock, record receipt counters and
  update total on-hand only when the prior on-hand baseline is known.
- If a line cannot be mapped confidently, record it as an unmatched receipt and
  do not guess the stock owner or SKU.

Amazon reference file:

- `../reports/daisymaison-amazon-stock-reference.md`

Amazon-sourced stock should not run as its own automation. It should draft
reorder suggestions with Amazon links only when a stock role, on-hand baseline,
and reorder threshold exist. It must not place Amazon orders, mutate Shopify,
send email, or mark messages. If an Amazon item is already authoritatively
tracked by Shopify inventory or the packaging tracker, keep that existing
tracker authoritative and use Amazon only as supplier/order evidence.

## Current Packaging Rules

See also:

- `../daisymaison-packaging-stock-reference.md`
- `../daisymaison-packaging-order-review-2026-07-09.md`

### Pebble Pictures

- Framed pebble pictures use the custom Daisy Maison pebble picture box.
- Up to 2 pebble pictures fit in 1 box.
- 3 pebble pictures require 2 boxes.
- Each pebble box uses 2 Guardian paper strips.
- Each pebble box uses approx 0.2m fragile tape.

### Small Pebble Hearts

- Small pebble hearts use the Small envelope setting, supplier code D/1.
- Do not classify pebble hearts as framed pebble pictures.

### Small Street Signs

- The envelopes use a Small / Medium / Large setting.
- Small street signs use the Medium or Large envelope setting.
- Use Medium/F3 or Large/H5 depending on the street sign size/context.
- If unsure, check street sign size/context before choosing.

### Medium/Large Street Signs

- Any street sign with a Medium or Large size upgrade does not fit in Mail Lite.
- Use 725 x 1135mm single-wall corrugated sheet.
- 1 corrugated sheet produces 3 street sign packages.
- Use approx 1m fragile tape per package.

### East of India

- Matchboxes fit in the Small envelope setting, supplier code D/1.
- Tealights: up to 2 fit in the Small envelope setting, supplier code D/1.
- More than 2 tealights move to Medium or Large envelope settings.

### Add-ons

The following still need confirmed handling:

- Gift Wrap Kit.
- Gift Box.
- Frame add-on.
- Mounting strips.

Current assumption:

- Add-ons travel inside the main package unless the order context suggests otherwise.

## Delivery Pricing And Margin Notes

Captured from Max on 2026-07-10. These are working quoted/estimated figures for
the newer Daisy delivery structure, not yet a final realized-profit model.

| Service | Carrier / route | Current cost basis | Customer charge | Simple spread before unresolved items | Status |
| --- | --- | ---: | ---: | ---: | --- |
| Standard | Existing standard service | GBP 3.09 | GBP 4.95 | GBP 1.86 | Photo-confirmed working price |
| Ship to shop 24-hour | DPD, ship to shop; Brett's price | GBP 4.25 all-in | GBP 5.95 | GBP 1.70 | Photo-confirmed working price |
| Express next-day | DPD; insurance still needs precise treatment | GBP 3.56 plus insurance | GBP 6.95 | GBP 3.39 before insurance | Photo-confirmed working price |
| Super 24-hour home | DPD home service | GBP 6.29 | GBP 9.95 | GBP 3.66 | Photo-confirmed working price |
| Super 24-hour home, alternative | DPD home service | GBP 6.29 | GBP 12.95 | GBP 6.66 | Proposed price; question mark |

### Assumptions And Open Questions

- A `0.6` adjustment was mentioned in the spoken note. Small street-sign
  cost components described as pennies are excluded from this comparison until
  the exact basis is written down.
- The prior Express cost was described as GBP 3.94 plus an additional insurance
  amount of roughly GBP 0.80, before moving toward GBP 3.56 plus insurance.
  This transition wording is retained as an assumption, not treated as a
  confirmed invoice cost.
- Confirm whether each carrier figure includes VAT, insurance, collection,
  and any account surcharge. Only then should net profit and total Daisy
  contribution be calculated.
- Add attach rate, service mix, refunds/losses, and actual carrier invoices to
  the total-profit model once the new options are live.

### Highland And Islands Conditional Royal Mail 48HR

Photo-confirmed reference from 2026-07-10. The handwritten cost lines are:

| Item | Royal Mail 48HR cost | Conditional customer charge shown | Simple spread if that charge applies |
| --- | ---: | ---: | ---: |
| Letter | GBP 2.84 | GBP 4.95 | GBP 2.11 |
| Frame | GBP 3.61 | GBP 6.95 | GBP 3.34 |
| Sign | GBP 5.57 | GBP 8.95 | GBP 3.38 |

The same note also has `GBP 8.95` beside the Letter line before the words
"Introduce conditional logic". It is retained as an ambiguous handwritten
reference until Max confirms whether it is an old/current charge or a general
note. The conditional charges above are the cleanest readable table from the
photo.

## Supplier Packaging Items

| Item code | Description | Unit | Price |
| --- | --- | ---: | ---: |
| BAMN-WH-180-260-D1 | Small envelope: Mail Lite White 180x260mm D/1 | P200 | GBP 16.629 |
| BAMN-WH-220-330-F3 | Medium envelope: Mail Lite White 220x330mm F/3 | P100 | GBP 10.900 |
| BAMN-WH-270-360-H5 | Large envelope: Mail Lite White 270x360mm H/5 | P100 | GBP 16.330 |
| CPSW-0427-380-285-100 | 380x285x100mm 0427 B125KT Plain Daisy Maison custom box | EACH | GBP 0.5974 |
| PP2-7075-180-BR-GUARDIAN-REC | Guardian paper 2-ply 70/75gsm 180m 381mm brown recycled | EACH/roll | GBP 51.2345 |
| PSW-0901-725-1135 | 725 x 1135mm single-wall corrugated sheet 125T/T-B | EACH | GBP 0.6500 |
| PSW-0901-900-1140 | 900 x 1140mm single-wall corrugated sheet | EACH | GBP 0.8319 |
| TAL-WH-A-48-66-FRAGILE-REC | White fragile PPL tape 48mm x 66m recycled | EACH/roll | GBP 1.2259 |

## Known Shopify Connector Notes

- Connected store: Daisy Maison, daisymaison.co.uk.
- Currency: GBP.
- Use full Shopify order GIDs for `get_order`.
- Use full Shopify product GIDs for `get_product` and `get_inventory_levels`.
- Pebble products are often findable by `tag:"Pebble People"`.
- Street signs are findable by text search `"street sign"` but need better tagging later.

## Packaging Receipt Evidence

Macfarlane Packaging transport note supplied by Max on 2026-07-16:

- Delivery note `10073374`, order `6277938`, order date 2026-07-14, dispatch/delivery date 2026-07-16.
- `CPSW-0427-380-285-100` custom Daisy Maison boxes: **300 each delivered** (order quantity 300).
- `PSW-0901-725-1135` 725 x 1135mm corrugated sheets: **150 delivered** (order quantity 150), equivalent to 450 street-sign package outputs under the current 3-per-sheet rule.
- `PP2-7075-180-BR-GUARDIAN-REC` Guardian paper: **1 roll delivered** (order quantity 2); **1 roll remains to follow**. The delivered roll represents approximately 180 Guardian strips.

These are receipt counters, not total on-hand counts. Existing stock and consumption before delivery remain unknown.

## Missing Stock Inputs

Needed before reliable ordering recommendations:

- Current stock-on-hand for each packaging item.
- Minimum reorder level for each item.
- Supplier lead time.
- Preferred reorder quantity or case quantity.
- Confirmed add-on packaging rules.
