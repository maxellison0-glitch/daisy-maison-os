# Globo Product Options — removal brief (paste into ChatGPT)

*Prepared 22 Sep 2026 from a full audit of the live storefront payload. The two
CSVs beside this file are the evidence: `globo-audit-option-sets.csv` (all 410
option sets, one decision each) and `globo-audit-products.csv` (all 526 products
Globo currently targets).*

## The numbers behind it

- Every product page ships **~5 MB of HTML**, of which **~4.5 MB is Globo's embedded
  config of ALL 410 option sets** (`window.GPOConfigs.options[...]`), on every page,
  whether or not the product uses Globo. Stripped of that payload the Mr & Mrs page
  is 0.5 MB. On a 95%-mobile store this is the single largest page-weight item.
- Globo targets 526 products: **188 are no longer active**, 7 are Globo's own helper
  add-on products, **142 active products already have a native Daisy builder**
  (Globo is dead weight there), and **189 active products still depend on Globo**
  for their personalisation fields.
- Option sets: **242 can be deleted outright** (every product they target is
  native, inactive, or a helper), **11 need editing** (remove the native products,
  keep the Globo-dependent ones), **149 must stay** for now, **8 target nothing**.
- The 189 Globo-dependent products by family: 63 framed pebble pictures not yet on
  the native pebble builder, 20 A4 prints, 17 teacher items, 16 Christmas hanging
  decorations (incl. the Family Festive pebble star — a top-10 Christmas landing
  page), 14 East of India porcelain, 13 garden/hanging/laser signs, 8 wedding
  stationery boards, 6 pebblescapes, 4 Halloween signs, 28 other.

## Copy from here ↓

---

You are helping the owner of Daisy Maison (daisymaison.co.uk, Shopify, Ella theme
6.6.2, ~95% mobile traffic) retire the **Globo Product Options** app safely.
Background you must respect:

1. Over the last year the store replaced Globo on its best-selling products with
   native, hand-built personalisation builders in the theme (`snippets/dm-*.liquid`,
   `assets/daisy-*.js`). On those pages the native builder hides and ignores
   Globo, but Globo still (a) targets the product with an option set and (b)
   injects its full configuration of all 410 option sets — ~4.5 MB — into every
   page of the site through its theme app embed.
2. Globo is still genuinely needed on 189 active products that have no native
   builder yet. Nothing may break personalisation on those.
3. Orders reference Globo's helper "add-on" products (386 products tagged
   `globo-product-options`, e.g. `option-set-768163-select-2`). Those products
   must never be deleted; they can be archived only after Globo is fully gone.

I am attaching two CSVs:

- `globo-audit-option-sets.csv` — every Globo option set with a decision:
  `DELETE`, `EDIT — remove the native products`, or `KEEP for now`, plus how many
  targeted products are native / Globo-dependent / inactive.
- `globo-audit-products.csv` — every product Globo targets, its state (native
  builder / still depends on Globo / inactive / helper) and which option sets it
  sits in.

Produce, in this order:

**A. A verification pass before anything is touched.** Give me a browser-console
snippet I can paste on any product page that reports: whether a native Daisy
builder is present (look for `.daisy-street-options`, `.dm-cyg`,
`.dm-pebble-picture`, `.dm-heart-options`, `[data-native-legacy-sign]`), whether
Globo rendered any visible fields (`.gpo-form-wrapper`, `.gpo-product-variants`
with children), and the page's HTML transfer size. I will run it on 5 native pages
and 5 Globo-dependent pages and paste the results back to you.

**B. The exact click-by-click procedure in the Globo admin** (Apps → Globo Product
Options → Option sets) for: deleting the 242 `DELETE` sets in batches; editing the
11 `EDIT` sets to remove only the products marked "native Daisy builder — Globo
NOT needed" (list those products by handle for each of the 11 sets from the CSV);
and leaving the 149 `KEEP` sets alone. Tell me what to check after each batch of
~25 deletions: page weight on one native page and one Globo-dependent page, and a
test personalisation on one Globo-dependent product.

**C. A rollback plan.** Globo has no undo for a deleted set, so before batch one
tell me how to export every set (Globo's export, or screenshots of each set's
fields and product targeting) and where to store it in my repo.

**D. The end-state plan.** The remaining 149 sets cover the 189 products listed
in the CSV. Group them into the native builders that would replace them fastest
(the native pebble-picture builder already exists and is config-driven — most of
the 63 framed pebble pictures can be added as config, not code; likewise hearts
and street signs). Order the groups by revenue/traffic impact and give me a
sequence: which family to migrate first, and the point at which the Globo theme
app embed can be switched off and the app uninstalled.

Rules: be decisive, name specific option-set IDs and product handles from the
CSVs, and never propose deleting a set that targets a product marked "still
depends on Globo". If something in the CSVs looks inconsistent, say so and ask
before recommending an action on it.

---
