# Repeatable white wedding-sign Reel automation

Status: **validated only for the approved white wedding-sign family after the
DM-C017 Jannaway v03 native proof.**

Automation supports product preparation and QC. It does not paste product
graphics onto video.

The full validated method is
`../../WEDDING_SIGN_ENGINEERING_PROMPT_WORKFLOW.md`. Max rated the untouched
native v03 video 8.5/10 for realism.

Do not use this automation for coloured signs with black text, coloured signs
with coloured text or non-wedding products. Those need separate successful
still and native-video proofs first.

## What can become automatic

After a display-safe sign idea is selected, local tools may:

1. build the exact Large SVG from the audited Daisy Maison sign system;
2. rasterise the canonical transparent PNG;
3. create the exact 570 × 125 mm visual PDF;
4. assemble a prompt/reference manifest for Higgsfield;
5. verify that required printed-front, back-to-edge, front-to-edge and
   white-back references are present;
6. record prompts, model settings, IDs, outputs and costs;
7. extract untouched native frames for human and machine QC;
8. add hook, CTA, captions, sound and delivery encoding only where they do not
   alter or cover the sign.

The automation must not read more Shopify data than required, mutate Shopify,
submit paid work without the agreed gate or publish.

## What is permanently forbidden

- reusing Jannaway motion with a different sign face;
- whole-panel replacement;
- replacement white field or border;
- tracked lettering-only correction;
- planar tracking, corner pinning or homography for product graphics;
- masks/inpainting that hide the native sign under canonical artwork;
- using a composited exact-face still as a video reference;
- treating OCR, IoU or source-pixel provenance as proof of physical realism.

The rejected compositor entry points are retired and deliberately raise errors:

- `tools/composite_exact_face_still.py`;
- `tools/composite_reel.py`;
- `tools/make_tracking_plate.py`;
- `tools/finish_seedance_reel.py`;
- `tools/run_render.ps1`.

`tools/build_next_reel.py` is restricted to exact SVG/PNG/PDF asset generation.

`tools/scaffold_wedding_sign_reel.py` is the reusable next-wedding-sign
entrypoint. It inserts new display-safe wedding wording, prepares the exact
artwork, adapts the four validated prompt stages, creates reference slots and
locks every human gate. It requires explicit confirmation that the new product
belongs to the validated white wedding-sign family. It cannot submit paid
work, overlay a product or publish.

Use `VIDEO_PREFLIGHT.md` before any new still or video spend.

## Required human gates

### Gate A — sign idea

Choose real demand-backed wording or a clearly labelled invention. Names and
intended sign wording are acceptable display content. Never carry addresses,
contact, payment or unrelated customer data into production.

### Gate B — locked product image

Give Higgsfield:

- one real Daisy Maison printed-front photograph as the locked manufactured
  product; and
- the exact SVG/PNG as replacement printing only.

Use the literal instruction to keep the real sign and change only its existing
printing. Generate 4-8 inexpensive identical-prompt takes so repeatability is
measured without adding pose or identity variables. Do not overlay the SVG
afterwards. A human must approve one untouched take in which the exact sign
already looks physically real.

### Gate C — synthetic-Max hero image

Give Higgsfield the human-approved product image as the locked sign authority
and the consented synthetic Max/workshop references as identity/context truth.
The product may not be redesigned while adding Max, the pose and the vertical
composition. A human must approve the untouched hero image.

### Gate D — four-view construction pack

Before video, require:

- printed-front real sign;
- back-to-edge/rear-three-quarter view;
- front-to-edge/front-three-quarter view;
- back-facing real sign showing the white reverse.

The side views lock the genuinely thin profile. If they do not clearly show
thickness and edge construction, the gate fails.

For DM-C017 this gate is complete. The source is one real Daisy Maison turn,
not four unrelated images:
`source/real-product-reference-pack/instagram-DPjdseCDbDR/REFERENCE_PACK.md`.
All 300 frames are available and the product-only crops exclude the person's
face.

### Gate E — paid native video

Quote and submit one eight-second, 1080p, 9:16, 24 fps target, no-multi-shot
video only after Gates B, C and D pass. Use native `vendor\hf.exe`, one intact
prompt argument and returned job JSON verification.

### Gate F — untouched product QC

Inspect the native output before any edit:

- exact wording/font/heart/border;
- thin profile through both edge-on phases;
- white reverse;
- rigid shape and mounting-hole/end construction;
- coherent lighting, reflections, blur, hands, occlusion and shadows;
- monotonic continuous turn with no hard cut;
- large readable final hold.

If any product point fails, reject and regenerate. Do not patch.

## Exact-asset command

The retained script is asset-only:

```powershell
& "C:\Users\Max Ellison\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" `
  ".\tools\build_next_reel.py" `
  --line1 "MR & MRS NEXTNAME" `
  --line2 "ESTABLISHED 2026" `
  --slug "DM-C017-NEXTNAME"
```

It creates the exact SVG/PNG/PDF and stops. It cannot render a Reel or reuse a
planar track.

## Complete next-sign scaffold

```powershell
& "C:\Users\Max Ellison\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" `
  ".\tools\scaffold_wedding_sign_reel.py" `
  --line1 "MR & MRS NEXTNAME" `
  --line2 "WHEN TWO NAMES BECOME ONE 1ST JANUARY 2027" `
  --slug "DM-NEXT-NEXTNAME" `
  --demand-source "shopify-read-only-demand" `
  --real-master ".\source\real-sign-front.jpg" `
  --confirm-white-wedding-sign
```

Dry-run verification completed on 23 July 2026. It generated no files, spent
no credits and confirmed that paid submission, product overlays and publishing
remain disabled.

The generated run manifest starts at `awaiting human-approved product image`.
After each human gate, record the approved file and SHA-256. Only the final
native-video stage is paid, and it remains one quoted Seedance job rather than
a batch.

## Why this boundary exists

DM-C017 demonstrated that a deterministic graphic can be exact while the
physical object looks fake. Its replacement face was a different white from
the surrounding border; it also lacked the scene's material response. Missing
side/back references let Seedance invent excessive thickness and a black
reverse. Automation made the wrong result repeatable.

The new system automates preparation and evidence while keeping physical sign
creation native and human-approved.
