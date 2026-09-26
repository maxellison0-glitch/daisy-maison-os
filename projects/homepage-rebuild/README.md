# Mobile homepage rebuild (23 Sep 2026)

**Status:** **published by Max on 24 Sep 2026.** The theme copy **"In construction 🚧" (id 207623029075)** is now the live theme, replacing "🚧 " (id 207563915603). Measure around 22 Oct (see "Measuring").

**Live:** https://daisymaison.co.uk/

**Revised after Max's review (23 Sep, afternoon):** the hero is now a two-photo carousel of the two biggest sellers (wedding sign first), "Lytham St Annes" is "Lancashire" everywhere, the workshop video is gone, and the announcement bar is one quiet line with no "[date]". See "Max's review" below.

Full brief with the reference board: https://claude.ai/artifact/1EsvvfN6gzEartTrVNw4b7

## Why

Last 30 days (ShopifyQL, 23 Sep 2026), sessions that landed on the homepage:

| Referrer | Sessions | Completed checkout | Conversion |
|---|---:|---:|---:|
| Direct | 1,413 | 14 | **0.99%** |
| Search | 311 | 31 | **9.97%** |

Direct landers know the brand but find nowhere obvious to go. The homepage's job is to route them to a product in one tap. The old page opened with a generic line and a wedding button in the Christmas run-up, then a hand-picked "Trending Now" led by a £10.99 tealight holder, a text-only promise slider, one giant tile per screen, and "New Arrivals" wearing green SALE badges.

## What changed, top to bottom (phone)

| # | Section id | Ella section | What it is now | Why |
|---|---|---|---|---|
| 1 | `announcement_bar_a4ALfD` (header group) | announcement-bar | One line: "Free UK delivery over £50". Soft stone bar (`#f3f2ee`) with charcoal text (`#2b2b2b`), 13 px, no close button. | 7 of 9 benchmark stores lead with a promise. The Christmas cut-off line ("Order by … for guaranteed Christmas dispatch") goes back in as a second, rotating line once Max sets the date. Site-wide on this theme. |
| 2 | `image_banner_UJGTQq` | image-banner | **Carousel of two street-sign photos**, fading on its own every few seconds, with dots: 1. the "MR & MRS POTTER" sign at a wedding → **Shop the Mr & Mrs sign**; 2. "THE POTTER FAMILY" sign on a lit mantel → **Shop the family sign**. The words stay the same on both slides: "Handmade to order in Lancashire", headline **"Personalised gifts, handmade to order"**, ★★★★★ Thousands of 5-star reviews, and a small text link **Shop Christmas gifts** (`/collections/christmas`). On phones the text card sits under the photo. On tablets and desktop the photo sits on the left and the words on the right, so the picture changes there too. | The two biggest sellers, which were also #1 and #2 in last year's Christmas quarter. Both photos are the main shots already on their product pages (1,566 and 2,048 px), and each keeps the whole sign inside the crop. Wedding and engagement are the first tiles in the next row. |
| 3 | `spotlight_block_JFKrLj` + `dm_occasion_row_2` | spotlight-block ×2 | **Shop by occasion**: two rows of four, three visible plus a peek, each row swipes. Christmas · Wedding · Engagement · Christening / New home · Anniversary · Teacher · For Mum. | Replaces the one-tile-per-screen "Our Most Cherished Gifts" (same section id, reused). |
| 4 | `product_block_QcxFaJ` | product-block | **Best sellers**: 8 products from the new automated `best-sellers` collection, with prices, no sale badges or struck-through prices, and a "Shop all best sellers" link. | Replaces the hand-picked "Trending Now" (tealight first). Never needs curating. |
| 5 | `16393870238958f868` | custom-service-block | **Proof strip**, 2 × 2 with icons: Thousands of 5-star reviews · Handmade in Lancashire · Made and dispatched in 5–7 working days, express 2–3 · Free UK delivery over £50. | Proof with numbers, no slider. The text-only "Why thousands choose us" (`custom_service_block_jYPjBJ`) is removed. |
| 6 | `dm_christmas_edit` | spotlight-block | **The Christmas edit**, 2 × 2: Christmas street signs · First Christmas hearts · Christmas reed diffuser · Elf arrival postcard. | Replaces "New Arrivals" (`163945138066afddf5`, removed), which showed SALE badges. |
| 7 | `dm_how_it_works` | custom-service-block | **How it works**: 1. Choose the gift · 2. Personalise it and see it live · 3. We make it by hand and dispatch it. Step 2 is a phone screenshot of the live sign preview on the Mr & Mrs page ("MR & MRS TAYLOR" typed in). | The live preview is the differentiator. Built from an existing Ella section (image + title + text), so it needs no new section code. |
| 8 | `dm_reviews` + `17394583817a28cc5e` | customer-review-block + apps (Feefo) | **What our customers say**: three verbatim 5-star reviews with product photos, each linking to its product. The Feefo block sits straight after it. | See "Feefo" below: the Feefo widget renders nothing. Quotes are copied word for word from `snippets/dm-proof.liquid` (harvested 4 Jul 2026 from Trustpilot/Feefo). |
| 9 | `dm_recipient_row_1` + `dm_recipient_row_2` | spotlight-block ×2 | **Shop by recipient**, 3 across: For couples · For Mum · For grandparents / For teachers · For the family · For friends. | Second way in. |
| 10 | `dm_made_in_lancashire` | rich-text | Sage panel, no video: **"Personalised by you. Handmade by us in Lancashire."** plus "Our signs and pebble pictures are made to order in Lancashire. You choose the words, and we make each one by hand, just for you." | Max asked for the low-resolution video to go. The old video section (`video_block_86qWNA`) is disabled and parked at the end of the file, with its placeholder text cleared. |
| 11 | `16378128152fdd5fe7`, `1726396330d08baf63`, `dm_newsletter` | instagram, apps (Instafeed), newsletter | #DaisyMaison unchanged, then an inline sign-up: **"10% off your first order"**. No popup. | Newsletter with an incentive, inline. |
| – | `dm_home_styles` | custom-liquid | A `<style>` block, first in the order, renders nothing visible. | The only new code. See `dm-home-styles.liquid`. |

The six sections that were already disabled (Elfsight, press banner, wedding best sellers, two spare spotlights, "Why's us?") are kept, still disabled, at the end of the file. The video section joins them there.

### Where the build differs from the brief, and why

1. **"column_mb 3" does not exist in Ella.** The setting only accepts 1 or 2, and a spotlight-block holds at most 4 tiles. So the 8 occasion tiles are two spotlight sections of 4, the 6 recipient tiles are two of 3, and a few lines of CSS make them three across.
2. **The "second service block" had no icon images.** All three of its blocks were `icon_type: image` with the image left empty. Content > Files has no suitable icon images (the full library of 3,230 files was checked; the only line icon is a shipping-protection shield). The proof strip therefore uses Ella's other icon option: `icon_type: "text"`, which takes inline SVG. The four simple line icons are star, heart, clock and van.
3. **Feefo cannot show anything.** Feefo's API answers `'Closed' account is not able to interact with the Reviews API` for `daisy-maison`. The on-page widget renders at 0 px on the live homepage today. The two "400 Bad Request" console errors on every page are Feefo. That is why the Feefo block was moved but three real reviews were added above it.
4. **No stars on product cards.** The card template (`product-card-02`) has no rating markup, and Feefo is closed. Stars on cards would need a snippet edit plus a working reviews app.
5. **The workshop video is off the page.** It was "Untitled design (3).mp4" (a Canva export): hands making a pink paper flower with a DM watermark, not signs or pebbles. Max found it low resolution, so the section is disabled. If real workshop footage is shot later, re-enable `video_block_86qWNA` in the theme editor and point it at the new file.
6. **Newsletter wording.** The live welcome discount (`welcome10`, unique codes) gives 10% off **54 named collections**, not the whole order. The heading keeps the brief's "10% off your first order", and the line underneath says "10% off selected ranges".
7. **Sentence case.** The theme capitalises every word of every heading. On the homepage only, headings now show as written ("Best sellers", not "Best Sellers"). Buttons keep the theme's site-wide uppercase style.
8. **Dispatch times appear once**, in the proof strip, as the brief asks. The FAQ says Christmas dispatch "can be up to 7-14 working days", and the free-delivery rate says "3-5 Working day dispatch". The three disagree, so check them before the Christmas cut-off goes up.
9. **Tablets.** The 3-across occasion rows also apply from 768 to 992 px, where Ella would otherwise show a big-tile carousel.

## Max's review (23 Sep) and what changed

| Max said | Done |
|---|---|
| "Handmade to order in Lytham St Annes": change to Lancashire, more broad and recognisable | Hero sub-line, the made-to-order panel heading and text, and how-it-works step 3 all say **Lancashire**. No "Lytham" is left on the page. |
| Announcement bar colours clash; "Order by [date]" looks unfinished | Now one line, "Free UK delivery over £50", in soft stone and charcoal to match the header. The Christmas cut-off line comes back once Max gives the date. |
| The main image is one still image; a swiping carousel of best sellers would look cleaner | The hero is a carousel that fades on its own, with dots you can tap or swipe. Each slide has its own photo on phone and desktop. |
| Get rid of the low-resolution video under "Personalised by you…" | Removed. The words stay, as a plain sage panel. |
| Christmas heart, Mr & Mrs sign, family blossom tree; high quality and proven winners | First pass: star, Mr & Mrs sign, blossom tree (the star replaced the heart on sales). Replaced by the next row. |
| "10,000+ five-star reviews": change to "thousands of 5-star reviews", more truthful with the current review setup | Changed in the hero (both slides) and the proof strip. "10,000" no longer appears on the page. |
| "Make the wedding street sign the 1st image, the other 2 are lowkey chopped" | The Mr & Mrs sign leads. The star and the blossom tree are gone: framed and hand-held products lose their edges in the crop. Slide 2 is the family street sign on a mantel. "Shop Christmas gifts" moved to the small link under the button, so the season is still one tap away. |

Proven winners (ShopifyQL, units sold):

| Product | Evidence | Photo | Source size |
|---|---|---|---|
| Mr & Mrs personalised street sign (slide 1) | #1 product: 5,194 units in the last 12 months (£63k); 690 in Oct–Dec 2025 | `rn-image_picker_lib_temp_58b6d173….png` ("MR & MRS POTTER" at a wedding) | 1,566 px square |
| Family personalised street sign (slide 2) | 1,641 units in the last 12 months (£23k); #2 product in Oct–Dec 2025 with 652 | `hf_20260519_145719….png`, the product's own main photo ("THE POTTER FAMILY" on a mantel) | 2,048 px square |
| Family Blossom Tree pebble picture (dropped) | 670 in 12 months; 356 in Oct–Dec 2025 | `Family_Blossom_Tree_1.jpg` | 1,200 px square |
| Family Festive star (dropped) | The best-selling *Christmas-themed* product, but only 128 in Oct–Dec 2025 | `Large-Star-3.jpg` | 1,200 px square |
| "Our 1st Christmas Together" heart (never used) | 16 in Oct–Dec 2025 | | |

In last year's Christmas quarter, each of the two signs sold about five times as many as the best-selling Christmas-themed product. The Christmas street signs sold 11 or fewer each.

Phones load at most 750 px wide, and desktop shows each photo 585 px wide, so both photos are at least 2× sharp on a retina screen.

## New things on the store (outside the theme)

- **Collection "Best sellers"** (`/collections/best-sellers`, id 699834728787). It is automated, sorted by best-selling, published to the Online Store, and had 588 products on 23 Sep. Its rules include everything except shop plumbing:
  - tags `globo-product-options`, `Add-on`/`add-on`, `internal-add-on`, `internal-offer`, `gift-box`, `elf-upsell`;
  - type containing "Add-on";
  - vendor `EastofIndia` (resale porcelain, which removes all four tealight holders);
  - titles "INCREDIBLE OFFER…", "Large Street Sign", "Shipping Protection", "Gift Wrap", "(+£";
  - anything priced £0.

  Without those rules, Mounting Strips and the size-upgrade helpers would be #2–#4. Shopify's best-selling order is all-time, so today's top 8 is: Mr & Mrs sign, **Valentine's sign**, Family sign, Wedding pebble picture, Mum blossom tree, Dad bar & grill sign, Family blossom tree, Engagement love tree.
- **File** `dm-how-it-works-live-sign-preview.jpg` in Content > Files (the step-2 screenshot).

## Tile map

| Tile | Links to | Image (Content > Files) | Note |
|---|---|---|---|
| Christmas | `christmas` | FullSizeRender_b9407277….heic | |
| Wedding | `wedding-engagement` | Beach-Wedding-Pebble-3.jpg | |
| Engagement | `engagement` | Engagement.jpg | |
| Christening | `christening-new-baby` | Baby-Blue.jpg | |
| New home | `my-home` | New-Home-Christmas.jpg | **No New Home collection exists** |
| Anniversary | `anniversary` | Pink_4f1f5235….jpg | |
| Teacher | `teachers-gifts` | Star-Keyring-BLUE-2.jpg | Collection includes a tealight holder (#2) |
| For Mum (occasion) | `mothers-day` | MUM-NEW-1.jpg | The collection's own image now shows a "NANNY, JACK & CONNOR" sign, so it isn't used |
| Christmas street signs | `christmas-street-signs` | Xmas-Sign-BS-Family.jpg | Collection sorts football stadium signs first |
| First Christmas hearts | `christmas-pebble-hanging-hearts` | 1st-Christmas-as-Mummy-and-Daddy-copy.jpg | **No First Christmas collection**; this one holds 6 of the 13 |
| Christmas reed diffuser | product `personalised-christmas-reed-diffuser-gift` | christmas_reed_diffuser.png | |
| Elf arrival postcard | product `personalised-elf-arrival-postcard-with-optional-elf-toy` | elvie.png | |
| For couples | `anniversary` | Valentines-Heart-Final_80e362b5….jpg | **No couples collection** |
| For Mum (recipient) | `mothers-day` | hf_20260515_132358….png | |
| For grandparents | `christmas-pebble-pictures` | Grandparent-Festive-pebble.jpg | **No grandparents collection**; in-season stand-in |
| For teachers | `teachers-gifts` | Apple-Bookmark-RED.jpg | |
| For the family | `pebble-sketch-pictures` | PERFECTLY-IMPERFECT-SEPT-20_1.jpg | **No family collection** |
| For friends | `friendship-special-occasions` | hf_20260515_134703….png | |

All tile images are square and already on the store; none were generated. Tiles are edited in the theme editor: each tile is a block with its own image, title and link.

## Swapping the seasonal hero

The hero is the first thing to rot, so give it an owner and put the dates below in the calendar.

1. Online Store → Themes → (live theme) → Customize → Home page → **Image banner**. It holds two slides (large image blocks), one per best seller. The season lives in the small link under the button ("Shop Christmas gifts").
2. To change a slide's photo, set **both** the **Image** and the **Mobile image** to the same product photo: square, at least 1,200 px, with the product in the middle third. Phones crop it to 5:4 and desktop to 4:3, so framed or hand-held products lose their edges. Signs and flat products crop well. Don't set a focal point, because that makes the box 20% taller.
3. For the season, change the small link's text and link (**Button 2**) on **every** slide, e.g. "Shop Valentine's gifts". The sub-line and headline are also repeated on each slide, so change them on all of them or the text will jump as it fades. Keep one main button per slide.
4. Swap the four **Christmas edit** tiles for the next season's four, and edit the announcement bar (header → Announcement bar).
5. Calendar:
   - Christmas → last dispatch date
   - → Valentine's (from ~26 Dec)
   - → Mother's Day (from ~15 Feb)
   - → wedding season (from Mother's Day)
   - → Christmas again (mid Sep)

## Measuring

Run in Shopify (Analytics → Reports → new ShopifyQL report, or through the API):

```
FROM sessions SHOW sessions, sessions_that_completed_checkout, conversion_rate
WHERE landing_page_path = '/' GROUP BY referrer_source SINCE -30d UNTIL today ORDER BY sessions DESC
```

- **Before** (30 days to 23 Sep 2026): direct 0.99% (1,413 sessions), search 9.97% (311).
- **After:** run the same query 28 days after publishing, with `SINCE` set to the publish date. The target is the direct number. Anything above **2.5%** pays for the day.
- Christmas lifts every number, so also compare direct against the same weeks last year if you can.

## How to publish (Max)

1. Look at the preview on your phone.
2. Optional: once the Christmas cut-off is set, add it on the copy (Themes → "In construction 🚧" → Customize → Header → Announcement bar → add an announcement: "Order by 〈date〉 for guaranteed Christmas dispatch"). The bar already rotates if it has two lines.
3. **Confirm the 10% welcome code actually reaches people who sign up with this form.** The form creates a customer tagged `newsletter`; the theme sends no code. The code has to come from a Shopify Email or Klaviyo welcome flow. If there is no such flow, change the newsletter heading before publishing. The code (`welcome10`) covers 54 collections, not the whole order.
4. **Check the live theme's "Last saved" time.** The copy was made at 10:43 on 23 Sep. If anything was changed on the live theme after that, publishing the copy would undo it.
   - Checked on 23 Sep at 17:40. Exactly one live file had changed since the copy was made: `locales/en.default.json` at 13:11. It added one checkout string, "Shipping method — estimated delivery dates".
   - That file was copied onto the copy, and the two versions were confirmed identical.
   - If the live theme's "Last saved" is later than 13:11 on 23 Sep when you publish, re-check before publishing, or port the two changed files (`templates/index.json`, `sections/header-group.json`) onto a fresh duplicate instead.
5. Themes → "In construction 🚧" → **Publish**.
6. **Rollback:** the old theme stays in the theme library. Publish it again, or put back `index.before.json` / `header-group.before.json`.

## Files

| File | What |
|---|---|
| `index.json` | The new `templates/index.json`, as uploaded (md5 `4abcc3e8af411ffbe16573b6f384c8ff`, re-read from Shopify after upload) |
| `index.before.json` | The original homepage, byte-exact (md5 `c2b6449ec05ca78c521c11100d140093`, identical on live and copy) |
| `header-group.json` / `header-group.before.json` | Header group with the new announcement bar (md5 `c7f8c852204761835b4bde82125046aa`) / the original as returned by the API |
| `dm-home-styles.liquid` | The one custom-liquid block: homepage-only CSS for the hero card (under the photo on phones, beside it on desktop), sentence-case headings, text link, badges and 2-line card titles, 3-across tiles, 2 × 2 proof strip, how-it-works rows, the made-to-order panel heading and review photos. Several rules target section ids (`16393870238958f868`, `dm_*`, `spotlight_block_JFKrLj`): if one of those sections is deleted and re-added in the theme editor, it gets a new id and its CSS stops applying. |
| `build_index.py`, `build_header_group.py` | Rebuild both JSON files from the originals |
| `validate_template.py` | Checks every setting against the section schemas, plus images, links and block limits |
| `screenshots/` | Phone screenshots of the preview (390 px, 1–6), the hero slides on desktop (7) and the step-2 image |

```
python3 build_index.py && python3 build_header_group.py
python3 validate_template.py index.json --theme-dir <theme>/ --before index.before.json \
  --files files_inventory.json --collections collections.json --products all_products.json
# 1,430 settings checked across 23 sections; 0 errors (23 Sep 2026, after Max's second review)
```

## QA (headless Chromium, 390 × 844, spaced page loads, privacy banner and sticky toolbar removed)

- No horizontal scroll (`scrollWidth` 390; the only off-screen elements are the closed drawers, same as live).
- Every tile and card links to a live collection or product (checked against the Admin API). All 8 best-seller cards show a price and no badges.
- The hero button is not covered and lands on `/collections/christmas`.
- Console errors are identical to the live homepage:
  - a theme `scripts.js` TypeError
  - two Feefo 400s
  - an `en-US@posix` locale warning
  - the same three page errors
- After Max's reviews (v9, md5 `4abcc3e8…`):
  - The carousel starts, has 2 slides and 2 dots, and moves on its own.
  - Slide 1 is the Mr & Mrs sign → `/products/mr-mrs-personalised-street-sign-gift`; slide 2 is the family sign → `/products/family-personalised-street-sign`. The small link on both goes to `/collections/christmas`.
  - Each slide's button fits on one line at 390 px.
  - "Lytham" and "[date]" appear 0 times in the page, and the video section doesn't render.
  - Console errors are still identical to live, and no `503` repeated.
- Desktop at 1440 px: each slide shows its own photo, 585 × 439 px from a 1,152–1,440 px file. It also looks right at 1,024 and 800 px. The page is 10 px wider than the window, but live is too.
- Reviewed by three independent passes (brief, copy and claims, CSS risk) before the PR. Their fixes are in.
- Not verifiable headless: video playback (the test browser has no H.264; the file is valid) and the Instafeed grid, which is empty headless on the live homepage too.
