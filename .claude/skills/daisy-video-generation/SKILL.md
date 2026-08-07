---
name: daisy-video-generation
description: >-
  Use BEFORE spending any Higgsfield credit or generating any Daisy Maison video
  or product image — Seedance, Veo, Kling, Hailuo, start/end frames, reference
  images, sign turns, product motion. Also use when the user mentions
  'Higgsfield', 'Seedance', 'credits', 'generate a video', 'turnaround',
  'make it turn', 'start image', 'end image', 'reference', 'the sign moves', or
  asks why a generation looked wrong. Encodes the gates, the reference-role
  discipline and the cost table this business has already paid to learn. Not a
  substitute for the generic `video` skill — this is the part that costs money
  when skipped.
---

# Daisy Maison — generating video and product imagery

Every rule here was bought. Two of them cost 54 credits each to learn in a
single afternoon. Read this before quoting a price, choosing a model, or
writing a prompt.

**Read `.claude/product-marketing.md` first** for the product truth and the hard
constraints — especially *Max does not film*, *no customer faces into a
generator*, and *propose, never publish*.

---

## Spend rules

**Never estimate a cost. Call `get_cost` and quote the number it returns.**
Prices differ by duration, resolution, audio and model tier, and a guess has
already been wrong.

*And `get_cost` does not always preflight.* On 28 Jul 2026 `get_cost: true`
passed at the **top level** of `generate_video` was silently ignored and the
job ran — 18 credits for a prompt that said "test". On this tool the flag goes
**inside `params`**, and the safest quote is a completed job's own price. If a
preflight comes back with a job `id` and `status: "pending"`, it is not a
preflight; it is a generation.

**Spend authority, CHANGED by Max on 7 Aug 2026: the daily social session
holds a standing budget of 60 credits/day** ("I'm going to give you a budget
of 30 credits a day... Up the budget to 60 credits, actually") with free rein
for organic content. Inside that ledger no per-spend ask is needed; the
take-home entry logs every credit. Anything beyond the daily 60 still needs
Max's explicit go in the conversation — not implied by a previous approval,
not implied by "carry on". His own proven lane for reference: a liked still
animated with Kling, 5s 1080p, ≈12 credits (the MEDICI reel).

**NEVER GENERATE THE SAME PROMPT TWICE IN ONE BATCH.** Added 28 Jul 2026 by
Max, after two identical 18-credit video takes: *"Don't ever make two videos of
the exact same thing. That is such a waste of credits. We could have had two
different styles… we could by contrast oppose it to Instagram and TikTok. Such
a waste."*

The still-image habit of "generate four, pick one" **does not transfer to
video.** On stills a take costs 2 credits and the variance is the point. On
video a take costs 18–54 and the same prompt returns the same idea twice, so
the second take buys nothing but a coin flip on framing. If two video takes are
worth paying for, the second one must differ in something a viewer would
notice: a different hook beat, a different length, a different aspect for the
other platform, a different bit of business. **Same footage twice is the one
outcome that is never worth the credits.**

The corollary: the way to de-risk video framing is not more takes, it is the
`end_image` law below and a `start_image` that is already correct.

Measured 24–28 Jul 2026 — see `Content Pipeline/VIDEO_MODEL_COSTS.md` for the
full table:

| Model | Spec | Credits |
|---|---|---:|
| Veo 3.1 Lite | 4s silent | 4 |
| Hailuo 2.3 Fast | 6s 768 | 4 |
| Seedance 1.5 Pro | 4s silent | 4.8 |
| Seedance 2.0 Mini | 480p/fast 6s | **6** |
| **Seedance 2.0 Mini** | **720p/fast 6s** | **15** |
| **Seedance 2.0 (full)** | **720p/std 4s** | **18** |
| Seedance 2.0 (full) | 720p/fast 6s | 21 |
| **Seedance 2.0 (full)** | **720p/std 6s** | **27** |
| **Seedance 2.0 (full)** | **1080p/std 6s** | **54** |

### Model tier and resolution are separate axes — this was being conflated

Every full-Seedance row above was re-quoted with `get_cost` on 28 Jul 2026.

The choice had been read as **15 or 54**, and it never was. **The full model at
720p costs 18 credits at 4s and 27 at 6s.** Resolution is what carries the 54,
not the model — and TikTok re-encodes to roughly 720p regardless, so 1080p is
27 credits handed to a platform that discards them.

So the real ladder is: `mini` at 15 for anything where the wording is not the
point, **full at 720p for 18–27 when it is**, and 1080p only when the asset has
a life outside TikTok. The old rule sent us from 15 straight to 54 whenever
lettering mattered; three-quarters of that jump bought resolution nobody sees.

Daily posting at 54 is ~1,620 credits/month. At 27 it is ~810, at 15 ~450.
**Cadence is the cure for a dormant account and cost is what stops cadence**,
so the tier is a strategy decision, not a saving.

*Not yet tested:* whether full-at-720p actually holds lettering better than
mini-at-720p. It is 12 extra credits to find out, and until someone does, do
not write it down as fact.

### Free levers, verified

- **`bitrate_mode: "high"` costs nothing.** 720p/std 6s quotes 27 either way;
  1080p/std 6s quotes 54 either way. A higher output bitrate means less
  compression on high-frequency detail, which is exactly what printed lettering
  is made of. There is no argument for leaving it on `standard`. **Default it
  on.**
- **`aspect_ratio` accepts `3:4` explicitly** (also `4:3`, `1:1`, `21:9`,
  `auto`). See the Gate 1 caveat below — the invented ceiling and floor is
  likely an unset parameter, not a fact about the model.
- **`generate_audio: false` saves nothing** (15 vs 15 on mini). Turn it off for
  silence if you want silence, not to save money.
- `genre` defaults to `auto` and takes `action`/`horror`/`comedy`/`noir`/
  `drama`/`epic`. Untouched here so far; `auto` is the honest default for a
  product clip.
- `mode: "fast"` exists on the **full** model too (21 at 6s/720p) — a rung
  between mini and full-std that had not been noticed.
- `duration` runs 4–15s. 4s is a real cost lever: it is 9 credits cheaper than
  6s on full/720p, and a turnaround does not need six seconds.

---

## The three gates

From `Content Pipeline/Creative Studio/WEDDING_SIGN_VIDEO_RULES.md`. All three
must pass before a request is submitted.

**Gate 1 — a human-approved source image.** Start from an approved plate in
`Creative Studio/reference-masters/`. Never start from a flat SVG: the SVG is
the *printing*, not the product.

*Caveat learned 28 Jul:* the start frame is not necessarily pixel-identical to
the plate. Seedance extended a 3:4 plate to 9:16 by generating ~474px of ceiling
and floor. Horizontal framing carried over (sign width 72.0% → 71.8% of frame),
the vertical margin did not. So Gate 1 protects the product, not the whole
frame — claim exactly that and no more.

*And probably self-inflicted:* the model's schema lists `3:4` as a supported
`aspect_ratio`. The extension looks like an **unset parameter defaulting to
9:16**, not a property of the model. Next 3:4 plate, pass `aspect_ratio: "3:4"`
and see whether the ceiling stops appearing. Until that runs, treat the
paragraph above as the observed behaviour and this as the likely cause.

**Gate 2 — four real physical views in every request:** front, front-to-edge,
back-to-edge, plain white back. They live in
`active/DM-C017-synthetic-sign-turn/source/real-product-reference-pack/instagram-DPjdseCDbDR/`.

Without them Seedance invents **a thick slab with a black back**. Real signs are
thin with a white reverse — that is a different product, and it is the specific
failure Gate 2 exists to stop. The failure is a property of *turning*, so a
front-on shot sidesteps it honestly when the frames are unavailable.

Those files went missing once and the loss was **silent**, because `.gitignore`
hides `Content Pipeline/**/*.jpg` and an ignored file cannot show as deleted.
They were recovered from git history, hash-verified, and force-added. **If they
vanish again, check `git log --all --objects` before the network** —
Instagram rate-limits in hours, `git cat-file` is instant and byte-exact.

**Gate 3 — no product-surface overlays in generated video.** No corner-pin, no
homography, no pasting artwork onto a surface in a moving frame. It produced a
visibly pasted panel once. The paste-a-wording route is approved for **stills
only** — that is what makes comment-to-sign viable at zero credits, and it must
never migrate into video.

---

## The law of the end frame

**`end_image` is the only hard limit the model respects on how far motion
travels.**

DM-C019 take 01 was thrown away over this. The prompt said the sign comes toward
the camera; only a `start_image` was supplied; nothing stopped it. The sign was
fully in frame for 2.0s and ran off both edges for the remaining 4.0 — so the
readable hold, the part a viewer actually looks at, had letters missing. Motion
excellent, product unreadable, **54 credits worthless**.

DM-C017 scored 8.5/10 with a start *and* an end frame. Lock both ends. An
`end_image` is not a nicety.

A native, uncomposited frame from a previous take makes a good end frame.

---

## One reference per question

From `Content Pipeline/Creative Studio/REFERENCE_PACK.md` — the discipline that
separates approved output from rejected output.

State in the prompt **which reference answers which question, and what must NOT
be taken from each.** Worked example:

| Role | Answers | Explicitly NOT taken |
|---|---|---|
| `start_image` — approved plate | identity, room, wardrobe, light, framing, wording | — |
| `image` — product master | thin rigid sheet, shaped ends, border weight, holes, sheen, finger contact | its wording, its workshop, its person, its framing |

Roles available: `start_image`, `end_image`, `image_references`,
`video_references`, `audio_references`.

Decline preset recommendations that fight the brief — pass `declined_preset_id`.
A dramatic lighting preset offered for a bright hallway snapshot is wrong.

---

## QC before you look at anything else

**Run the framing gate first.** It is a hard gate, not a formality:

```bash
python3 "Content Pipeline/Creative Studio/active/DM-C019-summer-holidays-lift/qc_framing.py" <video.mp4>
```

It decodes every frame and fails if the sign comes within 24px of either side.
Copy it alongside any new sign video.

*How it finds the sign, and why the obvious method fails:* by the **longest
contiguous dark run in the densest dark row**, because the printed border is a
long unbroken horizontal line and nothing else in a hallway is. Naive
dark-pixel *extent* returns the full frame width on every frame — a coat and a
doorway are also dark — and silently reports a pass-shaped answer to the wrong
question. That was the first attempt and it was wrong.

**The scale gate.** Sign width against shoulder width must land **1.20–1.45**
for a man. Calibrated on Max's own verdicts: 1.33 passed, 2.19 was "really off".

**The phone-snapshot rule.** House standard on anything with a person: focus on
the product, not the face; add flaws, never quality. Polish reads as an advert;
this brand's best-performing asset is a phone video of a real sign.

---

## Overlays are free — use them

The footage is the only part that costs credits. Hooks, captions, sign-offs and
timing are HTML rendered locally by hyperframes in ~47 seconds at **zero
credits**.

So one good take is not one post. It is one asset that ships repeatedly with a
different hook each time — cheeky, then romantic, then sentimental. Budget per
*post* falls by however many hooks a take can carry.

Compositions live in `Content Pipeline/Creative Studio/video/`; see that
README plus `hyperframes-core`, `hyperframes-animation` and `motion-doctrine`
for the motion craft. Overlays sit in the **top third** — TikTok's own UI owns
the bottom and the right.

---

## Leads from outside — not bought yet, so not doctrine

Surveyed 28 Jul 2026. Of six public Higgsfield "skill" repos, one is
MIT-licensed and substantive, one is unlicensed and avatar-led, one is a thin
wrapper, the rest are template filler or SEO. **Nothing was worth installing.**
Nobody has written the thing we actually want — a documented craft for keeping
printed wording legible on a rotating product.

There is a reason for that, and it is worth knowing: arXiv 2511.05573 (Nov
2025) states plainly that **no prior work has targeted preserving text across
frames during video synthesis**, and its own remedy is a training-data
intervention. **There is no prompt that fixes this.** Every remaining lever is
indirect — bitrate, resolution, shorter motion, fewer degrees of rotation,
supplying the wording as its own reference. That retroactively justifies
rendering overlays locally instead of generating them.

What did survive the filter, all **unverified against this account**:

| Lead | Source | Cost to settle |
|---|---|---|
| A **logo/text reference image** is Bytedance's own nominated route for "stricter text appearance requirements" — supply the wording as a reference rather than describing it. Closest thing to a documented answer to our #1 failure mode. | Seedance 2.0 vendor docs | ~18 credits |
| Seedance 2.0 supports **video-edit Replace** across SKUs. One earned motion take could in principle be re-skinned to new wording. **But it re-generates the printed surface**, which is the exact thing Gate 3 exists to stop — so this is a test, not a plan, and a failure here is expected rather than surprising. | heymarmot | ~21 credits |
| **Negative prompts may not exist** — the claim is that every token reads as positive instruction, so "no blur" summons blur. **Our own evidence argues against it** (see below), so treat the claim as doubtful rather than pending. | OSideMedia (MIT) | already checked |
| **Label reference roles in the prompt text**, not only in the API role field: "use image 1 as the character reference, image 2 as the product". A text-layer echo of the discipline already enforced at the API layer. | heymarmot | free |

**One of those leads is already contradicted here, which is why they are not
rules.** The "never use negatives" claim does not survive contact with this
account: the Bond product-calibration prompt carries four *do not* / *must not*
clauses and the approved hero prompt carries five, and both produced
Max-approved output — one of them the chain that ended in the 8.5/10
turnaround. Negations have been load-bearing in every prompt that has ever
worked here. **Do not strip them out on a stranger's say-so.**

**A real one for turnarounds:** Higgsfield's own Kling start/end guide warns to
*avoid extreme perspective differences between the two frames*, and says the
model handles micro-movement far better than long travel. **A 180° sign turn is
an extreme perspective difference by definition.** That is a documented reason
turns fight the interpolator, and an argument for splitting a turn into two
shorter arcs rather than pushing one clip harder. Kling also takes its aspect
ratio from the start frame, unlike Seedance — a model-choice fact for
plate-shaped sources.

Asset ceiling, per vendor docs: **9 images, 3 video clips, 3 audio clips, 12
total** per generation. The four-view Gate 2 pack is well under budget, so
adding views costs nothing but upload time.

**Do not promote any row above into a rule until it has been run.** This file's
whole claim is that its rules were bought.

---

## Provenance

Every batch records, in the active concept folder: both job IDs, the SHA-256 of
every input, the gate results, the verdict per take, and the credits spent. Use
`agent-pass` and `max-approved` as **distinct states** — an agent may reject an
obvious failure but may never mark something production-ready.

---

## Related

`video` (generic AI-video craft) · `hyperframes-*` and `motion-doctrine`
(the zero-credit overlay lane) · `image` (still generation) ·
`daisy-paid-media` (where a winning creative is worth the most) ·
`Content Pipeline/DISTRIBUTION_PLAN.md` (why the turnaround format is the target)
