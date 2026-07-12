# Daisy Maison Packaging Stock Project

Created: 2026-07-09

## Role

Codex role: packaging stock analyst and automation maintainer.

Responsibilities:

- Pull recent Shopify orders.
- Classify each order into a packaging recipe.
- Estimate packaging stock consumed.
- Highlight anomalies and low-confidence classifications for human correction.
- Maintain shared working files in this folder.
- Use corrections to refine future packaging rules.
- Prepare a daily 7:30am automation to calculate packaging used and flag what needs ordering.

Human role:

- Correct packaging assumptions where the automated estimate is wrong.
- Confirm exact mailer sizes and exception rules.
- Provide stock-on-hand counts, reorder thresholds, supplier pack sizes, and lead times.
- Approve any changes that would update live Shopify data or send messages.

## Shared Files

| File | Role |
| --- | --- |
| `daisymaison-packaging-stock-reference.md` | Master reference for packaging items, costs, usage rules, Shopify connector notes, and open variables. |
| `daisymaison-packaging-order-review-2026-07-09.md` | First 20-order Shopify packing review. Use this for corrections and anomaly discovery. |
| `daisymaison-packaging-stock-project.md` | Project control file: roles, file map, automation design, and next setup steps. |
| `shared-tracker-context/` | Coordination folder for Claude, Codex, and future Etsy tracker context. |

## Shared Tracker Context

The folder `shared-tracker-context/` is the bridge between the existing Claude automation and the Codex rebuild.

Files in that folder:

- `README.md`: folder purpose and file map.
- `shared-stock-context.md`: shared operational rules for both trackers.
- `claude-current-prompt.md`: exact Claude automation prompt goes here.
- `etsy-current-prompt.md`: Etsy prompt goes here for later adaptation.
- `codex-rebuild-prompt.md`: Codex version of the stock tracker prompt.
- `tracker-change-log.md`: correction log so the two trackers do not drift.

## Daily Automation Design

Automation ID:

- `daisy-maison-packaging-stock-usage-daily-report`

Related stock automation:

- `daisy-maison-east-of-india-stock-report`: Codex takeover of the previous Claude East of India stock report, scheduled daily at 7:00am Europe/London.

Schedule:

- Daily at 7:30am Europe/London time.

Automation purpose:

1. Pull recent Shopify orders that are paid and need packaging analysis.
2. Use the shared rules in `shared-tracker-context/shared-stock-context.md` and the packaging rules in `daisymaison-packaging-stock-reference.md`.
3. Estimate packaging used by order and by packaging item.
4. Highlight low-confidence or unknown product types.
5. Compare estimated usage against stock-on-hand and reorder thresholds once those are provided.
6. Produce a dated report in this shared folder.

Initial automation output should include:

- Orders reviewed.
- Packaging used by item.
- Product/order anomalies needing human correction.
- Suggested items to order, once stock-on-hand and reorder thresholds are known.

## Data Needed Before Ordering Recommendations Are Reliable

| Needed data | Why it matters |
| --- | --- |
| Current stock-on-hand for each packaging item | Required to know what remains after daily usage. |
| Minimum reorder threshold for each item | Required to decide when to order. |
| Supplier lead time for each item | Required to decide how early to reorder. |
| Preferred reorder quantity or case quantity | Required to suggest a practical order quantity. |
| Confirmed mailer size by product family | Required to reduce low-confidence Mail Lite guesses. |
| Rules for gift wrap, gift boxes, frames, mounting strips | Required to handle add-ons correctly. |

## Current Known Automation Caveats

- Shopify order detail must be pulled by full order GID from `list_orders`.
- Product/order names alone are not always enough for exact packaging, because add-ons such as size upgrades appear as separate line items.
- Street signs need reliable classification. Products are searchable by `"street sign"`, but a dedicated tag or product type would make automation stronger.
- Pebble pictures are easier to identify because many use the `Pebble People` tag and/or `Pebble Picture` title wording.
- The automation must not update live Shopify data unless separately approved.

## Next Rule Refinements

1. Confirm small street sign mailer size.
2. Confirm D/1, F/3, and H/5 mappings for Hearts, East of India, jigsaws, keyrings, tea lights, hanging hearts, and gift boxes.
3. Decide whether add-ons should ever count as separate packages.
4. Add stock-on-hand and reorder thresholds.
5. Start saving daily stock usage reports with one date per file.
