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
| Street-sign clones (family, kitchen, retirement, teacher, …) | ~23 `daisy-*-street-sign.js` files, checkbox row | "Choose your kit" row with both thumbnails appears under the ticked row | ~8% |
| Reed diffusers (4) | `daisy-diffuser-builder.js` extras | Same "Choose your kit" row | ~4% |
| Hearts | `daisy-heart-builder.js` | **No wrap kit offered today at all** — see follow-ups | ~5% |
| Products still on Globo (Christmas pebble star, A4 prints, …) | Globo checkbox | Classic only — see the Globo brief | ~5% |

For the checkbox rows the default is **Classic** (the safe kit for a wedding or
christening); the Christmas card sits right beside it. For the card surfaces
there is no default because choosing a style is the add action.

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
| `theme/snippets/dm-wrap-kits.liquid` | NEW. Outputs `window.DAISY_WRAP_KITS` (both kits: variant id, price, name, thumb, zoom), the CSS, and the script tag — only while the Christmas kit is live. |
| `theme/assets/daisy-wrap-kits.js` | NEW. The shared style toggle. Family A (dm-cyg cards) swaps the card's `data-variant`/`data-price` so the builders' own cart code adds the right product. Families B/C (checkbox rows) swap the classic variant id at submit time through three hooks: `DaisyCartSubmit.create().add`, `DaisyNativeStreetSizes.submit/add`, and `window.fetch` for direct `/cart/add.js` posts. Hooks are inert unless a style row exists on the page and Christmas is chosen. |
| `theme/snippets/dm-mobile-fixes.liquid` | EDITED. Now renders `dm-wrap-kits` on product pages. Chosen because `layout/theme.liquid` renders it in `<head>` after `daisy-cart-submit.js` and before every builder — the load order the script needs — without re-uploading the 147 KB layout. Move the one-line render into `theme.liquid` next time that file is edited. |

Uploaded to the API duplicate of the live theme: **"In construction 🚧 v2 — Christmas
wrap kit (copy of live 22 Sep)"**. The earlier "In construction 🚧" duplicate is
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
4. Family street sign: tick Gift Wrap Kit → "Choose your kit" row appears;
   choose Christmas → basket line is the Christmas kit at £5.95.
5. Diffuser: tick "Add a Gift Wrap Kit" → row appears; basket line correct.
6. Set the Christmas product to Draft → every page reverts to today's single
   classic control with no console errors.

## Follow-ups (not done here)

- **Hearts offer no wrap kit at all** (`dm-heart-builder.liquid` has `extras`
  only on the remembrance heart). The First Christmas hearts were the #11
  landing page this month and Christmas hearts sold 120+ units last Q4. Add the
  Gift Wrap Kit extra to the heart configs (the diffuser configs show the exact
  JSON) and the Christmas toggle appears automatically.
- **The legacy Christmas street signs** (Family Sleigh, Santa Stop Here, …) use the
  inline builder in `theme.liquid` and offer strips but no wrap. Same gap.
- **Cart page "finish" upsells** (`dm-cart-upsells.liquid`) and the checkout
  "Useful Extras" still push the classic kit only. Fine for now; a seasonal swap
  there is a small follow-up.
- **Upsell tracker:** add "Christmas Gift Wrap Kit" to the core upsell list in
  `operating systems/context.md` on the day it goes live so the digest counts it.
- **Two Kits £9.99 variant** of the classic kit has never sold through any
  builder (all paths add 2 × Single). Either retire it or wire it to the
  "Two" button — not worth the code before Q4.
