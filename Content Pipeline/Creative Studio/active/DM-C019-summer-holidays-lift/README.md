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
request. When this video was made those frames existed only as a description:
`active/DM-C017-synthetic-sign-turn/source/real-product-reference-pack/instagram-DPjdseCDbDR/REFERENCE_PACK.md`
survived, the images did not.

**They were recovered later the same day** — out of git history rather than off
Instagram, with all five SHA-256 hashes re-verified. So the constraint below was
real when this take was shot and is **no longer in force**. The next sign video
can turn. See that `REFERENCE_PACK.md` for how they were lost and why the loss
was silent.

Gate 2 exists because of exactly one failure: with no edge or reverse truth,
Seedance invented a thick slab and a black back, and real Daisy Maison signs are
thin with a white reverse. That failure is a property of *turning* the sign. So
rather than run a turn on missing references and hope, the motion was designed
so the sign stays front-on for every frame — its edge and its reverse are never
in shot, and the gate's failure mode cannot occur.

This was a genuine constraint, not a preference — and it has since been lifted.
**The four reference frames are back, so the turn is available again and it is
the stronger shot.**

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
because the four physical reference frames it needs were missing from the repo
on the day. The lift was what was left, not what was best. Those frames have
since been recovered, so that excuse is spent — see `../../../DISTRIBUTION_PLAN.md`
§3a.

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

## v2 — the cut that actually went out

Max, 28 July, after seeing v1: *"try and get a bit smarter with the captions,
and also I want to use our circular profile picture off Instagram for the outros
instead of the square Daisy maison... let's just do some exciting, higher-level
video effects."* Same 6 seconds of paid footage, everything above it rebuilt.
**Zero additional credits.**

### The three components, finally doing three different jobs

`ad-creative/hook-system` says the visual, the on-screen line and the caption
must never restate each other. v1 spent its caption slot describing the picture.

| Slot | v2 |
|---|---|
| Visual | she lifts the sign until it fills the frame |
| On-screen | "She says she's fine." → "She is **not** fine." |
| Caption | "Drop your wording in the comments and we'll make it 🤍" |

The hook never names the season and never counts days — the sign does both. It
makes a claim and the product contradicts it, so the punchline is the product.
The caption then does the one job neither of the others can: it asks for a
comment. That is `DISTRIBUTION_PLAN.md` §3e wired into the post itself rather
than left as a plan, because every reply is a sign we can make for free.

### The mark

The rectangular wordmark is gone. The outro now carries the **circular brand
roundel — the account's own profile picture**, cropped to the exact bounding box
of the drawn circle so a 50% radius lands on the edge instead of shaving it or
leaving a white rim.

Sourced from **TikTok, not Instagram**: Instagram's public endpoint answered 429
and the cooldown runs in hours. Same mark, different door.

### The motion

From `hyperframes-animation`. One tempo grid (`PULSE = 0.4s`) drives every
entrance, so the piece locks to a pulse instead of drifting on hand-tuned
offsets, and each line gets a **different** entrance rather than one reused
helper:

- line one — scale-and-focus slam, `power4.out`, out of a 14px blur
- line two — side snap from `x: -300`, `expo.out`
- the underline under "not" wipes in a beat later, in GRASS `#68893C`, a real
  production colourway
- the roundel lands as a **stamp press** — oversized and soft, snapping to size
  on `expo.out`, releasing one ring on impact

**No `back.out` anywhere.** The skill is blunt that bouncy overshoot is the
clearest tell of a machine-made video, and the words stay ink `#4A3A2C` with the
colour doing only decorative work, so all five text checks pass WCAG AA.

**Still no tween on the footage.** A synthetic push-in over real generated
motion would walk straight back into the thing this whole piece exists to stop
doing.

### Gates

`check` 0 errors, 5/5 WCAG AA. Framing gate PASS on all 180 frames. Hook pills
measured centred to within 1.5px. Render 47s, zero credits.

## Status

**Published to TikTok, 28 July 2026.** `PUBLISH_COMPLETE`, post id
`7667548310357544224` (publish id `v_pub_url~v2.7667548146414897185`). Public,
comments/duet/stitch open, AIGC declared, "Idea 15" by Gibran Alcocer attached at
volume 60 with the video's own audio muted.

This is the first Daisy Maison post to go out of this pipeline. There is no
per-video TikTok analytics endpoint we can read without a signed request, so
whether it worked will show up as a `heartCount` delta between daily snapshots
from `tools/social_api/tiktok_public.py` — a proxy, not a measurement, and it
must be quoted as one.

Max's calls, recorded because they are his to make: **no commercial-content
disclosure** (his own account, his own product, connection self-evident from the
profile) and that track over the two alternatives.

Instagram remains unpublished. Publishing needs Max's explicit go, separately,
every time.
