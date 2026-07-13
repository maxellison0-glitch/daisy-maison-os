# AGENT HANDOFF — Daisy Production Lab v0 (for Codex review)

**Date:** 2026-07-13
**Author:** Claude (at Max's request)
**Status:** Working prototype, self-contained, NOT wired to any live system.
**Ask:** Please review the engineering — correctness of the four core modules, the
validation logic, and the SVG export contract. This is a proof-of-concept, so
also flag anything that would block turning it into a real production step later.

---

## What this is

A single-file offline tool that turns one (fake) Shopify order for the
**Personalised Mr & Mrs Street Sign** into a validated, downloadable **PREVIEW
SVG** of the sign artwork. It is an engineering experiment only — it deliberately
does **not** connect to Shopify, Photoshop, a printer, or any production system.
There is a visible human-approval gate; output is never labelled print-ready.

## Files

| File | Purpose |
|------|---------|
| `daisy-production-lab-v0.html` | The entire prototype — HTML + CSS + JS, zero dependencies. Open in any browser. |
| `verify.js` | Node harness. Runs the REAL script from the HTML with a stubbed text-measurer and asserts structure/escaping/normalisation/verdict. `cd production-lab && node verify.js` → currently 35/35 pass. |
| `HANDOFF-codex-review.md` | This note. |

## Real product context baked into `CONFIG`

- Product: Personalised Mr & Mrs Street Sign — handle `mr-mrs-personalised-street-sign-gift`
- GID `gid://shopify/Product/9702132711763`, base SKU `36961`
- Line 1 required, Line 2 optional, both ≤75 chars
- Sizes → viewBox aspect: Small `280:120`, Medium `450:120`, Large `570:120` (10 user units = 1 cm, so **1 user unit = 1 mm**)
- Storefront normalisation mirrored: uppercase + standalone `AND` → `&`
- Storefront font stack mirrored: `'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif`, weight 400, letter-spacing `0.06em`
- Palette: `#B0AF9B` sage, `#1C1C1A` charcoal, white, signature red `#C0392B`

## Module map (all inside the single `<script>` in the HTML, marked `[A]`–`[E]`)

- **`[A] CONFIG`** — product IDs, sizes/viewBoxes, palette, geometry, per-line fit bounds, and the two `SAMPLES` (good + deliberately overlong).
- **`[B] TEXT + VALIDATION`** — `normalizeText()` (uppercase, `\bAND\b`→`&`, space-collapse), `escapeXML()`, control-char + emoji regexes, `analyzeChars()`, and `validate()` → check list + `PASS`/`REVIEW`.
- **`[C] TEXT FITTING`** — `measureWidth()` uses a real off-screen SVG `<text>` + `getComputedTextLength()` (so `0.06em` tracking is counted); `fitFontSize()` steps size down to a floor and never scales glyphs. Reports fitted size + spare width.
- **`[D] SVG TEMPLATE`** — `buildSVG()`, a pure string builder. Stable IDs `outer-plate · inset-panel · mounting-holes · line-1 · signature-heart · line-2`, plus a `<metadata>` block (order #, handle, GID, SKU, size, viewBox, raw + rendered inputs, font sizes, ISO timestamp, `status=PREVIEW`). Same builder drives preview AND download, so they cannot drift.
- **`[E] EXPORT + WIRING`** — `download()` (Blob → `.svg`, `<?xml?>` prolog, physical `cm` width/height, filename `daisy-preview_<order>_<size>_<stamp>.svg`) and the live event wiring.

## Engineering rules honoured (checklist to verify)

- [x] viewBox changes with physical aspect per size
- [x] Explicit artwork group IDs (listed above)
- [x] All user text passes `escapeXML()` before entering the SVG
- [x] Line 1 required; Line 2 optional
- [x] Normalise uppercase + standalone `AND` → `&`
- [x] Warn on control chars / emoji / text that cannot fit safely
- [x] Fit by measuring rendered width, reduce font within a min, never stretch glyphs
- [x] Show calculated font size + remaining safe width
- [x] Download contains exact current input values + metadata (order, handle, SKU, size, timestamp)
- [x] Human approval gate visible; output called PREVIEW SVG, never print-ready
- [x] No added dependencies

## How to run / review

1. Open `daisy-production-lab-v0.html` in a browser. It boots on sample `TEST-001`.
2. Click **Load deliberately-overlong sample** to see the `REVIEW` state (line 2 > 75 → warn; both lines overflow at min font → fail).
3. Click **Download PREVIEW SVG**, open the file independently — confirm the grouped elements and `<metadata>`.
4. Re-run the harness: `cd production-lab && node verify.js` (Node only; no npm install).

## Verification already done

- `node verify.js` → 35/35 (normalisation, all group IDs, viewBox per size, metadata fields, `&`→`&amp;` escaping, a `<script>`-injection probe, PASS on good sample, REVIEW + overflow on overlong, empty-line-1 → REVIEW).
- Both exported SVGs re-parsed clean in a real XML parser (Python minidom); all IDs + metadata present.
- Geometry checked numerically: panel inside plate, mounting holes in the charcoal border, signature heart nestled over the ampersand inside the white panel.

## Known limitations / open questions for review

1. **Text measurement uses live browser fonts.** `verify.js` stubs the measurer (0.55·fs/char), so the fitted font sizes it prints are approximate — real fitting only happens in-browser. A headless/CI check of exact fitting would need a real rendering engine (Playwright/puppeteer) — not added to keep it dependency-free. Worth deciding if CI fitting matters.
2. **Heart placement** is measured relative to the first `&` in line 1; if there is no ampersand it falls back to a centred top accent. Confirm the design intent for no-`&` orders.
3. **75-char limit** is treated as a soft `warn` (over-limit) rather than a hard block, since the brief said the storefront "currently" allows 75. Confirm whether over-limit should hard-fail.
4. **Corner/ornament styling** is a chamfered octagon + inner keyline approximation of the reference photo, not a traced match. If the real plate has a specific ornamental corner profile, `chamferRectPath()` / the keyline in `[D]` is the one place to change it.
5. **No fonts embedded.** The SVG references the Palatino stack by name; a machine without Palatino renders a fallback serif. For true print fidelity a later version should embed/outline the font — intentionally out of scope for v0.
6. Not wired to Shopify order lookup — order number is free-text. The `[A] CONFIG.product` block + a fetch would be the integration seam.
