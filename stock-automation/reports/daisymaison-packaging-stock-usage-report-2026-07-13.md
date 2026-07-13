# Daisy Maison Packaging Stock Usage Report - 2026-07-13

Run time: 2026-07-13 09:48 Europe/London.

Scope: paid Shopify orders created after the last counted order from the 2026-07-12 packaging report. This run counts orders from `#DM37005` through `#DM37073` that were visible in read-only Shopify queries by 2026-07-13 09:48 Europe/London.

Read-only Shopify data was pulled during this run. No Shopify data was updated, no messages were sent, and no orders were placed.

## Source Files Read

- `stock-automation/shared-tracker-context/shared-stock-context.md`
- `stock-automation/reports/daisymaison-packaging-stock-reference.md`
- `stock-automation/reports/daisymaison-packaging-stock-project.md`
- `stock-automation/shared-tracker-context/tracker-change-log.md`
- `stock-automation/reports/daisymaison-packaging-stock-usage-report-2026-07-12.md`

## Rules Applied

- Framed pebble pictures use the custom Daisy Maison pebble picture box. Up to 2 pebble pictures fit in 1 box.
- Each pebble box uses 2 Guardian paper strips and approx 0.2m fragile tape.
- Small pebble hearts use the Small envelope setting, D/1, and are not counted as framed pebble pictures.
- East of India matchboxes and up to 2 tealights use Small/D1. More than 2 tealights move out of D/1; this report uses Medium/F3 as the working estimate and flags it as low confidence.
- Street signs with Medium or Large size upgrades use corrugated sheet packaging: 1/3 of a 725 x 1135mm sheet and approx 1m fragile tape per sign package.
- Small street signs without a Medium/Large upgrade use the Large/H5 fallback when unsure, following the prior report convention.
- Gift wrap kits, gift boxes, easels, mounting strips, Lucky Sixpence, and Shipping Protection are not counted as separate packages unless the order context requires it. This remains an assumption.

## Packaging Usage Summary

| Packaging item | Estimated usage | Cost basis | Estimated cost |
| --- | ---: | --- | ---: |
| Small envelope, D/1 | 17 envelopes | GBP 0.0831 each | GBP 1.41 |
| Medium envelope, F/3 | 1 envelope | GBP 0.1090 each | GBP 0.11 |
| Large envelope, H/5 | 15 envelopes | GBP 0.1633 each | GBP 2.45 |
| Custom pebble picture box | 13 boxes | GBP 0.5974 each | GBP 7.77 |
| Guardian paper strips | 26 strips | GBP 0.2846 each | GBP 7.40 |
| 725 x 1135mm corrugated sheet | 9.33 sheets allocated from 28 sign packages | GBP 0.6500 per sheet | GBP 6.07 |
| Fragile tape for corrugated and pebble boxes | 30.6m | GBP 0.0186 per metre | GBP 0.57 |
| Fragile tape for Mail Lite envelopes | Not quantified | Exact tape length missing | Not costed |

Estimated packaging cost counted here: GBP 25.78, excluding unconfirmed Mail Lite tape usage and any separate add-on packaging.

## Orders Reviewed

The Shopify paid-order pull returned 69 new orders not counted in the 2026-07-12 packaging report.

| Order | Created at | Main Shopify line items | Packaging estimate | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `#DM37005` | 2026-07-12 07:43 UTC | 2 x Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | High | Up to 2 tealights fit D/1. |
| `#DM37006` | 2026-07-12 07:53 UTC | 2 x Teacher Star Keyring; 2 x offer keyring; 1 x Teacher Flower Hanging Heart; offer decoration | 1 Small envelope, D/1 | Low | Exact keyring / hanging decoration mailer rule is not confirmed. |
| `#DM37007` | 2026-07-12 08:27 UTC | Medium Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37008` | 2026-07-12 08:32 UTC | Teacher Bookmark plus offer bookmark | 1 Small envelope, D/1 | Low | Bookmark mailer size still needs confirmation. |
| `#DM37009` | 2026-07-12 09:00 UTC | 2 x Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | High | Up to 2 tealights fit D/1. |
| `#DM37010` | 2026-07-12 09:02 UTC | 2 x Teacher Street Sign plus offer sign | 3 Large envelopes, H/5 | Low | No size upgrades found; counted as three small signs in H/5 fallback. |
| `#DM37011` | 2026-07-12 09:13 UTC | 2 x Teacher Pebble Picture; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Up to 2 pebble pictures fit 1 box; easel assumed inside. |
| `#DM37012` | 2026-07-12 09:18 UTC | 2 x Teacher Superhero Minifigure Keyring | 1 Small envelope, D/1 | Low | Minifigure keyring mailer size is not confirmed. |
| `#DM37013` | 2026-07-12 09:31 UTC | 2 x Teacher Star Keyring plus offer keyring | 1 Small envelope, D/1 | Low | Keyring mailer size is not confirmed. |
| `#DM37014` | 2026-07-12 09:57 UTC | Wedding Pebble Picture; Gift Wrap Kit | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Gift wrap assumed inside pebble package. |
| `#DM37015` | 2026-07-12 09:59 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37016` | 2026-07-12 10:13 UTC | Teacher Star Keyring plus offer keyring | 1 Small envelope, D/1 | Low | Keyring mailer size is not confirmed. |
| `#DM37017` | 2026-07-12 10:25 UTC | Teacher Pebble People Hanging Heart; Gift Box | 1 Small envelope, D/1 | Low | Small pebble hearts use D/1, but gift box handling may change mailer size. |
| `#DM37018` | 2026-07-12 10:28 UTC | Teacher Bookmark plus offer bookmark | 1 Small envelope, D/1 | Low | Bookmark mailer size still needs confirmation. |
| `#DM37019` | 2026-07-12 10:33 UTC | Medium Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37020` | 2026-07-12 10:54 UTC | Medium Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37021` | 2026-07-12 11:35 UTC | Teacher Pebble People Hanging Heart | 1 Small envelope, D/1 | High | Small pebble heart rule applies. |
| `#DM37022` | 2026-07-12 11:55 UTC | Retirement Street Sign; Easel | 1 Large envelope, H/5 | Low | No size upgrade found; easel may change package size. |
| `#DM37023` | 2026-07-12 12:11 UTC | Teacher Superhero Minifigure Keyring | 1 Small envelope, D/1 | Low | Minifigure keyring mailer size is not confirmed. |
| `#DM37024` | 2026-07-12 12:26 UTC | Large Family Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37025` | 2026-07-12 12:41 UTC | Small Mr & Mrs Street Sign; Mounting Strips | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37026` | 2026-07-12 12:46 UTC | 3 x Teacher Porcelain Tea Light Holder | 1 Medium envelope, F/3 | Low | More than 2 tealights leave D/1; Medium vs Large still needs confirmation. |
| `#DM37027` | 2026-07-12 12:58 UTC | Large Family Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37028` | 2026-07-12 13:22 UTC | Small Mr & Mrs Street Sign; Lucky Sixpence | 1 Large envelope, H/5 | Low | Sixpence assumed inside; add-on handling not confirmed. |
| `#DM37029` | 2026-07-12 13:31 UTC | Wedding Pebble Picture; Gift Wrap Kit | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Gift wrap assumed inside pebble package. |
| `#DM37030` | 2026-07-12 13:53 UTC | Medium Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37031` | 2026-07-12 14:09 UTC | Teacher Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37032` | 2026-07-12 14:10 UTC | Large Mr & Mrs Street Sign; Gift Wrap Kit | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Gift wrap assumed inside corrugated package. |
| `#DM37033` | 2026-07-12 14:28 UTC | Engagement Pebble Picture; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Easel assumed inside pebble package. |
| `#DM37034` | 2026-07-12 14:37 UTC | 1 x Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | High | Single tealight fits D/1. |
| `#DM37035` | 2026-07-12 14:39 UTC | Large Family Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37036` | 2026-07-12 15:11 UTC | 2 x Christening Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Up to 2 pebble pictures fit 1 box. |
| `#DM37037` | 2026-07-12 15:21 UTC | Teacher Hanging Jigsaw Piece plus offer decoration | 1 Small envelope, D/1 | Low | Jigsaw / decoration mailer size still needs confirmation. |
| `#DM37038` | 2026-07-12 15:27 UTC | Wedding Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture. |
| `#DM37039` | 2026-07-12 15:56 UTC | Family Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37040` | 2026-07-12 16:16 UTC | Small Mr & Mrs Street Sign; Mounting Strips | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37041` | 2026-07-12 16:24 UTC | Mr & Mrs Street Sign; second-sign offer; 1 x Large upgrade | 1 corrugated sign package plus 1 Large envelope, H/5 | Low | Two sign lines but only one Large upgrade; counted as one upgraded sign and one small sign. |
| `#DM37042` | 2026-07-12 16:29 UTC | Small Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37043` | 2026-07-12 16:39 UTC | Large Family Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37044` | 2026-07-12 16:49 UTC | Small Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37045` | 2026-07-12 17:14 UTC | Large Family Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37046` | 2026-07-12 17:21 UTC | Medium Family Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37047` | 2026-07-12 17:35 UTC | Mum Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture. |
| `#DM37048` | 2026-07-12 17:36 UTC | Teacher Street Sign; Easel | 1 Large envelope, H/5 | Low | No size upgrade found; easel may change package size. |
| `#DM37049` | 2026-07-12 17:38 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37050` | 2026-07-12 18:06 UTC | Mr & Mrs Street Sign; second-sign offer; 2 x Large upgrade; two-sign mounting strips | 2 corrugated sign packages; 2/3 sheet; 2m fragile tape | Medium | Two Large upgrades make two corrugated packages likely. |
| `#DM37051` | 2026-07-12 18:24 UTC | Large Mr & Mrs Street Sign; Easel | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Easel assumed inside corrugated package. |
| `#DM37052` | 2026-07-12 18:24 UTC | Medium Family Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37053` | 2026-07-12 18:27 UTC | Large Dad Bar & Grill Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37054` | 2026-07-12 18:45 UTC | Christening Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture. |
| `#DM37055` | 2026-07-12 18:50 UTC | Christening Pebble Picture; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Easel assumed inside pebble package. |
| `#DM37056` | 2026-07-12 19:06 UTC | Teacher Superhero Minifigure Keyring | 1 Small envelope, D/1 | Low | Minifigure keyring mailer size is not confirmed. |
| `#DM37057` | 2026-07-12 19:28 UTC | Engagement Pebble Picture; Shipping Protection | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Shipping Protection is non-physical. |
| `#DM37058` | 2026-07-12 19:32 UTC | Home Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37059` | 2026-07-12 19:36 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37060` | 2026-07-12 19:38 UTC | Small Mr & Mrs Street Sign; Mounting Strips | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37061` | 2026-07-12 19:50 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37062` | 2026-07-12 19:57 UTC | 2 x Teacher Star Keyring plus offer keyring | 1 Small envelope, D/1 | Low | Keyring mailer size is not confirmed. |
| `#DM37063` | 2026-07-12 20:22 UTC | 2 x Christening Pebble Hanging Heart | 1 Small envelope, D/1 | Medium | Small pebble hearts use D/1; two-heart fit needs confirmation. |
| `#DM37064` | 2026-07-12 20:24 UTC | Medium Mr & Mrs Street Sign; Lucky Sixpence; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Add-ons assumed inside corrugated package. |
| `#DM37065` | 2026-07-12 20:25 UTC | Medium Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37066` | 2026-07-12 22:40 UTC | Christening Pebble Picture; Gift Wrap Kit; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Add-ons assumed inside pebble package. |
| `#DM37067` | 2026-07-13 00:12 UTC | Grandparent Pebble Sketch Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Counted as standard framed pebble picture. |
| `#DM37068` | 2026-07-13 05:31 UTC | Medium Mr & Mrs Street Sign; Easel | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Easel assumed inside corrugated package. |
| `#DM37069` | 2026-07-13 07:01 UTC | Mr & Mrs Street Sign; second-sign offer; 2 x Large upgrade; 2 x Mounting Strips; 2 x Gift Wrap Kit | 2 corrugated sign packages; 2/3 sheet; 2m fragile tape | Medium | Two Large upgrades make two corrugated packages likely; add-ons assumed inside. |
| `#DM37070` | 2026-07-13 07:15 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37071` | 2026-07-13 07:26 UTC | Medium Retirement Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37072` | 2026-07-13 07:51 UTC | Teacher Pebble People Hanging Heart; Gift Box; Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | Low | Small heart and 1 tealight fit D/1 individually; gift box may require a larger mailer. |
| `#DM37073` | 2026-07-13 08:27 UTC | Engagement Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard pebble picture. |

## Low-Confidence Classifications And Anomalies

- `#DM37006`, `#DM37008`, `#DM37012`, `#DM37013`, `#DM37016`, `#DM37018`, `#DM37023`, `#DM37037`, `#DM37056`, and `#DM37062`: exact Mail Lite size for teacher keyrings, bookmarks, minifigure keyrings, hanging jigsaws, and offer decorations is not confirmed. Counted as Small/D1 for now.
- `#DM37010`: three teacher street-sign line items have no size upgrades. Counted as 3 x Large/H5, but confirm whether multiple small signs can be combined.
- `#DM37017` and `#DM37072`: Gift Box is present with small-heart / tealight products. Current rule assumes it travels inside the main package, but it may require Medium/F3 or Large/H5.
- `#DM37022` and `#DM37048`: street signs with easels but no size upgrade are counted as Large/H5. Confirm whether easel changes these into corrugated packs.
- `#DM37026`: three tealights are counted as Medium/F3 because more than 2 tealights leave D/1. Confirm whether Medium/F3 or Large/H5 is normally used.
- `#DM37028` and `#DM37064`: Lucky Sixpence is assumed inside the main sign package. Confirm whether boxed sixpence ever creates a separate Mail Lite package.
- `#DM37041`: two sign lines but only one Large upgrade. Counted as 1 corrugated package plus 1 Large/H5 package; confirm whether the upgrade applies to both signs or only one.
- Mail Lite fragile tape usage remains unquantified in the source files, so tape cost is understated for envelope orders.

## Ordering Recommendation

No reliable ordering recommendation can be made yet. The shared files still do not include current stock-on-hand, minimum reorder levels, supplier lead times, or preferred reorder quantities for the packaging items.

Based on usage alone, the highest consumables in this run were:

- 28 corrugated street-sign packages, equal to approx 9.33 of the 725 x 1135mm corrugated sheets.
- 13 custom pebble picture boxes and 26 Guardian paper strips.
- 15 Large/H5 envelopes and 17 Small/D1 envelopes.

Add stock-on-hand and reorder thresholds for each packaging item before this automation can say what needs ordering and why.

## Next Cutoff For Future Run

Next run should start after `#DM37073`, unless Shopify later shows an order correction, cancellation, or missing order in this range.
