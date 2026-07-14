# Daisy Maison Packaging Stock Usage Report - 2026-07-14

Run time: 2026-07-14 08:30 Europe/London.

Scope: paid Shopify orders created after the last counted order from the 2026-07-13 packaging report. This run counts orders from `#DM37074` through `#DM37142` that were visible in read-only Shopify queries by 2026-07-14 08:30 Europe/London.

Read-only Shopify data was pulled during this run. No Shopify data was updated, no messages were sent, and no orders were placed.

## Source Files Read

- `stock-automation/shared-tracker-context/shared-stock-context.md`
- `stock-automation/reports/daisymaison-packaging-stock-reference.md`
- `stock-automation/reports/daisymaison-packaging-stock-project.md`
- `stock-automation/shared-tracker-context/tracker-change-log.md`
- `stock-automation/reports/daisymaison-packaging-stock-usage-report-2026-07-13.md`

No new human packaging corrections were present in the shared context or tracker change log after the 2026-07-10 delivery-pricing notes.

## Rules Applied

- Framed pebble pictures use the custom Daisy Maison pebble picture box. Up to 2 pebble pictures fit in 1 box.
- Each pebble box uses 2 Guardian paper strips and approx 0.2m fragile tape.
- Small pebble hearts use the Small envelope setting, D/1, and are not counted as framed pebble pictures.
- East of India matchboxes and up to 2 tealights use Small/D1. More than 2 tealights move out of D/1; no more-than-2 tealight order appeared in this run.
- Street signs with Medium or Large size upgrades use corrugated sheet packaging: 1/3 of a 725 x 1135mm sheet and approx 1m fragile tape per sign package.
- Small street signs without a Medium/Large upgrade use the Large/H5 fallback when unsure, following the prior report convention.
- Gift wrap kits, gift boxes, easels, mounting strips, Lucky Sixpence, and Shipping Protection are not counted as separate packages unless the order context requires it. This remains an assumption.
- Keyrings, bookmarks, jigsaws, hanging decorations, and A4 prints still lack confirmed packaging rules. This report keeps the prior low-confidence Mail Lite fallback and flags those orders.

## Packaging Usage Summary

| Packaging item | Estimated usage | Cost basis | Estimated cost |
| --- | ---: | --- | ---: |
| Small envelope, D/1 | 22 envelopes | GBP 0.0831 each | GBP 1.83 |
| Medium envelope, F/3 | 0 envelopes | GBP 0.1090 each | GBP 0.00 |
| Large envelope, H/5 | 8 envelopes | GBP 0.1633 each | GBP 1.31 |
| Custom pebble picture box | 12 boxes | GBP 0.5974 each | GBP 7.17 |
| Guardian paper strips | 24 strips | GBP 0.2846 each | GBP 6.83 |
| 725 x 1135mm corrugated sheet | 10.33 sheets allocated from 31 sign packages | GBP 0.6500 per sheet | GBP 6.72 |
| Fragile tape for corrugated and pebble boxes | 33.4m | GBP 0.0186 per metre | GBP 0.62 |
| Fragile tape for Mail Lite envelopes | Not quantified | Exact tape length missing | Not costed |

Estimated packaging cost counted here: GBP 24.48, excluding unconfirmed Mail Lite tape usage and any separate add-on packaging.

## Orders Reviewed

The Shopify paid-order pull returned 69 new orders not counted in the 2026-07-13 packaging report.

| Order | Created at | Main Shopify line items | Packaging estimate | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `#DM37074` | 2026-07-13 08:45 UTC | Large Family Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37075` | 2026-07-13 08:53 UTC | Medium Home Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37076` | 2026-07-13 08:55 UTC | Teacher Porcelain Matchbox Star; Teacher Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Matchbox assumed to travel inside the pebble package; confirm mixed EOI plus framed pebble handling. |
| `#DM37077` | 2026-07-13 09:01 UTC | Teacher Porcelain Matchbox Star; Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | High | Matchbox and 1 tealight fit D/1 under current rules. |
| `#DM37078` | 2026-07-13 09:02 UTC | Mr & Mrs Street Sign; second-sign offer; 2 x Large upgrade | 2 corrugated sign packages; 2/3 sheet; 2m fragile tape | Medium | Two Large upgrades make two corrugated packages likely. |
| `#DM37079` | 2026-07-13 09:13 UTC | Retirement Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37080` | 2026-07-13 09:16 UTC | Teacher Hanging Jigsaw Piece plus offer decoration | 1 Small envelope, D/1 | Low | Jigsaw / decoration mailer size still needs confirmation. |
| `#DM37081` | 2026-07-13 09:38 UTC | Christening Pebble Hanging Heart; Large Decoration | 1 Small envelope, D/1 | Low | Small heart rule applies, but large decoration handling is not confirmed. |
| `#DM37082` | 2026-07-13 09:50 UTC | Family Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37083` | 2026-07-13 09:53 UTC | Teacher Pebble Picture; offer decoration; 2 x Teacher Pebble Hanging Heart; 3 x Gift Box | 1 pebble box plus 1 Small envelope, D/1 | Low | Mixed framed pebble, hearts, decoration, and gift boxes may need different packaging. |
| `#DM37084` | 2026-07-13 10:20 UTC | Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37085` | 2026-07-13 10:29 UTC | Family Pebblescape | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Counted as standard framed pebble artwork. |
| `#DM37086` | 2026-07-13 10:52 UTC | Wedding Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37087` | 2026-07-13 10:58 UTC | Family Pebble Picture; 7/8 Pebbles add-on | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Extra pebbles do not change the package under current rules. |
| `#DM37088` | 2026-07-13 11:02 UTC | Large Football Stadium Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37089` | 2026-07-13 11:06 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37090` | 2026-07-13 11:15 UTC | 4 x Teacher Star Keyring plus 4 x offer keyring | 1 Small envelope, D/1 | Low | Large multi-keyring mailer size is not confirmed. |
| `#DM37091` | 2026-07-13 11:22 UTC | Teacher Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37092` | 2026-07-13 11:25 UTC | Large Dad Bar & Grill Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37093` | 2026-07-13 11:32 UTC | Large Vintage Style Train Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37094` | 2026-07-13 12:21 UTC | Teacher Rainbow Pebble Hanging Heart; Gift Box | 1 Small envelope, D/1 | Low | Gift box may change mailer size. |
| `#DM37095` | 2026-07-13 12:22 UTC | Teacher Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37096` | 2026-07-13 12:43 UTC | Teacher Pebble Hanging Heart; Gift Box | 1 Small envelope, D/1 | Low | Gift box may change mailer size. |
| `#DM37097` | 2026-07-13 13:07 UTC | Mr & Mrs Street Sign; Mounting Strips | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37098` | 2026-07-13 13:19 UTC | Teacher Rainbow Pebble Hanging Heart; offer decoration | 1 Small envelope, D/1 | Low | Hanging decoration mailer size still needs confirmation. |
| `#DM37099` | 2026-07-13 15:06 UTC | Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37100` | 2026-07-13 15:21 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37101` | 2026-07-13 15:44 UTC | Wedding Swing Pebble Picture; Gift Wrap Kit | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Gift wrap assumed inside pebble package. |
| `#DM37102` | 2026-07-13 15:50 UTC | Large Family Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37103` | 2026-07-13 16:20 UTC | Couple Pebble Hanging Heart | 1 Small envelope, D/1 | High | Small pebble heart rule applies. |
| `#DM37104` | 2026-07-13 16:28 UTC | Family Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37105` | 2026-07-13 16:47 UTC | Medium Mr & Mrs Street Sign; Easel | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Easel assumed inside corrugated package. |
| `#DM37106` | 2026-07-13 16:52 UTC | Teacher Bookmark plus offer bookmark | 1 Small envelope, D/1 | Low | Bookmark mailer size still needs confirmation. |
| `#DM37107` | 2026-07-13 16:54 UTC | Mum Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37108` | 2026-07-13 17:08 UTC | Medium Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37109` | 2026-07-13 17:10 UTC | Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | High | Single tealight fits D/1. |
| `#DM37110` | 2026-07-13 17:16 UTC | Medium Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37111` | 2026-07-13 17:21 UTC | Mr & Mrs Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37112` | 2026-07-13 17:46 UTC | Large Dad Bar & Grill Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37113` | 2026-07-13 18:29 UTC | Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | High | Single tealight fits D/1. |
| `#DM37114` | 2026-07-13 18:53 UTC | Medium Vintage Style Train Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37115` | 2026-07-13 19:05 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37116` | 2026-07-13 19:06 UTC | Teacher Flower Hanging Heart plus offer decoration | 1 Small envelope, D/1 | Low | Hanging heart / decoration rule is not confirmed. |
| `#DM37117` | 2026-07-13 19:09 UTC | Large Dad Bar & Grill Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37118` | 2026-07-13 19:26 UTC | Porcelain Matchbox Guardian Angel; Teacher Rainbow Pebble Hanging Heart | 1 Small envelope, D/1 | Medium | Both individually fit D/1; combined fit should be confirmed. |
| `#DM37119` | 2026-07-13 19:27 UTC | Teacher Rainbow Pebble Hanging Heart | 1 Small envelope, D/1 | High | Small pebble heart rule applies. |
| `#DM37120` | 2026-07-13 19:30 UTC | Medium Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37121` | 2026-07-13 19:31 UTC | Large Mr & Mrs Street Sign; Lucky Sixpence; Gift Wrap Kit; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Add-ons assumed inside corrugated package. |
| `#DM37122` | 2026-07-13 19:40 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37123` | 2026-07-13 19:48 UTC | Mum Pebble Picture; 7/8 Pebbles add-on | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Extra pebbles do not change the package under current rules. |
| `#DM37124` | 2026-07-13 19:50 UTC | Large Mr & Mrs Street Sign; Easel | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Easel assumed inside corrugated package. |
| `#DM37125` | 2026-07-13 20:00 UTC | Teacher Superhero Minifigure Keyring | 1 Small envelope, D/1 | Low | Minifigure keyring mailer size is not confirmed. |
| `#DM37126` | 2026-07-13 20:21 UTC | Teacher Star Keyring plus offer keyring | 1 Small envelope, D/1 | Low | Keyring mailer size is not confirmed. |
| `#DM37127` | 2026-07-13 20:36 UTC | Mr & Mrs Street Sign; second-sign offer; 2 x Medium upgrade; 2 x Easel | 2 corrugated sign packages; 2/3 sheet; 2m fragile tape | Medium | Two Medium upgrades make two corrugated packages likely; easels assumed inside. |
| `#DM37128` | 2026-07-13 20:59 UTC | Large Mr & Mrs Street Sign; Gift Wrap Kit | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Gift wrap assumed inside corrugated package. |
| `#DM37129` | 2026-07-13 21:23 UTC | Family Wedding Pebble Picture; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Easel assumed inside pebble package. |
| `#DM37130` | 2026-07-13 21:29 UTC | Medium Mr & Mrs Street Sign; Easel | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Easel assumed inside corrugated package. |
| `#DM37131` | 2026-07-13 21:53 UTC | Family Pebble Picture; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Easel assumed inside pebble package. |
| `#DM37132` | 2026-07-13 22:04 UTC | Large Mr & Mrs Street Sign; Easel | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Easel assumed inside corrugated package. |
| `#DM37133` | 2026-07-13 22:58 UTC | Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | High | Single tealight fits D/1. |
| `#DM37134` | 2026-07-13 23:31 UTC | Medium Mr & Mrs Street Sign; Mounting Strips; Shipping Protection | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite; Shipping Protection is non-physical. |
| `#DM37135` | 2026-07-14 01:03 UTC | 2 x Teacher Rainbow Pebble Hanging Heart; 2 x offer decoration; 4 x Gift Box | 1 Small envelope, D/1 | Low | Multi-heart plus four gift boxes likely needs human confirmation. |
| `#DM37136` | 2026-07-14 04:33 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37137` | 2026-07-14 05:49 UTC | Teacher Hanging Jigsaw Piece | 1 Small envelope, D/1 | Low | Jigsaw mailer size still needs confirmation. |
| `#DM37138` | 2026-07-14 05:52 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37139` | 2026-07-14 05:52 UTC | Medium Mr & Mrs Street Sign; Easel | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Easel assumed inside corrugated package. |
| `#DM37140` | 2026-07-14 05:53 UTC | Couple Pebble Hanging Heart; Large Decoration; Medium Mr & Mrs Street Sign; Mounting Strips | 1 Small envelope, D/1 plus 1 corrugated sign package | Low | Mixed small-heart and upgraded-sign package; confirm whether this ships as one or two packages. |
| `#DM37141` | 2026-07-14 06:03 UTC | Wedding Pebble Hanging Heart | 1 Small envelope, D/1 | High | Small pebble heart rule applies. |
| `#DM37142` | 2026-07-14 06:28 UTC | Watercolour Flower New Baby A4 Print | 1 Large envelope, H/5 | Low | A4 print packaging rule is not in the shared files; H/5 used as a fit-based fallback. |

## Low-Confidence Classifications And Anomalies

- `#DM37080`, `#DM37090`, `#DM37106`, `#DM37116`, `#DM37125`, `#DM37126`, and `#DM37137`: exact Mail Lite size for teacher keyrings, bookmarks, minifigure keyrings, hanging jigsaws, and offer decorations is not confirmed. Counted as Small/D1 for now.
- `#DM37083`: mixed framed pebble picture, two hanging hearts, an offer decoration, and three gift boxes. Counted as 1 pebble box plus 1 D/1, but this needs real packing confirmation.
- `#DM37094`, `#DM37096`, and `#DM37135`: Gift Box is present with small hanging-heart products. Current rule assumes D/1, but gift boxes may require Medium/F3, Large/H5, or more than one package.
- `#DM37076`: East of India matchbox plus a framed pebble picture was counted as one pebble box. Confirm whether matchboxes travel inside the pebble box or require a separate D/1 envelope.
- `#DM37118`: matchbox plus small pebble heart counted as one D/1. Confirm combined fit.
- `#DM37140`: upgraded street sign plus hanging heart/decoration counted as one corrugated package plus one D/1. Confirm whether this ships as two packages or together.
- `#DM37142`: A4 print packaging is not defined in the stock reference. Counted as Large/H5 as a fit-based fallback.
- Mail Lite fragile tape usage remains unquantified in the source files, so tape cost is understated for envelope orders.

## Ordering Recommendation

No reliable ordering recommendation can be made yet. The shared files still do not include current stock-on-hand, minimum reorder levels, supplier lead times, or preferred reorder quantities for the packaging items.

Based on usage alone, the highest consumables in this run were:

- 31 corrugated street-sign packages, equal to approx 10.33 of the 725 x 1135mm corrugated sheets.
- 22 Small/D1 envelopes and 8 Large/H5 envelopes.
- 12 custom pebble picture boxes and 24 Guardian paper strips.

Add stock-on-hand and reorder thresholds for each packaging item before this automation can say what needs ordering and why.

## Next Cutoff For Future Run

Next run should start after `#DM37142`, unless Shopify later shows an order correction, cancellation, or missing order in this range.
