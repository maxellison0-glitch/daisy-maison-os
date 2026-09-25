# Theme changes: Christmas decoration builders + Mr & Mrs line 2 (24 Sep 2026)

**Status:** built and tested, now in Max's working draft **"Copy of In construction 🚧"** (id 207727198547). Max made that draft on 24 Sep as the theme to keep working in before publishing. The same three files were first built and tested on "Claude – Xmas builders + Mr & Mrs (24 Sep)" (id 207729066323), which is now redundant and can be deleted. Before the swap, the draft's copies of the three files were byte-identical to live. After the swap, all three match (md5 `b9463a19…`, `b9d71c47…`, `f26557b2…`). Not published. Max publishes.

Preview links:
- Family Festive star: https://daisymaison.co.uk/products/personalised-family-festive-christmas-pebble-star-hanging-decoration?preview_theme_id=207727198547
- Merry & Bright: https://daisymaison.co.uk/products/personalised-merry-bright-family-christmas-pebble-hanging-decoration?preview_theme_id=207727198547
- Mr & Mrs sign: https://daisymaison.co.uk/products/mr-mrs-personalised-street-sign-gift?preview_theme_id=207727198547

Three files differ from live. The full change is in `xmas-builders-and-mr-mrs-line2.diff`, and `build_xmas.py` regenerates the builder edit from the live files.

| File | Change |
|---|---|
| `layout/theme.liquid` | The two decoration handles join the list of pages that load the native heart builder (`dm-heart-builder` + `daisy-heart-builder.js`). |
| `snippets/dm-heart-builder.liquid` | Two new kinds, `merrybrightheart` and `festivestar`, each a config block cloned from Wonderland. |
| `assets/daisy-street-sign-options.js` | Mr & Mrs preview: the sample line 2 only shows while line 1 is still the example. |

## 1. Merry & Bright and Family Festive star: off Globo, onto the native builder

Both pages now use the same builder as the other Christmas decorations (Wonderland, Love at Christmas, Our 1st Christmas). The builder hides the Globo form itself. `dm-wrap-kits` automatically adds the Gift Wrap Kit with the Classic / Christmas choice to every heart-builder page, so both pages get the Christmas kit with no change to the wrap-kit code.

**Property keys are verbatim from each product's own Globo form** (read from the live pages on 24 Sep), because fulfilment reads them exactly:

| | Merry & Bright | Family Festive star |
|---|---|---|
| Pebble count key / values | `Number of pebbles`: `1`–`4`, `5 (Large heart +£3)`, `7 (Large heart +£5)` | `Number of pebbles`: `1`–`4`, `5 (Large heart)`, `7 (Large heart)` |
| Size key / values | `Size 1`: `Small 10 x 10cm (£15.95)` / `Large 15 x 15cm (£18.95)` | `Size`: same two values |
| Pebble types | Adult, Child, Dog, Cat | Adult, Teen, Child, Baby, Dog, Cat |
| Wording | `Text above`, `Text below` | `Text above`, `Text below` |
| Year question | `Add 2026?` (Globo still says 2025; Wonderland's native config moved to 2026) | none (Globo never asked) |
| Second item | `**INCREDIBLE OFFER**` YES Please / NO Thanks, then `(Offer) …` keys | same |
| Helpers | (+£3) Large Decoration, (+£5) 7/8 pebbles, (+£10.95) INCREDIBLE OFFER DECORATION | same |
| Gift boxes | the three Wonderland designs | **none**, see below |

The star's keys match its three most recent paid orders (Aug–Sep 2026): `Number of pebbles`, `Size`, `Pebble N`, `Text above`, `Text below`, `**INCREDIBLE OFFER**`, and the `(+£3) Large Decoration` line at 5 pebbles. Merry & Bright had no orders in the last 60 days, so its keys come from the live Globo form. They are identical to Wonderland's, whose native config has been live all season.

**No gift boxes on the star.** Its description says "small 12cm x 12cm, large 20cm x 20cm", but the gift boxes are 10 × 10 and 14 × 18, so a box might not fit. The Globo page never offered one either. Add the `giftBox` block (copy it from Wonderland) once the size is confirmed.

### Tested on the preview (390 px phone, headless)

- **Star, 5 pebbles (Adult, Adult, Teen, Baby, Dog) with the Christmas wrap kit:** the total showed £24.90, and the basket received exactly:
  - the star, £15.95, with `Number of pebbles: 5 (Large heart)`, `Size: Large 15 x 15cm (£18.95)`, `Pebble 1–5`, `Text above`, `Text below`, `**INCREDIBLE OFFER**: NO Thanks`;
  - `(+£3) Large Decoration`, £3.00;
  - `Christmas Gift Wrap Kit`, £5.95.
  No Globo blocks were visible.
- **Merry & Bright, 7 pebbles with the year and a second heart (on Max's draft):** the total showed £31.90, and the basket received exactly:
  - the heart, £15.95, with `Number of pebbles: 7 (Large heart +£5)`, `Size 1: Large 15 x 15cm (£18.95)`, `Pebble 1–7`, `Text above`, `Text below`, `Add 2026?: YES Please`, `**INCREDIBLE OFFER**: YES Please`, and every `(Offer) …` key;
  - `(+£5) 7/8 pebbles`, £5.00;
  - `(+£10.95) **INCREDIBLE OFFER** DECORATION`, £10.95.
  No Globo blocks were visible.
- **Merry & Bright, 3 pebbles, small, no year, with the Christmas wrap kit (on Max's draft):** the total showed £21.90, and the basket received:
  - the heart, £15.95, with `Number of pebbles: 3`, `Size 1: Small 10 x 10cm (£15.95)`, `Add 2026?: NO Thanks leave blank`, `Gift Wrap Kit: YES Please`;
  - `Christmas Gift Wrap Kit`, £5.95.

## 2. Mr & Mrs: line 1 only means a one-line sign

Before, an empty line 2 always previewed the sample "FROM THIS DAY FORWARD - 14.08.2027", even after the customer had typed their own line 1 and the caption said "Your sign". Now the sample subtitle belongs to the untouched example only:

| Customer has typed | Preview |
|---|---|
| nothing | example sign, both lines, "Example — fill in the lines below" |
| line 1 only | their line 1 only, "Your sign", "Personalisation complete" badge |
| line 1 + line 2 | both of their lines |
| clears line 2 | line 1 only again |
| clears line 1 | the example returns |

Production already handles this: `production/run-batch.ps1` passes a blank line 2 as `--no-line2`, and `artwork/build.py` keeps line 1 in the same place whether or not there is a line 2. So the preview now matches what gets made. Adding to basket with only line 1 sends `Line 2: ""`, which was tested.

## Before publishing

1. Everything now lives in the draft "Copy of In construction 🚧". Keep working there, and don't publish the redundant "Claude – Xmas builders…" theme.
2. Re-check the live theme for changes made after the draft was created (16:46 on 24 Sep), and copy any across first (as on 23 Sep, when a checkout wording change was nearly lost).
3. Confirm the star's real size (10 × 10 / 15 × 15 per its Globo form, or 12 × 12 / 20 × 20 per its description).

---

# 25 Sep 2026: speed, honesty and basket fixes (on the same draft)

Max asked for a full check of the site before publishing: landing pages, the basket drawer, the basket, checkout and the homepage. The audit found the causes of the slowness, some leftover and misleading widgets, and basket friction. Max approved the fixes ("proceed with them, especially the ones that move the needle"). All of them are on the draft "Copy of In construction 🚧" (207727198547) only. Not published.

The full change is in `speed-honesty-basket-0925.diff`, apart from `config/settings_data.json`, which is listed below. `build_font.py` rebuilds the light sign font.

## What changed

| File | Change | Why |
|---|---|---|
| `sections/image-banner.liquid` | On phones, the first slide of a banner near the top of a page loads straight away with high priority (`loading="eager"`, `fetchpriority="high"`). Later slides and the hidden desktop photo stay lazy. | The homepage's main photo was set to load last. It appeared at 13.5 s on a mid-range phone on 4G. |
| `assets/daisy-street-sign-times-latin.woff2` (new) and `layout/theme.liquid` | The sign preview font is now a 27 KB Latin WOFF2. The original 1.2 MB TTF remains as an automatic fallback for any other character, and is only downloaded if a customer types one. The same change applies to all six places that load the font. | The full font (Times New Roman with every alphabet) was about 0.75 MB to download on the Mr & Mrs, family and other sign pages. Glyphs and spacing are unchanged (checked character by character). |
| `templates/product.json` | Disabled: the "Price increases in X days / Sale price ends in" countdown (custom liquid; it reset every Monday), the "X customers are viewing this product" block (it used preset numbers), the Feefo stars block and the Feefo reviews section. | Fake urgency and fake social proof are banned practices under the DMCC Act 2024 (CMA fines up to 10% of turnover). Feefo is closed and only produced errors. |
| `config/settings_data.json` | Feefo core app embed off; theme currency switcher off (`enable_currencies`); "GBP" after prices off (`currency_format_enable`); leftover Ella demo "Before you leave… 20% off CODESALE20" pop-up off; drawer "You May Also Like" off (it was fed from "HIDE best sellers", which recommended add-on SKUs like "(+£10.45) Large Street Sign"); the "3.98%" label on the free-delivery bar off. | Speed and tidiness. Checkout always charges GBP, so a browser-side USD/EUR converter was misleading. |
| `locales/en.default.json` | Drawer: "Shopping Cart" → "Your cart" (matches the basket page); "free shipping" → "free UK delivery"; "Tax included and shipping calculated at checkout" → "Tax included. Delivery calculated at checkout." | UK wording, matching the announcement bar and basket. |
| `sections/main-cart.liquid` | 1) The occasion diffuser card (family, friendship and Christmas diffusers) now sits below the basket and its totals, not above the customer's own item. The Mr & Mrs matching-set card ("✓ Your sign is in the basket") stays at the top. 2) Express checkout buttons (Shop Pay, PayPal, Google Pay, Apple Pay on iPhones) under the totals, outside the sticky mobile checkout bar. 3) The line under the checkout button now says "UK delivery from £4.95 · free from £50" (threshold read from the theme setting). 4) "despatch" → "dispatch". | Of 9 top UK gift stores on Shopify, none put another product above the customer's item. Most offer express pay and state the delivery price up front. The Mr & Mrs basket already reaches checkout 65% of the time with its card on top; family and pebble-picture baskets were under 40%. |
| `sections/header-utility.liquid` | The mobile menu script checks that its elements exist before writing to them. | It threw an error on every page load. |

The occasion card is moved by splitting the snippet's output in `main-cart.liquid`, and the snippet itself is unchanged. It stays outside `#main-cart-items` on purpose: `daisy-matching-gift.js` watches that element for basket changes, and a card inside it would keep re-triggering its own refresh.

## Tested on the draft (390 px phone, headless, one page load every 5 minutes)

- **Homepage:** the main photo appeared at 7.6 s instead of 13.5 s (live, same conditions), even though preview pages are served more slowly (time to first byte 2.2 s against 1.0 s). Total blocking time fell from 5.5 s to 4.7 s. Only the 750 px phone photo downloads. There were no failed requests and no page errors, where before there were Feefo 400s and the menu error.
- **Mr & Mrs, line 1 only:** no countdown, viewer counter or Feefo. Only the light font was downloaded. The add sends `Line 1: MR & MRS SMITH`, `Line 2: ""` and `Size: Small 29 x 8.5cm`. In the basket, the matching-set card is at the top, then the sign, the totals and the express buttons. The delivery line is correct.
- **Family sign:** the sign is now the first thing in the basket (y = 205 px; before, it came after the diffuser card at about 557 px). The diffuser card is below the totals. The express buttons show. "Finish your gift" still opens on "Proceed to checkout", and "Continue without extras" reaches Shopify checkout.
- **Drawer:** opens in about 0.4 s and shows "Your cart" and "Only £48.01 away from free UK delivery". The "GBP" suffix, the % label and "You May Also Like" are gone, and the text reads "Tax included. Delivery calculated at checkout." No page errors.
- **Mr & Mrs page speed:** fonts fell from 759 KB to 187 KB and total weight from 5.4 MB to 5.2 MB, with no Feefo errors. Largest paint is still about 10 s, because the gallery jumps to photo 12 (see below). Total blocking time on the preview reads higher (6.2 s), but previews add about 260 KB of preview-bar script that customers never load. One run got four 503s on add-on lookups, which were rate limits from repeated test loads. The walkthrough 15 minutes earlier loaded all four add-ons normally.
- **Live drift check:** the live theme was last changed at 10:30 on 24 Sep, before the draft was copied (16:46). Its `settings_data.json`, `index.json`, `product.json`, `cart.json`, header and footer groups, `en.default.json`, `main-cart.liquid` and the basket snippets match the draft's originals byte for byte, so publishing the draft loses nothing.

## Not changed, waiting for Max

- **Mr & Mrs gallery jumps to photo 12 of 14 after loading.** The Small variant has its own photo attached (`Wed.S.Sign-5.jpg`). Fixing it means detaching that photo, which is live product data.
- **"Finish your gift" pop-up at checkout:** keep, show once, or remove.
- **Checkout "Sign in", "Not now" and footer links are white on the pale pebble background.** Fix in Settings → Checkout → Customise. The Admin API can't change checkout branding on this plan.

## Later (not tonight)

- **Globo inline config:** 4.5 MB on every page, the single biggest cause of the frozen screen. It covers 526 products: 177 are archived, deleted or draft, and 143 already use our builders. Clean it up in the Globo admin, then convert the remaining products (the wall planner is the main one) and retire Globo.
- **Google Tag Manager is loaded twice,** once hard-coded in `theme.liquid` (GTM-TCZZV8JS via the Stape loader) and once by the Stape app embed. Blocking the tracking stack in a test cut 1.6 s of blocking time and 1 MB of script. The ads team should check for double-counted conversions first.
- **All-year "SALE 61%" reference prices** (Mr & Mrs £28.95 → £11.25) fall under the same DMCC rules. Review them after Christmas.
- **The basket's dispatch copy says 5–7 / 2–3 working days,** but the checkout method names say "within 5" / "within 2". Align them.
- **The sign font file is Microsoft's Times New Roman,** which needs a web-font licence to be served from the site. Check it.
- **A modern OS 2.0 theme in January.**

## Rollback

Revert the files using the diff in this folder (reverse-apply it). For `config/settings_data.json`, set `enable_currencies`, `currency_format_enable`, `show_before_you_leave`, `calculator_free_shipping_message_show_percent` and `show_quick_cart_popular_product` back to `true`, and re-enable the Feefo core app embed. The new font asset can stay; it is only used when `theme.liquid` references it.
