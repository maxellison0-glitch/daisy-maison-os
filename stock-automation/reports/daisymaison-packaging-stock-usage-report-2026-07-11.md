# Daisy Maison Packaging Stock Usage Report

Run date: 2026-07-11

Run time: 2026-07-11 08:32 Europe/London

Scope: paid and unfulfilled Shopify orders created after the last counted order from the 2026-07-10 packaging report. This run counts orders from `#DM36874` through `#DM36932` that were visible in the read-only Shopify query.

Read-only Shopify data was pulled during this run. No Shopify data was updated, no messages were sent, and no orders were placed.

## Source Files Used

- `outputs/shared-tracker-context/shared-stock-context.md`
- `outputs/shared-tracker-context/tracker-change-log.md`
- `outputs/daisymaison-packaging-stock-reference.md`
- `outputs/daisymaison-packaging-stock-project.md`
- `outputs/daisymaison-packaging-order-review-2026-07-09.md`
- `outputs/daisymaison-packaging-stock-usage-report-2026-07-10.md`

## Human Corrections Applied

No new packaging recipe corrections were found after the 2026-07-10 delivery-pricing notes. This report applies the active packaging corrections already in the shared context:

- Small pebble hearts use Mail Lite envelopes, not framed pebble picture boxes.
- East of India matchboxes fit the Small envelope setting, but larger mixed or multi-item bundles are flagged for confirmation.
- East of India tealights: up to 2 fit Small envelope when packed alone; more than 2 moves to Medium or Large.
- Small street signs use Medium or Large envelope settings unless a Medium/Large size upgrade is present.
- Street sign orders with Medium/Large size upgrades use corrugated sheet packaging, not Mail Lite.
- Gift Wrap Kit, Gift Box, Frame, Mounting Strips, Wooden Display Easel, cards, and similar add-ons are assumed to travel inside the main package unless context suggests otherwise.

## Orders Reviewed

The Shopify paid/unfulfilled query returned 52 new orders not counted in the 2026-07-10 packaging report:

- `#DM36874`, `#DM36876`, `#DM36879`
- `#DM36883` through `#DM36897`, excluding order numbers not present in the current paid/unfulfilled result
- `#DM36899` through `#DM36932`, excluding order numbers not present in the current paid/unfulfilled result

Orders already counted in the 2026-07-10 report, ending at `#DM36872`, were excluded to avoid double-counting.

## Order-By-Order Packaging Estimate

| Order | Created at | Shopify line items | Packaging estimate | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `#DM36874` | 2026-07-10 07:49 UTC | 1 x Size Upgrade - Medium; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM36876` | 2026-07-10 09:02 UTC | 1 x Size Upgrade - Large; 1 x Valentine's Day Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM36879` | 2026-07-10 09:08 UTC | 1 x 7/8 Pebbles add-on; 1 x Family Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Extra pebble characters assumed to fit in the same pebble box. |
| `#DM36883` | 2026-07-10 09:41 UTC | 1 x Size Upgrade - Medium; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM36884` | 2026-07-10 09:46 UTC | 1 x Size Upgrade - Large; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM36885` | 2026-07-10 10:01 UTC | 1 x Teacher Tea Light Holder; 1 x Teacher Rainbow Pebble People Hanging Heart; 1 x Gift Box | 1 Medium envelope, F/3 | Medium | Mixed small items plus gift box counted as Medium. |
| `#DM36886` | 2026-07-10 10:06 UTC | 1 x Teacher Pebble People Hanging Heart; 2 x Large Decoration add-ons / offer decoration | 1 Medium envelope, F/3 | Low | Hanging heart is not a pebble picture; multiple decoration add-ons need a confirmed mailer rule. |
| `#DM36887` | 2026-07-10 10:14 UTC | 1 x Size Upgrade - Medium; 1 x Retirement Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM36888` | 2026-07-10 10:28 UTC | 2 x Teacher Star Keyring; 2 x offer keyring | 1 Medium envelope, F/3 | Low | Four keyrings may fit D/1; counted as F/3 until confirmed. |
| `#DM36889` | 2026-07-10 10:40 UTC | 1 x Size Upgrade - Medium; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM36890` | 2026-07-10 10:46 UTC | 1 x Wedding Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture rule. |
| `#DM36891` | 2026-07-10 11:18 UTC | 1 x Mounting Strips; 1 x Wooden Display Easel; 1 x Teacher Street Sign | 1 Large envelope, H/5 | Low | No size upgrade found. Small street sign with add-ons counted as Large. |
| `#DM36892` | 2026-07-10 11:28 UTC | 1 x Gift Wrap Kit; 1 x Mounting Strips; 1 x Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; gift wrap and mounting strips assumed inside. |
| `#DM36893` | 2026-07-10 11:53 UTC | 1 x Engagement Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture rule. |
| `#DM36894` | 2026-07-10 11:57 UTC | 1 x Magic Books Teacher Bookmark; 1 x offer bookmark | 1 Small envelope, D/1 | Low | Bookmark mailer size still needs confirmation. |
| `#DM36895` | 2026-07-10 12:42 UTC | 1 x Size Upgrade - Large; 1 x London Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM36896` | 2026-07-10 13:10 UTC | 1 x Teacher Star Keyring; 1 x offer keyring | 1 Medium envelope, F/3 | Low | Kept consistent with prior two-keyring assumption, but D/1 may be sufficient. |
| `#DM36897` | 2026-07-10 13:15 UTC | 1 x Engagement Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture rule. |
| `#DM36899` | 2026-07-10 14:46 UTC | 2 x Teacher Tea Light Holder | 1 Small envelope, D/1 | High | Up to 2 East of India tealights fit Small. |
| `#DM36900` | 2026-07-10 15:09 UTC | 1 x Mounting Strips; 1 x Size Upgrade - Medium; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Mounting strips assumed inside. |
| `#DM36901` | 2026-07-10 15:52 UTC | 1 x Mounting Strips; 1 x Size Upgrade - Large; 1 x Family Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Mounting strips assumed inside. |
| `#DM36902` | 2026-07-10 16:13 UTC | 1 x Mounting Strips; 1 x Size Upgrade - Medium; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Mounting strips assumed inside. |
| `#DM36903` | 2026-07-10 16:29 UTC | 1 x Teacher Hanging Jigsaw Piece | 1 Small envelope, D/1 | Low | Prior review assumed D/1; product-family rule still unconfirmed. |
| `#DM36904` | 2026-07-10 16:37 UTC | 1 x Wedding Card; 1 x Mounting Strips; 1 x Size Upgrade - Medium; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | Medium | Card and mounting strips assumed inside corrugated pack. |
| `#DM36905` | 2026-07-10 16:53 UTC | 1 x Teacher Hanging Heart Poem; 1 x offer poem | 1 Medium envelope, F/3 | Low | Hanging-heart/poem bundle mailer size needs confirmation. |
| `#DM36906` | 2026-07-10 18:02 UTC | 1 x Teacher Pebble People Hanging Heart; 1 x Teacher Tea Light Holder | 1 Medium envelope, F/3 | Medium | Mixed small items counted as Medium. |
| `#DM36907` | 2026-07-10 18:04 UTC | 1 x Size Upgrade - Medium; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM36908` | 2026-07-10 18:19 UTC | 1 x Teacher Bookmark | 1 Small envelope, D/1 | Low | Bookmark mailer size still needs confirmation. |
| `#DM36909` | 2026-07-10 18:22 UTC | 1 x Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found. Large used when unsure. |
| `#DM36910` | 2026-07-10 18:24 UTC | 1 x Lucky Sixpence boxed; 1 x Size Upgrade - Large; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | Medium | Boxed sixpence assumed inside corrugated pack. |
| `#DM36911` | 2026-07-10 18:30 UTC | 1 x Couple Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture rule. |
| `#DM36912` | 2026-07-10 18:47 UTC | 1 x Family Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found. Large used when unsure. |
| `#DM36913` | 2026-07-10 18:56 UTC | 1 x Teacher Star Keyring | 1 Small envelope, D/1 | Low | Single keyring counted as Small; confirm keyring rule. |
| `#DM36914` | 2026-07-10 18:56 UTC | 1 x Teacher Rainbow Pebble People Hanging Heart; 1 x Gift Box | 1 Medium envelope, F/3 | Medium | Gift box assumed to push heart from Small to Medium. |
| `#DM36915` | 2026-07-10 19:26 UTC | 1 x Mounting Strips; 1 x Size Upgrade - Large; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Mounting strips assumed inside. |
| `#DM36916` | 2026-07-10 19:52 UTC | 3 x Teacher Tea Light Holder | 1 Medium envelope, F/3 | Medium | More than 2 tealights moves out of Small; exact Medium vs Large needs confirmation. |
| `#DM36917` | 2026-07-10 19:53 UTC | 1 x Teacher Pebble Picture; 1 x Teacher Rainbow Pebble People Hanging Heart; 1 x Gift Box | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Teacher pebble picture counted as main package; heart and gift box assumed inside. Confirm whether this needs an extra Mail Lite. |
| `#DM36918` | 2026-07-10 20:14 UTC | 1 x Engagement Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture rule. |
| `#DM36919` | 2026-07-10 20:17 UTC | 1 x Gift Box; 1 x Teacher Star Keyring; 1 x offer keyring | 1 Medium envelope, F/3 | Low | Gift box plus two keyrings counted as Medium. |
| `#DM36920` | 2026-07-10 20:17 UTC | 1 x Gift Wrap Kit; 1 x Mounting Strips; 1 x Size Upgrade - Medium; 1 x Mr & Mrs Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | Medium | Gift wrap and mounting strips assumed inside corrugated pack. |
| `#DM36921` | 2026-07-10 21:03 UTC | 1 x Mounting Strips; 1 x Size Upgrade - Large; 1 x Vintage Style Train Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM36922` | 2026-07-10 21:03 UTC | 1 x Wedding Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture rule. |
| `#DM36923` | 2026-07-10 21:33 UTC | 1 x Teacher Superhero Minifigure Keyring | 1 Small envelope, D/1 | Low | Single keyring counted as Small; confirm keyring rule. |
| `#DM36924` | 2026-07-10 21:40 UTC | 1 x Family Wedding Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture rule. |
| `#DM36925` | 2026-07-10 21:46 UTC | 1 x Mounting Strips; 1 x Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found. Large used when unsure. |
| `#DM36926` | 2026-07-10 22:29 UTC | 1 x Size Upgrade - Medium; 1 x Family Street Sign | 1 corrugated street sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM36927` | 2026-07-11 04:21 UTC | 1 x Wooden Display Easel; 1 x 7/8 Pebbles add-on; 1 x Family Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Easel and extra pebbles assumed to fit in the pebble box. |
| `#DM36928` | 2026-07-11 06:18 UTC | 1 x Teacher Rainbow Pebble People Hanging Heart; 1 x Gift Box | 1 Medium envelope, F/3 | Medium | Gift box assumed to push heart from Small to Medium. |
| `#DM36929` | 2026-07-11 06:47 UTC | 1 x Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found. Large used when unsure. |
| `#DM36930` | 2026-07-11 06:49 UTC | 1 x Teacher Star Keyring; 1 x offer keyring | 1 Medium envelope, F/3 | Low | Kept consistent with prior two-keyring assumption, but D/1 may be sufficient. |
| `#DM36931` | 2026-07-11 07:09 UTC | 1 x Teacher Superhero Minifigure Keyring | 1 Small envelope, D/1 | Low | Single keyring counted as Small; confirm keyring rule. |
| `#DM36932` | 2026-07-11 07:25 UTC | 1 x Teacher Superhero Minifigure Keyring | 1 Small envelope, D/1 | Low | Single keyring counted as Small; confirm keyring rule. |

## Estimated Packaging Used

| Packaging item | Estimated quantity used | Cost basis | Estimated cost |
| --- | ---: | --- | ---: |
| Small envelope, D/1 | 8 | GBP 0.0831 each | GBP 0.6652 |
| Medium envelope, F/3 | 11 | GBP 0.1090 each | GBP 1.1990 |
| Large envelope, H/5 | 6 | GBP 0.1633 each | GBP 0.9798 |
| Custom pebble picture box | 10 | GBP 0.5974 each | GBP 5.9740 |
| Guardian paper strips | 20 | GBP 0.2846 per strip | GBP 5.6927 |
| Guardian paper rolls | 0.1111 | 180 strips per roll | Included above |
| 725 x 1135mm corrugated sheets | 5.6667 | 1 sheet per 3 upgraded street signs | GBP 3.6833 |
| Fragile tape for pebble boxes | 2.0m | GBP 0.0186 per metre | GBP 0.0371 |
| Fragile tape for upgraded street signs | 17.0m | GBP 0.0186 per metre | GBP 0.3152 |
| Fragile tape total from known rules | 19.0m | GBP 0.0186 per metre | GBP 0.3524 |

Estimated total packaging cost from known rules: GBP 18.5463.

This excludes tape used on Mail Lite envelopes because the exact tape length per Mail Lite package is still open.

## Anomalies And Low-Confidence Classifications

1. Keyrings remain uncertain. Single keyrings were counted as D/1, while two or more keyrings were counted as F/3 to match prior assumptions. Confirm whether two keyrings still fit D/1.
2. Bookmarks and hanging jigsaw pieces were counted as D/1, but the product-family mailer rule is still unconfirmed.
3. Small street signs without size upgrades were counted as H/5 when uncertain. Confirm whether specific street sign families can default to F/3 instead.
4. `#DM36891`: Teacher Street Sign plus Wooden Display Easel and Mounting Strips was counted as H/5. Confirm whether the easel changes the package size.
5. `#DM36886`: multiple large decoration / offer decoration add-ons with a pebble hanging heart were counted as one F/3. Confirm whether this should be H/5 or multiple mailers.
6. `#DM36917`: Teacher Pebble Picture plus a pebble hanging heart and gift box was counted as one pebble box. Confirm whether the heart and gift box travel inside the pebble box or need a separate Mail Lite.
7. `#DM36927`: Wooden Display Easel and extra pebble characters were assumed to fit inside the pebble picture box. Confirm whether this changes void fill, box, or tape usage.
8. `#DM36916`: three East of India tealights were counted as F/3 because more than two no longer fits the confirmed D/1 rule. Confirm F/3 vs H/5.

## Ordering Recommendation

No reliable reorder recommendation can be made from the shared files yet.

Missing stock inputs:

- Current stock-on-hand for each packaging item.
- Minimum reorder level for each packaging item.
- Supplier lead time.
- Preferred reorder quantity or case quantity.
- Confirmed Mail Lite rules for keyrings, bookmarks, jigsaws, hanging-heart bundles, cards, gift boxes, and display easels.

Once stock-on-hand and thresholds are added to the shared files, this workflow can compare daily usage against remaining stock and flag items to order.

## Suggested Corrections To Add To Shared Context

Ask operations to confirm:

- Whether two keyrings should be D/1 or F/3.
- Whether four keyrings should be F/3 or H/5.
- Whether bookmarks and hanging jigsaw pieces should default to D/1.
- Whether small street signs without upgrades should default to F/3 or H/5 by product family.
- Whether a Wooden Display Easel changes packaging for street signs or pebble pictures.
- Whether a Teacher Pebble Picture plus pebble hanging heart and gift box can travel in one pebble box.
- Whether three East of India tealights should use F/3 or H/5.
