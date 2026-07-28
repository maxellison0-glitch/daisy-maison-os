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

## Why the first frame is safe — and where that claim stops

Gate 1 requires a human-approved source image, so the start frame is
`reference-masters/PLATE-summer-holidays-BLACK-freya-hallway-APPROVED.png`,
already approved and already carrying the phone-snapshot look. No new image
generation was needed or paid for.

**But frame 1 is not pixel-identical to that plate, and it would be wrong to
claim it is.** The plate is 896x1200 (3:4); the output is 1080x1920 (9:16).
Seedance closed that gap by extending the canvas **vertically** — roughly 474px
of ceiling and floor that no human ever approved.

Measured, rather than assumed: the sign occupies **72.0%** of the frame width in
the approved plate and **71.8%** in take 02 frame 1. The horizontal framing —
and with it the sign-to-body scale Max signed off — carried over intact. It is
the vertical margin that is new.

So Gate 1 is satisfied on the thing it exists to protect, the product, and the
generated part is empty hallway.

## References and roles

One reference per question, and the prompt says which answers which — the rule
from `REFERENCE_PACK.md` that separates approved output from rejected output.

| Role | File | Answers | Explicitly NOT taken |
|---|---|---|---|
| `start_image` | `PLATE-summer-holidays-BLACK-freya-hallway-APPROVED.png` | identity, room, wardrobe, light, framing, wording | — |
| `image` | `street-sign-BLACK-on-white-MASTER.jpg` | the physical object: thin rigid sheet, shaped ends, border weight, holes, sheen, finger contact | its wording, its workshop, its person, its framing |

## Verdict

**Take 01 rejected. Take 02 agent-pass, and Max has seen it.**

His read, 28 July: it renders well, the size looks real, it works — *"but it's
just a tiny bit boring. Literally, we're just pushing a sign forward."*

That is correct and it is worth recording why rather than filing it as taste.
A 180° turn is the format the numbers actually like — the account's best post
ever is a real sign turning, at 11,889 views — and it was unavailable here only
because the four physical reference frames it needs are missing from the repo.
The lift was what was left, not what was best. See `../../../DISTRIBUTION_PLAN.md`
§3a: those frames are recoverable from Daisy Maison's own reel, for free.

## Spend

| | Credits |
|---|---|
| Take 01 (rejected) | 54 |
| Take 02 | 54 |
| Image generations | 0 |
| **Total** | **108** |

Audio is off deliberately — native audio is an uncontrolled variable and sound
is a decision to make on purpose, later.

Balance 993.12 → 885.12. A future take of this kind should use
`seedance_2_0_mini` at 720p/fast: **15 credits**, measured, and TikTok
re-encodes to roughly 720p anyway.

## Status

Not published. Not approved for publishing. That needs Max's explicit go,
separately, every time.
