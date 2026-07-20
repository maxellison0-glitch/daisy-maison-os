# Daisy Maison Amazon Stock Reference

Created: 2026-07-15

This is the working reference for Amazon-sourced stock and supplies inside the
unified Daisy Maison stock tracker. It tracks items by stable ASIN where
possible so Gmail evidence can be matched over time.

## Candidate Items

| ASIN | Item | Category | Pack / unit basis | Reorder URL | Current state |
| --- | --- | --- | --- | --- | --- |
| `B0FQTSHJ6D` | 32 Pcs 9 inch Wood Easels | Easel / display stock | 32 easels per pack; latest delivered order quantity 1 pack; separate blocked order quantity 2 packs | https://www.amazon.co.uk/dp/B0FQTSHJ6D | Candidate; order `206-3457020-8782768` delivered 2026-07-20 as supplier receipt evidence; separate order `206-3695011-7982722` remains payment-blocked |
| `B0DXDPSM4F` | JOLCEEY 120pcs Swivel Lobster Clasps and Split Rings | Keyring hardware | 60 clips + 60 split rings per pack | https://www.amazon.co.uk/dp/B0DXDPSM4F | Candidate; order `206-0505064-1012353` delivered 2026-07-20 as supplier receipt evidence |
| `B0GLMQPND7` | HOMSFOU 10pcs Small White Plastic Art Easel Display Stand | Easel / display stock | 10 stands per pack | https://www.amazon.co.uk/dp/B0GLMQPND7 | Candidate; order `206-0080348-4608363` delivered 2026-07-16 as supplier receipt evidence |
| `B09MM95YGF` | Evergreen Goods 240 Matte Kraft Sticker Paper Labels | Labels / packaging | 30 sheets, 8 labels per sheet, 240 labels total | https://www.amazon.co.uk/dp/B09MM95YGF | Candidate; Gmail shows delivered 2026-07-14 |

## State Fields To Add

Use these fields when Max confirms the stock role:

| Field | Meaning |
| --- | --- |
| `on_hand` | Physical stock count from Max or staff |
| `baseline_date` | Date the stock count was confirmed |
| `usage_rule` | How Shopify/order activity consumes the item |
| `reorder_threshold` | Minimum remaining units before ordering |
| `preferred_order_quantity` | Practical order quantity / pack count |
| `lead_time` | Expected delivery window |
| `substitutes_ok` | Whether equivalent Amazon products are acceptable |
| `last_amazon_order` | Last known Amazon order number and state |

## Gmail Extraction Notes

Amazon order emails expose enough structure to parse:

- order number;
- item title;
- ASIN in the product link;
- quantity;
- item/order total;
- seller;
- delivery state text;
- delivery estimate;
- whether the order is on behalf of Daisy Maison.

Store canonical product links only as `https://www.amazon.co.uk/dp/<ASIN>`.
Do not store long Gmail/Amazon redirect links because they contain tracking
tokens and are not durable.

## Non-Overlap Rules

- Amazon stock watch is a section of the unified Daisy Maison stock tracker, not
  a standalone automation.
- If the item is a Shopify inventory item already handled by the East of India
  stock report, keep the Shopify stock report authoritative and only use Amazon
  evidence as a reorder/source note.
- If the item is packaging material consumed per order, keep usage calculation
  in the packaging stock tracker and use this file only for the Amazon supplier
  link/order state.
- If the item is a production tool, sample, or one-off office purchase, mark it
  `UNKNOWN` or `ONE-OFF` and do not include it in reorder alerts.
