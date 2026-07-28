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

**No paid generation without Max's explicit go in the conversation.** Not
implied by a previous approval, not implied by "carry on".

Measured 24–28 Jul 2026 — see `Content Pipeline/VIDEO_MODEL_COSTS.md` for the
full table:

| Model | Spec | Credits |
|---|---|---:|
| Veo 3.1 Lite | 4s silent | 4 |
| Hailuo 2.3 Fast | 6s 768 | 4 |
| Seedance 1.5 Pro | 4s silent | 4.8 |
| **Seedance 2.0 Mini** | **720p/fast 6s** | **15** |
| **Seedance 2.0** | **1080p/std 6s** | **54** |

**Default to `seedance_2_0_mini` at 720p.** TikTok re-encodes to roughly 720p
regardless, so 1080p/std is usually 39 credits thrown away by the platform we
most want to win on. Escalate to full Seedance 2.0 only when the printed
wording or the product must stay pixel-locked across the clip.

Daily posting at 54 credits is ~1,620/month. At 15 it is ~450. **Cadence is the
cure for a dormant account and cost is what stops cadence**, so the cheap tier
is a strategy decision, not a saving.

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
