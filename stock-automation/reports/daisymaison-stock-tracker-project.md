# Daisy Maison Stock Tracker Project

Created: 2026-07-15

## Role

Codex role: unified stock analyst and automation maintainer.

The stock tracker should run as one daily flow, not as separate automations. It
combines:

- East of India and accessory Shopify stock reporting.
- Packaging stock usage and reorder signals.
- Amazon-sourced operational stock evidence from Gmail.
- Etsy/manual sales coverage when Max supplies the missing data.

The tracker must stay read-only against Gmail, Shopify, Amazon, and Etsy unless
Max explicitly asks for a specific mutation.

## Automation Design

Automation ID:

- Active in Codex as legacy ID `daisy-maison-east-of-india-stock-report`, named
  "Daisy Maison stock tracker daily report".

Canonical future ID, if recreated later:

- `daisy-maison-stock-tracker-daily-report`

Schedule:

- Daily at 07:30 Europe/London, or the nearest available morning stock slot.

Purpose:

1. Read the shared tracker context and persistent East of India state.
2. Pull Shopify inventory, yesterday sales, and 7-day velocity for East of
   India products and the existing extra accessory SKUs.
3. Pull recent paid Shopify orders for packaging usage classification.
4. Search Gmail read-only for recent Amazon order lifecycle messages that match
   known operational stock ASINs.
5. Reconcile all stock signals into one report with clear sections and one
   combined reorder draft.
6. Write one dated stock report into `stock-automation/reports`.

## Report Flow

The daily report should use this order:

1. **Critical reorder actions**: one combined list of items that need ordering,
   with source, reason, quantity basis, and supplier/Amazon links where known.
2. **East of India and accessory stock**: stock, sold yesterday, velocity, days
   left, predicted stock-out date, and alert.
3. **Packaging usage**: orders reviewed, estimated packaging consumed, unknown
   classifications, and packaging reorder risks where stock baselines exist.
4. **Amazon stock watch**: only known candidate items, latest Gmail order state,
   whether the item is available stock, incoming stock, blocked, or unknown.
5. **Missing inputs**: the shortest possible list of counts, thresholds, usage
   rules, or corrections needed from Max.

## Source Files

| File | Role |
| --- | --- |
| `shared-tracker-context/shared-stock-context.md` | Main operational rules and non-overlap policy. |
| `shared-tracker-context/east-of-india-stock-state.md` | Persistent state for Etsy coverage, extra tracked accessories, exclusions, and thermal labels. |
| `shared-tracker-context/codex-east-of-india-stock-report-prompt.md` | Existing East of India logic to fold into the unified run. |
| `reports/daisymaison-packaging-stock-reference.md` | Packaging item costs, pack sizes, and usage rules. |
| `reports/daisymaison-amazon-stock-reference.md` | Amazon ASIN watch list and candidate reorder links. |
| `reports/daisymaison-stock-tracker-project.md` | This control file. |

## Non-Overlap Rules

- Shopify inventory remains authoritative for East of India products and the
  existing accessory SKUs already tracked there.
- Packaging calculations remain the authority for packaging material usage.
- Amazon Gmail evidence is supplier/order-state evidence only. It can identify
  incoming stock, pending verification, delivery, and reorder links, but it does
  not prove current on-hand stock.
- If one item appears in multiple places, keep one stock owner and mention the
  other source only as evidence.
- Do not create a separate Amazon automation unless Max explicitly asks later.
- Do not run the old packaging-only automation alongside this tracker.

## Draft Reorder Logic

For each item, the tracker should classify:

| Status | Meaning |
| --- | --- |
| `ACTION` | Confirmed stock is below threshold, or a required incoming Amazon order is blocked/cancelled. |
| `WATCH` | Usage exists, but on-hand count, threshold, or supplier lead time is missing. |
| `OK` | No shortage signal exists and recent evidence supports enough stock. |
| `UNKNOWN` | Item appears in orders/email but does not yet have a confirmed stock role. |

The combined reorder draft should include:

- item name;
- stock owner: East of India, packaging, or Amazon watch;
- current stock/on-hand if known;
- daily or 7-day usage signal if known;
- threshold and days left if known;
- proposed order quantity if known;
- supplier link or Amazon `https://www.amazon.co.uk/dp/<ASIN>` link;
- reason the item is on the list.

## Current Amazon Candidate Items

Seeded from Gmail on 2026-07-15. These are candidates until Max confirms stock
role, on-hand count, and reorder threshold.

| Item | ASIN | Link | Current role |
| --- | --- | --- | --- |
| 32 Pcs 9 inch Wood Easels | `B0FQTSHJ6D` | https://www.amazon.co.uk/dp/B0FQTSHJ6D | Candidate easel/display stock. |
| JOLCEEY 120pcs Swivel Lobster Clasps and Split Rings | `B0DXDPSM4F` | https://www.amazon.co.uk/dp/B0DXDPSM4F | Candidate keyring hardware. |
| HOMSFOU 10pcs Small White Plastic Art Easel Display Stand | `B0GLMQPND7` | https://www.amazon.co.uk/dp/B0GLMQPND7 | Candidate easel/display stock or substitute. |
| Evergreen Goods 240 Matte Kraft Sticker Paper Labels | `B09MM95YGF` | https://www.amazon.co.uk/dp/B09MM95YGF | Candidate label/packaging stock. |

## Data Needed Before Reorder Recommendations Are Reliable

| Needed data | Applies to | Why it matters |
| --- | --- | --- |
| Current stock-on-hand | Packaging and Amazon watch items | Required to know what remains after daily usage. |
| Minimum reorder threshold | Packaging and Amazon watch items | Required to decide when to order. |
| Supplier lead time | Packaging and Amazon watch items | Required to decide how early to order. |
| Preferred reorder quantity or case quantity | Packaging and Amazon watch items | Required to suggest a practical order quantity. |
| Confirmed usage rule | Packaging and Amazon watch items | Required to translate sales/orders into stock consumed. |
| Accepted substitutes | Amazon watch items | Required before suggesting alternative Amazon links. |
| Etsy catch-up quantities | East of India/accessory products | Required for true combined stock velocity. |

## Safety

### Physical document receipts

When Max supplies a clear photo of a physical invoice or delivery note, treat
the goods as delivered just now and automatically update the referenced stock
counters. Record the document reference and the exact Europe/London processing
timestamp in the state and report. Use safe compare-and-set updates for Shopify;
for manual packaging stock, record delivered quantities separately when total
on-hand is not yet known. Do not wait for a second confirmation message.

- Never send, archive, label, mark, or delete email.
- Never place Amazon orders automatically.
- Never update Shopify stock unless Max explicitly asks for a specific update.
- Never treat Amazon order acknowledgement as delivered stock.
- Never treat Amazon delivered state as current on-hand if the item may already
  have been used.
- Never store personal addresses, payment details, or long Amazon redirect URLs.

## User-Facing Report Layout Override (2026-07-16)

The report must be formatted as: **East of India**, **Amazon stock watch**,
**Accessories**, then **Packaging usage and order list**. Remove the standalone
Critical reorder actions section. East of India should show only out-of-stock
or confirmed run-out products with correct SKUs and direct links; say `None
today` when there are no run-outs. Keep every relevant Amazon upsell or
operational product on watch until Gmail confirms delivery, then transfer it to
the relevant accessory or packaging owner. Packaging must state exact confirmed
orders needed or the precise missing input preventing a quantity calculation.
