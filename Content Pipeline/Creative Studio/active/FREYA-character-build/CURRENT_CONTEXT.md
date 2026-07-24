# Freya character build — living context

Updated: 23 July 2026

## Objective

Build Freya (proposed social/creative-lead character,
`Content Pipeline/Personas/FREYA.md`) as a consistent, reusable Higgsfield
Soul identity, following the staged workflow in
`Content Pipeline/Personas/HIGGSFIELD_CHARACTER_BUILD.md`.

## Stage 0 — hero portrait candidates (complete)

Four independent candidates generated in one batch to give a real choice
before committing to an identity, the same "cheap proof pass" discipline
already used for street-sign product stills.

- Model: `soul_2` (Higgsfield Soul 2.0, resolved internally to
  `text2image_soul_v2`), one-off mode — no `soul_id` yet, nothing trained.
- Aspect ratio requested `4:5`, served as `3:4` (closest match). Quality 2k.
- Cost: 1 credit total for the batch (0.12 credits exact). Balance before
  spend: 1,382 (Max plan).
- Prompt (identical for all four, only the seed varied):

  > Photorealistic portrait of a British woman in her late twenties, soft
  > oval face shape, warm brown eyes, natural unsculpted eyebrows, a light
  > scatter of freckles across her nose and cheeks, mid-brown hair with a
  > natural wave worn loose at shoulder-to-collarbone length. Real skin
  > texture, visible pores, natural asymmetry, no airbrushing or beauty
  > retouching. Wearing a single thin gold ring on her right hand. Dressed
  > in soft cream linen. Soft natural daylight, warm neutral palette, matte
  > cream and putty background with hints of light natural wood, gentle
  > realistic shadows, shallow depth of field. Neutral, genuine,
  > front-facing expression, direct eye contact with camera, calm and warm.
  > Boutique editorial photography style, natural prime-lens look,
  > photorealistic — no illustration, no cartoon style, no glossy influencer
  > sheen, no artificial symmetry.

- Candidates and job IDs (stored in `working/stage-0-hero-candidates/`):
  - `candidate-01.png` — job `8210e6a7-8228-4440-926d-0ae8e822bf45`, seed 406192
  - `candidate-02.png` — job `c0656acb-6dad-477f-8e16-dd8bd219d0da`, seed 107820
  - `candidate-03.png` — job `368014cd-bd1a-402f-9d1e-cebbea50c60e`, seed 444827
  - `candidate-04.png` — job `3fc1751d-a84f-4b7a-b9af-1b7cf5e32873`, seed 698768

## Agent QC pass (agent-pass, not max-approved)

All four match the brief: freckles present, warm brown eyes, mid-brown wavy
hair, the signature thin gold ring, cream linen wardrobe, warm neutral
setting, real skin texture — no obvious anatomical or "AI spectacle" tells
(hands, jewellery, eyes all read clean). They are four **independent**
identities (different seeds), not four angles of one locked face — expected
at this stage, and exactly why one has to be chosen before Stage 2's
reference-expansion set is built from it.

Agent recommendation: **candidate-03** — warmest, most genuine expression,
clearest freckle detail, reads closest to the "approachable social lead"
brief rather than a polished editorial model. Candidate-01 is the runner-up.
This is a recommendation only; `agent-pass` is never `max-approved`, and the
face that becomes the brand's public identity is Max's call alone.

## Decision

**Approved — candidate-03** (job `368014cd-bd1a-402f-9d1e-cebbea50c60e`).
Max confirmed 23 July 2026. This is now the locked hero: every future
reference and generation for Freya traces back to this image.

## Stage 2 — reference expansion (partial pass, human review still needed)

10 shots attempted (varied angle/expression), all using candidate-03's job
ID as the image-conditioning reference. Two generations logged below because
the first failed QC and the second is a partial, not full, fix. Full images
in `working/stage-2-reference-expansion/`.

**First attempt (`rejected-first-attempt/`, 8 images) — FAIL, batch-level.**
Model `soul_2`, no explicit `enhance_prompt` set. QC against
`Content Pipeline/PUBLISH_READINESS.md` dimension 4 (brand tone / no AI
spectacle) failed across the whole batch: deeper fake tan, oiled/dewy skin
sheen, added blonde/caramel hair highlighting absent from the hero, lower
necklines than the brand's real product photography, and a "fashion
campaign" intensity replacing the hero's warm expression. Root cause:
Higgsfield's own prompt-enhancer rewrote the prompt on this generation path
(confirmed by the returned job params — `enhance_prompt` came back `true`
here vs `false` on Stage 0's plain text-to-image batch), injecting language
like "sun-kissed... healthy, hydrated glow" and "modern editorial or
commercial fashion photography" never written into the source prompt.

**Attempted fix:** pass `enhance_prompt: false` explicitly. **Result:**
silently rejected — `"Higgsfield Soul 2.0 does not support this parameter"`.
Not a usable lever on this model/path.

**Second attempt (`retry-set/`, 10 images incl. one extra close-crop and one
re-run of the waist-up shot) — PARTIAL PASS.** Same reference, prompt
strengthened with explicit negatives ("no fake tan, no glossy influencer
sheen, no added hair highlights, matte skin not oiled or dewy"). The
enhancer still fired regardless (still `enhance_prompt: true` in every
returned job, text still contains "model-like"/"editorial" language in all
ten) — but the actual pixel output measurably improved on the images
directly checked. Visually QC'd against the hero (3 of 10 checked in
detail):

- `s2-01-retry.png` (three-quarter, neutral) — solid pass. Matte skin, no
  added highlighting, calm expression close to the hero. Freckle density
  reads slightly heavier than candidate-03 — worth a second look before
  treating as a training reference.
- `s2-04-retry.png` (intended: genuine mid-laugh) — expression fail. Reads
  as a sultry parted-lip look, not a laugh; the requested expression did not
  land. Neckline also lower/more open than the brand's real product
  photography ever shows.
- `s2-09-close-crop.png` (close front-facing crop, candid smile) — same
  neckline issue as above; expression itself is fine.

**Full QC pass completed (all 10 individually eyeballed, not just described)
— verdict is worse than the initial partial-pass read:**

| Image | Requested | Verdict | Why |
|---|---|---|---|
| `s2-01-retry` | 3/4 left, neutral | **PASS** | Matte skin, hair/eye colour match the hero, closest thing to a real second angle |
| `s2-02-retry` | 3/4 right, smile | FAIL | Hair lightened toward caramel highlights not in the hero |
| `s2-03-retry` | profile, considering | FAIL | Eye colour drifted hazel/green (spec is warm brown); hair significantly lighter; deep tan; low neckline |
| `s2-04-retry` | genuine mid-laugh | FAIL | Reads sultry, not a laugh; neckline too low |
| `s2-05-retry` | elevated angle, warm smile | Borderline | Genuinely warm expression, but hair highlighting drift |
| `s2-06-retry` | looking down at object in hands | FAIL | Requested scenario not delivered at all — no object, wrong pose |
| `s2-07-retry` | mid-sentence | Borderline | Expression intent landed, but hair/tan/neckline drift into fashion-editorial territory |
| `s2-08-retry` | hand near jaw | FAIL | Eye colour drift (hazel/green again), heavy tan, low neckline |
| `s2-09-close-crop` | candid smile | Borderline | Expression fine, neckline runs low |
| `s2-10-waistup-attempt` | wider waist-up framing | FAIL | Model didn't deliver the requested framing at all — still a tight face crop |

**1 clean pass out of 10.** This is a harder finding than "brand tone
drift" — two separate shots show genuine identity drift (eye colour), not
just styling. That's a different, more serious category of failure per
`Content Pipeline/PUBLISH_READINESS.md` dimension 3.

**Verdict: this generation pathway — one hero image as an image-reference,
batch-generated — is not reliable enough to build a persistent Soul
identity from.** Not "needs a look before training," but "the method
itself needs to change before more credits go into it," per the KILL
criteria in `PUBLISH_READINESS.md`: the concept survives (candidate-03 and
`s2-01-retry` prove Freya *can* look right), the batch-generation method
against a single reference doesn't.

**Recommended next attempt, not yet tried:** either (a) generate one shot
at a time with immediate QC before the next, rather than an 8-10 batch on
trust, (b) try `nano_banana_pro` instead of `soul_2` for the expansion set
— different pipeline, may not carry the same drift — or (c) skip ad hoc
reference-conditioning entirely and wait until enough individually-approved
shots exist to train a Soul directly, generating all future images from
that trained identity instead of a single reference image each time.

## Next action

Do not spend further credits training Stage 4 on this reference set. Next
session should retry Stage 2 with method (a) or (b) above before
attempting Stage 4 again.
