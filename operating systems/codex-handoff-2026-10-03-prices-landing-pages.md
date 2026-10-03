# Codex handoff — 3 Oct 2026: price mismatches + cluttered landing pages

Paste everything below the line into Codex.

---

You are working on Daisy Maison UK, a Shopify store (`daisymaisonuk.myshopify.com`, GBP). Context lives in the `daisy-maison-os` repo. Read `operating systems/context.md`, especially "Site Changes", "UPSELL DROP" and "Open Decisions", and `operating systems/learnings.md`. Never read, print or commit tokens, `.env` files or customer data.

## The problem, in Max's words

"I'm changing prices and they're not accurately changing everywhere. Displayed prices are different to actual prices. Upsells are priced wrong. The website's getting scrappy and messy." He also says this week's landing-page work has crammed too many upsells onto the pages, upsells have stopped selling, and the pages should be frictionless for what actually sells.

## The data (Shopify, pulled 3 Oct)

- **Upsell take rate** (orders that included the add-on ÷ all orders):

  | Add-on | July | w/c 21 Sep | w/c 28 Sep |
  |---|---|---|---|
  | Mounting Strips | ~15% | 20.3% (best week) | 14.8% |
  | Easel | ~10% | 15.1% | 8.7% |
  | Gift Wrap | ~8% | 8.5% | 5.1% |

  Fri 2 Oct was the first day with zero Easel and zero Gift Wrap, on 19 street-sign orders. Easel still sold 7 on Thu 1 Oct. So the drop is this week, and it lines up with this week's landing-page changes.
- Funnel on Fri 2 Oct: checkout abandonment 44.9% (normally ~25%), and conversion 3.28% (lowest of the run).
- Pages that sell (sessions landing 1–2 Oct → orders): Mr & Mrs Street Sign 190 → 17; Engagement Love Tree pebble 52 → 5; Family Street Sign 65 → 3; Create Your Own sign 34 → 2; Wedding Flower Arch pebble 66 → 3.

## Price oddities already spotted (verify, don't assume)

- Grandparent Garden sign Small is £11.25 (Medium £17.24, Large £20.24). It looks like a stray discount, not a set price.
- Compare-at ("was") prices sit only on Small variants (e.g. Family sign Small £14.95 was £28.95; Medium/Large have none). That's inconsistent.
- Create Your Own sign: Medium is now £22.94 and Large £25.94, but on 2 Oct a Medium sold at £24.94. Check whether this was a deliberate change and whether every page and app shows the new price.
- The "2nd sign for £9.95" offer: a Large line sold at £18.94, not £9.95.
- History: add-on apps (Globo / Candy Rack) and theme blocks have shown hardcoded price labels that didn't match the real price before (the Mounting Strips label bug, 4 Jul). Add-on titles also carry prices in the name, e.g. "(£1.99) Mounting Strips" and "(+£3) Large Heart".

## Job 1 — Price audit, then fix

1. List every active product and variant with: price, compare-at price, any price written in the title, and any price hardcoded in the theme, sections, snippets, app blocks (Globo, Candy Rack or others), metafields, checkout extras and collection badges.
2. Flag every mismatch: title vs real price, theme or app label vs real price, compare-at lower than or equal to price, odd non-standard prices (like £11.25), and add-ons priced differently in different places.
3. **Fix clear mismatches directly**, where the displayed label is wrong and the real price is obviously the intended one. **Ask Max before changing any real selling price.** List those as questions.
4. Save the audit as `operating systems/price-audit-2026-10-03.md` (table: product | where | shows | actual | fixed? ).

## Job 2 — Declutter the landing pages

1. Pull the live theme. List every change made to product and landing-page templates from 28 Sep to 3 Oct (theme versions, git history, app blocks added).
2. Check the top 5 selling product pages above, on mobile first. Count the add-on blocks, check for anything broken or duplicated, check the add-ons actually add to cart at the right price, and check the path to the main Add to Cart button.
3. Compare against 2–3 strong UK personalised-gift competitors (e.g. Not On The High Street listings, Etsy top sellers). How many add-ons do they show on the product page, and where?
4. Build a cleaner version on a **duplicate theme, not the live one**. The product page should cover the product, personalisation, size, price and Add to Cart, plus at most ONE relevant add-on (strips for wall signs, easel for pebbles). Move the rest to cart/checkout, where they sold fine through the summer. Keep reviews and delivery info.
5. Give Max a preview link plus a before/after screenshot of each of the top 5 pages. Max publishes it himself.

## Done means

- The price audit file is in the repo, clear label errors are fixed, and the price questions are listed for Max.
- A decluttered duplicate theme is ready to preview, with before/after screenshots.
- A dated entry for each change is in `operating systems/site-change-log.md`, so the morning digest can measure the upsell take rate before vs after.
- Commit and push to `main` in `daisy-maison-os`.
