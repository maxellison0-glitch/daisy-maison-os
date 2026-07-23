# DM-C017 prompts and generation settings

Recorded: 23 July 2026

Status: the earlier overlaid prompt/video route remains rejected. The later
locked-real-sign → approved hero → approved white-back → native Seedance route
is validated. Max rated the untouched native video 8.5/10.

## Validated product-calibration gate

Exact prompt:

`working/batches/product-calibration/v01-locked-real-sign-edit/prompt.txt`

Literal instruction under test:

> Keep this real Daisy Maison sign as the locked manufactured object. Change
> only its existing printing to the supplied LightBurn-derived Jannaway
> design.

Reference order:

1. real Daisy Maison printed-front photograph — locked product authority;
2. exact Jannaway face — replacement printing only.

Four identical Nano Banana 2 runs used 16:9, 1K and two references. Each cost
1.5 credits:

- take 01: `6b50a1b2-ac90-4621-a763-bb0ea72a1902`
- take 02: `91c3e535-fe6f-400b-9abe-a5c263ffd681`
- take 03: `4c0831d8-b5b2-4beb-960a-9848a5b76823`
- take 04: `8962bdd9-8bb4-4cc4-880a-2f1850d7d080`

The result fixes the pasted-panel appearance and underweight black border
across all four runs. Max approved untouched Take 03 as the validated product
checkpoint. No output was composited or repaired.

Review:

`working/batches/product-calibration/v01-locked-real-sign-edit/QC_REVIEW.md`

The prompt is promoted in
`../../prompts/wedding-signs/cases/DM-C017-JANNAWAY/01-validated-product-print-edit.txt`.

## Validated synthetic-Max hero gate

Prompt:

`working/batches/hero-still/v05-approved-product-lock/prompt.txt`

The approved product Take 03 is reference 1 and owns the entire sign. The
consented synthetic-Max keyframe is reference 2 and owns identity, clothing,
body scale and workshop only; its invalid marker plate is explicitly ignored.

Four identical 9:16, 1K Nano Banana 2 runs cost 6 credits:

- take 01: `166349ab-b616-4213-b385-f5e028ce7fb1`
- take 02: `a0a8180f-b1c2-4ba0-99fb-160cbea1860b`
- take 03: `6af1cfb7-6542-4690-aeb4-05ebddb997f3`
- take 04: `7aea6341-a82b-47cd-ac72-a855025ee2fc`

All four pass agent review without a product overlay. Max approved Take 01.
The promoted prompt is
`../../prompts/wedding-signs/cases/DM-C017-JANNAWAY/02-validated-synthetic-max-hero.txt`.

## Validated plain-white reverse gate

Prompt:

`working/batches/start-keyframe/v01-white-back-match/prompt.txt`

Four identical 9:16, 1K Nano Banana 2 runs cost 6 credits. Max approved Start
Take 01 after viewing it in isolation. It is completely plain white with the
two genuine mounting holes and no black border or coloured points.

The promoted prompt is
`../../prompts/wedding-signs/cases/DM-C017-JANNAWAY/03-validated-white-back-start.txt`.

## Validated native video prompt

Prompt:

`working/batches/video/v03-native-approved-pair/prompt.txt`

Settings:

- Seedance 2.0 standard;
- 9:16, 1080p, high bitrate;
- eight seconds, generated audio off, multi-shot off;
- approved plain-white start and exact-front end;
- approved product plus real front-edge, back-edge and white-back references;
- privacy-cropped real turn for motion/construction only;
- 72 credits.

Job: `bf94cfac-e34f-4da7-8922-6cfc8322b1fc`.

Max rated the untouched native result 8.5/10 for realism. The promoted prompt
is
`../../prompts/wedding-signs/cases/DM-C017-JANNAWAY/04-validated-native-video.txt`.

## Rejected V03 six-reference still prompt

Exact prompt:

`working/batches/hero-still/v03-real-construction/prompt-base.txt`

Take directions:

`working/batches/hero-still/v03-real-construction/variants.json`

Locked six-reference order:

1. consented synthetic Max identity/composition only;
2. exact Jannaway sign-face artwork;
3. real printed front;
4. real front-to-edge;
5. real back-to-edge;
6. real plain-white back.

References 3-6 are product-only crops from all 300 frames of one real Daisy
Maison turn. The prompt explicitly discards the invalid marker plate in the
identity image and locks a thin pale/white physical edge, white reverse and
black perimeter on the printed front only.

Four Nano Banana 2 jobs ran at 9:16, 1K, one output each and 1.5 credits each:

- take 01: `76d6dd29-6a9a-4f89-b2ed-4913516fd7df`
- take 02: `c5f44c5f-55fe-4617-ad21-7dcb0f3b203a`
- take 03: `4f240f84-0622-488d-805f-191b6cd06763`
- take 04: `01436c8d-b89a-414a-91db-9db1ccd35954`

Take 03 omitted the black front border. Takes 01, 02 and 04 made the printed
black band roughly half its required visual weight. All four are rejected. No
sign surface was composited, replaced or corrected.

## Aborted V04 geometry-correction prompt

`working/batches/hero-still/v04-border-correction/`

This prompt was quoted but stopped before generation, so it spent zero
credits. It still asked the model to reconcile separate artwork, material,
angle and numeric-geometry authorities. Max correctly identified that the
better engineering abstraction is one locked real sign with one permitted
change: its printing.

## Rejected V02 still prompt record

The exact base prompt is preserved at:

`working/batches/hero-still/v02-jannaway/prompt-base.txt`

Take 08 appended this direction:

```text
Geometry-correction maker frame: the OUTER plaque silhouette must be exactly 4.56:1, matching the 570 x 125 mm LightBurn artwork with the correct taller height and shaped ends. Max glances naturally toward the plaque. The workshop contains no duplicate signs, sample signs or legible background wording.
```

The combined prompt is preserved independently at:

`../../prompts/wedding-signs/cases/DM-C017-JANNAWAY/successful-still-prompt.txt`

The filename is historical. It does not mean the complete workflow succeeded.

### Still settings

- Model/job type: Higgsfield `nano_banana_flash` / Nano Banana 2
- Resolution: 1K
- Aspect ratio: 9:16
- Batch discipline: one output per job, six valid takes
- Cost: 1.5 credits per still; 9 credits for the valid batch
- References:
  1. consented synthetic Max/workshop identity and composition;
  2. exact LightBurn-derived Jannaway artwork;
  3. real Daisy Maison physical construction/material reference.
- Selected output: take 08
- Selected job: `48d7a48b-f7dd-4205-9345-bed2775b1d04`

All valid still job IDs:

- take 04: `638bcec0-f347-42e2-9e5c-ff9499991121`
- take 01: `0f67694c-4b09-4a97-9bf5-2591208ffcb1`
- take 02: `28e294fe-942d-4246-874b-85a34136566a`
- take 06: `75610b5a-e9ed-4b6a-a368-8d00e4e6d260`
- take 07: `c256bc4b-3b2e-4065-b3d5-0d127fe2b93c`
- take 08: `48d7a48b-f7dd-4205-9345-bed2775b1d04`

Take 08 was selected for the natural maker glance, plausible anatomy,
recognisable Max and stronger 4.56:1 plaque geometry. Its exact face was then
applied locally in `hero-take-08-exact-face.png`. Max has rejected that method:
the file is a composite and was not a valid video reference. A future source
image must contain the exact sign natively and receive human approval without
an SVG overlay.

## Seedance prompt record — output rejected

The submitted prompt is preserved verbatim at:

`working/batches/video/v02-jannaway/prompt.txt`

A second portable copy is at:

`../../prompts/wedding-signs/cases/DM-C017-JANNAWAY/successful-video-prompt.txt`

The filename is historical. The job and output are rejection evidence.

### Video settings

- Model: Seedance 2.0
- Mode: Standard
- Aspect ratio: 9:16
- Resolution: 1080p, 1080 × 1920
- Bitrate mode: High
- Duration: 8 seconds
- Generated audio: off
- Multi-shot: off
- Job ID: `7d7f3cb6-13ce-4721-bcc1-fc0d369de561`
- Cost: 72 credits
- Start image media ID: `d6675e0b-0224-4220-80b7-bd2692592e08`
- End image media ID: `ed03186d-b8ea-4966-9a4d-a61dbe9b8e8f`
- Additional exact-art reference ID:
  `fec3fcac-f0db-4676-ba99-12a6d23b00f1`

The generated raw file contains 193 frames over approximately 8.0417 seconds.
The finish uses the first 192 frames for an exact 24 fps, 8.00-second delivery.

## Honest prompt-obedience result

Seedance produced one-shot movement, but the product failed:

- the supplied exact-face reference was already a composite;
- the sign becomes much too thick because no real side views were supplied;
- the reverse becomes black because no real white-back reference was supplied;
- the generated face was replaced again in post, creating a visibly whiter
  panel and border seam;
- the action is a diagonal/vertical flip, not the requested pure horizontal
  long-axis roll.

The entire result is rejected.

## Retired deterministic overlay settings

The following records what was done; it is not an approved method. The
finishing script is disabled and these settings must not be reused.

- Canvas: 1080 × 1920
- Frame rate: 24 fps
- Delivery frames: 192
- Track start: frame 70
- SIFT anchor: frame 84
- Track: source-to-frame homography plus backward pyramidal optical flow
- Exact source opacity: full from frame 70
- Mapped range: frames 70–191
- Overlay support: detected photographed white face
- Occlusion: YCrCb/HSV skin evidence restricted to semantic end-grip zones
- Hook: full text fade from 0.04–2.95 seconds
- CTA: full text fade from 4.30–7.90 seconds
- Hook type: Segoe UI Bold
- Master: H.264 High, `yuv420p`, AAC 192 kb/s, fast-start
- Preview: 720 × 1280, H.264/AAC

Future finishing may add hook, CTA, captions, whole-shot colour and sound only
outside the product surface. Native sign frames remain untouched.

## Sound

Sound is generated deterministically at 48 kHz stereo:

- low room texture;
- turn whoosh;
- damped settle/click;
- short reveal chime.

## Higgsfield Windows invocation rule

Do not use the PowerShell/npm `higgsfield.cmd` wrapper for long multiline
prompts. Use:

`C:\Users\Max Ellison\AppData\Local\Programs\nodejs\node_modules\@higgsfield\cli\vendor\hf.exe`

Before an expensive job:

1. pass the prompt as one native argument; on Windows, use the included Node
   `spawnSync` helper when PowerShell splits a long value;
2. avoid unescaped embedded literal double quotes;
3. run `generate cost` with the intended model, media and settings;
4. after creation, run `generate wait <job-id> --json`;
5. reject immediately if aspect ratio, media roles, prompt length, duration,
   resolution or multi-shot state differ.

The six malformed wrapper jobs cost 9 credits. The native route then delivered
all intended parameters.
