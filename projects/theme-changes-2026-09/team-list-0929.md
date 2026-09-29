# Team list, 29 Sep 2026: bolder Add to Cart, bigger menu type, add-on accordion, mobile parallax

**Status:** built and tested on Max's new draft **"RDD Copy of Copy of constructed 🚧"** (id 208036757843). Not published. Max publishes.

This is the list from the team meeting:

> Add to cart button needs to stand out, make text bolder / Increase fonts on the menu / Accordion menu for upsells as too many currently showing on landing pages / Carousel images keep showing when scrolling on mobile, parallax fixes that

Three files changed on the draft for the team list. Before each write I re-checked that the draft's copy still matched what I had fetched, so none of the team's edits were overwritten. The full change is in `team-list-0929.diff`. The gift wrap fix further down changes two more files.

| File | Change | md5 after |
|---|---|---|
| `assets/custom.css` | New block at the end: bolder, bigger Add to Cart, plus bigger menu type. Later on 29 Sep it also gained green ticks on chosen add-on buttons. | `29f4b332…` |
| `snippets/dm-upsell-accordion.liquid` | New file: the add-on accordion (styles and script together). | `12220e70…` |
| `layout/theme.liquid` | One line renders the accordion on product pages, just after `dm-proof`. | `c4ea2041…` |

## 1. Add to Cart stands out

It's the same sage pill with ink text, so it stays on brand. Ink on sage is about 6:1 contrast, which is already readable, so weight and size carry the change:

| | Before | After |
|---|---|---|
| Theme / builder button | 16px, weight 500, 40px tall | 17px, weight 800, 54px tall, deeper shadow |
| Mr & Mrs button | 15px, 700 (set by `daisy-product-poc.css`) | 17px, 800 |
| Mr & Mrs sticky bar | 14px, 700 | 14px, 800 |
| Soap / bath bomb picker button | 15px, 700 | 16px, 800, 54px tall |

`daisy-product-poc.css` styles the Mr & Mrs button with a (0,3,3) selector, so custom.css adds a heavier selector for builder pages. If the team wants it to pop even more, the next step is a dark ink button with white text. That's a one-line colour change.

## 2. Bigger menu type

| | Before | After |
|---|---|---|
| Desktop top bar | 16px / 500 | 18px / 600 (all six items still on one row, ending at 1,102px on a 1,366px screen) |
| Desktop drop-downs (level 2 / 3) | 16px | 17px / 16px |
| Mobile burger, top level | 15px / 700 | 17px / 700 |
| Mobile burger, sub-menus | theme default | 16px |

This is done in CSS rather than theme settings, because the mobile drawer has no size setting of its own.

## 3. Add-on accordion

Every add-on card is now a one-line row showing its name, price and thumbnail. It covers every builder's `.dm-cyg__card` (gift box, Gift Wrap Kit, mounting strips, easel, matching heart and so on) and the diffusers' "Fancy another look?". Tapping a row opens it, and tapping its header closes it again.

- A row starts closed unless something in it is already chosen.
- Once something is picked, the header shows **✓ Added**, so a closed row still tells the customer what's in the basket.
- Pressing Add to Cart opens every chosen row first. Any wording a builder asks for, such as the extra tag or the matching heart, is then on screen if validation needs it.
- The thumbnail still opens the zoom lightbox.
- The diffusers' "Buying another gift?" was already a drop-down, so it's only restyled to match.
- The "Incredible offer" second-item row is a single line already, so it's left as is.

**How it works:** nothing is moved or re-rendered, so the builders are untouched. Each card's own header becomes the toggle, everything else in the card is marked, and CSS hides the marked parts while the row is closed. Hidden fields still submit. Content a builder draws later, such as the wrap-kit colour tiles, is caught by a watcher on each row.

**One trade-off to flag:** the five Gift Wrap Kit colour tiles are now one tap away rather than always showing. That's what the team asked for. If Max wants the wrap tiles to stay visible, the fix is a one-line exception in the snippet.

## 4. Mobile parallax: left as the team set it (off)

I misread this one at first. Live has "Enable Parallax for Mobile?" **on**, and the pinned gallery is what keeps showing while you scroll. The team had already switched it **off** on this draft at 12:51 to fix that. I briefly switched it back on, then restored the team's `templates/product.json` byte for byte (md5 `3414c841…` locally), so the draft is back to off. The phone test confirmed the parallax class is gone.

Width check, after Max asked whether the Mr & Mrs page got narrower: it didn't. The draft and live measure the same on a 390px phone, where the content is 370px, and on a 1,440px desktop, where the page is 1,170px, the gallery 655px and the builder 412px. Parallax on or off doesn't change the width either.

## Tested on the draft preview (390px phone, headless; one load per 5 minutes)

- **Mr & Mrs:** four add-on rows start closed at 70px each (they were 148–274px). Tapping "Wooden Display Easel" opens it, and "Add an easel" shows ✓ Added. Closing the row keeps ✓ Added. With the sign filled in, Add to Cart gave a basket of 1× sign £11.25 + 1× easel £5.95 = **£17.20**. No script errors.
- **Family Reed Diffuser:** the Fancy another look?, Gift Box and Gift Wrap Kit rows all start closed. Gift Box, then "1 gift box", shows ✓ Added. Basket: 1× diffuser £14.95 + 1× gift box £5.95 = **£20.90**. No script errors. Add to Cart moved from 2,643px down the page to 1,966px.
- **Desktop 1,366px:** menu 18px/600 on one row. Add to Cart 17px/800, 54px. The parallax class is on the product page.

## 5. Gift wrap: the second kit now shows in the price (29 Sep, Max's screenshots)

Max's screenshots showed two problems, and both were live as well as on the draft:
- Christmas was picked, but the page summary said "Gift Wrap Kit – Ivory & Twine".
- Picking a half-price second kit left the total unchanged, at £17.20.

The basket was always right, because the kit colour and the second kit are swapped in when the order is posted. Only the page's running total was wrong.

| File | Change | md5 after |
|---|---|---|
| `assets/daisy-wrap-kits.js` | Picking a colour, or picking or removing a second kit, now redraws the Mr & Mrs summary, so it names the colour picked. The second kit is added to every total on the page: the Mr & Mrs summary gets its own green row, and the sticky bar and the heart/diffuser total get it too. Each total keeps the builder's own figure and adds the kit on top, so builder recalculations never double-count. | `60f827cc…` |
| `snippets/dm-wrap-kits.liquid` | The offer becomes a green panel with a HALF PRICE tag: "Wrapping another gift? Add a second kit for just ~~£5.95~~ **£2.98**, any colour." Picking a kit changes the line underneath to "✓ Second kit added: Blush for £2.98. Tap it again to remove." The chosen colour and the chosen second kit get a green tick badge. | `040dd401…` |
| `assets/custom.css` | A green ✓ on whichever add-on button is on (Add gift wrap kit, Add an easel, Add heart…). "No thanks" never gets one. | `29f4b332…` |

The full change is in `wrap-kit-total-0929.diff`.

**Tested on the draft preview (390px phone):**
- **Mr & Mrs:** after picking Christmas, the summary shows "Gift Wrap Kit – Christmas £5.95" and the total is £17.20. With a Blush second kit it shows "Second gift wrap kit · Blush (half price) £2.98", and the summary and sticky bar both read **£20.18**. Removing the second kit takes it back to £17.20, and adding it again brings back £20.18. The basket was sign £11.25 + Christmas kit £5.95 + Blush kit £2.98 (automatic discount), total **£20.18**, the same as the page.
- **Family Reed Diffuser:** with the Christmas kit the total is £20.90, and with a Blush second kit £23.88. The basket came to **£23.88**, the same as the page.
- No script errors on either page.
