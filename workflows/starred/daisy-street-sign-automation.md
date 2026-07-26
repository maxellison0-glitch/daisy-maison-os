# Daisy Street Sign Automation

> Canonical Jarvis workflow for Daisy Maison street signs.
> Copy and paste this entire file into Claude, Codex, or another capable AI chat.
> Current production scope: Mr & Mrs, **Large**, black, printed on white acrylic.
>
> **Updated 2026-07-26.** Printing is now IMPLEMENTED and authorised. The previous
> version of this file said never to send anything to a printer or hot folder; that
> rule is superseded, and the reasons are recorded below.

## Start Here

You are operating Daisy Maison's street-sign system. There are three modes:

1. **PRODUCE SIGNS** - order numbers to printed signs.
2. **IMPROVE AUTOMATION** - modify, debug, test, or extend the system.
3. **NEW SIZE** - extend to Medium or Mini (not yet built; see Sizes).

Infer the mode from Max's request. Ask only if genuinely ambiguous.

## Source Of Truth

`%USERPROFILE%\AA Daisy Maison OS\projects\daisy-street-sign`

Run `git pull --ff-only` from `%USERPROFILE%\AA Daisy Maison OS` before changing
files. Do not create a copy elsewhere.

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

## Produce Signs

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

Supported line: **SKU 36961** with `Size` starting `Large`. Read `Line 1` and
`Line 2` exactly - never silently correct spelling, punctuation or spacing.
Customers do type `MR&MRS CHAMBERLAIN` with no spaces, and that is legitimate.

Ignore upgrade/add-on lines (`ACC-*`, `Size Upgrade`) - no personalisation on them.

### 2. Generate the artwork

```powershell
& 'C:\Users\Max Ellison\AppData\Local\Programs\Python\Python313\python.exe' `
  artwork\build.py "<ORDER>" "<LINE1>" "<LINE2>" 486 "artwork\orders\<ORDER>.svg"
```

Python 3.13.9 is installed per-user with numpy, pillow, shapely, fonttools.

Watch `line1HorizontalScale`. build.py only auto-flags below 0.55, but anything
under ~0.70 is visibly condensed and worth showing Max (`MR&MRS CHAMBERLAIN` came
out at 0.672; `MR & MRS YATES` at 0.990).

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

### 4. Impose up to three on a bed

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command `
  "& 'production\make-3up.ps1' -SignSvgs 'a.svg','b.svg','c.svg' -OutSvg 'production\3up.svg'"
```

Use `-Command`, not `-File`: `-File` flattens the array into one comma-joined string.
Then convert the 3-up SVG with the same `svg-to-print-pdf.ps1`.

**Three is the hard maximum.** Four signs need 285,000 mm2 against a 256,200 mm2
bed, and 570 mm exceeds the 420 mm axis so rotation cannot help.

Jig positions (blank top-left, mm): **(20, 12.5) / (20, 147.5) / (20, 282.5)**.
The 20 mm side margins are forced by 610-570. Independently corroborated by the old
PC's production PSDs, which sat at Y 12.1 / 147.0 / 280.6.

**POS 2 is exactly bed centre**, so a single sign there needs no assumption about
which corner is the origin - use "Arrange in the Center".

### 5. Print the jig (once per fresh bed)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File production\make-jig.ps1 `
  -ContourSvg artwork\orders\<any>.svg -OutSvg production\jig-3up.svg
```

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
pattern is in `memory/rasterlink7-gui-automation.md`. Essentials:

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
| Large | **570.00 x 124.99** (409-vertex contour) | 3 | **yes** |
| Medium | **450.00 x 120.00** | 3 | no |
| Mini | **289.72 x 85.00**, 13 mm corner radius | 8 | no |
| Mini Football | 150.6 x 50.3 | 14 | no |

**Shopify's "Small 28 x 12cm" IS the Mini.** The listing's 12 cm height is wrong -
the real blank is 85 mm. Shopify "Medium 45 x 12cm" matches the 450 x 120 cut
exactly. There is no separate product called "Small".

Mini historical 8-up positions: X ~10 and 315, Y ~10 / 108 / 206 / 303.
Medium 3-up: X ~71.7, Y ~10.7 / 145.5 / 278.

## Colourways (exact, validated against the known `#010101`)

Black `#010101` · Grey `#7C7C7C` · Sage `#9AA192` · Grass `#68893C` ·
Blue `#799CAA` · light sage `#BEC0A9` · blush `#EBC3C3` · dusky pink `#CB9CA5`.

Three near-identical blues exist in the source files (`#799CAA` / `#799DAB` /
`#7A9EAC`) - eyedropper drift, not three products. Normalise to one.

Family street signs (SKU 36965) carry a `Colour border` attribute whose values map
onto these names directly.

## Bleed

Production PSDs print a panel of ~572.94 x 127.76 against a 570 x 125 blank - about
**1.4 mm bleed per edge**, already established practice. Max asked for 2 mm.
Implement as an expanded canvas plus a `#010101` backing rectangle behind the
untouched artwork, keeping the blank at the same jig coordinates. Do not alter the
approved artwork to achieve it.

## Still Unbuilt

- Medium and Mini generators, jigs and imposition.
- Laser/cut handoff. Cut settings recovered from LightBurn: Large = power 75,
  speed 8, **2 passes**; Medium = 75 / 9 / 1; Mini = 75 / 10 / 1.
- Shopify webhook trigger. Deliberately last - automating the front of a pipeline
  whose back half needs a manual button press only queues work.
- The RasterLink **favourite** still defaults new imports to 1200x1200 / 16 pass.
  Set it to 600x900 / 12 pass so hot-folder imports inherit the right condition.

## Response Format

For PRODUCE SIGNS report: order and supported sign count; exact extracted text and
size; `line1HorizontalScale` per sign; output paths; jig positions used; unsupported
items; and explicitly that the ENTER press is still required.

For IMPROVE AUTOMATION report: what changed; what was verified and how; the commit
hash; any remaining production boundary.
