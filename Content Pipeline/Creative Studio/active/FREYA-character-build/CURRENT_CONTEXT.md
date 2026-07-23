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

**Pending.** Waiting on Max to pick one candidate (or reject all four and
adjust the spec) before any further spend.

## Next action

On Max's pick: lock that image as the hero, update this file with the
decision, then run Stage 2 (8–15 image reference-expansion set using the
approved hero as a reference each time) per
`HIGGSFIELD_CHARACTER_BUILD.md`, followed by Stage 3 human QC before Stage 4
Soul training.
