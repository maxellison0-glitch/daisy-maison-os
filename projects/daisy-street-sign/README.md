# Daisy Mr & Mrs Street-Sign Artwork

This is the single canonical engineering project for the Daisy Maison Mr & Mrs
street-sign artwork. Do not create another copy in MaxOS, Gym, or an
agent-specific folder.

## Canonical Location

`%USERPROFILE%\AA Daisy Maison OS\projects\daisy-street-sign`

The single copy-pasteable Jarvis entry is:

`%USERPROFILE%\AA Daisy Maison OS\workflows\starred\daisy-street-sign-automation.md`

Jarvis indexes that workflow, not every engineering file in this folder.

The active generator and its only live outputs are in `artwork/`:

- `build.py` - order/text to standalone SVG generator
- `mr-mrs-large-preview.svg/.png/.pdf` - current approved visual sample
- `orders/` - generated order previews
- `assets/` - the real heart and source Times font assets
- `verify-heart-placement.py` - geometry and font-separation fixtures

`source/` is a required evidence component, not a second artwork copy. It
contains the audited LightBurn/PSD geometry consumed by `artwork/build.py` and
the script that can rebuild that data. `references/` contains the original
visual evidence.

Obsolete prototypes, experiments, and agent handoffs are intentionally absent.
They remain recoverable from Git history.

## Approved Visual Rule

- Top name: Times New Roman regular, weight 400
- Bottom subtitle: Times New Roman regular, weight 400; smaller than line one but not bold
- Heart and ampersand: one locked signature unit copied from Max's approved
  NICHOLS result. The source heart remains exactly 236 x 229 px, its pointed tip
  meets the black upstroke, and its body never touches the ampersand.
- Finished sizes: Large 570 x 125 mm, Medium 450 x 120 mm, Small 290 x 85 mm
- Status: **Large artwork complete and visually approved by Max on 14 July 2026.**
  Medium and Small are built to the same rule and verified in software, but have not
  yet been printed on acrylic or visually approved.

Only the customer names around the locked signature may compress to fit. The
heart size, heart height, ampersand scale, and tip contact do not vary by order.
The heart is the same physical size at Medium as at Large - only the surrounding
type is re-fitted. At Small it scales to 13.52 mm, the one agreed exception: the
85 mm blank is shorter than Large's 100.2 mm interior, so no inset can preserve the
interior and the whole signature unit must shrink together. Print and cut automation
does not reopen the approved artwork rule at any size.

## One Command

```powershell
python scripts\plan-batch.py orders.json --out-dir plan
powershell -ExecutionPolicy Bypass -File production\run-batch.ps1 -OrdersJson plan\batch-plan.json -OutDir production\print\<date>
```

`run-batch.ps1` is the only orchestrator: it chains build -> recolour -> bleed ->
impose -> jig -> PDF for every sign, groups them into beds by size + colourway, and
halts on the first failure. It never contacts the printer. Individual stage scripts
remain callable for debugging, but production runs go through the one command.

## Product Rules

`production\product-rules.json` is the single source of truth for the eight
colourways and for which SKUs get the red heart. `recolour-sign.ps1 -Sku <sku>`
applies it; `plan-batch.py` uses the same file to decide which order lines are
street signs. An unclassified SKU is refused, not guessed.

This matters because `build.py` draws the heart whenever line 1 contains an
ampersand - it does not know the SKU. Without `-Sku`, a Family or Retirement sign
whose text happens to contain `&` would print with the Mr & Mrs heart.

## Contours

`source/size-contours.json` holds all three blank contours and is the single source
of truth. It is committed, so **no USB drive is needed to run the pipeline**.
`source/extract-size-contours.py` regenerates it from the LightBurn cut files and is
only needed if one of those changes; it verifies the extracted Large against the
audited `source/source-data.js`, which is kept as the audit trail and is never read
at runtime.

## Bed Layouts

`production\bed-layout.json` is the single source of truth for how each size nests
on the 610 x 420 mm bed. `make-jig.ps1` and `make-imposition.ps1` both read it
through `bed-layout.ps1`, so the printed jig outlines and the artwork placed on
them cannot drift apart. Change a layout there, never in one of the scripts.

## Rebuild And Test

Generator verification - 8 geometry checks over 6 name lengths plus a blank
subtitle. It also asserts the mounting-hole IDs are **absent**, since they are
physical holes and printing them puts ink where the acrylic is missing:

```powershell
python artwork\verify-heart-placement.py
```

Full pipeline verification against the committed fixture - 8 signs, 3 sizes, 4
colourways, 4 beds:

```powershell
powershell -ExecutionPolicy Bypass -File production\run-batch.ps1 -OrdersJson scripts\fixtures\run-batch-orders.json -OutDir <scratch>
```

To regenerate `source-data.js` from another copy of the source bundle:

```powershell
powershell -ExecutionPolicy Bypass -File source\build-source-data.ps1 -SourceRoot 'E:\sean\max'
```

The source build expects the supplied LightBurn project, PSD, and four Times
font files. It records hashes and extracts the LightBurn XML with a structured
parser.

## Confirmed Geometry

Max accepted 570 x 125 mm as the finished cut size on 2026-07-14, matching the
supplied LightBurn contour. The storefront's 570 x 120 mm value is retained as
reference history only. The PSD's approximately 570 x 127.1 mm visible bounds
are consistent with Max's explanation of intentional print overrun across the
black border, not a second finished size.

Max approved the final Large visual treatment on 14 July 2026 after a multi-order
test.

## Printing

Printing is live. The full order-to-print pipeline - artwork, PDF conversion,
3-up imposition, jig, and hot-folder handoff to RasterLink7 - is documented in
`workflows/starred/daisy-street-sign-automation.md`, which is the operational
source of truth. The only manual step is the ENTER press on the printer panel,
forced by the faulty head heater.
