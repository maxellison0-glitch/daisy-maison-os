# signauto operations manual

> The machine manual and repair routes behind `AGENT.md`. For the daily morning
> run, use AGENT.md; come here when something needs understanding or fixing.
> Current production scope: the classified SKUs in `production/product-rules.json`
> on white acrylic, **Small, Medium and Large**, any of the eight border colourways.
>
> **Updated 2026-08-06.** This system now lives in its own repo (signauto),
> moved from daisy-maison-os on Max's instruction. Printing is IMPLEMENTED and
> authorised (since 2026-07-26).

## Start Here

You are operating Daisy Maison's street-sign system. There are three modes:

1. **PRODUCE SIGNS** - the daily run. Follow `AGENT.md`; this file is its appendix.
2. **IMPROVE AUTOMATION** - modify, debug, test, or extend the system.
3. **NEW SIZE** - all three sizes are built. See Sizes before adding a fourth.

Infer the mode from Max's request. Ask only if genuinely ambiguous.

## Source Of Truth

The signauto repo root, wherever it is cloned. Run `git pull --ff-only` before
changing files. Do not create a copy elsewhere.

## The Machine And Its One Broken Thing

- Mimaki **UJF-6042MkII** UV flatbed, printable bed **610 x 420 mm**.
- Ink **LUS-120**, 8 channels in physical order `PR CL Y C M K W W`
  (Primer, Clear, Yellow, Cyan, Magenta, Black, White, White).
- Driven by **RasterLink7 4.1.3** on Max's main PC, USB, printer serial `AC02E569`,
  registered as `UJF6042MkII`.
- Signs print onto **pre-cut white acrylic** blanks placed on a printed paper jig.
  White acrylic means no white underlayer - straight CMYK on white. (Clear acrylic
  is occasionally used and WOULD need a white plate.)

**KNOWN FAULT - read this before promising unattended printing.** The head heater
is faulty. The panel sits on `HEAD TEMP. CONTROL / PLEASE WAIT` and **never reaches
temperature**, so it never clears by itself. A human must press **ENTER** on the
printer panel to release each job. There is no software equivalent - RasterLink
cannot acknowledge a panel prompt. Therefore:

- Everything up to that press is automated. The press is manual.
- Do not claim the pipeline is unattended.
- Do not advise "wait until the printer reports ready" - it never will.
- The real fix is a heater repair, not a workaround.

## Print Condition (use these; they are not the defaults)

| Setting | Value |
|---|---|
| Resolution | **600 x 900 VD** |
| Pass | **12** |
| Profile | `UJF6042MKII8CLUS1204C_PET_F115040.icc` |
| Media | UV-PET v3.5 / White PET Gloss |

This is the condition the previous RasterLink 6 PC used for all 32 of its archived
jobs (recovered from `F:\MijSuite\Jobs`). It is roughly **3x faster** than the
1200x1200 / 16-pass default a freshly downloaded profile assigns. Measured: a
full-bed jig went from ~10 minutes to ~3.

There is **no 1200x900 mode**, despite that being the figure quoted verbally.

**The media profile is UV-PET film, not acrylic.** This is deliberate and inherited
- the old PC also printed acrylic through a PET profile, and Mimaki's profile server
offers no acrylic profile for this printer/ink. If a real acrylic profile is ever
wanted, Mimaki material code `0048` (acrylic) covers media codes 000000402,
000000441, 000000445, 000000459, 000000460, 000000463, 000000464, 000000615,
000000640.

## Produce Signs - The One Command

Orders in, print-ready PDFs out. Everything after this section is the manual
per-stage route, kept because it is what you need when something goes wrong.

**Pull the orders yourself** with the Shopify connector, using the exact query
committed in `queries/orders.graphql`. Save each page's reply verbatim as
`plan/orders-p1.json`, `plan/orders-p2.json`, ... and page with the `after`
cursor until `hasNextPage` is false. Do not reshape the JSON - `plan-batch.py`
reads the raw `{data:{orders:{nodes:[...]}}}` reply, and a hand-reshape is a
place for signs to go missing.

The `created_at` bound in that file is not cosmetic: ancient orders marked
unfulfilled would otherwise appear in every plan forever. Move the date on as
the backlog ages. Do not filter by SKU in the query - `plan-batch.py` decides
what is a sign, from `product-rules.json`.

Then:

```powershell
python scripts\plan-batch.py plan\orders-p1.json plan\orders-p2.json --printed-log state\printed.log --out-dir plan
```

Read `plan\batch-plan.md`, check the personalisation, then gate and produce:

```powershell
python scripts\select-beds.py plan\batch-plan.json --out plan\go.json
powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 `
    -OrdersJson plan\go.json -OutDir production\print\2026-08-07
```

After a `-SendToPrinter` run succeeds, record and share what was printed:

```powershell
python scripts\log-printed.py plan\go.json --log state\printed.log
git add state\printed.log; git commit -m "print log 2026-08-07"; git push
```

`run-batch.ps1` chains build -> recolour -> bleed -> impose -> jig -> PDF and
**stops dead on the first failure**, because a half-finished bed that still emits a
PDF is how the wrong thing gets printed. It groups signs into beds by size +
colourway (one bed is one print run at one ink setup), validates every sign before
generating anything, and writes `run-manifest.json` last - so the manifest existing
means every stage succeeded.

It does **not** touch the printer. The hot-folder copy stays a separate act.

`-OrdersJson` also accepts a plain array if you are not going through Shopify:

```json
[ { "order":"DM37694", "sku":"36961", "size":"Large", "colour":"Black",
    "line1":"MR & MRS NICHOLS", "line2":"FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024" } ]
```

Part beds are produced and reported as part beds. Whether to print one or wait for
more orders is Max's call, not the script's.

## Produce Signs - Manual Route

### 1. Pull the order from Shopify

**The built-in `get-order` tool does NOT return personalisation** - it omits
`customAttributes`. Use GraphQL:

```graphql
query($id: ID!) {
  order(id: $id) {
    name
    lineItems(first: 10) {
      nodes { sku unfulfilledQuantity customAttributes { key value } }
    }
  }
}
```

Supported lines: any SKU listed in `production\product-rules.json`, with `Size`
starting `Small`, `Medium` or `Large`. An unlisted SKU is refused rather than
guessed - classify it in that file first. Read `Line 1` and `Line 2` exactly - never
silently correct spelling, punctuation or spacing. Customers do type
`MR&MRS CHAMBERLAIN` with no spaces, and that is legitimate.

A sign with genuinely no subtitle (house and garden signs) needs `build.py
--no-line2`. Do **not** pass an empty string: Windows PowerShell 5.1 drops empty
arguments on the way to a native command, so `""` leaves build.py on its wedding
default and prints `FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024` on a potting-shed
sign. `run-batch.ps1` handles this for you.

Ignore upgrade/add-on lines (`ACC-*`, `Size Upgrade`) - no personalisation on them.

### 2. Generate the artwork

```powershell
& 'C:\Users\Max Ellison\AppData\Local\Programs\Python\Python313\python.exe' `
  artwork\build.py --size large "<ORDER>" "<LINE1>" "<LINE2>" 486 "artwork\orders\<ORDER>.svg"
```

`--size` takes `small`, `medium` or `large` and defaults to `large`. The fourth
positional argument is the line-1 target width, which differs per size - **omit it
and the size's own default is used**, which is what you want: 486 Large, 383.7
Medium, 247.8 Small. Passing Large's 486 to a smaller sign overflows the frame.

Python 3.13.9 is installed per-user with numpy, pillow, shapely, fonttools.

Watch `line1HorizontalScale`. build.py only auto-flags below 0.55, but anything
under ~0.70 is visibly condensed and worth showing Max (`MR&MRS CHAMBERLAIN` came
out at 0.672 at Large; `MR & MRS YATES` at 0.990). **Medium compresses harder for
the same name** - it fits the same text into 383.7 mm instead of 486 - so
`MR & MRS CHAMBERLAIN` drops to 0.496 there and trips the flag.

### 3. Convert to a print-ready PDF

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File production\svg-to-print-pdf.ps1 `
  -SvgPath artwork\orders\<ORDER>.svg -PdfPath <out>\<ORDER>.pdf
```

**Never re-implement text layout to build a PDF.** That was tried and failed:
summing glyph advance widths ignores kerning and produced artwork ~2% too wide
(78/255 mean error against the approved reference). The script hands the SVG to
headless Chrome, which does real text shaping and loads the SVG's own embedded font
- measured 0.86/255, i.e. antialiasing only.

### 4. Impose onto a bed

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command `
  "& 'production\make-imposition.ps1' -Size large -SignSvgs 'a.svg','b.svg','c.svg' -OutSvg 'production\bed1.svg'"
```

Use `-Command`, not `-File`: `-File` flattens the array into one comma-joined string.
Then convert the imposed SVG with the same `svg-to-print-pdf.ps1`.

Fewer signs than the layout holds is fine - they fill POS 1 upward and the spare
slots stay empty. White is no ink on this machine, so an empty slot costs nothing.

**Layouts live in `production\bed-layout.json`, and only there.** Both the jig and
the imposition read it through `bed-layout.ps1`, which is what stops the printed
outlines and the artwork placed on them from ever disagreeing. Change a layout in
the JSON; never in one of the scripts.

| Size | Blank | Grid | Per bed | Blank top-left (mm) | Bed used |
|---|---|---|---|---|---|
| Large | 570 x 125 | 1 x 3 | 3 | (20, 12.5 / 147.5 / 282.5) | 83.4% |
| Medium | 450 x 120 | 1 x 3 | 3 | (80, 20 / 150 / 280) | 63.2% |
| Small | 290 x 85 | 2 x 4 | 8 | X 7.5 / 312.5, Y 16 / 117 / 218 / 319 | 77.0% |

All three are exact bed fits. Side margins are derived, never configured, so a bad
margin cannot push artwork off an edge. Large and Medium cannot go two across (1140
and 900 mm against a 610 mm bed) and neither fits the 420 mm axis rotated. Large's
positions are corroborated by the old PC's production PSDs (Y 12.1 / 147.0 / 280.6);
Small's by the 8-up production PSD (X 8.6 / 313.9, Y 11.3 / 107.6 / 206.3 / 303.3),
which was hand-nested with an uneven row pitch - the regular grid here is within
~2 mm of it and lets the jig and imposition share one rule.

**POS 2 is exactly bed centre for Large and Medium**, so a single sign there needs no
assumption about which corner is the origin - use "Arrange in the Center".

Bleed is checked against the row gap: 4 mm bleed against a 10 mm gap leaves 2 mm
clear between neighbours. A bleed wider than half the gap is refused, because
adjacent signs would print into each other's edges.

### 5. Print the jig (once per fresh bed, per size)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File production\make-jig.ps1 `
  -Size large -ContourSvg artwork\mr-mrs-large-preview.svg -OutSvg production\jig-large.svg
```

Pass a contour SVG of the **matching size and without bleed** - the jig traces the
blank. Both mistakes are refused rather than silently scaled. The committed Large
sample above is a valid contour; for Medium or Small, generate one with
`build.py --size medium` or take the `*-styled.svg` that `run-batch.ps1
-KeepIntermediates` leaves in `_work`. Do not pass a `*-bleed.svg`.

The jig is printed **by the Mimaki itself** onto paper taped to the bed. That is the
point: positions become known by construction, the physical bed-origin corner never
has to be identified, and jig and artwork cannot disagree.

### 6. Send to the printer

Drop the PDF into the hot folder:

```
C:\MijCtrl\Hot\UJF6042MkII
```

RasterLink7 imports within ~5 seconds and the file vanishes from the folder. Then
select the job, `Alt+X` (Execution), `RIP and Print`, `Start`. Full-bed page at
position **0,0** - the imposition already places the signs.

Then a human presses **ENTER** on the printer. See the known fault above.

## Driving RasterLink7 From Code

RasterLink7 has no CLI. It can be driven with PowerShell synthetic input; the full
pattern is in the max-os repo, `memory/rasterlink7-gui-automation.md`. Essentials:

- Processes are `unitUI` (the window), `unitCtrl`, `unitRip`, `unitMDC` - **not**
  anything called "RasterLink". Searching for that name finds nothing.
- **Focus guard before every input batch**: compare the foreground window's PID to
  `unitUI`'s and abort on mismatch. Without it, clicks land in whatever window is in
  front. This has happened.
- **Verify the job name before firing.** `Alt+G` / `Alt+Q` show the loaded job in
  the header. A stale cached row coordinate once started the wrong job and nearly
  printed jig outlines onto acrylic blanks.
- Job-list rows are **~80 px apart** at 3840x2160, first row ~y=244. Re-measure
  rather than caching, and note the row list collapses to a narrow strip inside the
  Quality/General Print screens - switch jobs from Properties (`Alt+I`).
- Shortcuts beat pixel-hunting: `Alt+I` Properties, `Alt+G` General Print,
  `Alt+Q` Quality, `Alt+J` **Jig Print** (built-in, unexplored), `Alt+X` Execution,
  `Alt+E` Favorite.
- The printer Status field is **cached** - click the green refresh beside it before
  trusting it. Live truth is the Job Queue progress percentage.
- If a connected printer does not appear as a `USB2.0` output port, or all ink
  channels read `Not Detected`, restart the Device Controller
  (`C:\Program Files\Mimaki\MimakiDeviceController\unitMDC.exe`) with the printer
  powered on. It enumerates USB only at startup.
- Close modal dialogs before clicking elsewhere; a left-open dialog silently
  invalidates every coordinate.

## Approved Large Design

- Finished size **570 x 125 mm**; blanks are cut to exactly this.
- Both lines Times New Roman regular 400, tracking 0, **vertical scale 1.4**.
  `artwork/assets/times.ttf` internal name is `TimesNewRomanPSMT`, matching the
  production PSDs. The 1.4 scale is the house rule across every colourway.
- Text and frame `#010101`; panel white.
- The heart and ampersand are one **locked** signature unit. The heart does not
  scale with the name. Its pointed tip meets the black upstroke; its body does not
  touch the ampersand.
- Only customer text around the signature may compress.

Do not reintroduce bounding-box percentages, guessed heart landmarks,
name-dependent heart scaling, or per-order heart nudging.

## Sizes

| Product | Cut size (mm) | Per bed | Built? |
|---|---|---|---|
| Large | **570.00 x 125.00**, 409-vtx contour | 3 | **yes** - printed on acrylic, passed |
| Medium | **450.00 x 120.00**, 8 vtx + 4 cubics | 3 | **yes** - not yet printed |
| Small | **290.00 x 85.00**, 8 vtx + 4 cubics | 8 | **yes** - not yet printed |
| Mini Football | 150.6 x 50.3 | 14 | no |

All three run the whole chain and all three contours live in ONE committed file,
`source/size-contours.json`. No USB is needed to run the pipeline.

**All three are the same scalloped design** - four CONCAVE corners, area over convex
hull ~0.993. That ratio is the guard: `build.py` refuses a contour outside
0.985-0.9985, because a **convex 1.0000** outline is the Personalised Traditional
Road Sign, a different product with deliberately un-edged corners. Do not use
`MINI TRADITIONAL ROAD SIGN SHAPE.lbrn2` for a street sign; it cost a day once.

### Where Small comes from

There is no Small cut file and none is needed. The Medium cut file's XForm is a
**non-uniform scale** (1.55172, 1.41176) over local geometry spanning exactly
**290.000 x 85.000 mm** - and 290 x 1.55172 = 450.0, 85 x 1.41176 = 120.0. Medium
was authored by scaling the Small shape up, so Small is that master at unit scale:
read from a real Daisy file, not invented.

Validated against the real 8-up production bed
(`E:\Jigs\Street Sign Jigs\MINI\MEDIUM ALL COLOUR 2023.psd`, 300 dpi - note the
folder naming trap below): buffering the 290x85 master out by 1.00 mm reproduces the
printed silhouette to **mean 0.182 mm, all 2750 sampled edge points within 1.0 mm**.
That 1.00 mm independently matches the 1.018 mm/edge bleed measured on the Medium
production PSD.

Small's **type sizes are measured**, not scaled: two real signs both give a 40.13 mm
line-1 cap height, where a 0.68 scale of Large would have given 37.2 mm - 8% small
and visible on an 85 mm sign. `capCenterY` remains the scaled value; the two sample
cells disagree by 3 mm on vertical position, so there is no sound basis to move it.
**This is the open item for Max's visual approval.**

**NAMING TRAP.** "MEDIUM" at Daisy historically meant the 290x85 blank - today's
Small. The folder `Street Sign Jigs\MINI\` contains files called
"MEDIUM ALL COLOUR 2023.psd", and those are SMALL signs. Today's Medium is the
450x120 blank, new in June 2026, and lives in `Street Sign Jigs\MEDIUM\`.

**Shopify's "Small 28 x 12cm" IS this Small.** The listing's 12 cm height is wrong -
the real blank is 85 mm. Shopify "Medium 45 x 12cm" matches the 450 x 120 cut
exactly.

### Re-extracting the contours

Only needed if a cut file changes. Run once, on the PC with the USB attached:

```powershell
python source\extract-size-contours.py --cut-files "F:\sean\max\cutting files street signs"
```

It finds the drive itself if you omit the flag, refuses any outline that is not the
scalloped family, and its output is committed. It also verifies the extracted Large
against the audited `source/source-data.js` - they agree to 0.0006 mm.

## Product Styling Rules (conditional logic - apply to ALL sizes)

Confirmed by Max 2026-07-26. **`production\product-rules.json` is the source of
truth** - it is read by `recolour-sign.ps1` and `plan-batch.py`, so change a rule
there and never in a script.

| Product class | Border | Text | Red heart |
|---|---|---|---|
| Mr & Mrs family (see SKUs below) | black | black | **yes** |
| Create Your Own - SKU **36967** (`kitchen-personalised-street-sign`) | customer choice | **always black** | no |
| Every other street sign | customer choice | customer choice | no |

Pass `-Sku` and the rule is applied for you:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File production\recolour-sign.ps1 `
  -SvgPath in.svg -OutPath out.svg -Sku 36965 -Colourway Grass
```

**The heart is an EXACT SKU match, never a prefix.** Prefix matching is wrong
because sibling SKUs are different products:

```
ST-001-MR  Mr & Mrs Personalised Street Sign   -> HEART   (re-SKU of 36961)
ST-002-VAL My Valentine                        -> HEART   (re-SKU of 36965-3)
36961      Mr & Mrs (old SKU)                  -> HEART
36965-1-1  Mr & Mrs First Christmas            -> HEART
36965-3    My Valentine (old SKU)              -> HEART
36965-3-1  My Galentine                        -> HEART
ST-003-FAM Family Street Sign                  -> no heart (re-SKU of 36965)
ST-516-YD  Engagement (Yes Day)                -> no heart (re-SKU of 36961-1)
36961-1    Engagement (old SKU)                -> no heart, despite the 36961 base
36961-2    Retirement                          -> no heart, despite the 36961 base
36965      Family Street Sign (old SKU)        -> no heart
36965-3-2  Mother's Day Our Family             -> no heart
```

Heart rules confirmed complete by Max 2026-07-26; the ST-* re-SKUs were mapped to
the same products by handle and title against the live catalogue on 2026-08-06.
Anything not on that list gets no heart - and an unlisted SKU is refused outright.

**build.py draws the heart whenever line 1 contains an ampersand**, because that is
where the locked signature unit sits. It has no idea what SKU it is building. So the
heart decision has to be made from the SKU afterwards, which is what `-Sku` does -
without it, `THE SMITH & JONES FAMILY` on a Family sign comes out with a red heart.
Verified: SKU 36965 with that exact text strips the heart; SKU 36961-2 Retirement
does too, despite sharing the 36961 base.

Signs outside Mr & Mrs rarely contain an ampersand at all, but when they do they
still get **no heart**. Note that with the heart removed the ampersand retains
`signatureHorizontalScale` from build.py, which existed only to seat the heart -
`recolour-sign.ps1` warns about this. Fixing it means touching build.py's approved
layout, so it has been left alone.

**Mounting holes are removed from every sign.** They are physical holes in the
acrylic, so build.py's stroked circles print black rings around absent material.
Removal is the default in `recolour-sign.ps1`; `-KeepMountingHoles` exists only to
reproduce an old proof.

All product classification must come from **SKU** and/or the `_Custom option flow`
attribute - every street-sign product exposes only "Default Title" as a Shopify
option, so Shopify variant options carry no useful information.

## Colourways (exact, validated against the known `#010101`)

Black `#010101` · Grey `#7C7C7C` · Sage `#9AA192` · Grass `#68893C` ·
Blue `#799CAA` · light sage `#BEC0A9` · blush `#EBC3C3` · dusky pink `#CB9CA5`.

These live in `production\product-rules.json` and nowhere else. Any `#RRGGBB` is
also accepted; an unrecognised colour NAME is refused rather than guessed.

Three near-identical blues exist in the source files (`#799CAA` / `#799DAB` /
`#7A9EAC`) - eyedropper drift, not three products. Normalise to one.

Family street signs (SKU 36965) carry a `Colour border` attribute whose values map
onto these names directly.

## Bleed - MANDATORY, 4 mm

**Every printed sign must be bled by 4 mm.** Printing at exactly the blank size
leaves visible white acrylic on any edge where the blank sits a fraction out in the
jig; Max confirmed real prints showing white edges on 2026-07-26 and specified 4 mm.

```powershell
python production\add-bleed.py <styled.svg> <bled.svg> 4.0
```

`add-bleed.py` buffers the real contour outward with shapely and inserts it *behind*
the artwork in the border colour. It does not touch the approved elements. The
canvas grows by the bleed on every side - 578 x 133 mm at Large, 458 x 128 at
Medium - with a **negative viewBox origin of -4,-4**, and that origin is how
`make-imposition.ps1` knows to keep the BLANK, not the canvas, on its jig
coordinate.

Do NOT use a backing rectangle: the sign has four concave scalloped corners and a
rectangle floods them with ink, wasting colour and inking up the paper jig.

The script refuses to run twice on the same file, so bleed cannot be stacked.

**Headroom check:** at 4 mm bleed with 10 mm row gaps, adjacent bleeds come within
2 mm of each other. Anything above 5 mm would overlap, and `make-imposition.ps1`
now refuses it rather than letting one sign print into its neighbour - raise `gapY`
in `bed-layout.json` first.

Historical note: the production PSDs already carried ~1.4 mm per edge, so bleeding
is established practice; 4 mm simply makes it reliable.

## Runs On Any PC

Everything the pipeline needs is in the git checkout. Requirements:

| Need | Why | If missing |
|---|---|---|
| Python 3.13 + numpy, pillow, shapely, fonttools | `build.py`, `add-bleed.py` | `pip install numpy pillow shapely fonttools` |
| Google Chrome or Edge | the SVG->PDF renderer | `svg-to-print-pdf.ps1` searches both and names what it looked for |
| PowerShell 5.1 | the production scripts | ships with Windows |

Deliberately NOT needed:

- **No USB drive.** All three contours are committed in `source/size-contours.json`.
  Only `extract-size-contours.py` touches a USB, only if a cut file changes, and it
  locates the drive itself rather than hard-coding a letter.
- **No absolute paths.** Scripts resolve siblings via `$PSScriptRoot` and the repo
  root, so the checkout works anywhere.
- **No RasterLink** to produce the PDFs. Only the final hot-folder drop and the ENTER
  press need the printer PC.

Fonts are embedded in each generated SVG, so the PDF renders identically on a machine
without Times New Roman installed. `svg-to-print-pdf.ps1` throws if no font program
made it into the PDF rather than shipping fallback glyphs.

## Still Unbuilt

- **Only Large has been physically printed.** Medium and Small are verified in
  software - jig outlines overlaid on the imposed artwork register exactly and the
  bleed falls outside the blank on every edge - but no acrylic has come off the
  machine at either size. Print the jig and dry-fit real blanks before a customer
  order.
- **Small's `capCenterY` is unverified** (see Sizes) and its type sizes, though
  measured, want Max's eye against a real sign.
- Two Medium decisions Max has not ruled on: the frame inset is 9.9 mm, 20% thinner
  than Large's proportion; and line 2 uses em 11.5 as in build.py rather than the
  PSD's 10.583, which affects Large equally.
- Laser/cut handoff. Cut settings recovered from LightBurn: Large = power 75,
  speed 8, **2 passes**; Medium = 75 / 9 / 1; Mini = 75 / 10 / 1.
- Shopify webhook trigger. Deliberately last - automating the front of a pipeline
  whose back half needs a manual button press only queues work. `plan-batch.py`
  still takes an order JSON export rather than calling Shopify itself.
- The hot-folder copy is still manual on purpose. `run-batch.ps1` stops at the PDF.
- The RasterLink **favourite** still defaults new imports to 1200x1200 / 16 pass.
  Set it to 600x900 / 12 pass so hot-folder imports inherit the right condition.

## Response Format

For PRODUCE SIGNS report: order and supported sign count; exact extracted text and
size; `line1HorizontalScale` per sign; output paths; jig positions used; unsupported
items; and explicitly that the ENTER press is still required.

For IMPROVE AUTOMATION report: what changed; what was verified and how; the commit
hash; any remaining production boundary.
