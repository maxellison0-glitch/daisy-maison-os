# Tracker Change Log

Use this file to record stock-tracker rule changes so Claude and Codex stay aligned.

## 2026-07-09

- Created shared tracker context folder.
- Added packaging rules from Codex stock reference.
- Confirmed small street signs use larger Mail Lite envelopes.
- Confirmed East of India matchboxes fit D/1.
- Confirmed East of India tealights: up to 2 fit D/1.
- Confirmed small pebble hearts fit D/1 and should not be treated as framed pebble pictures.
- Created placeholder files for exact Claude and Etsy prompts.
- Added easier envelope wording: Small / Medium / Large envelope settings, mapped to D/1, F/3, and H/5 supplier codes.
- Imported exact Claude `daisy-maison-stock-report` prompt into `claude-current-prompt.md`.
- Created Codex takeover prompt for East of India stock reporting.
- Created `east-of-india-stock-state.md` as Codex persistent state for Etsy tracking and special cases.
- Created active Codex automation `daisy-maison-east-of-india-stock-report`, scheduled daily at 7:00am Europe/London.

## 2026-07-10

- Added working Daisy delivery pricing for Standard, DPD ship-to-shop 24-hour,
  DPD Express next-day, and DPD Super home 24-hour options.
- Kept VAT, insurance, the spoken `0.6` adjustment, and the prior GBP 3.94 /
  approximately GBP 0.80 Express wording explicitly as unresolved assumptions.
- Added photo-confirmed DPD pricing and corrected Super from the earlier spoken
  GBP 9.99 / GBP 3.70 figure to the written GBP 9.95 / GBP 3.66 figure.
- Added Highland and Islands Royal Mail 48HR conditional Letter, Frame, and
  Sign pricing from the handwritten reference; the extra GBP 8.95 Letter note
  remains explicitly ambiguous.

## 2026-07-15

- Consolidated the proposed stock work into one active Codex automation. The
  legacy ID remains `daisy-maison-east-of-india-stock-report`, but the in-app
  name and prompt now run the unified Daisy Maison stock tracker.
- Paused the old packaging-only automation
  `daisy-maison-packaging-stock-usage-daily-report` so the stock workflow does
  not run twice.
- Added `reports/daisymaison-stock-tracker-project.md` as the single control
  file for East of India/accessory stock, packaging usage, Amazon Gmail stock
  evidence, and future Etsy/manual coverage.
- Removed the separate Amazon project lane so Amazon is a section/reference
  inside the unified daily tracker, not another scheduled automation.

## 2026-07-16

- Added Max-supplied East of India invoice evidence dated 2026-07-14, invoice 14044-82: Matchbox-Seal (5), supplier code 1568 line (20), Matchbox-Thanks teacher (25), and Handled tea light holder-Thank you (70).
- Applied the East of India invoice quantities to Shopify with compare-and-set checks and reason `received`: Seal 1→6, Lucky Sixpence 36→56, Teacher Star 4→29, and Teacher Tea Light -3→67.
- Added Macfarlane Packaging delivery note 10073374 / order 6277938: 300 custom boxes delivered, 150 corrugated sheets delivered, 1 Guardian paper roll delivered, and 1 Guardian roll still to follow. These are receipt counters, not total on-hand stock.
- Max clarified the standing rule: a clear physical invoice or delivery note shown in a photo means the goods were delivered just now. Automatically apply legible receipt quantities, record the document reference and Europe/London processing timestamp, and use safe SKU mapping/compare-and-set checks.
- Rule recorded at 2026-07-16 11:37:09 +01:00 Europe/London.
- Max requested a clearer report layout: East of India run-outs first, Amazon stock watch second, Accessories third, and Packaging usage/order list fourth; removed the standalone Critical reorder actions presentation.
- Amazon watch policy clarified: retain relevant upsell and operational products until delivery is confirmed, then transfer them to the owning stock tracker.
- Max corrected Thermal Labels to one remaining roll of 250 labels. Reset the manual baseline to 250 on 2026-07-16; usage tracking restarts 2026-07-17 and the prior 30-label estimate is superseded.

## 2026-07-20

- Max clarified that when Amazon orders are confirmed delivered, the stock
  tracker should update automatically rather than only holding the fact in
  MaxOS/email context.
- Added explicit Amazon delivery-confirmation rule: delivered Amazon items move
  into the relevant stock owner as receipt evidence, with delivered pack/unit
  quantity where known.
- Delivery confirmation still does not prove current remaining on-hand after
  possible same-day use, and does not authorize Shopify inventory mutation unless
  the SKU/variant mapping and compare-and-set received update are explicitly
  safe.
- Corrected the 2026-07-20 Amazon receipt handling for order
  `206-3457020-8782768`: the delivered email visibly includes L LIKED thermal
  labels and Ormith 48-piece mounting pads as well as wood easels. These must be
  recorded as receipt evidence, not omitted because they were missing from the
  previous Amazon reference file.
- Max corrected the L LIKED thermal labels pack basis: the delivered unit is a
  pack of 2 rolls, 250 labels per roll, so receipt evidence is 500 labels total.
- Max confirmed the mounting-strip usage rule: one single mounting-strip order
  uses 2 physical pads/strips and one double/two-sign mounting-strip order uses
  4 physical pads/strips. The delivered Ormith 48-piece pack therefore covers
  24 single mounting-strip orders or 12 double/two-sign orders.
