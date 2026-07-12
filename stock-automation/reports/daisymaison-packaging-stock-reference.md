# Daisy Maison Packaging Stock Reference

Created: 2026-07-09

This is the starting stock-management reference for Daisy Maison packaging products. It separates bought-in packaging items from the order types they are used for, so more products and rules can be added later.

## Packaging Items

| Item code | Description | Bought unit | Unit price | Practical use |
| --- | --- | ---: | ---: | --- |
| BAMN-WH-180-260-D1 | Small envelope: Mail Lite White 180x260mm D/1 | Pack of 200 | GBP 16.629 | Small-envelope setting. Smaller items, including Hearts and East of India products. |
| BAMN-WH-220-330-F3 | Medium envelope: Mail Lite White 220x330mm F/3 | Pack of 100 | GBP 10.900 | Medium-envelope setting. Larger small items and some small street signs. |
| BAMN-WH-270-360-H5 | Large envelope: Mail Lite White 270x360mm H/5 | Pack of 100 | GBP 16.330 | Large-envelope setting. Largest Mail Lite option and some small street signs. |
| CPSW-0427-380-285-100 | 380x285x100mm 0427 B125KT Plain Daisy Maison custom box | Each | GBP 0.5974 | Custom pebble picture box. Fits up to 2 pebble pictures. |
| PP2-7075-180-BR-GUARDIAN-REC | Guardian paper 2-ply 70/75gsm 180m 381mm brown recycled | Roll | GBP 51.2345 | Cut into strips for pebble picture packaging. About 180 strips per roll. |
| PSW-0901-725-1135 | 725 x 1135mm single-wall corrugated sheet 125T/T-B | Each | GBP 0.6500 | Used for street signs. Cut in-house, 3 street signs per sheet. |
| PSW-0901-900-1140 | 900 x 1140mm single-wall corrugated sheet | Each | GBP 0.8319 | Planned to discontinue; ignore for future costing unless still using remaining stock. |
| TAL-WH-A-48-66-FRAGILE-REC | White fragile PPL tape 48mm x 66m recycled | Roll | GBP 1.2259 | Used on all packages. Usage varies by package type. |

## Derived Unit Costs

| Packaging item | Calculation | Approx cost |
| --- | --- | ---: |
| Small envelope, D/1 | GBP 16.629 / 200 | GBP 0.0831 each |
| Medium envelope, F/3 | GBP 10.900 / 100 | GBP 0.1090 each |
| Large envelope, H/5 | GBP 16.330 / 100 | GBP 0.1633 each |
| Pebble picture box | Direct each price | GBP 0.5974 each |
| Guardian paper strip | GBP 51.2345 / 180 strips | GBP 0.2846 per strip |
| Guardian paper per pebble box | 2 strips per box | GBP 0.5693 per box |
| 725 x 1135 corrugated sheet per street sign | GBP 0.6500 / 3 signs | GBP 0.2167 per street sign |
| Fragile tape per metre | GBP 1.2259 / 66m | GBP 0.0186 per metre |
| Fragile tape for medium/large street sign | Approx 1m | GBP 0.0186 per package |
| Fragile tape for pebble box | Approx 0.2m | GBP 0.0037 per box |

## Packaging Recipes

### Smaller Items

Used for Hearts, East of India, and similar small products.

Current packaging:

- Small, Medium, or Large envelope setting depending on item size.
- Fragile tape is used, but the exact tape length per mailer is not fixed yet.

Confirmed small-item rules:

- Small pebble hearts fit in the Small envelope.
- East of India matchboxes fit in the Small envelope.
- East of India tealights: up to 2 tealights fit in the Small envelope.
- East of India tealights: more than 2 tealights need Medium or Large envelope settings.

Envelope settings and cost before tape:

- Small envelope, D/1: GBP 0.0831 per package
- Medium envelope, F/3: GBP 0.1090 per package
- Large envelope, H/5: GBP 0.1633 per package

### Small Street Signs

Small street signs can use the Medium or Large envelope settings.

Important rule:

- Street sign orders with a medium or large upgrade attached do not fit in the envelope settings.
- Small street signs use the Medium or Large envelope settings. If uncertain, check the actual street sign size/context before choosing Medium vs Large.

Envelope options:

- Medium envelope, F/3: GBP 0.1090 each
- Large envelope, H/5: GBP 0.1633 each

Tape usage still needs a fixed assumption.

### Medium/Large Street Signs

Used packaging:

- 725 x 1135mm single-wall corrugated sheet, cut in-house.
- One sheet produces 3 street sign packs.
- Fragile tape, approx 1 metre per package.

Estimated packaging cost:

| Component | Cost |
| --- | ---: |
| Corrugated sheet allocation | GBP 0.2167 |
| Fragile tape, approx 1m | GBP 0.0186 |
| Estimated total | GBP 0.2353 |

Note: the 900 x 1140mm corrugated sheet is planned for discontinuation because the 725 x 1135mm sheet is cheaper.

### Pebble Pictures

Used packaging:

- Custom Daisy Maison box.
- Guardian paper strips.
- Fragile tape.

Packing rules:

- 1 pebble picture: 1 box.
- 2 pebble pictures: 1 box.
- 3 pebble pictures: 2 boxes.

Per-box consumables:

- 1 custom box.
- 2 Guardian paper strips.
- Approx 0.2m fragile tape.

Estimated cost per pebble box:

| Component | Cost |
| --- | ---: |
| Custom box | GBP 0.5974 |
| Guardian paper, 2 strips | GBP 0.5693 |
| Fragile tape, approx 0.2m | GBP 0.0037 |
| Estimated total per box | GBP 1.1704 |

Estimated order packaging cost:

| Pebble pictures in order | Boxes needed | Estimated packaging cost |
| ---: | ---: | ---: |
| 1 | 1 | GBP 1.1704 |
| 2 | 1 | GBP 1.1704 |
| 3 | 2 | GBP 2.3408 |

## Current Stock Rules To Track

1. Track stock in the units purchased: packs, rolls, sheets, boxes, and tape rolls.
2. Convert stock into usable output units:
   - Mail Lite packs into envelopes.
   - Guardian paper rolls into approx 180 strips.
   - Corrugated sheets into 3 street sign packs.
   - Fragile tape rolls into 66 metres.
3. Use packaging recipes to forecast depletion from orders.
4. Treat the 900 x 1140mm corrugated sheet as discontinued unless remaining stock needs using.
5. Add more packaging recipes as new product/order types are clarified.

## Shopify Connection Notes

Read-only Shopify checks were run on 2026-07-09.

Connected store:

- Store name: Daisy Maison
- Domain: daisymaison.co.uk
- Currency: GBP
- Timezone: BST
- Country: United Kingdom

Working Shopify parameters:

- `get_shop_info` works with no parameters and confirms the connected Daisy Maison store.
- `list_orders` works with `first`, for example `first: 5`.
- `search_products` works with `first`, `sort_key`, `reverse`, and `search_query`.
- `get_product` needs a full product GID, for example `gid://shopify/Product/9436245819731`.
- `get_inventory_levels` needs a full product GID in `productId`.
- `get_order` should use the full order GID from `list_orders`. A prefixed Daisy Maison order name such as `#DM36819` did not work, even though bare numeric order names may work in other stores.

Useful product searches:

- Pebble pictures: `tag:"Pebble People"`
- Street signs: `"street sign"`

Useful live data for stock forecasting:

- Product search returns title, handle, status, tags, SKU, price, variant ID, inventory quantity, and product GID.
- Order detail returns line item title, quantity, SKU, image, fulfillment status, and shipping address.
- Inventory level lookup returns inventory item ID, location ID, available, committed, and on-hand quantity.

Known Shopify classification issue:

- Pebble pictures are tagged consistently enough to search by `tag:"Pebble People"`.
- Street sign products are findable by title/search text, but many examples do not appear to have a dedicated product type or tag. For reliable packaging automation, street signs should eventually be tagged or grouped consistently.

## Open Variables

These need confirming later:

- Which envelope setting maps to which specific small products.
- Exact Medium vs Large envelope setting used for each small street sign size/context.
- Tape length for Mail Lite packages.
- Whether pebble picture orders of 4+ follow the same "2 pictures per box" rule.
- Current stock-on-hand for each packaging item.
- Reorder thresholds and lead times.
