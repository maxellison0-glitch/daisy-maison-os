# Wedding-sign video production rules

Status: **locked production rule**, confirmed by Max on 23 July 2026.

This rule applies to the validated white Daisy Maison wedding-sign image and
video family, including drafts presented for review. It is not evidence that
coloured signs, coloured lettering or non-wedding products are solved.

The complete engineering implementation is
[`WEDDING_SIGN_ENGINEERING_PROMPT_WORKFLOW.md`](WEDDING_SIGN_ENGINEERING_PROMPT_WORKFLOW.md).
DM-C017 Jannaway v03 is the first validated proof: Max rated its untouched
native video `8.5/10` for realism on 23 July 2026.

For the current DM-C017 evidence and spend gates, also complete
`active/DM-C017-synthetic-sign-turn/VIDEO_PREFLIGHT.md`.

## Gate 1: the source sign image must be human-approved

Do not start a paid video generation from an image that contains a pasted,
corner-pinned or otherwise composited sign face.

The required source-image workflow is:

1. Put the chosen wording into the audited Daisy Maison SVG system.
2. Choose one real Daisy Maison sign photograph as the locked manufactured-
   object master.
3. Give Higgsfield that real master first and the exact SVG/LightBurn face
   second. The literal instruction is: keep this sign exactly as manufactured;
   change only its existing printing to the supplied design.
4. The real photograph owns border weight, silhouette, holes, material,
   proportions, hand contact, light and surface response. The SVG owns the
   replacement wording, letter forms, spacing, heart and line placement. Do
   not make border, thickness or construction independent design tasks.
5. Generate 4-8 inexpensive identical-prompt takes to test repeatability before
   adding identity, pose or motion variables.
6. A human must approve one untouched product image.
7. Use that approved product image as the locked sign authority when creating
   the synthetic-Max hero image. A human must approve the untouched hero image
   before it can become a video start/end frame.

An agent metric, correct OCR or source-exact pixels do not equal human
approval. If no image passes, there is no valid video input yet.

### Why

DM-C017 used a locally overlaid exact-face still as a Seedance reference. That
made the video inherit an artificial face rather than teaching it one coherent
physical product. The later video could never repair that invalid starting
point.

The first native correction also failed because it split product truth across
flat artwork, angle references and written geometry. The model treated the
black front band as something it could redesign and made it too narrow or
removed it. Locking one real sign and permitting only a printing change
removes that ambiguity and produces a surface that looks physically coherent
to humans.

## Gate 2: four physical views are mandatory

Every video request must include a human-approved physical reference pack:

1. front-facing sign;
2. back-to-edge or rear three-quarter view;
3. front-to-edge or front three-quarter view;
4. back-facing sign.

The two edge views must make the real thickness, edge profile, corner shape
and face-to-edge relationship readable. The back view must show the actual
white reverse and mounting-hole construction. Use real Daisy Maison
photographs or clear frames from real Daisy Maison video. Record the provenance
of every frame.

Do not infer thickness from the front SVG. Do not let a video model invent the
reverse. If a required view is unavailable or ambiguous, video generation is
blocked until the reference exists.

### Why

DM-C017 supplied front artwork but no credible halfway/edge or reverse product
truth. Seedance therefore invented an overly thick plaque during the turn and
a black back. Real Daisy Maison signs have a thin physical profile and a white
back. Both changes describe a different product, so the video is invalid
regardless of motion quality.

## Gate 3: no product-surface overlays

Forbidden final-video techniques include:

- a whole-panel replacement;
- a replacement white field or border;
- tracked lettering, even when it is source-exact;
- planar tracking, corner pinning or homography used to paste artwork onto the
  moving product;
- masks or inpainting used to hide the generated face under a new graphic;
- a post-render 3D or 2D texture laid over an already generated sign.

The exact LightBurn-derived sign may be used to create and approve the source
still or a genuinely rendered physical scene. It must then survive the native
video generation as part of the photographed/rendered object. If the video
model changes a letter, colour, border, proportion or material cue, reject the
video and regenerate it. Do not patch it.

### Why

Humans do not judge a sign by lettering accuracy alone. They instantly compare
the sign face with the rest of the object and scene.

An overlaid face does not inherit the same:

- white balance, exposure and colour falloff;
- acrylic grain, reflections and specular highlights;
- border tone and edge thickness;
- lens softness, motion blur and compression;
- finger contact, occlusion and contact shadows;
- perspective, parallax and frame-to-frame lighting changes.

In DM-C017 the replacement panel was visibly whiter than the generated
physical border. That moving colour seam made the face look pasted on. The
lettering could be mathematically exact and automated QC could pass, but the
object still looked fake and unacceptable to a human. Once the composite is
visible, the whole advert loses trust.

This is a human-perception failure, so pixel provenance, text similarity,
homography quality and hard-cut checks cannot overrule it.

## Locked product truths during the turn

The following must remain true in every native frame:

- exact SVG wording, font, heart, border and proportions;
- thin sign thickness matching the approved edge references;
- white front field and white back;
- black border as front-face artwork, with a thin pale/white physical edge;
- rigid, flat construction with no bending or swelling;
- mounting holes and end shape consistent with the real product;
- physically coherent fingers, occlusion, reflections, shadows and motion
  blur.

Any breach rejects the complete take. Do not salvage part of it with an edit.

### Front border and physical edge are different properties

Never use the word `thin` without naming the **physical sheet depth**. It must
not be interpreted as a thin or underweight printed front border.

For the audited 2280 × 500 Jannaway source:

- complete front artwork: 2280 × 500, exactly 4.56:1;
- white inset: 2180 × 400;
- black printed band: 50 source pixels at top and bottom, exactly 10% of the
  complete front-face height on each side;
- physical side edge: shallow and pale/white, visible only through perspective.

The printed black band must retain the exact SVG weight. A narrow outline,
hairline border or missing band is a different product and rejects the image
or video.

## Required native video workflow

1. Build the exact sign from the audited LightBurn-derived system.
2. Assemble the four-view real-product reference pack.
3. Use the real front as a locked product master and the SVG only as
   replacement printing. Create 4-8 identical-prompt low-cost product images.
4. Obtain explicit human approval of one coherent, non-composited product
   image.
5. Use the approved product as the locked sign authority to create and obtain
   approval for a synthetic-Max hero image.
6. Generate the continuous video using that approved hero image plus the front,
   both edge and white-back references.
7. Inspect the untouched native video frame by frame and at normal phone
   playback speed.
8. Reject and regenerate if any letter, colour, border, thickness, back,
   proportion, material, hand interaction or temporal behaviour changes.
9. Add only edit elements that do not alter or cover the product surface.

If the selected video model cannot preserve the native sign, that model or
generation route has failed this job.

The current real-product construction example is:
`active/DM-C017-synthetic-sign-turn/source/real-product-reference-pack/instagram-DPjdseCDbDR/REFERENCE_PACK.md`.

## Allowed finishing

- opening hook outside the sign;
- captions and CTA outside the sign;
- colour work applied coherently to the whole shot;
- sound design and music;
- timing, encode and phone-preview preparation.

No final asset passes until it looks physically credible next to real Daisy
Maison Instagram footage. Max remains the final product-realism gate.
