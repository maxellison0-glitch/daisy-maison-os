# Daisy Maison price and landing-page review — 3 Oct 2026

**Preview only. Max publishes theme 208326623571.** Current live theme is 208291496275.

- [Read the audit, traffic priorities and price decisions](../../operating%20systems/price-audit-2026-10-03.md).
- [Open all five before/after screenshot pairs](screenshots/index.html).
- [Review the actual theme patch](draft-theme.patch): 14 files, **281 added / 16 removed lines** against the downloaded live baseline. Catalogue inventories are evidence, not theme code changes.
- [Download the 14 uploaded source files](draft-theme-files.zip). Extract into this directory to create `theme-changes/`.

The five pages are Mr & Mrs, Engagement Love Tree, Family, Create Your Own and Wedding Flower Arch. They accounted for 407 landing sessions / 30 orders in the handoff's 1–2 Oct window. Each draft page has one relevant optional add-on. Secondary offers move to basket; reviews and delivery remain.

## Verification

All 14 uploaded draft file bodies match the local changes. All 959 final selling prices and compare-at values match the starting catalogue. A transient Globo save side effect on Robin was caught and restored; see the audit, rather than treating all app saves as label-only operations.

`screenshots/cart-test-results.json` records eight successful browser cart/checkout cases. Fake QA personalisation was used, baskets were cleared and no order placed. Aftersell's relevant editor preview was checked without saving. Its existing A/B test remains active.

After extracting the source archive:

```powershell
node price-model.test.cjs
node cart-extra-gifts.test.cjs
```

The price-model checks cover full selected prices, genuine comparison prices, quantities and independently changing second-sign prices. Basket checks cover parent linkage, personalisation and locking retries when a response is uncertain. The final transport-only change was checked locally after the isolated browser session closed; the eight recorded browser cases preceded that substitution.

`validation-scoped.txt` records validation of all 14 files. `validation-final-cart.txt` validates the last cart-JS revision. `validation.txt` records inherited baseline failures. Scoped validation used the full downloaded theme and its fonts, with only this local override:

```yaml
extends: theme-check:recommended
ParserBlockingScript:
  enabled: false
```

That suppression is for three unchanged legacy scripts; it is not deployed theme configuration. Other inherited warnings remain in the validator output.

## Package boundaries

The full live-theme download, validation copy and intermediate generator data are local working material and excluded from Git. The large raw catalogue/metafield/manifests are compressed into `operating systems/price-audit-2026-10-03/catalogue-metadata-evidence.zip`. Human-readable CSVs list the variants, theme price references and Globo options. Correction JSON files preserve exact original/new labels.

No automatic publication or ongoing monitor is configured. Start performance comparison from Max's actual publication timestamp, accounting for Aftersell's existing split and traffic mix.
