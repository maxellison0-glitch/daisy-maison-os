# Building Freya as a Consistent Higgsfield Character

Accurate as of the live Higgsfield connector available in this workspace —
this describes the real mechanism, not a guess. Balance at time of writing:
**1,382 credits, Max plan** — check `balance` again before spending, it
moves with other production work in `Creative Studio`.

Do not run any step past Stage 1 until Max has approved the direction in
`FREYA.md`.

## The core mechanism: Soul characters

Higgsfield's character tool trains a reusable identity — a **Soul** — from
5–20 reference images of one person. Training takes about 10 minutes and
runs in the background; once it reports ready, that identity can be reused
indefinitely to generate new images and video of the same face, in Soul V2
(images) or Soul Cinema (video) — without re-uploading references every
time. This is the tool for exactly what "build a consistent female
character" means.

The constraint that matters: a trained Soul only works with those two
models. Anything outside them — including the higher-end image/video models
already proven elsewhere in this repo (Nano Banana, Seedance) — needs the
lighter-weight **Elements** system instead: save one image as a reusable
reference, usable across many more models, but with a weaker identity-lock
across big pose or expression changes than a trained Soul gives.

## The bootstrapping problem

Soul training needs 5–20 *existing* images of the same person. Freya doesn't
exist yet, so there's nothing to photograph. The real workflow needs an
extra first stage that a real-person Soul wouldn't need.

**Stage 0 — Hero portrait.**
Generate one strong, clean reference image from the appearance spec in
`FREYA.md` — neutral, front-facing, even daylight, no stylised filter. This
is the ground-truth face. One cheap generation.

**Stage 1 — Human approval of the hero.**
Max reviews this single image before another credit is spent — the same
discipline already used for every product image in Creative Studio:
`agent-pass` is never `max-approved`. If the face is wrong, iterate here;
it's the cheapest point in the whole process to fix it.

**Stage 2 — Reference expansion set.**
Once the hero is approved, generate 8–15 more images using the *approved
hero itself* as a reference each time — varying angle (three-quarter,
profile), varying expression (neutral, smiling, mid-laugh, considering),
while holding wardrobe, lighting and the signature "tell" accessory
constant. Feeding the same hero back in each time is what keeps drift down;
regenerating from the text spec alone will not reliably produce the same
face twice.

**Stage 3 — Human QC on the set.**
Reject any image where the identity has drifted — different nose, jaw, eye
spacing, face shape, or where the freckle pattern or the signature ring or
earrings have vanished. Bad references poison the training that follows.
This is a five-minute visual check and it's worth doing properly, the same
way the wedding-sign work rejects anything that "looks pasted on" no matter
what the automated checks say.

**Stage 4 — Train the Soul.**
Submit the approved image set under the confirmed name, 5–20 images. Runs
roughly 10 minutes in the background; check status by the returned
character ID until it reports ready.

**Stage 5 — Generate from the trained Soul.**
Once ready, every future image uses Soul V2 with that character ID. Every
future video moment uses Soul Cinema the same way. No more reference
juggling.

## Consistency toolkit — what actually breaks a face across generations

- Eye colour drifting between shots — restate it explicitly in every prompt,
  don't assume it carries over.
- Face slimming or widening across angles — the signature accessory (the one
  ring, the one earrings) is the fast visual tripwire; if it's present but
  the face reads different, reject the shot.
- Freckle pattern or hairline shifting — same tripwire logic.
- Lighting or wardrobe drifting toward a glossier, more "influencer
  ring-light" look than the rest of the brand's photography — brief
  against this actively. It's the fastest way to make her look like a
  separate, fake-feeling world from the real product shots.
- Over-symmetric, airbrushed skin — the single biggest "AI tell." Brief for
  real texture and natural asymmetry every time, not just in the hero shot.

## Voice and talking video — phase it, don't jump straight to lip-sync

Two separate capabilities exist and don't need to be adopted together:

- A dedicated voice-creation tool builds a consistent voice identity,
  already authorised for use in this workspace per Creative Studio's
  `CLAUDE.md` ("use ElevenLabs... without requesting permission for each
  normal production step").
- Soul Cinema can animate a trained Soul into video, including talking,
  once a voice exists.

Recommended sequencing — this mirrors the "cheap proof before expensive
spend" discipline already proven on the wedding-sign work:

**Phase 1 (start here).** Freya as a caption voice and a *non-talking*
on-screen presence — styled stills, hands, reactions, holding product,
walking the workshop, choice/carousel content. No lip-sync risk, cheap to
iterate, and it's exactly what her actual content role (curation, choices,
captions) needs first.

**Phase 2 (later, optional).** Once the identity is locked and a few dozen
non-talking shots have proven consistent, graduate to short talking-to-
camera clips — FAQs, "quick pick" reveals — using Soul Cinema plus her
voice. This is where lip-sync and uncanny-valley risk actually live, so it's
the right thing to de-risk *after* the face is proven, not at the same time.

## Credit discipline

Treat this exactly like every other Creative Studio spend already logged in
`MEMORY.md`: cheapest proof pass first (Stage 0's single hero image), human
approval gate before Stage 2's larger batch, and never repeat a failing
generation strategy — if the hero face isn't landing after two or three
attempts, stop and change the spec rather than brute-forcing variations.
Re-check `balance` before Stage 2 and before any video work; it's shared
with the rest of Creative Studio's production spend.

## Logging

Once Max approves a direction, this build should follow the exact same
provenance discipline already used for every Higgsfield generation in this
repo: record the winning prompt, model, character ID, job IDs, and the
approved reference set inside a new Freya concept folder under
`Content Pipeline/Creative Studio/active/`, the same way DM-C017 and DM-C016
are tracked. This document covers only the character-identity build — once
she's approved, ordinary content production for her runs through Creative
Studio's existing `README.md` → `CURRENT.md` → `MEMORY.md` process like
everything else.

## Ethics and disclosure

Confirmed, not just trending (research pass, 23 July 2026): TikTok's 2026
Synthetic and Manipulated Media policy requires visible labels on
AI-generated content depicting realistic people, with automated detection
and a four-tier penalty (warning → reduced distribution → removal →
account action). Meta auto-flags and supports labelling on
Instagram/Facebook too. Labelling itself doesn't appear to cost reach — the
real risk is platform classifiers deprioritising generic/uncanny AI output
regardless of disclosure, which is exactly what the "no AI spectacle"
consistency toolkit above already guards against.

Concrete requirements, not just principles: use each platform's AI-content
disclosure toggle on anything featuring Freya before it publishes. Never
let her appear in paid advertising without whatever labelling the platform
requires at the time. Never let her make a first-person factual claim (a
review, a "this happened to me" story) that isn't true. Keep her current
build non-talking/non-lip-synced (Phase 1 above) for now — realistic
talking-head AI video is the category facing the tightest platform scrutiny
right now, so it's the right thing to stay cautious on longest.

`FREYA.md`'s positioning section also names a real alternative worth
knowing about: an overtly stylised/mascot-format character sidesteps this
whole disclosure question rather than managing it. Not adopted here, but
cheap to switch to now and expensive to switch to after Soul training —
worth Max seeing that fork explicitly rather than it staying implicit.
