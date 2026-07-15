# Daisy Maison Packaging Stock Usage Report - 2026-07-15

Run time: 2026-07-15 06:06 Europe/London.

Scope: paid Shopify orders created after the last counted order from the 2026-07-14 packaging report. This run counts orders from `#DM37143` through `#DM37212` that were visible in read-only Shopify queries by 2026-07-15 06:06 Europe/London.

Read-only Shopify data was pulled during this run. No Shopify data was updated, no messages were sent, and no orders were placed.

## Source Files Read

- `stock-automation/shared-tracker-context/shared-stock-context.md`
- `stock-automation/reports/daisymaison-packaging-stock-reference.md`
- `stock-automation/reports/daisymaison-packaging-stock-project.md`
- `stock-automation/shared-tracker-context/tracker-change-log.md`
- `stock-automation/reports/daisymaison-packaging-stock-usage-report-2026-07-14.md`

No new human packaging recipe corrections were found after the 2026-07-10 delivery-pricing notes.

## Rules Applied

- Framed pebble pictures use the custom Daisy Maison pebble picture box. Up to 2 pebble pictures fit in 1 box.
- Each pebble box uses 2 Guardian paper strips and approx 0.2m fragile tape.
- Small pebble hearts use the Small envelope setting, D/1, and are not counted as framed pebble pictures.
- East of India matchboxes and up to 2 tealights use Small/D1. One mixed order had 2 tealights plus a small hanging heart and was counted as D/1 with medium confidence.
- Street signs with Medium or Large size upgrades use corrugated sheet packaging: 1/3 of a 725 x 1135mm sheet and approx 1m fragile tape per sign package.
- Small street signs without a Medium/Large upgrade use the Large/H5 fallback when unsure, following the prior report convention.
- Gift wrap kits, gift boxes, easels, mounting strips, Lucky Sixpence, and Shipping Protection are not counted as separate packages unless the order context requires it. This remains an assumption.
- Keyrings, bookmarks, hanging decorations, A4 prints, frames, and boxed lucky sixpence still lack confirmed packaging rules. This report keeps the prior low-confidence Mail Lite fallback and flags those orders.

## Packaging Usage Summary

| Packaging item | Estimated usage | Cost basis | Estimated cost |
| --- | ---: | --- | ---: |
| Small envelope, D/1 | 16 envelopes | GBP 0.0831 each | GBP 1.33 |
| Medium envelope, F/3 | 0 envelopes | GBP 0.1090 each | GBP 0.00 |
| Large envelope, H/5 | 9 envelopes | GBP 0.1633 each | GBP 1.47 |
| Custom pebble picture box | 19 boxes | GBP 0.5974 each | GBP 11.35 |
| Guardian paper strips | 38 strips | GBP 0.2846 each | GBP 10.81 |
| 725 x 1135mm corrugated sheet | 9.33 sheets allocated from 28 sign packages | GBP 0.6500 per sheet | GBP 6.07 |
| Fragile tape for corrugated and pebble boxes | 31.8m | GBP 0.0186 per metre | GBP 0.59 |
| Fragile tape for Mail Lite envelopes | Not quantified | Exact tape length missing | Not costed |

Estimated packaging cost counted here: GBP 31.62, excluding unconfirmed Mail Lite tape usage and any separate add-on packaging.

## Orders Reviewed

The Shopify paid-order pull returned 70 new orders not counted in the 2026-07-14 packaging report.

| Order | Created at | Main Shopify line items | Packaging estimate | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `#DM37143` | 2026-07-14 06:33 UTC | Teacher Pebble People Hanging Heart; Large Decoration | 1 Small envelope, D/1 | Low | Small-heart rule applies, but large decoration handling is not confirmed. |
| `#DM37144` | 2026-07-14 07:21 UTC | Retirement Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37145` | 2026-07-14 08:03 UTC | Engagement Pebble Picture; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Easel assumed inside pebble package. |
| `#DM37146` | 2026-07-14 08:03 UTC | Teacher Superhero Minifigure Keyring | 1 Small envelope, D/1 | Low | Minifigure keyring mailer size is not confirmed. |
| `#DM37147` | 2026-07-14 08:10 UTC | Large Mr & Mrs Street Sign; Gift Wrap Kit | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Gift wrap assumed inside corrugated package. |
| `#DM37148` | 2026-07-14 08:26 UTC | Teacher Watercolour Flower A4 Print; White Frame add-on | 1 Large envelope, H/5 | Low | A4 print and frame packaging are not defined. |
| `#DM37149` | 2026-07-14 08:29 UTC | Teacher Rainbow Pebble Hanging Heart; offer decoration; 2 x Gift Box | 1 Small envelope, D/1 | Low | Gift boxes may change mailer size. |
| `#DM37150` | 2026-07-14 09:16 UTC | Engagement Pebble Picture; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Easel assumed inside pebble package. |
| `#DM37151` | 2026-07-14 10:06 UTC | Teacher Star Keyring plus offer keyring | 1 Small envelope, D/1 | Low | Keyring mailer size is not confirmed. |
| `#DM37152` | 2026-07-14 10:55 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37153` | 2026-07-14 11:16 UTC | Medium Dad Bar & Grill Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37154` | 2026-07-14 11:26 UTC | Teacher Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37155` | 2026-07-14 11:30 UTC | Medium Family Street Sign; Gift Wrap Kit; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Add-ons assumed inside corrugated package. |
| `#DM37156` | 2026-07-14 11:32 UTC | Teacher Shine Star Keyring | 1 Small envelope, D/1 | Low | Keyring mailer size is not confirmed. |
| `#DM37157` | 2026-07-14 11:41 UTC | Laser Cut BBQ Sign with free gift box | 1 Large envelope, H/5 | Low | This sign/gift-box format needs confirmed packaging. |
| `#DM37158` | 2026-07-14 11:58 UTC | Lucky Sixpence boxed | 1 Small envelope, D/1 | Low | Standalone Lucky Sixpence packaging is not confirmed. |
| `#DM37159` | 2026-07-14 12:20 UTC | Mr & Mrs Street Sign; 2 x Large upgrade; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Two upgrade lines appeared for one sign line; counted as one sign package. |
| `#DM37160` | 2026-07-14 12:21 UTC | Wedding Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37161` | 2026-07-14 12:30 UTC | Medium Family Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37162` | 2026-07-14 12:40 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37163` | 2026-07-14 13:11 UTC | Medium Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37164` | 2026-07-14 13:28 UTC | Medium Dad Bar & Grill Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37165` | 2026-07-14 13:41 UTC | Teacher Rainbow Pebble Hanging Heart | 1 Small envelope, D/1 | High | Small pebble heart rule applies. |
| `#DM37166` | 2026-07-14 13:50 UTC | Teacher Bookmark plus offer bookmark | 1 Small envelope, D/1 | Low | Bookmark mailer size is not confirmed. |
| `#DM37167` | 2026-07-14 13:52 UTC | Family Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37168` | 2026-07-14 14:03 UTC | Teacher Rainbow Pebble Hanging Heart; 2 x Teacher Tea Light Holder | 1 Small envelope, D/1 | Medium | Two tealights fit D/1 alone; combined fit with heart should be confirmed. |
| `#DM37169` | 2026-07-14 14:04 UTC | Family Blossom Tree Pebble Picture; 7/8 Pebbles add-on | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Extra pebbles do not change the package under current rules. |
| `#DM37170` | 2026-07-14 15:01 UTC | Wedding Pebble Picture; Gift Wrap Kit; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Add-ons assumed inside pebble package. |
| `#DM37171` | 2026-07-14 15:02 UTC | Medium Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37172` | 2026-07-14 15:03 UTC | Vintage Style Train Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37173` | 2026-07-14 15:20 UTC | Wedding Pebble Picture; Easel | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Easel assumed inside pebble package. |
| `#DM37174` | 2026-07-14 16:13 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37175` | 2026-07-14 16:16 UTC | Engagement Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37176` | 2026-07-14 16:26 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37177` | 2026-07-14 16:47 UTC | Family Wedding Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37178` | 2026-07-14 16:50 UTC | Wedding Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37179` | 2026-07-14 17:17 UTC | Teacher Porcelain Tea Light Holder | 1 Small envelope, D/1 | High | Single tealight fits D/1. |
| `#DM37180` | 2026-07-14 17:18 UTC | Medium Mr & Mrs Street Sign; Easel; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Add-ons assumed inside corrugated package. |
| `#DM37181` | 2026-07-14 17:36 UTC | 2 x Family Street Sign; 1 x Medium upgrade | 2 corrugated sign packages; 2/3 sheet; 2m fragile tape | Medium | Two sign lines appeared but only one size upgrade line. |
| `#DM37182` | 2026-07-14 17:40 UTC | Teacher Bookmark | 1 Small envelope, D/1 | Low | Bookmark mailer size is not confirmed. |
| `#DM37183` | 2026-07-14 17:41 UTC | Vintage Train Sign; second-sign offer; 2 x Medium upgrade | 2 corrugated sign packages; 2/3 sheet; 2m fragile tape | Medium | Two Medium upgrades make two corrugated packages likely. |
| `#DM37184` | 2026-07-14 17:49 UTC | Medium Grandparent Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| `#DM37185` | 2026-07-14 17:56 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37186` | 2026-07-14 17:59 UTC | Large Mr & Mrs Street Sign; Mounting Strips | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37187` | 2026-07-14 18:23 UTC | Medium Mr & Mrs Street Sign; Easel | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Easel assumed inside corrugated package. |
| `#DM37188` | 2026-07-14 18:37 UTC | Christening Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37189` | 2026-07-14 18:46 UTC | Christening Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37190` | 2026-07-14 18:53 UTC | Wedding Pebble Picture; Gift Wrap Kit | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Gift wrap assumed inside pebble package. |
| `#DM37191` | 2026-07-14 18:53 UTC | Teacher Rainbow Pebble Hanging Heart; offer decoration; Gift Box | 1 Small envelope, D/1 | Low | Decoration and gift box may change mailer size. |
| `#DM37192` | 2026-07-14 19:05 UTC | Large Family Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37193` | 2026-07-14 19:06 UTC | Family Street Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |
| `#DM37194` | 2026-07-14 19:13 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37195` | 2026-07-14 19:18 UTC | Teacher Star Keyring plus offer keyring | 1 Small envelope, D/1 | Low | Keyring mailer size is not confirmed. |
| `#DM37196` | 2026-07-14 19:24 UTC | Mum Pebble Hanging Heart | 1 Small envelope, D/1 | High | Small pebble heart rule applies. |
| `#DM37197` | 2026-07-14 19:25 UTC | Friendship Pebble Picture; 7/8 Pebbles add-on | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Extra pebbles do not change the package under current rules. |
| `#DM37198` | 2026-07-14 19:27 UTC | Engagement Pebble Picture; Gift Wrap Kit | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Gift wrap assumed inside pebble package. |
| `#DM37199` | 2026-07-14 19:31 UTC | Christening Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37200` | 2026-07-14 19:34 UTC | Christening Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture. |
| `#DM37201` | 2026-07-14 19:40 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37202` | 2026-07-14 20:04 UTC | Teacher Pebble Picture | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High | Standard framed pebble picture by title. |
| `#DM37203` | 2026-07-14 20:59 UTC | Large Mr & Mrs Street Sign; Mounting Strips; Easel; Shipping Protection | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Add-ons assumed inside corrugated package; Shipping Protection is non-physical. |
| `#DM37204` | 2026-07-14 21:43 UTC | Medium Family Street Sign; Gift Wrap Kit | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | Medium | Gift wrap assumed inside corrugated package. |
| `#DM37205` | 2026-07-14 21:47 UTC | Family Blossom Tree Pebble Picture; Gift Wrap Kit | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Gift wrap assumed inside pebble package. |
| `#DM37206` | 2026-07-14 21:49 UTC | Teacher Shine Star Keyring plus offer keyring | 1 Small envelope, D/1 | Low | Keyring mailer size is not confirmed. |
| `#DM37207` | 2026-07-14 21:58 UTC | Large Mr & Mrs Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37208` | 2026-07-14 22:04 UTC | Teacher Street Sign; Easel | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure; easel assumed inside. |
| `#DM37209` | 2026-07-14 22:14 UTC | Teacher Rainbow Pebble Hanging Heart; Gift Box | 1 Small envelope, D/1 | Low | Gift box may change mailer size. |
| `#DM37210` | 2026-07-14 23:31 UTC | Large Engagement Street Sign | 1 corrugated sign package; 1/3 sheet; 1m fragile tape | High | Large upgrade means not Mail Lite. |
| `#DM37211` | 2026-07-15 01:51 UTC | New Home Pebble Picture; Gift Wrap Kit; Shipping Protection | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | Medium | Gift wrap assumed inside pebble package; Shipping Protection is non-physical. |
| `#DM37212` | 2026-07-15 05:00 UTC | Vintage Style Train Sign | 1 Large envelope, H/5 | Medium | No size upgrade found; Large used when unsure. |

## Low-Confidence Classifications And Anomalies

- `#DM37146`, `#DM37151`, `#DM37156`, `#DM37166`, `#DM37182`, `#DM37195`, and `#DM37206`: exact Mail Lite size for teacher keyrings, minifigure keyrings, bookmarks, and offer keyrings/bookmarks is not confirmed. Counted as Small/D1 for now.
- `#DM37143`, `#DM37149`, `#DM37191`, and `#DM37209`: small hanging-heart products with decorations and/or gift boxes. Counted as D/1, but gift boxes and larger decorations may require Medium/F3, Large/H5, or more than one package.
- `#DM37148`: A4 print plus frame add-on. Counted as Large/H5 as a fit-based fallback, but frame packaging is not defined in the shared files.
- `#DM37157`: Laser Cut BBQ Sign with free gift box. Counted as Large/H5, but this product family is not in the packaging reference and should be confirmed.
- `#DM37158`: standalone boxed Lucky Sixpence. Counted as D/1, but standalone packaging has not been confirmed.
- `#DM37159`: two Large upgrade lines appeared with one Mr & Mrs street sign line. Counted as one corrugated package; check whether this was a duplicated option line or a real second package.
- `#DM37168`: two East of India tealights plus one small hanging heart were counted as one D/1 envelope. Confirm combined fit.
- `#DM37181`: two Family Street Sign lines but one Medium upgrade line. Counted as two corrugated sign packages because there are two physical sign lines; confirm whether both signs were upgraded.
- Mail Lite fragile tape usage remains unquantified in the source files, so tape cost is understated for envelope orders.

## Ordering Recommendation

No reliable ordering recommendation can be made yet. The shared files still do not include current stock-on-hand, minimum reorder levels, supplier lead times, or preferred reorder quantities for the packaging items.

Based on usage alone, the highest consumables in this run were:

- 28 corrugated street-sign packages, equal to approx 9.33 of the 725 x 1135mm corrugated sheets.
- 19 custom pebble picture boxes and 38 Guardian paper strips.
- 16 Small/D1 envelopes and 9 Large/H5 envelopes.

Add stock-on-hand and reorder thresholds for each packaging item before this automation can say what needs ordering and why.

## Next Cutoff For Future Run

Next run should start after `#DM37212`, unless Shopify later shows an order correction, cancellation, or missing order in this range.
