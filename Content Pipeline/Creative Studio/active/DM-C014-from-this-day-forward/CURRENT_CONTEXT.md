# Current context

Updated: 21 July 2026

## Status

REDO in progress (22 July). Max rejected the deterministic crop-pan animatic
("zoomed into an image, zoomed out, zoomed out again — pixelated"). New
pipeline per Max + Codex direction: foundation-first — 9:16 base stills built
from original product pixels with outpainted margins only, approved by Max,
now animated with camera-only image-to-video (kling3_0 pro, silent takes from
the approved stills), then frame-level fidelity check, assembly, restrained
sound. Higgsfield generation suite is live in-session (Max fixed the
connector). bytedance upscaler rejected (rewrote lettering); nano_banana_2
prompted restoration accepted for the lid zone only. See COLLABORATION_LOG.md
Turns 8-10.

Delivered (`exports/`): v4 benchmark master (silent + sound) and 720x1280 mobile
copy; v3 first cut (silent + sound + mobile); contact sheets, cut-alignment
blends, and a private case-study artifact
(claude.ai/code/artifact/dcbceae2-36f9-466f-9143-41dc1b226e8e).

## Accepted decisions (Claude + Codex)

- Match cut: pebble centre `(494,761)`, hearts `(822,955)`, equal crop height 600
  at the cut; align by centre-of-mass, not literal shape (Codex pixel analysis).
- Pacing: 8.5s = 48/72/105/30 frames; the cut frame is held rock-steady.
- Finishing (v4): smootherstep easing with exact endpoints; luma-only tone curve;
  saturation 0.97; NO rgb warming; -0.08-stop vignette from 65% radius; monochrome
  grain sigma 32 at 1.5% with a 3-frame rolling average; no camera breath. Codex
  verified the implementation faithful to spec.
- Sound: room tone -34 LUFS + one dry ~100ms stone tick ~-20 dBFS on the cut.
- Higgsfield: recommended to sit this concept out unless a margin-only warm light
  field composites with zero seam; deferred to a future interactive pass.

## Max's objective

Finish one high-end, emotionally tactile vertical advert from a single honest
Daisy Maison product photograph. The edit must feel deliberately engineered,
not like an AI product reconstruction.

## Visual source of truth

`assets/from-this-day-forward-master.jpg`

The photograph contains one coherent real scene:

- an open white gift box;
- its matching `From this day forward` illustrated lid;
- a personalised wedding pebble heart containing two pebble people;
- cream linen and pale wood styling.

The packaged file is the immutable visual authority. All motion must be made
from crops, scale, position and normal colour treatment of that photograph.

- File size: 169,630 bytes
- SHA-256: `267052D20A844A5204B0C481F149FD52700203A28C343FCDE6CBC9B861596A58`

## Locked creative decision

- Tell the wedding story already present in the master image.
- Begin on the lid's paired-heart illustration.
- Match-cut that pair to the two pebble people inside the acrylic heart.
- Pull back to reveal the real gift in its box.
- Use a restrained, premium pace. The transformation is the hook.
- Prove the picture silently before adding text, sound, a hand insert or CTA.

## Rejected directions

- Do not overlay a family-heart design onto this wedding heart.
- Do not ask AI to redraw, replace or reinterpret the product.
- Do not generate a hand over the still photograph.
- Do not fabricate a box-opening action from one frame.
- Do not outpaint through product pixels or reconstruct printed lettering.
- Do not force the `Family Is a Gift` story onto this wedding master.

The rejected composite failed because the design inside the heart visibly did
not belong to the photographed product. Better masking would not fix the lie.

## Claude and Codex agreement

The real Claude CLI completed a read-only inspection successfully. Claude and
Codex agree that Max's single-master-image correction is the right production
path. The concept mechanism survives; the story changes from family to wedding.

One refinement from Codex: the square master cannot display the entire scene
inside a full-height 9:16 crop. The reveal should favour the open heart and box,
or briefly show the intact square image on a restrained warm-neutral canvas.
Never invent missing sides to make the frame fit.

## Unresolved dependencies

- A higher-resolution original is required before aggressive 1080x1920
  punch-ins become a final master. The supplied 1280px image is sufficient for
  the timing test.
- A real ten-second hand-touch insert is optional after the match cut works.
- Sound, copy, CTA and paid variants wait until picture approval.

## Next physical action

Max reviews the muted cut (v3 or v4) and judges the paired-hearts -> pebble-couple
match. On approval, source a higher-resolution original before any final delivery
master - this is the only true remaining blocker (Codex and Claude agree). Then
decide copy, CTA, an optional Higgsfield margin-atmosphere pass, and paid variants.

## Approval gate

Max is judging only whether the paired-hearts-to-pebble-couple cut feels clear,
tactile and emotionally meaningful. Everything else remains provisional.
