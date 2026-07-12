# Daisy Maison Packaging Stock Usage Report

Run date: 2026-07-10

Scope: latest visible Shopify orders that are paid and unfulfilled, excluding orders already covered by the 2026-07-09 packaging review.

Read-only Shopify data pulled during this run. No Shopify data was updated, no messages were sent, and no orders were placed.

## Source Files Used

- `outputs/shared-tracker-context/shared-stock-context.md`
- `outputs/shared-tracker-context/tracker-change-log.md`
- `outputs/daisymaison-packaging-stock-reference.md`
- `outputs/daisymaison-packaging-stock-project.md`
- `outputs/daisymaison-packaging-order-review-2026-07-09.md`

## Human Corrections Applied

The tracker change log contains corrections from 2026-07-09. This report applies them as follows:

- Small pebble hearts use Mail Lite envelopes, not framed pebble picture boxes.
- East of India matchboxes fit the Small envelope setting, but larger mixed or multi-item bundles are flagged for confirmation.
- East of India tealights: up to 2 fit Small envelope when packed alone.
- Small street signs use Medium or Large envelope settings unless a Medium/Large size upgrade is present.
- Street sign orders with Medium/Large size upgrades use corrugated sheet packaging, not Mail Lite.
- Gift Wrap Kit, Gift Box, Frame, Mounting Strips, and similar add-ons are assumed to travel inside the main package unless context suggests otherwise.

## Orders Reviewed

The Shopify paid/unfulfilled query returned these currently visible orders:

- New since prior packaging review: `#DM36820`, `#DM36828`, `#DM36829`, `#DM36837`, `#DM36851`, `#DM36854`, `#DM36872`.
- Still unfulfilled but already reviewed on 2026-07-09: `#DM36815`, `#DM36812`, `#DM36810`.
- Older visible paid/unfulfilled order outside the current packaging run scope: `#DM36628`.

This report counts only the 7 new orders to avoid double-counting the 2026-07-09 review.

## Order-By-Order Packaging Estimate

| Order | Created at | Shopify line items | Packaging estimate | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `#DM36872` | 2026-07-10 07:00 UTC | 1 x Teacher Star Keyring; 1 x offer keyring; 2 x Teacher Porcelain Tea Light Holder | 1 Medium envelope, F/3 | Low | Two tealights alone fit Small, but this mixed bundle includes two keyrings. Confirm whether D/1 is still sufficient. |
| `#DM36854` | 2026-07-09 20:07 UTC | 1 x Teacher Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found. Small street signs use Medium/Large; Large used when unsure. |
| `#DM36851` | 2026-07-09 19:49 UTC | 1 x Mounting Strips; 2 x Size Upgrade - Medium; 1 x second-sign offer; 1 x Mr & Mrs Street Sign | 2 corrugated street sign packages; 2/3 of a 725 x 1135mm sheet; 2m fragile tape | Medium | Treated as two upgraded street signs because there are two Medium size upgrades and a second-sign offer. Mounting strips assumed inside. |
| `#DM36837` | 2026-07-09 18:32 UTC | 1 x Teacher Rainbow Pebble People Hanging Heart; 1 x Gift Box | 1 Medium envelope, F/3 | Medium | Small pebble heart is not a pebble picture. Gift box assumed to push this from Small to Medium, matching prior review assumption. |
| `#DM36829` | 2026-07-09 16:48 UTC | 1 x Teacher Porcelain Matchbox Star; 1 x 2-matchbox add-on | 1 Medium envelope, F/3 | Low | Three matchboxes may fit Small, but the exact threshold is unconfirmed. Counted as Medium until corrected. |
| `#DM36828` | 2026-07-09 16:29 UTC | 1 x Teacher Pebble People Hanging Heart; 1 x Gift Box | 1 Medium envelope, F/3 | Medium | Small pebble heart is not a pebble picture. Gift box assumed inside one Medium envelope. |
| `#DM36820` | 2026-07-09 15:04 UTC | 1 x Wooden Display Easel; 1 x Engagement Pebble Picture | 1 pebble picture box; 2 Guardian paper strips; 0.2m fragile tape | Medium | Easel assumed to travel inside the pebble picture box. Confirm if it changes void fill or box choice. |

## Estimated Packaging Used

| Packaging item | Estimated quantity used | Cost basis | Estimated cost |
| --- | ---: | --- | ---: |
| Small envelope, D/1 | 0 | GBP 0.0831 each | GBP 0.0000 |
| Medium envelope, F/3 | 4 | GBP 0.1090 each | GBP 0.4360 |
| Large envelope, H/5 | 1 | GBP 0.1633 each | GBP 0.1633 |
| Custom pebble picture box | 1 | GBP 0.5974 each | GBP 0.5974 |
| Guardian paper strips | 2 | GBP 0.2846 per strip | GBP 0.5693 |
| Guardian paper rolls | 0.0111 | 180 strips per roll | Included above |
| 725 x 1135mm corrugated sheets | 0.6667 | 1 sheet per 3 upgraded street signs | GBP 0.4333 |
| Fragile tape for pebble boxes | 0.2m | GBP 0.0186 per metre | GBP 0.0037 |
| Fragile tape for upgraded street signs | 2.0m | GBP 0.0186 per metre | GBP 0.0371 |
| Fragile tape total from known rules | 2.2m | GBP 0.0186 per metre | GBP 0.0409 |

Estimated total packaging cost from known rules: GBP 2.2402.

This excludes tape used on Mail Lite envelopes because the exact tape length per Mail Lite package is still open.

## Anomalies And Low-Confidence Classifications

1. `#DM36872`: mixed bundle of 2 tealights plus 2 keyrings. The report counts 1 Medium envelope, but this needs confirmation against actual packing practice.
2. `#DM36851`: counted as 2 upgraded street signs because two Medium size upgrades appear alongside one normal street sign and one second-sign offer. Confirm whether this always means two corrugated packages.
3. `#DM36829`: three matchboxes counted as 1 Medium envelope. Confirm whether three East of India matchboxes still fit D/1.
4. `#DM36854`: small street sign without size upgrade counted as Large/H5 because the exact Medium vs Large street sign mapping is not yet fixed.
5. `#DM36820`: wooden display easel add-on assumed to fit inside the pebble picture box. Confirm whether it changes box, paper, or tape usage.
6. Gift boxes continue to be treated as add-ons inside one Medium envelope for small pebble hearts, based on the prior review, but this still needs a confirmed rule.

## Ordering Recommendation

No reliable reorder recommendation can be made from the shared files yet.

Missing stock inputs:

- Current stock-on-hand for each packaging item.
- Minimum reorder level for each packaging item.
- Supplier lead time.
- Preferred reorder quantity or case quantity.
- Confirmed Mail Lite rules for multi-item small-gift bundles.

Once stock-on-hand and thresholds are added to the shared files, this report can compare the usage above against remaining stock and flag items to order.

## Suggested Corrections To Add To Shared Context

Ask operations to confirm:

- Whether `#DM36872` should be D/1 or F/3.
- Whether three East of India matchboxes should be D/1 or F/3.
- Whether one small street sign without a size upgrade should default to F/3 or H/5.
- Whether a second-sign offer with two size upgrades should always count as two corrugated street sign packages.
- Whether wooden display easels change pebble picture packaging.
