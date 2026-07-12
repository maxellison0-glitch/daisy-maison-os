# Daisy Maison Packaging Order Review

Pulled from Shopify on 2026-07-09.

Scope: latest 20 paid, unfulfilled orders from `#DM36819` through `#DM36800`.

Purpose: first pass at predicting packaging used per order. This is intentionally explicit so corrections can be added and converted into better rules.

## Packing Rules Used In This Pass

| Product/order signal | Packaging assumption |
| --- | --- |
| Product title contains `Pebble Picture` | Custom pebble picture box. Up to 2 pebble pictures per box. 2 Guardian paper strips per box. Approx 0.2m fragile tape per box. |
| Street sign with `Size Upgrade - Medium` or `Size Upgrade - Large` | Corrugated sheet allocation: 1/3 of 725 x 1135mm sheet per sign. Approx 1m fragile tape. Does not fit Mail Lite. |
| Street sign with no medium/large upgrade | Medium or Large envelope setting depending on sign size/context. Large used when unsure. |
| East of India matchboxes | Small envelope setting. |
| East of India tealights | Up to 2 tealights in Small envelope setting; more than 2 moves to Medium or Large. |
| Small pebble hearts | Small envelope setting. |
| Other small gift/keyring/jigsaw items | Small or Medium envelope setting depending on product size. Needs correction by product family. |
| Gift Wrap Kit / Gift Box / Frame / Mounting Strips add-ons | Assumed to travel inside the main package unless noted. Needs confirmation. |

## Order-By-Order Packing Estimate

| Order | Shopify line items | Packing estimate | Confidence | Correction notes |
| --- | --- | --- | --- | --- |
| #DM36819 | 1 x Personalised Wedding Pebble Picture, SKU 125755 | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High |  |
| #DM36818 | 1 x Mum Grandparent Pebble Picture - Moon & Back, SKU 86330 | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High |  |
| #DM36817 | 1 x Family Pebble Picture - Flutterby Blossom Tree, SKU 65693 | 1 pebble box; 2 Guardian strips; 0.2m fragile tape | High |  |
| #DM36816 | 1 x Teacher Pebble Picture; 1 x (£9.95) Frame | 1 pebble box; 2 Guardian strips; 0.2m fragile tape; frame assumed not to require separate outer packaging | Medium | Confirm whether frame add-on changes box or paper usage. |
| #DM36815 | 1 x Teacher Hanging Jigsaw Piece, SKU 109684 | 1 Mail Lite D/1 assumed | Low | Confirm D/1 vs F/3 and whether extra protection is used. |
| #DM36814 | 1 x Size Upgrade - Large; 1 x Mr & Mrs Street Sign, SKU 36961 | 1/3 corrugated sheet; 1m fragile tape | High | Size upgrade means not Mail Lite. |
| #DM36813 | 1 x Gift Wrap Kit, SKU ACC-GIFTWRAP; 1 x Teacher Street Sign | 1 larger envelope setting, likely Large if in doubt; gift wrap kit assumed inside package | Medium | Small street sign uses Medium/Large envelope options. Confirm if gift wrap kit changes mailer size. |
| #DM36812 | 1 x Teacher Superhero Minifigure Keyring, SKU 108445 | 1 Mail Lite D/1 assumed | Low | Confirm D/1 and any small accessory packaging. |
| #DM36811 | 1 x Teacher Hanging Jigsaw Piece, SKU 109684 | 1 Mail Lite D/1 assumed | Low | Same as #DM36815. |
| #DM36810 | 1 x Size Upgrade - Large; 1 x Dad Street Sign, SKU 88071 | 1/3 corrugated sheet; 1m fragile tape | High | Size upgrade means not Mail Lite. |
| #DM36809 | 1 x Mounting Strips; 1 x Size Upgrade - Large; 1 x Mr & Mrs Street Sign, SKU 36961 | 1/3 corrugated sheet; 1m fragile tape; mounting strips assumed inside package | Medium | Confirm whether mounting strips add any extra mailer/bag/card. |
| #DM36808 | 1 x Teacher Porcelain Matchbox Star, SKU EOI-MB-STAR-TEACHER; 1 x (+GBP 5.65)x2 Matchboxes; 1 x Teacher Porcelain Tea Light Holder, SKU EOI-TL-TEACHER-AMAZING | 1 Medium envelope assumed because this combines matchboxes plus 1 tealight | Medium | Single/2 tealights or matchboxes alone fit Small, but combined items likely need larger envelope. Confirm. |
| #DM36807 | 1 x Size Upgrade - Large; 1 x Mr & Mrs Street Sign, SKU 36961 | 1/3 corrugated sheet; 1m fragile tape | High | Size upgrade means not Mail Lite. |
| #DM36806 | 1 x Size Upgrade - Medium; 1 x Family Street Sign, SKU 36965 | 1/3 corrugated sheet; 1m fragile tape | High | Medium upgrade means not Mail Lite. |
| #DM36805 | 1 x Teacher Rainbow Pebble People Hanging Heart, SKU 47472-1; 1 x Gift Box - Thank you for being amazing, SKU GIFTBOX-TFBA | 1 Medium envelope assumed because gift box is included; small pebble heart alone would fit Small | Medium | Confirm whether gift box pushes this to Medium. Not a pebble picture box. |
| #DM36804 | 1 x Teacher Porcelain Tea Light Holder | 1 Small envelope | High | Up to 2 East of India tealights fit Small envelope. |
| #DM36803 | 1 x Mr & Mrs Street Sign, SKU 36961 | 1 larger envelope setting, likely Large if in doubt | Medium | No size upgrade found, so small street sign. Check sign size/context for Medium vs Large. |
| #DM36802 | 1 x Gift Wrap Kit; 1 x Wedding Pebble Picture, SKU 125755 | 1 pebble box; 2 Guardian strips; 0.2m fragile tape; gift wrap kit assumed inside package | Medium | Confirm whether gift wrap kit changes package. |
| #DM36801 | 2 x Teacher Superhero Minifigure Keyring, SKU 108445 | 1 Mail Lite F/3 assumed for two keyrings | Low | Could be D/1 if two fit safely. |
| #DM36800 | 1 x Gift Wrap Kit; 1 x Wedding Pebble Picture, SKU 125755 | 1 pebble box; 2 Guardian strips; 0.2m fragile tape; gift wrap kit assumed inside package | Medium | Same as #DM36802. |

## Estimated Packaging Used By These 20 Orders

These totals are a first-pass estimate and should be revised after corrections.

| Packaging item | Estimated quantity used |
| --- | ---: |
| Custom pebble picture boxes | 6 |
| Guardian paper strips | 12 |
| Guardian paper rolls | 0.0667 rolls |
| 725 x 1135mm corrugated sheets | 1.6667 sheets |
| Fragile tape for pebble boxes | 1.2m |
| Fragile tape for medium/large street signs | 5m |
| Fragile tape total from known rules | 6.2m |
| Small envelope, D/1 | 4 |
| Medium envelope, F/3 | 3 |
| Large envelope, H/5 | 2 |

Note after correction: Small envelope/D1 now has confirmed coverage for East of India matchboxes, up to 2 East of India tealights, and small pebble hearts. Small street signs should be counted as Medium or Large envelopes, chosen from the sign size/context.

## Anomalies / Rules To Confirm

1. Size upgrade products must be linked to the street sign in the same order, not counted as a separate package.
2. Small street signs use the Medium or Large envelope options; check sign size/context for Medium vs Large.
3. Gift Wrap Kit, Gift Box, Frame, and Mounting Strips add-ons need rules for whether they change packaging.
4. `Teacher Rainbow Pebble People Hanging Heart` contains `Pebble People` but is not a framed pebble picture. It should use Mail Lite, not pebble box.
5. East of India matchboxes and up to 2 tealights fit D/1; larger combined quantities move to larger Mail Lite sizes.
6. Multiple small accessories in one order may use one larger mailer rather than separate mailers.
