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
- Finished Large size: 570 x 125 mm
- Status: **Large artwork complete and visually approved by Max on 14 July 2026**

Only the customer names around the locked signature may compress to fit. The
heart size, heart height, ampersand scale, and tip contact do not vary by order.
Office print/cut automation is a separate future phase and does not reopen the
approved Large artwork rule.

## Rebuild And Test

Generator verification:

```powershell
python artwork\verify-heart-placement.py
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
test. Printer/RIP/nesting/laser handoff remains intentionally blocked until a
separate production integration is explicitly implemented.
