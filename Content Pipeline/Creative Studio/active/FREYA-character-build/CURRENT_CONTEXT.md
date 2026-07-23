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

The remaining 7 retry images were generated with the same improved prompt
but have **not yet been individually eyeballed** — only their auto-generated
text descriptions were read, which this whole exercise already proved is an
unreliable proxy for the actual pixels. Also worth noting: on this same
path, my requested "wider waist-up framing" shot (`s2-10-waistup-attempt.png`)
came back as another tight face crop — the enhancer overrides framing
instructions, not just style ones.

**Verdict: do not proceed to Stage 4 Soul training on this set as-is.**
Either Max reviews the full retry set and picks the images that actually
hold the brand's look, or a follow-up session completes the individual QC
pass before any are used to train a persistent identity. Training a Soul on
a mixed-quality reference set would bake the drift in permanently.

**Standing finding for future batches:** the `soul_2` + image-reference
generation path has a structural bias toward glossy/editorial styling that
prompt wording alone cannot fully suppress. Options for next time, not yet
tried: generate the expansion set with `nano_banana_pro` instead (different
provider/pipeline, may not carry the same forced enhancement), or wait until
Stage 4 training exists and generate directly from the trained identity
rather than through ad hoc image-reference conditioning.

## Next action

Human review of `working/stage-2-reference-expansion/retry-set/` — confirm
which images hold the locked look, then either regenerate the rejects with
the `nano_banana_pro` alternative or proceed to Stage 3/4 with only the
confirmed-good subset.
