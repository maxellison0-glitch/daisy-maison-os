# DM-C019 — "The summer holidays" lift

A real native video, not a still with motion laid over it. Task #9.

Max, 28 July 2026, rejecting the previous attempt: *"an image with video formats
around it is just a useless concept. If we're doing a video, it needs to be a
video, not an image with rendered text."*

## What this is

Six seconds, 9:16, 1080p, one continuous take. Freya stands in the hallway
holding `THE SUMMER HOLIDAYS / DAY 4 OF 42` and raises it toward the camera
until it fills the frame and holds there, readable.

The sign is on-season to the day. UK schools break up in the last week of July,
so "day 4 of 42" is roughly today — this is a piece of content with a shelf life
measured in days, which is the point of having a pipeline that can turn one
around in an hour.

## Why the sign never turns

DM-C017 proved a 180° turn at 8.5/10 realism, so the obvious move was to reuse
it. It was not available, for a reason worth writing down rather than
rediscovering.

`WEDDING_SIGN_VIDEO_RULES.md` Gate 2 requires four real physical views —
front, front-to-edge, back-to-edge and plain white back — in every video
request. Those frames are described in
`active/DM-C017-synthetic-sign-turn/source/real-product-reference-pack/instagram-DPjdseCDbDR/REFERENCE_PACK.md`
but **the image files themselves are not in the repository**; only the markdown
describing them survives. Checked 28 Jul 2026.

Gate 2 exists because of exactly one failure: with no edge or reverse truth,
Seedance invented a thick slab and a black back, and real Daisy Maison signs are
thin with a white reverse. That failure is a property of *turning* the sign. So
rather than run a turn on missing references and hope, the motion was designed
so the sign stays front-on for every frame — its edge and its reverse are never
in shot, and the gate's failure mode cannot occur.

This is a genuine constraint, not a preference. **If those four reference frames
are recovered, the turn becomes available again and is the stronger shot.**

## Why the first frame is safe

Gate 1 requires a human-approved source image. Rather than generate a new hero
and ask for approval, the start frame *is*
`reference-masters/PLATE-summer-holidays-BLACK-freya-hallway-APPROVED.png` —
already approved, already carrying the phone-snapshot look and a passing
sign-to-shoulder scale. Frame 1 is human-approved by construction, and no new
image generation was needed or paid for.

## References and roles

One reference per question, and the prompt says which answers which — the rule
from `REFERENCE_PACK.md` that separates approved output from rejected output.

| Role | File | Answers | Explicitly NOT taken |
|---|---|---|---|
| `start_image` | `PLATE-summer-holidays-BLACK-freya-hallway-APPROVED.png` | identity, room, wardrobe, light, framing, wording | — |
| `image` | `street-sign-BLACK-on-white-MASTER.jpg` | the physical object: thin rigid sheet, shaped ends, border weight, holes, sheen, finger contact | its wording, its workshop, its person, its framing |

## Spend

| Item | Credits |
|---|---|
| Cost quoted before submission (`get_cost`) | 54 |
| Seedance 2.0, 6s, 1080p, std, 9:16, audio off | 54 |
| New image generations | 0 |

Balance before: 993.12. Audio is off deliberately — native audio is an
uncontrolled variable and sound is a decision to make on purpose, later.

## Status

Not published. Not approved. Publishing needs Max's explicit go, separately.
