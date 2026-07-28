# Daisy Maison Street Signs — agent skill

Hand this file to any capable coding agent with a terminal on a Windows machine.
It is self-contained: everything the pipeline needs is committed here, so a fresh
`git clone` is enough.

**What it does:** turns Daisy Maison street-sign orders into print-ready bed PDFs
for the Mimaki UJF-6042MkII — correctly laid out, correctly coloured, with the
right signs carrying the heart — and loads them into the printer's hot folder.

**The one thing a person does:** press ENTER on the printer panel.

---

## Two rules

1. **4 mm bleed on every border, always.** The printed border overruns the cut
   edge, so normal alignment error never shows as a white sliver. This is
   automatic; never turn it off.
2. **Never invent personalisation.** If a line of customer text is missing or
   ambiguous, or the SKU is unrecognised, stop and ask. A sign you did not print
   is recoverable; a sign printed with a guessed surname is not.

---

## Setup

```powershell
git clone https://github.com/maxellison0-glitch/daisy-maison-os
cd "daisy-maison-os\projects\daisy-street-sign"
python -m pip install -r requirements.txt
```

You also need:

- **Windows PowerShell 5.1.** It has no ternary `?:`, no `??`, and it silently
  drops empty-string arguments to native commands. All three have caused bugs
  here — write accordingly.
- **Chrome or Edge**, used headless as the SVG renderer. Edge ships with Windows.
  Never re-implement the text layout; using a browser engine is what gives
  correct kerning.
- **A Shopify connection** to `daisymaisonuk.myshopify.com`.

No USB drive or network share. Every blank contour is committed in
`source/size-contours.json`.

Confirm the install:

```powershell
python artwork\verify-heart-placement.py
powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 -OrdersJson scripts\fixtures\run-batch-orders.json -OutDir .\_check
```

Eight geometry checks, then 8 signs across 3 sizes and 4 colourways. Every page
comes out **609.94 x 420.20 mm** — that is 610 x 420 within Chrome's whole-point
rounding, and it is how you know the renderer is behaving.

---

## What you can make

### Sizes

| Size | Finished blank | Per bed |
|---|---|---|
| Large | 570 x 125 mm | 3 |
| Medium | 450 x 120 mm | 3 |
| Small | 290 x 85 mm | 8 |

Bed is 610 x 420 mm. Capacity lives in `production/bed-layout.json` — change a
layout there, never in a script, because the jig and the imposition both read it
and must never disagree.

### Colourways

Eight, in `production/product-rules.json`:

| Name | Hex |  | Name | Hex |
|---|---|---|---|---|
| `black` | `#010101` | | `blue` | `#799CAA` |
| `grey` | `#7C7C7C` | | `lightsage` | `#BEC0A9` |
| `sage` | `#9AA192` | | `blush` | `#EBC3C3` |
| `grass` | `#68893C` | | `duskypink` | `#CB9CA5` |

`gray` is accepted as a spelling of `grey`. The border and lettering carry the
colour; the inner panel stays white. The heart is always red and never
recoloured — it is a raster asset inside a locked signature unit.

### The heart

`build.py` draws the heart whenever line 1 contains an ampersand. It does not
know the SKU. So a Family sign reading `THE SMITH & JONES FAMILY`, or a
Retirement sign whose text contains `&`, renders with the Mr & Mrs heart unless
the SKU is passed. **Always pass `-Sku`.** `run-batch.ps1` does this for you.

Exactly four SKUs get the heart:

| SKU | Product |
|---|---|
| `36961` | Mr & Mrs Personalised Street Sign |
| `36965-1-1` | Mr & Mrs First Christmas |
| `36965-3` | My Valentine |
| `36965-3-1` | My Galentine |

Every other classified SKU has it removed. Matching is **exact** — `36961-2` is
Retirement, and a prefix match would put a heart on it.

An unclassified SKU is refused, not guessed. Ask what it is, then add it to
`product-rules.json`. Never special-case a SKU inside a script.

### Create Your Own

`36967` is its own landing page and behaves differently: **the customer picks the
border colour, and the text stays black.** That is already encoded — its rule is
`border: customer, text: black`, against Mr & Mrs which is `border: black,
text: black`. Passing `-Sku` gets it right automatically.

---

## Running orders

### 1. Pull the orders

Pull unfulfilled paid orders from Shopify and write them as JSON. The planner
accepts Shopify's own field names — `lineItems`, `customAttributes`,
`unfulfilledQuantity`, `product.handle` — in camelCase or snake_case, so the
connector response normally drops straight in.

Per line item you need `sku`, `unfulfilledQuantity`, and the custom attributes
carrying `Line 1`, `Line 2`, `Size` and `Colour border`.

**Reading size correctly:** most orders carry it in the `Size` attribute
(`"Large 57 x 12cm (+£8.99)"`). Some carry it as a *separate line item* instead —
a `Size Upgrade — Large` row linked by `_Bundle ID` to the sign it upgrades. When
you see one, apply it to the bundled sign rather than treating it as its own
product.

A plain array also works, for a manual run:

```json
[ { "order":"DM37694", "sku":"36961", "size":"Large", "colour":"Black",
    "line1":"MR & MRS NICHOLS", "line2":"FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024" } ]
```

### 2. Plan the batch — read-only, changes nothing

```powershell
python scripts\plan-batch.py orders.json --out-dir plan
```

Keeps sign lines with a positive unfulfilled quantity, packs them into beds, and
writes `plan\batch-plan.json` plus a review sheet `plan\batch-plan.md`.

**Show the review sheet to a person before going further.** It lists every
personalisation exactly as it will print, with its colour, and flags anything it
is unsure about. A typo caught here costs nothing.

### 3. Produce the beds

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 `
    -OrdersJson plan\batch-plan.json -OutDir production\print\2026-07-28
```

Per sign: build the SVG, apply that sign's colour and heart rules, add the 4 mm
bleed. Per bed: impose the bled artwork, and cut a jig from the *unbled* contour.
Then render both to PDF at true physical scale.

It validates every sign before generating anything, stops on the first failure,
and writes `run-manifest.json` last — so the manifest existing means every stage
succeeded.

Out, per bed: `bed01-large.pdf` and `bed01-large-jig.pdf`.

**One bed is one size. Colour does not split a bed.** Border colour is artwork,
not a machine setting — the Mimaki lays CMYK onto white acrylic, so a grass sign
and a blush sign print in the same run with no re-setup. Pack every sign of a
size onto as few beds as possible; that is the whole point. Only the physical
blank changes the layout.

Part beds are produced and reported as part beds. Whether to print one or wait
for more orders is a person's call.

### 4. Jig, then blanks

Print the `*-jig.pdf` from the Mimaki onto paper taped to the bed, once per fresh
bed per size. Then set the laser-cut blanks into the printed outlines.

Printing the jig on the same machine that prints the artwork is the point:
positions become correct by construction, so nobody identifies the physical
bed-origin corner, and jig and artwork cannot drift apart.

### 5. Ask, then send

**Ask the person for approval before sending anything to the printer.** Show them
the bed list and what is on each. Once they approve:

```powershell
... -OutDir production\print\2026-07-28 -SendToPrinter
```

Copies each **artwork** PDF into `C:\MijCtrl\Hot\UJF6042MkII`. Never the jig —
the jig is its own deliberate job, and queueing outlines onto acrylic blanks has
nearly happened before.

RasterLink7 imports within about five seconds and the file disappears from the
folder; that disappearance is the confirmation. Then in RasterLink: select the
job, `Alt+X`, `RIP and Print`, `Start`, page at position 0,0.

**Use 600 x 900 VD / 12 pass** — not the 1200 x 1200 / 16 pass a freshly
downloaded profile assigns. The correct condition is roughly three times faster
and is what every archived job on the old machine used.

### 6. The ENTER press

A person presses **ENTER** on the printer panel to release each job.

The head heater is faulty: the panel sits on `HEAD TEMP. CONTROL / PLEASE WAIT`
and never reaches temperature, so it never clears itself. RasterLink cannot
acknowledge a panel prompt, so there is no software equivalent. Never describe
this pipeline as unattended, and never tell anyone to wait until the printer
reports ready — it will not.

---

## Where the laser fits

Blanks are cut in LightBurn from the `.lbrn2` cut files before any of the above.
**This project does not drive the laser.** It reads those contours
(`source/size-contours.json`) so the printed artwork matches the cut shape and
the bed layout matches the real blank.

If a cut file changes, re-extract with `source/extract-size-contours.py`.

---

## Change these, never a script

| File | Governs |
|---|---|
| `production/product-rules.json` | the eight colourways; which SKUs get the heart |
| `production/bed-layout.json` | how each size nests on the 610 x 420 bed |
| `source/size-contours.json` | the three blank contours |

Everything downstream reads them, which is what keeps the planner, the jig and
the imposition in agreement.

## What the pipeline refuses to do

If you hit one of these it is telling you something true. Fix the input; do not
bypass the guard.

- `make-jig` refuses a bled SVG, and refuses a contour of the wrong size rather
  than scaling the blank outline it claims to represent.
- `make-imposition` refuses a bleed wider than half the row gap, which would
  print neighbouring signs into each other.
- `svg-to-print-pdf` refuses a page not sized in mm rather than guessing scale.
- `recolour-sign` refuses an unclassified SKU.
- `extract-size-contours` refuses a contour from the wrong product — the
  Traditional Road Sign is a different, convex shape.
- `run-batch` validates every sign before generating anything, and writes the
  manifest last.

## Not yet automated

RasterLink7 has no CLI. The hot-folder copy is automated; the RIP-and-Print click
is not.
