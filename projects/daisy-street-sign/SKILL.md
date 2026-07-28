# Daisy Maison Street Signs — agent skill

Hand this file to any capable coding agent (Claude, Codex, or similar) with a
terminal on a Windows machine. It is self-contained: everything the pipeline
needs is in this folder and committed, so a fresh `git clone` is enough.

**What it does:** turns Daisy Maison street-sign orders into print-ready bed PDFs
for the Mimaki UJF-6042MkII, correctly laid out, correctly coloured, with the
right signs carrying the heart — and optionally loads them into the printer's
hot folder.

**What it never does:** decide to print. A person checks the PDFs, sets the
blanks on a printed jig, and presses ENTER on the panel.

---

## Agent: read this first

You are operating a real production pipeline that puts UV ink on acrylic blanks
that cost money. Wrong output is not a failed test, it is a ruined blank and a
late customer order.

Three rules that are never relaxed, for any order, at any size:

1. **Mounting holes are never printed.** They are physical holes drilled in the
   acrylic. Ink drawn there lands on nothing and rings a hole in black.
   `verify-heart-placement.py` asserts their IDs are absent from generated
   artwork. If you ever find yourself adding them back, stop.
2. **4 mm bleed on every border, always.** The printed border must overrun the
   cut edge, or normal alignment error shows as a white sliver down one side.
   A bleed wider than half the row gap is refused, because neighbouring signs
   would print into each other.
3. **Never invent personalisation.** If a line of customer text is missing,
   ambiguous, or the SKU is unrecognised, stop and ask. A blank you did not
   print is recoverable; a blank printed with a guessed surname is not.

If a stage fails, report which one and stop. Do not work around it.

---

## Setup on a fresh machine

```powershell
git clone https://github.com/maxellison0-glitch/daisy-maison-os
cd "daisy-maison-os\projects\daisy-street-sign"
python -m pip install -r requirements.txt
```

You also need:

- **Windows PowerShell 5.1** — the stage scripts are PowerShell. Note it has no
  ternary `?:`, no `??`, and it silently drops empty-string arguments to native
  commands; both quirks have caused real bugs here.
- **Google Chrome or Microsoft Edge** — used headless as the SVG renderer. Edge
  ships with Windows, so this is normally already satisfied. Never re-implement
  the text layout; the whole point of using a browser engine is correct kerning.
- **A Shopify connection** to `daisymaisonuk.myshopify.com` if you are pulling
  live orders rather than being handed them.

No USB drive and no network share are needed. Every blank contour the pipeline
uses is committed in `source/size-contours.json`.

Verify the install before touching a customer order:

```powershell
python artwork\verify-heart-placement.py
powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 -OrdersJson scripts\fixtures\run-batch-orders.json -OutDir .\_check
```

The first runs 8 geometry checks. The second builds 8 signs across 3 sizes and 4
colourways onto 4 beds. Every page must come out **609.94 x 420.20 mm** — that
is 610 x 420 within Chrome's whole-point rounding, and it is the number that
tells you the renderer is behaving.

---

## What you can make

### Sizes

| Size | Finished blank | Per bed |
|---|---|---|
| Large | 570 x 125 mm | 3 |
| Medium | 450 x 120 mm | 3 |
| Small | 290 x 85 mm | 8 |

Bed is 610 x 420 mm. Capacity comes from `production/bed-layout.json` — change a
layout there, never inside a script, because the jig and the imposition both
read it and must not disagree.

**Large is the only size printed and approved on acrylic.** Medium and Small are
built to the same rule and verified in software, but have never come off the
machine. Print a jig and dry-fit a real blank before running customer orders at
those sizes, and say so rather than assuming.

### Colourways

Eight, in `production/product-rules.json`, validated against the real product:

`black` `#010101` · `grey` `#7C7C7C` · `sage` `#9AA192` · `grass` `#68893C` ·
`blue` `#799CAA` · `lightsage` `#BEC0A9` · `blush` `#EBC3C3` ·
`duskypink` `#CB9CA5`

`gray` is accepted as an alias of `grey`. The border and the lettering carry the
colour; the inner panel stays white. The heart is always red and never recoloured
— it is a raster asset and part of a locked signature unit.

### The heart

**This is the part that goes wrong, so read it twice.**

`build.py` draws the heart whenever line 1 contains an ampersand. It has no idea
what the SKU is. So a Family sign reading `THE SMITH & JONES FAMILY`, or a
Retirement sign whose text happens to contain `&`, will render with the Mr & Mrs
heart unless the SKU is passed.

Exactly four SKUs get the heart:

| SKU | Product |
|---|---|
| `36961` | Mr & Mrs Personalised Street Sign |
| `36965-1-1` | Mr & Mrs First Christmas |
| `36965-3` | My Valentine |
| `36965-3-1` | My Galentine |

Every other classified SKU has it removed. Matching is exact — `36961-2` is
Retirement, not a Mr & Mrs variant, and a prefix match would put a heart on it.

An **unclassified SKU is refused, not guessed.** If Shopify returns a SKU that
is not in `product-rules.json`, stop and ask whether it is a street sign and what
its heart and colour policy should be, then add it to that file. Do not special-
case it in a script.

---

## Running orders

### 1. Get the orders

If you have a Shopify connection, pull unfulfilled paid orders and write them as
JSON. The planner accepts Shopify's own field names — `lineItems`,
`customAttributes`, `unfulfilledQuantity`, `product.handle` — in either camelCase
or snake_case, so the connector's response usually drops straight in.

The fields that matter per line item: `sku`, `unfulfilledQuantity`, and the
custom attributes carrying `Line 1`, `Line 2`, `Size` and `Colour border`.

If you have no connection, a plain array works:

```json
[ { "order":"DM37694", "sku":"36961", "size":"Large", "colour":"Black",
    "line1":"MR & MRS NICHOLS", "line2":"FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024" } ]
```

### 2. Plan the batch — read-only, touches nothing

```powershell
python scripts\plan-batch.py orders.json --out-dir plan
```

Keeps only sign lines with a positive unfulfilled quantity, groups them into beds
by size and colourway, and writes `plan\batch-plan.json` plus a human review
sheet `plan\batch-plan.md`.

**Show the review sheet to a person before going further.** It lists every
personalisation exactly as it will print and flags what it is unsure about: a
missing line 1, an unrecognised size, an unclassified SKU. A typo caught here
costs nothing.

### 3. Produce the beds

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 `
    -OrdersJson plan\batch-plan.json -OutDir production\print\2026-07-28
```

Per sign: build the SVG, apply the SKU's colour and heart rules, add the 4 mm
bleed. Per bed: impose the bled artwork, and cut a jig from the *unbled* contour.
Then render both to PDF at true physical scale.

It validates every sign before generating anything, **stops dead on the first
failure**, and writes `run-manifest.json` last — so the manifest existing means
every stage succeeded.

Out, per bed: `bed01-large-black.pdf` and `bed01-large-black-jig.pdf`.

One bed is one size at one colourway, because a bed is a single print run at one
ink setup. Part beds are produced and reported as part beds; whether to print one
or wait for more orders is a human's call, not the script's.

### 4. Jig, then load the blanks

Print the `*-jig.pdf` from the Mimaki itself onto paper taped to the bed, once
per fresh bed per size. Then set the laser-cut blanks into the printed outlines.

Printing the jig on the same machine that prints the artwork is the entire point:
positions become correct by construction, so nobody has to identify the physical
bed-origin corner, and the jig and the artwork cannot drift apart.

### 5. Send the artwork

```powershell
... -OutDir production\print\2026-07-28 -SendToPrinter
```

Copies each **artwork** PDF into `C:\MijCtrl\Hot\UJF6042MkII`. Never the jig —
the jig is its own deliberate job, and queueing outlines to print onto acrylic
blanks has nearly happened before.

RasterLink7 imports within about five seconds and the file disappears from the
folder; that disappearance is the confirmation. Then in RasterLink: select the
job, `Alt+X`, `RIP and Print`, `Start`, page at position 0,0.

**Use 600 x 900 VD / 12 pass.** Not the 1200 x 1200 / 16 pass a freshly
downloaded profile assigns — the correct condition is roughly three times faster
and is what every archived job on the old machine used.

### 6. The ENTER press

A person presses **ENTER** on the printer panel to release every job.

The head heater is faulty. The panel sits on `HEAD TEMP. CONTROL / PLEASE WAIT`
and never reaches temperature, so it never clears by itself. RasterLink cannot
acknowledge a panel prompt, so there is no software equivalent.

**Never describe this pipeline as unattended, and never tell anyone to wait until
the printer reports ready.** It will not. The real fix is a heater repair.

---

## Where the laser fits

Blanks are cut in LightBurn from the existing `.lbrn2` cut files, before any of
the above. **This project does not drive the laser.** It reads those contours
(`source/size-contours.json`) so the printed artwork matches the cut shape and
the bed layout matches the real blank.

If a cut file changes, re-extract with `source/extract-size-contours.py`. It
verifies the extracted Large against the audited `source/source-data.js` and
refuses a contour whose shape family is wrong — the Traditional Road Sign is a
different product with a convex outline.

---

## Change these, never a script

| File | Governs |
|---|---|
| `production/product-rules.json` | the eight colourways; which SKUs get the heart |
| `production/bed-layout.json` | how each size nests on the 610 x 420 bed |
| `source/size-contours.json` | the three blank contours |

Everything downstream reads them, which is what stops the planner, the jig and
the imposition from drifting apart.

## What the pipeline refuses to do

Each of these exists because something went wrong once. If you hit one, it is
telling you something true — fix the input, do not bypass the guard.

- `make-jig` refuses a bled SVG, and refuses a contour of the wrong size rather
  than scaling the blank outline it claims to represent.
- `make-imposition` refuses a bleed wider than half the row gap.
- `svg-to-print-pdf` refuses a page not sized in mm rather than guessing scale.
- `recolour-sign` refuses an unclassified SKU.
- `extract-size-contours` refuses a contour from the wrong product.
- `run-batch` validates every sign before generating anything, and writes the
  manifest last.
- `verify-heart-placement` fails if the mounting holes ever reappear.

## Known gaps, stated plainly

- Medium and Small have never been printed on acrylic.
- Small's cap-centre Y is a best estimate; the two PSD sample cells disagree by
  3 mm.
- Order logic is deliberately simple: SKU, size, colour, two text lines. Bundles,
  size-upgrade line items and add-ons are not yet interpreted, so a Shopify order
  whose size lives on a separate upgrade line needs a human to set the size.
- RasterLink7 has no CLI. The hot-folder copy is automated; the RIP and Print
  click is not.
