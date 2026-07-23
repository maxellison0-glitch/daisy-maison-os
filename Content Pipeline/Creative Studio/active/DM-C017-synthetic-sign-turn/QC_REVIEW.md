# DM-C017 Jannaway QC review

Reviewed: 23 July 2026

## Verdict

**VALIDATED v03 — native product realism passes human review.**

Max watched the untouched v03 native video and rated it 8.5/10 for realism.
The complete engineering method may be reused. Publishing is still blocked
until Max gives separate explicit publishing approval.

The earlier v02 overlaid master remains rejected and must never be reused.

## Fatal failures in the earlier v02 route

| Failure | Visible evidence | Why it invalidates the Reel |
| --- | --- | --- |
| Composited video reference | The selected exact-face still was made by laying the canonical face onto a generated image | Video generation started from an artificial product image rather than a coherent human-approved sign |
| Product-surface overlay | The finished master maps a new face over the moving plaque | The face and object were created by different image processes and do not share physical cues |
| Border colour discontinuity | The replacement white is visibly brighter/cleaner than the surrounding physical border | A moving colour seam exposes the pasted layer immediately |
| Missing thickness reference | The halfway/edge-on sign becomes much too thick | The video depicts a different construction from Daisy Maison's thin sign |
| Missing reverse reference | The revealed back is black | Daisy Maison signs have a white back |

Any one of these is a complete rejection. Together they show the reference
strategy was structurally wrong.

## Why the earlier technical pass was wrong

The following measurements were true but insufficient:

- 1080 × 1920;
- 24 fps, 192 frames, exactly eight seconds;
- one continuous generated motion with no hard cut;
- stable synthetic Max and mostly plausible hands;
- source-derived lettering pixels on frames 70–191.

Those checks focused on file format, continuity and text provenance. They did
not test whether the sign face and physical plaque shared the same colour,
light, surface, edge, thickness and reverse construction. Humans see that
whole object instantly. Therefore the prior “technical pass” is withdrawn.

## Rejected evidence retained

- `exports/DM-C017-JANNAWAY-master-1080x1920.mp4`
- `exports/DM-C017-JANNAWAY-phone-preview-720x1280.mp4`
- `qc/DM-C017-JANNAWAY-V02/DM-C017-JANNAWAY-full-reel-filmstrip.jpg`
- `qc/DM-C017-JANNAWAY-V02/DM-C017-JANNAWAY-source-vs-video-lettering-filmstrip.jpg`
- `qc/DM-C017-JANNAWAY-V02/DM-C017-JANNAWAY-frame-by-frame-lettering-QC.pdf`
- `qc/DM-C017-JANNAWAY-V02/DM-C017-JANNAWAY-planar-track.json`

The track and lettering report are failure diagnostics, not reusable
production assets.

## Future acceptance gate

A future take can pass only when:

- the exact SVG has become a single coherent photoreal sign image;
- a human approves that source image before video;
- printed-front, back-to-edge, front-to-edge and white-back references are
  present;
- the untouched native video preserves exact lettering, thin thickness, white
  reverse, border colour, material, rigid shape, hands and shadows;
- normal-speed phone viewing reveals no composite seam or pasted surface;
- no product-surface replacement was used;
- the hook, readable reveal, CTA, sound, duration and format also pass.

Automated checks may reject a take. They may not override a human product-
realism rejection.

## Current product-image gate

The rejected video verdict above remains unchanged. The V03 six-reference
stills are also all rejected: take 03 omitted the front border and takes 01,
02 and 04 made it too thin.

A new four-take product-calibration batch makes the real Daisy sign photograph
the locked manufactured-object authority and uses the Jannaway face only as
replacement printing.

Review:
`working/batches/product-calibration/v01-locked-real-sign-edit/QC_REVIEW.md`.

- All four remove the pasted-panel look and retain the broad real black border.
- Take 01 is rejected because its heart became a simplified solid icon.
- Max approved Take 03 as the validated product checkpoint.
- No take receives a strict automatic exact-art pass because the heart is
  natively re-rendered rather than demonstrably identical.
- At that checkpoint no video had yet been generated. The later approved hero,
  white-back and native-video gates are recorded below.

## Completed synthetic-Max and native-video gates

Four untouched hero images were generated using approved product Take 03 as
the sole sign authority and the consented synthetic-Max keyframe as identity
and workshop authority.

- All four hero images passed agent review.
- No product surface was composited or repaired.
- Max approved Hero Take 01.
- Max approved matching plain-white Start Take 01.
- One 72-credit Seedance 2.0 video was generated from the approved pair, real
  edge/back construction pack and privacy-cropped real motion.
- Max rated the untouched native video 8.5/10.

Review:
`working/batches/hero-still/v05-approved-product-lock/QC_REVIEW.md`.

## V03 all-frame result

- Native file: 1080 × 1920, 24 fps, 193 decoded frames, 8.0417 seconds.
- Finished master: 1080 × 1920, 24 fps, 192 frames, exactly 8.000 seconds.
- One continuous monotonic 180° vertical-axis turn.
- No hard-cut spike.
- Plain-white reverse: pass.
- Thin pale edge: pass.
- Rigid shape and front-only black border: pass.
- Synthetic Max identity and hands: pass.
- Exact face readable from frame 112 through frame 192.
- All 81 readable frames are in source-comparison pages.
- Readable hold: 3.375 seconds.
- Product-surface overlay: none.
- Hook and CTA do not intersect the protected product region.
- Human native-video realism score: 8.5/10.

Evidence:

- `working/batches/video/v03-native-approved-pair/qc/all-frames-dense-overview.jpg`
- `working/batches/video/v03-native-approved-pair/qc/all-frame-sheets/`
- `working/batches/video/v03-native-approved-pair/qc/lettering-compare-pages/`
- `working/batches/video/v03-native-approved-pair/delivery/qc/verification.json`
