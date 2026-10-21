# Christmas Gift Wrap Kit on the landing pages

*Decision + implementation record. Written 22 Sep 2026 from live Shopify data.*

## The decision

**Offer both kits, everywhere the classic kit is already offered, as ONE card with a
style choice inside it — never as two separate add-on cards.**

```
┌ Gift Wrap Kit ──────────────────────────────── £5.95 ┐
│ [classic] [xmas]  Paper, twine, ribbon and a gift tag,  │
│  Classic  Christmas  sealed in cellophane and ready to │
│                      use — classic neutrals or festive. │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                  │
│ │ No thanks│ │ Classic  │ │Christmas │                  │
│ │          │ │  £5.95   │ │  £5.95   │                  │
│ └──────────┘ └──────────┘ └──────────┘                  │
└──────────────────────────────────────────────────────────┘
```

Why this shape and not the alternatives:

- **Two cards (one per kit) = two "add wrap?" decisions on a phone.** Every add-on
  on the Mr & Mrs page already uses a single "No thanks / Add · £" row. A second
  wrap card doubles the reading, invites adding both by accident, and makes the
  customer work out the difference from two thumbnails in different rows.
- **Christmas-only during the season loses real orders.** The Mr & Mrs sign is
  46–56% of daily orders and was the #2 product last Oct–Dec (682 orders); the
  wedding flower arch picture was the #6 landing page last Christmas (4,050
  sessions). A wedding or christening gift bought in December wrapped in pine
  and red twine is the wrong gift. Classic must stay available.
- **Classic-only leaves the festive impulse on the table.** Wrap attach has been
  sliding since June: 12.3% of orders in June → 8.7% July → 6.8% Aug → 6.3% Sep.
  A festive kit is the obvious lever to lift it in the one season where most
  parcels are presents. Last Oct–Dec had 3,815 orders; every extra point of
  attach is ~38 kits × £5.95 at near-100% margin.
- **Both styles side by side, before any tap, answers "what are they?"** The two
  thumbnails carry the difference at a glance (ivory tissue + jute vs kraft +
  red twine + pine). Tapping a thumbnail zooms the annotated "what's inside"
  graphic. Choosing a style IS the add — one tap, same as today.
- **Nothing is pre-selected.** Paid extras must be opt-in (Consumer Contracts
  Regulations 2013, reg 40 — pre-ticked add-ons are not consent), and the
  existing cards already work that way.
- **Price parity (£5.95 / £5.95).** Removes a comparison the customer does not
  need to make. If the Christmas kit ever costs more, the buttons show it, but
  keep parity unless there is a margin reason.

Naming: **Classic** and **Christmas**. "Everyday" was rejected — it cheapens a
wedding gift. "Classic" reads as the timeless default and pairs cleanly.

## Where it shows

The classic kit is wired into five different pieces of custom code. The Christmas
option piggybacks on all of them from ONE shared script, so no builder was edited:

| Surface | Builder | How the choice appears | Share of sessions (last 30d) |
|---|---|---|---|
| Mr & Mrs street sign | `snippets/dm-gc.liquid` card + `daisy-street-sign-options.js` | Two thumbnails + Classic / Christmas buttons in the existing card | 30% |
| Pebble pictures (flower arch, love tree, blossom tree, christening…) | `daisy-pebble-picture.js` renders the same card style | Same as above | ~28% |
| Street-sign clones (family, kitchen, retirement, teacher, football, …) | 22 `daisy-*-street-sign.js` builders with a gift-wrap tick box (each sign has its own file; the two football signs key the box on a data attribute) | The tick-box row is hidden and **the identical Mr & Mrs card** is mounted in its place, kept in sync with the hidden tick box. The USA road sign and the vintage train sign never offered a wrap kit, so nothing appears there | ~8% |
| Reed diffusers (4) | `daisy-diffuser-builder.js` extras | Same: the "Add a Gift Wrap Kit" row becomes the card | ~4% |
| Hearts (25 pages) | `daisy-heart-builder.js` | The hearts never carried a wrap-kit extra. `dm-wrap-kits.liquid` now adds the classic Gift Wrap Kit extra to the heart config at page load (a module script that runs before the builder, always on, not just in season), so the heart builder renders its own row and the same card replaces it | ~5% |
| Products still on Globo (Christmas pebble star, A4 prints, …) | Globo checkbox | Classic only — see the Globo brief | ~5% |

One card, everywhere. It was built once for Mr & Mrs and the tick-box pages
mount the same markup, so any later change to the card is a change in one
place. There is no default style: choosing a style IS the add action. On
Christmas products (URL contains christmas / xmas / santa / elf / festive…)
the Christmas thumbnail and button come first; everywhere else Classic does.

## Second kit, half price

Once a kit is chosen the card grows a line: **"Wrapping another present?
Second kit half price · +£2.98 at basket"** with two small chips, Christmas and
Classic. Tapping a chip adds a second kit as its own basket line
(`Add-on: Second gift wrap kit (half price)`), so the customer can mix a
Christmas kit with a Classic one or take two of the same.

The price cut itself is **not** done in the theme. It comes from the automatic
discount **"Second gift wrap kit half price"** (buy 1 of either kit, get 1 of
either kit at 50%, once per order; `gid://shopify/DiscountAutomaticNode/1839836299603`,
live store-wide since 22 Sep). The basket is therefore always right, whatever
path the kits arrive by — including the existing "Two · £11.90" button, which
now reads "Two · £8.93". Turning the offer off is two steps: deactivate that
discount in admin **and** set `"secondKit": false` in `dm-wrap-kits.liquid`.

The classic **Two Kits** variant (£9.99, `XT-300-WK-2`) is what the diffuser
builders send when the second-diffuser offer is on. It is in the discount's
buy/get sets too, so "two kits + a second kit chip" still halves the extra
single. When Christmas is chosen it becomes 2 × the Christmas single (there
is no Christmas two-pack): £8.93 at the basket against the £9.99 the builder
displayed, which is the kinder direction.

Why a second kit rather than a bundle product or a pop-up: it is one tap in the
place the customer is already deciding about wrapping, it needs no new SKU, and
the discount shows on the basket line where they check it.

## The season switch is a product, not code

`snippets/dm-wrap-kits.liquid` only renders the Christmas option while the product
`christmas-gift-wrap-kit` is **Active, published to the Online Store and
purchasable**. Everything (price, name, images) is read live from the two products.

- **Turn on:** product Active (it is, since 22 Sep).
- **Turn off after Christmas:** set the product to Draft. No theme change.
- Recommended go-live: with the mid-October Christmas ad ramp. Until then leave
  the product Active only if you want the option showing from the day the theme
  is published.

## Files (this folder mirrors the theme)

| File | What |
|---|---|
| `theme/snippets/dm-wrap-kits.liquid` | NEW. Outputs `window.DAISY_WRAP_KITS` (both kits: variant id, price, name, thumb, zoom, the classic two-pack id), the CSS, and the script tag — only while the Christmas kit is live. Also, always on: a module script that appends the classic Gift Wrap Kit extra (same JSON the diffuser configs carry) to `[data-daisy-heart-config]` on heart pages, so every heart offers the kit. It no-ops on diffusers, on the elf page, and once the heart configs in `dm-heart-builder.liquid` carry the extra themselves — fold it in there at that file's next edit (250 KB, not worth a blind upload tonight). |
| `theme/assets/daisy-wrap-kits.js` | NEW. The shared card. Family A (dm-cyg cards on Mr & Mrs and the pebble pictures) gets the two thumbnails and Classic / Christmas buttons added to the existing card; choosing a style swaps the card's `data-variant`/`data-price` so the builders' own cart code adds the right product. Families B/C (tick-box rows on the street-sign clones, diffusers and hearts) hide the row and mount the identical card, kept in sync with the hidden tick box; the classic variant id those builders hold is swapped at submit time through three hooks: `DaisyCartSubmit.create().add`, `DaisyNativeStreetSizes.submit/add`, and `window.fetch` for direct `/cart/add.js` posts (JSON, form-encoded and FormData). The same hooks append the half-price second kit line. Hooks are inert unless a choice was made on the page. |
| `theme/snippets/dm-mobile-fixes.liquid` | EDITED. Now renders `dm-wrap-kits` on product pages. Chosen because `layout/theme.liquid` renders it in `<head>` after `daisy-cart-submit.js` and before every builder — the load order the script needs — without re-uploading the 147 KB layout. Move the one-line render into `theme.liquid` next time that file is edited. |

Built on the API duplicate of the live theme, **"In construction 🚧 v2 — Christmas
wrap kit (copy of live 22 Sep)"**, which Max published as the live theme on
22 Sep 2026 at 17:42 UTC. The earlier "In construction 🚧" duplicate is
broken — Shopify refuses to preview it because it has no `layout/theme.liquid`
or `config/settings_schema.json` (43 files instead of ~900). Delete it.

## Product changes made (live store, 22 Sep)

- `Christmas Gift wrap kit` → **Christmas Gift Wrap Kit**; SKU `XT-301-WK-1`
  (classic is `XT-300-WK-1`); description written (kraft paper, red & white
  twine, pine sprig with berries, kraft tag with satin ribbon).
- Variant was **tracked, policy DENY, stock 0 = unbuyable / "sold out"**. Set to
  untracked + continue selling, mirroring the classic Single Kit. Storefront now
  reports `available: true`.

## QA checklist (preview theme, phone width)

1. Mr & Mrs: card shows two thumbnails + No thanks / Classic / Christmas. Tap
   Christmas → card highlights, name reads "Gift Wrap Kit · Christmas", subtotal
   row says Christmas Gift Wrap Kit, sticky total unchanged (same price). Add to
   basket → basket line is **Christmas Gift Wrap Kit** with `_Linked product`.
2. Second-sign offer ticked → "Two · £11.90" still appears and adds 2 of the
   chosen style.
3. Pebble picture (e.g. wedding flower arch): same card behaviour; second frame
   → "Two wraps" still works.
4. Family street sign: the add-ons list shows the same card as Mr & Mrs (old
   tick-box row hidden). Tap Christmas → total rises by £5.95; basket line is
   the Christmas kit at £5.95 with `_Linked product` / `_Bundle ID`.
5. Diffuser: the "Add a Gift Wrap Kit" extra is the same card; basket line
   correct.
6. Second kit: after choosing a style, the "Second kit half price" chips
   appear; tap Classic → basket has two kit lines and the automatic discount
   takes £2.97–£2.98 off the second. Tap "No thanks" → chips disappear and the
   second kit is dropped.
7. Set the Christmas product to Draft → every page reverts to today's single
   classic control with no console errors.

## Elf Arrival Postcard landing page (added 22 Sep on request)

`theme/sections/dm-elf-landing.liquid` — the elf page is its own section with a
"Build the set" list (plush elf, pyjamas, report sheets). A fourth row,
**Christmas Gift Wrap Kit +£5.95**, now sits in that list in the same pattern:
tick to add, and when the sibling offer is on it shows "Just one · £5.95 /
One each · £8.93 (2nd half price)" — two kits on one line, halved by the same
automatic discount. Variant id, price and thumbnail are read live from the
product, and the row only renders while the kit is active + purchasable, so
the same Draft switch turns it off. Cart line carries `Add-on: Christmas Gift
Wrap Kit`. Christmas kit only on this page — it is a Christmas product. The
checkbox deliberately has no `gift-wrap` name, so the shared script leaves it
alone.

## Follow-ups (not done here)

- **Hearts:** the wrap-kit extra is injected at page load by
  `dm-wrap-kits.liquid` (see the files table). Move it into the heart configs
  in `dm-heart-builder.liquid` at that file's next edit; the injection then
  becomes a no-op and can be deleted.
- **The legacy Christmas street signs** (Family Sleigh, Santa Stop Here, …) use the
  inline builder in `theme.liquid` and offer strips but no wrap. Same gap. Same
  for the USA road sign and the vintage train sign builders.
- **Cart page "finish" upsells** (`dm-cart-upsells.liquid`) and the checkout
  "Useful Extras" still push the classic kit only. Fine for now; a seasonal swap
  there is a small follow-up.
- **Upsell tracker:** add "Christmas Gift Wrap Kit" to the core upsell list in
  `operating systems/context.md` on the day it goes live so the digest counts it.
- **Two Kits £9.99 variant** of the classic kit has never sold through any
  builder (all paths add 2 × Single). Either retire it or wire it to the
  "Two" button — not worth the code before Q4.
