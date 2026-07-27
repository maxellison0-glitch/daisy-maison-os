# Daisy Maison Street Signs

Shopify orders to printed acrylic. Small, Medium and Large; eight border
colourways; the nine SKUs listed in `production/product-rules.json`.

This is the only copy. Do not create another in MaxOS, Gym, or an agent folder.
Run `git pull --ff-only` from `%USERPROFILE%\AA Daisy Maison OS` before editing.

## The Workflow

Run everything from this folder.

**1. Plan the batch** - read-only. Never changes Shopify or touches the printer.

Pull the unfulfilled orders with the Shopify connector and save the reply
verbatim as `orders.json` - the raw `{data:{orders:{nodes:[...]}}}` is read as-is,
so nothing has to be reshaped by hand. The exact query, and why it carries a date
bound, are in the workflow doc linked at the bottom of this file.

```powershell
python scripts\plan-batch.py orders.json --out-dir plan
```

In: a JSON export of Shopify orders. Out: `plan\batch-plan.json` plus
`plan\batch-plan.md`. **Read the Markdown sheet before going further** - it lists
every personalisation exactly as it will be printed, flags anything unclear, and
marks which beds are full. A typo caught here costs nothing; caught later it costs
a blank.

**2. Produce the beds** - one command, the whole artwork chain.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 `
    -OrdersJson plan\batch-plan.json -OutDir production\print\2026-07-27
```

Out, per bed: `bed01-large-black.pdf` (the artwork) and
`bed01-large-black-jig.pdf` (its matching jig), plus `run-manifest.json`.

Inside, per sign: build the SVG, apply the SKU's colour and heart rules, add
bleed, then impose the bed and cut its jig from the same layout. It validates
every sign before generating anything, **stops dead on the first failure**, and
writes the manifest last - so the manifest existing means every stage succeeded.
It never contacts the printer.

`-OrdersJson` also takes a plain array when you are not going through Shopify:

```json
[ { "order":"DM37694", "sku":"36961", "size":"Large", "colour":"Black",
    "line1":"MR & MRS NICHOLS", "line2":"FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024" } ]
```

**3. Print the jig and load the blanks.** Print `*-jig.pdf` from the Mimaki onto
paper taped to the bed - once per fresh bed, per size. Then set the laser-cut
blanks into the printed outlines. Printing the jig on the machine itself is the
point: the positions become correct by construction, so the bed-origin corner
never has to be identified and jig and artwork cannot drift apart.

**4. Send the artwork.** Copy the bed PDF into the RasterLink7 hot folder:

```
C:\MijCtrl\Hot\UJF6042MkII
```

It imports in about five seconds. Select the job, `Alt+X`, `RIP and Print`,
`Start`, page at position 0,0. Use **600 x 900 VD / 12 pass** - not the defaults.

**5. Press ENTER on the printer.** The head heater is faulty and the panel never
clears itself, so a human releases every job by hand. There is no software
equivalent. The pipeline is not unattended, and it never will be until the heater
is repaired.

### Where the laser fits

The blanks are cut in LightBurn from the existing `.lbrn2` cut files, before any
of the above. This project does not drive the laser - it *reads* those contours
(`source/size-contours.json`) so the printed artwork matches the cut shape and the
bed layout matches the real blank. Change a cut file and the contours must be
re-extracted; see `source/extract-size-contours.py`.

## Two Rules That Never Bend

- **Mounting holes are never printed.** They are physical holes in the acrylic;
  ink drawn there lands on nothing. `artwork/verify-heart-placement.py` asserts
  their IDs are absent from generated artwork.
- **4 mm bleed on every border.** The border must overrun the cut edge or
  alignment error shows as a white sliver. A bleed wider than half the row gap is
  refused, because neighbouring signs would print into each other.

## Change These, Never A Script

| File | Governs |
|---|---|
| `production/product-rules.json` | the eight colourways, and which SKUs get the red heart |
| `production/bed-layout.json` | how each size nests on the 610 x 420 mm bed |
| `source/size-contours.json` | the three blank contours |

`product-rules.json` matters more than it looks: `build.py` draws the heart
whenever line 1 contains an ampersand, and it does not know the SKU. Without
`-Sku`, a Family or Retirement sign whose text happens to contain `&` would print
with the Mr & Mrs heart. An unclassified SKU is refused, not guessed.

`bed-layout.json` is read by both `make-jig.ps1` and `make-imposition.ps1`, so the
printed outlines and the artwork placed on them cannot disagree.

## Folder Map

| Folder | Contents |
|---|---|
| `production/` | the runner, its stage scripts, and two of the three truth files |
| `artwork/` | `build.py`, the locked heart and Times asset, and the approved Large sample |
| `scripts/` | the batch planner and its test fixtures |
| `source/` | cut-file geometry. `size-contours.json` is live truth; `source-data.js` is the audit trail behind it and is never read at runtime |
| `references/` | photograph of the real product |

Stage scripts stay individually callable for debugging. Production runs go through
the one command.

### Generated output is not tracked

`artwork/orders/`, `production/print/`, `production/jig-*` and `plan/` are working
output and are git-ignored. Everything in them is reproducible from the order text
plus these scripts, and the repository syncs to every PC with `git add -A` - so
tracking them would grow it by roughly 130 KB per order forever and copy customer
names onto every machine.

Orders generated up to 2026-07-27 stay in Git history rather than the folder. To
recover exactly what was sent to the printer for one of them:

```powershell
git show 8e1d0f8:projects/daisy-street-sign/artwork/orders/DM37201.svg > DM37201.svg
```

## The Design Rule

- Both lines Times New Roman **regular 400**, vertical scale 1.4, never bold.
- Heart and ampersand are one locked signature unit from Max's approved NICHOLS
  result: heart exactly 236 x 229 px, pointed tip meeting the black upstroke, body
  never touching the ampersand. Only the surrounding names compress to fit.
- The heart is the same physical size at Medium as at Large. At Small it scales to
  13.52 mm - the one agreed exception, because the 85 mm blank is shorter than
  Large's 100.2 mm interior, so the whole unit must shrink together.
- Finished sizes are the cut sizes: Large **570 x 125**, Medium **450 x 120**,
  Small **290 x 85** mm. The storefront's 570 x 120 is stale copy, not a second
  size; Max confirmed 125 on 2026-07-14.

Print and cut automation does not reopen this rule at any size.

## Status

**Large is printed, physically checked and visually approved by Max on
2026-07-14.** Medium and Small are built to the same rule and verified in
software, but have never come off the machine - print a jig and dry-fit a real
blank before running customer orders at those sizes.

## Tests

Generator geometry - 8 checks across six name lengths plus a blank subtitle:

```powershell
python artwork\verify-heart-placement.py
```

Full pipeline against the committed fixture - 8 signs, 3 sizes, 4 colourways,
4 beds:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 -OrdersJson scripts\fixtures\run-batch-orders.json -OutDir <scratch>
```

Neither needs the printer, and no USB drive is required - every contour the
pipeline uses is committed.

## Deeper Reference

`workflows/starred/daisy-street-sign-automation.md` is the operational manual:
printer and ink detail, the full print condition and why it is not the default,
driving RasterLink7 from PowerShell, the per-stage manual route for when something
breaks, and the reasoning behind each refusal guard. Read this file to run the
workflow; read that one to understand or repair it.
