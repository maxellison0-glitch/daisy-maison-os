# Engineering workflow — the sign carousel engine

**Status: BUILT and proven on two plates, 25 Jul 2026. Zero credits spent to
produce 22 finished slides.**

Supersedes the video-first assumption in `SIGN_IN_SITU_WORKFLOW.md` for volume
content. Video is not cancelled — it is demoted to the rare format.

---

## 1. Max's call, which is the reason this exists

> "If we perfected a photo like this and then just did 10 different designs,
> that's about as expensive as a video in terms of credits. You could make a
> carousel of hundreds of ideas for our customers to use. This might be more
> efficient than videos, and videos could become more rare… more opportunities
> for less margin of error, better engagement, and more automation and mass
> manufacturing."

He is right on the economics and right on the error surface, and the second one
matters more.

**Economics.** A paid print-edit generation per wording meant ten designs cost
about what one film costs — and the film is one idea. Now the plate is paid for
once and every wording after it is free. Ten designs or fifty, same cost.

**Error surface.** A film has motion, drift, occlusion, pacing, audio and a
caption layer to get wrong; we shipped one and Max still found two faults in it
(an overlaid string, and a sign that read "almost too perfect"). A reprint has
exactly one thing to get wrong — the printing — and the printing is rendered
from the audited PSD, so it cannot drift. Fewer moving parts, more output.

## 2. What the engine actually does

`templates/sign-reprint/reprint.py`

The expensive part of a print-edit was never the ink. It was establishing the
**photograph**: real material and sheet depth, the true border, the shaped ends,
drilled mounting holes, the contact shadow on the wall, lens character. Once a
plate is approved that is all solved and permanent.

So the engine replaces ink **strictly inside the panel** and nothing else. The
photographed border, shaped ends, mounting holes, edge highlights and wall
shadow are never touched. This honours `Creative Studio/REFERENCE_PACK.md`
exactly rather than bending it: *the approved product photograph is the
authority for the object; the build.py SVG is the printing, and only the
printing.*

| Step | What | Cost |
|---|---|---|
| 1 | `build.py` renders the new wording — any real colourway, heart optional | free |
| 2 | Rasterise, squeeze to the plate's measured sign box | free |
| 3 | Mask to the panel interior, holes punched back out | free |
| 4 | Relight from the plate's own light, match grain and focus | free |
| 5 | Crop 4:5, add the wordmark end-slide | free |

Establishing a new plate still costs ~2 credits per candidate through the
validated print-edit. That is the only paid step, and it is paid once per scene.

## 3. Relighting — the fix for "it looks a little bit fake, almost too perfect"

Max called this by eye. It measures out exactly:

> On the approved cat plate the panel cream held **239 / 231 / 222 across all
> 880px** of the sign's width — under 1.5 levels of variation — while the wall
> behind it swung hard warm in the same daylight.

Real matte cream in that room picks up 8–15 levels of falloff plus a colour
shift toward the window. **Optical flatness is what the eye reads as CGI.** It
is not a texture problem or a resolution problem, and no amount of grain fixes
it.

Two components, both derived from the plate itself so nothing is invented:

1. **Transfer** — reconstruct the panel's true illumination and apply it to the
   new ink, so the reprint inherits the photograph's exposure and colour
   temperature.
2. **Synthesise** — sample the across-width gradient of the wall immediately
   above the sign and apply it, damped. The wall is lit by the same light, so
   its gradient is ground truth for direction and strength; matte board picks up
   less range than emulsion paint, hence the damping.

Result on the cat plate: cream now runs 224.7 → 219.2 in blue across the width,
warming toward the window, and matches the plate's own level to within 0.5.

## 4. The five bugs this cost, all of them silent

Recording these because every one produced plausible-looking output that was
wrong, and three of them would have shipped unnoticed.

| Bug | Symptom | Cause |
|---|---|---|
| Blown panel | cream clipped to 255 in a band across the caps | the light field was estimated by blurring an **inked** panel, so it dipped wherever letters were and the ratio spiked. Fixed with normalised convolution over cream pixels only, which reconstructs the illumination *underneath* the old letters |
| Mask ran to the frame edge | new ink laid over the photographed border | PIL's rank filters replicate the edge pixel at the image boundary, so a silhouette touching the frame does not erode inward from that side. Fixed by padding with transparency before eroding |
| Sign amputated | bottom 14% of every render missing; earlier, a 211px window painted only ~120px | headless Chromium's usable viewport is ~87px shorter than the window it is given, and it pads the screenshot back out with transparency. Fixed by requesting slack height and cropping |
| Line 2 pushed through the border | subtitle clipped in half | two failed attempts to make Chromium stretch the SVG (`meet` letterboxed, `none` silently rendered short and the correction then stretched the type). Fixed by rasterising at the true 570:125 ratio and doing the anisotropic squeeze in PIL |
| Sage blown out and washed | pale colourway lost all contrast | the render's "panel colour" was a mean over bright pixels, and sage lettering at luminance 184 counts as bright, so the divisor was too small. Fixed with a percentile |

**The lesson, again:** every one of these was found by *measuring* the output
against the plate, not by looking at it. Three looked fine at thumbnail size.

## 4b. The "I can tell it came from the SVG" tell — found and fixed

Max: *"the actual sign, I can tell that it was used from the SVG."*

He could see it and could not name it. It measures out unambiguously. Ink
luminance and ink/panel contrast ratio, same product, same colourway:

| | ink | ratio |
|---|---|---|
| **Real photograph** of a real sign, real room (letters) | **38.5** | **0.213** |
| **Real photograph**, border sample | **27.3** | **0.140** |
| The generated plate | 7.8 | 0.034 |
| A reprint on that plate | 11.6 | 0.050 |

**The generated sign is four to six times more contrasty than the real object
ever photographs.** Vector black is `#000` and renders as `#000`. Real black ink
in a real room never comes back below roughly 25–45, because ambient light
scatters off the panel surface into the ink, the lens adds veiling glare, and the
ink is a satin surface rather than a void.

**Absolute blacks in a lit interior are a rendering signature.** The eye reads
them as synthetic instantly, which is exactly why Max could see it without being
able to point at it. It was never a resolution, sharpness or texture problem —
measured edge rise was already 2.0px on both the plate and the reprint, matched.

The fix is the physics in reverse. Glare *adds* a roughly constant amount of
light and exposure then renormalises, so the correction is an affine map chosen
so the panel level stays exactly put and the ink lands on the target ratio.
Nothing moves; it is a grade, not a redraw. Applied across the whole sign
silhouette, letters and printed border together — grading only the panel would
leave reprinted letters lighter than the photographed border around them, which
is a worse artefact than the one it fixes.

Result on the cat plate: ink **11.6 → 47.0**, ratio **0.050 → 0.193**, against
the real photograph's 0.213. Per-plate via `"ink_ratio"` in `plates.json`.

## 4c. Scale — the fault Max called on the sage plate

Max: *"the sizing isn't right for the sage sign. It just looks like a Chinese AI
photo."*

Correct. The real sign is 570mm wide. Read against three independent anchors in
the dog plate's own room:

| Anchor | implies sign should be | oversized by |
|---|---|---|
| panelling dado, floor→rail 680px @ ~1050mm | 369px | **2.08×** |
| golden retriever lying, nose to rump 800px @ ~950mm | 480px | **1.60×** |
| ceramic dog bowl 174px @ ~180mm | 551px | **1.39×** |

It measures **768px** — roughly **1.6× too big**, a 90cm plaque instead of a 57cm
one. That alone explains the reaction.

**And the anchors disagree with each other by 1.5×**, which means the generated
*room* is not internally consistent on scale. That is a second, deeper tell and
**resizing the sign cannot fix it** — only a better plate can.

`rescale_plate.py` corrects the sign size on an existing plate by shrinking the
**photographed** sign rather than redrawing it, so material, border, holes and
contact shadow all survive. It works in ratio space (`patch / wall_estimate`)
rather than pixel space, because scaling pixels drags the old wall tone along and
leaves a visible rectangle. Applied at 0.625× the dog sign is now 480px and
correctly proportioned; a faint tonal trace remains where the old sign was
erased. **Treat it as a repair tool, not a licence to accept mis-scaled plates.**

## 5. Gates — blocking, automated

- **Raster fill.** The 409-vertex contour fills its 570×125 viewBox exactly, so
  the sign must fill its raster edge to edge. Below 99% on either axis the run
  aborts — a silent shortfall is the amputation bug returning.
- **Outside the sign box must be bit-identical to the plate.** Measured at max
  delta 0 on both plates. If anything outside the box changed, the engine has
  touched something it does not own.
- **Round-trip.** Reprint the plate's *own* wording and compare. Cream and ink
  must match the plate within a few levels. Recorded: cat cream 242/235/226 vs
  242/234/228, ink 1/0/0 vs 1/1/1. Dog cream 239/236/224 vs 244/240/229.
- **SCALE GATE — new, and it should have existed from the start.** Before a plate
  is accepted, measure the sign against **at least two** independent objects of
  known real size in the same frame (dado rail ~1050mm, interior door leaf
  ~800–900mm, dog bowl ~180mm, a lying retriever ~950mm nose-to-rump, floorboard
  width ~180–200mm). The sign is 570mm. Reject the plate if the implied width is
  more than **±15%** off, and reject it if the anchors disagree with each other by
  more than **±20%** — that means the room itself has no consistent scale and no
  amount of correction will save it. This gate is what would have caught the sage
  plate before it was ever reprinted onto.
- **INK-RATIO GATE — a floor, not a window.** Ink/panel contrast ratio must be
  **≥ 0.11**; below 0.08 is the vector-black signature and reads as CGI. For BLACK
  specifically expect **0.12–0.24**, the range measured on real photographs.
  *Corrected 25 Jul 2026:* this was first written as a 0.12–0.24 window for all
  colourways, which is wrong — the Freya blue master measures **0.440** and Max
  passed it as the best image in the whole audit. Pale colourways legitimately sit
  high, so an upper bound would fail good work.
- **NO MOUNTING HOLES.** `SIGN_HOLES=0` on every content render. Max's call: they
  read as a laser-cutter artefact. `reprint.py` sets it automatically and paints
  over holes already baked into a plate.
- **Never assert canonical 4.56:1 on an in-situ frame.** The cat plate's sign
  measures 4.17:1 and the dog plate's 4.09:1 on screen; that is real
  foreshortening on a wall-mounted sign, not a defect. Measure the box, do not
  correct it. (Same trap as the QC gate in `SIGN_IN_SITU_WORKFLOW.md` §5.)

## 6. Adding a plate

`templates/sign-reprint/plates.json`, one entry:

```json
"dog": {
  "image": "plate-dog-approved.png",
  "box": [387, 790, 1155, 978],     // measured sign outline in plate px
  "colourway": "SAGE",              // must match the PHOTOGRAPHED border
  "wall_band": 90,                  // px above the sign to sample light from
  "damp": 0.45,                     // how hard the wall gradient is applied
  "crop45": [96, 660, 1488, 2400],  // explicit 4:5 window
  "wordmark_y": 0.30
}
```

Two things that are judgement, not formula, and belong in the config:

- **The crop.** It has to buy the sign large enough that line 2 is legible on a
  phone *and* leave wall above the sign so it is not jammed against the frame
  edge. The first pass took full width from a y offset and got neither.
- **`damp`.** The cat room has a strong window gradient (0.55); the boot room is
  evenly lit, so its wall is weaker evidence (0.45).

**The colourway cannot be changed locally.** The border is photographic, so a
sage plate makes sage signs only. A black-bordered version of a scene is a new
plate and a new ~2 credits.

## 7. Known limits, stated plainly

- **Sage is the softest colourway.** On the dog plate line 1 reads cleanly and
  line 2 reads soft at feed size. That is the real product, not a rendering
  fault — but keep line 2 short on pale plates, and prefer black or grey when
  the sign sits small in frame.
- **Axis-aligned paste.** Fine to about 0.5° of tilt; the dog plate measures
  −0.38° and passes. A visibly rotated or strongly keystoned sign needs a quad
  warp, which is not built.
- **Line 1 is fitted to width**, so short wordings render large. Correct for the
  real product, but it means a two-word sign and a five-word sign look
  different in weight. Sequence a carousel with that in mind.
- **The wordmark is still house-built.** No Daisy Maison logo file exists in the
  repo. Max called the v1 lockup "quite nice" and asked for better, and v2 is in
  `Creative Studio/reference-masters/daisy-maison-WORDMARK-v2.png`. It is
  replaced the moment a real asset arrives.

## 8. Wording — what makes one land

From Max on `THE LITTLE MADAM / SHE RUNS THIS HOUSE`: *"I actually love that."*

**The rule it follows: the sign insults the owner, not the animal.** "She runs
this house" is a confession. "You just pay the mortgage" is a confession.
"Muddy paws welcome — everyone else, wipe your feet" is a confession. The buyer
is the owner, and people buy the joke they are willing to make about themselves.

Signs that describe the pet flatteringly ("GOOD BOY LANE") are the weakest in
both sets and should be dropped or reworked.

## 9. What this changes about the content plan

- **Stills are now the volume format.** One approved plate supports an unlimited
  back catalogue of wordings at zero marginal cost.
- **Video is the rare format**, reserved for when motion genuinely is the story.
  It stays governed by `CONTENT_BRIEF_GATE.md` §"When video is actually worth it".
- **Scene count is the only real budget line.** Each new room, animal or season
  is ~2 credits to establish and then free forever. Spend on *scenes*, not on
  *wordings*.
- The proven scaling unit is a plate, so the roadmap is a list of plates:
  cat house ✅, boot room ✅, then kitchen, hallway, garden fence, bar, Christmas
  mantelpiece.

## 10. Hard rules, unchanged

- The sign is rendered, never generated. The approved photograph is reference 1.
- No filming, no presenter (`CONTENT_BRIEF_GATE.md`).
- Only the five real colourways. `build.py` hard-fails on anything else.
- No customer PII, and never pass real customers' faces to a generator.
- Propose, never publish. No paid credit spend without Max's explicit go.

## 11. Price the paid option BEFORE building the free one

26 Jul 2026. Max asked for the cat reel with a different wall colour. I built a
free local wall-regrade pipeline instead of regenerating the background, and it
took four rounds of debugging. His verdict: *"that's way too much effort, it cost
2 credits to change the background bro... way over engineered."*

He is right, and the mistake is a specific one worth naming: **"free" was
optimised for the wrong resource.** Credits are cheap and abundant; Max's
attention and the day's momentum are not. A 2-credit regeneration would have put
three options in front of him in minutes.

**The rule: before writing any code to avoid a generation, state the credit cost
of just generating it.** If that cost is under ~10 credits, generate. Only build
the free path when it is genuinely reused many times over (the wording reprint
engine qualifies — it replaces an unlimited back catalogue of paid renders; a
one-off wall colour does not).

Free is not automatically the right answer. Cheap-and-now beats free-and-slow.

## 12. Do not hand-build pixel pipelines on moving footage

Same day, the harder half of the same lesson. The wall regrade and the
string paint-out were both mathematically fine on single frames and both
looked wrong in motion. Max: *"the string is not consistent, it's like a
literal video effects glitch... the rendering you did looks awful."*

Stills forgive a seam; 24fps does not. A per-frame fit that is 2px out on one
frame reads as a flicker, and a horizontal inpaint band that is invisible in a
still crawls when the frame moves. Frame-by-frame QC cannot catch this — only
watching the encoded video can, and by then the time is spent.

**The rule: on video, change the product wording and nothing else.** The sign
composite is safe because it is identical on every frame. Backgrounds, lighting
and anything the camera moves through get changed by regenerating the clip, not
by local processing. Stills remain the place for free pixel work.
