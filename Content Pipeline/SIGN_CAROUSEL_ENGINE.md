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
