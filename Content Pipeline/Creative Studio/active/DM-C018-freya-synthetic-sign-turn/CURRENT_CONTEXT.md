# DM-C018 current context

Updated: 24 July 2026

## Objective

Test whether the DM-C017 engineering method (real product photo as the
locked manufactured-object authority, one human-approved hero image before
any video spend) works when the person is Freya instead of Alan — proving
the workflow generalises across characters before it's assumed to.

## Hero-still generation

Single take, not a batch (direct application of the lesson from
`Creative Studio/active/FREYA-character-build/CURRENT_CONTEXT.md`'s Stage 2
finding: generate one, QC it properly, rather than batch-and-hope).

- Model: `nano_banana_pro` (resolved internally to `nano_banana_2`).
- Two references: (1) the real, unedited product photo
  `Creative Studio/active/DM-C017-synthetic-sign-turn/source/real-product-reference-pack/instagram-DPjdseCDbDR/product-only-crops/01-front-product-only.jpg`
  as the locked product authority; (2) Freya's locked hero, job
  `368014cd-bd1a-402f-9d1e-cebbea50c60e`, as the identity reference.
- Cost: 2 credits.
- Job ID: `98d31c1a-6bd1-4536-adcd-e4b34eb8517b`.
- Output: `working/hero-still/freya-holding-sign-take01.png`.

## Agent QC pass (agent-pass, not max-approved)

Checked against `Content Pipeline/PUBLISH_READINESS.md`:

- **Product fidelity: pass, verified pixel-by-pixel against the source.**
  Sign wording ("YOU'RE NOT WELCOME (UNLESS YOU'VE BROUGHT SNACKS)"),
  border weight, oval endcaps and font all match the real source photo
  directly compared side by side — not assumed, actually checked.
- **Identity consistency: strong pass, notably better than the Stage 2
  batch.** Warm brown eyes held (no hazel/green drift), hair colour
  consistent with the locked hero (no added blonde highlighting), genuine
  warm smile, matte skin, no glossy sheen. The `nano_banana_pro` + two
  real-image-reference approach clearly handled identity conditioning more
  faithfully here than `soul_2` did in the Stage 2 batch.
- **Brand tone: pass.** Cream linen wardrobe, warm workshop-adjacent
  setting, matches the established product-photography palette.

This is a genuinely strong single take. Still agent-pass, not
max-approved — the same discipline as every other product image in this
repo.

## Take-01 verdict: EDIT — scale failure, caught by Max

Max compared take-01 against Alan's Mr & Mrs Bond hero (Higgsfield job
`9d473e5d-314a-4f9a-a99d-ea4f044d10bc`, 23 July — copy in
`working/qc/alan-bond-hero-9d473e5d.jpeg`) and called the sign undersized.
Measurement confirmed it (`working/qc/shoulder-normalised-comparison.png`):

- Alan Bond hero: sign 1293px / shoulders 791px = ratio **1.63**
- Freya take-01: sign 805px / shoulders 480px = ratio **1.68**
- Shoulder-normalised, the signs render almost identical — but female
  shoulders are ~18% narrower, so equal ratio = a ~13-15% physically
  smaller sign. Same real object on Freya needs ratio ≈ **1.93+**.

This is exactly the failure mode `Creative Studio/MEMORY.md` warns about:
lettering QC passed while whole-object scale was wrong. Agent QC checked
letterforms pixel-by-pixel and skimmed scale; Max's eye caught it in
seconds. Scale check is now a mandatory first step before lettering on any
person-plus-product generation.

## True test (Max's request): new wording + Freya + scale fix

Run as two stages per the validated DM-C017 discipline, not one compound
generation. Wording chosen: **"GO AWAY (UNLESS YOU'VE BROUGHT CAKE)"** —
same novelty family as the real snacks sign (Max's voice note was garbled;
wording is trivially swappable). Not production artwork — engineering
probe only, no audited SVG behind it.

**Stage A — printing replacement on the locked real product.** Reused the
proven Bond printing-replacement prompt structure. Model `nano_banana_2`
(requested as catalog name `nano_banana_pro` — note: Higgsfield executes
that catalog entry as nano_banana_2, so "are we on Nano Banana 2" = yes).
Job `c0644e05-c041-45e7-8da3-ceaa743b1fe9`, 16:9, 2 credits. Output
`working/stage-A-printing/stageA-cake-sign.png`. **PASS**: every character
correct, same letterforms, border/holes/hands/background all survive
untouched.

**Stage B — Freya holding the Stage A sign, scale-corrected.** Three
references: Stage A job (product authority), Freya locked hero (identity),
plus the real human-scale frame
(`instagram-DPjdseCDbDR/selected/01-front-frame-240-t08.000.jpg`, uploaded
as media `9f0cf355-f2e7-4c67-99e3-3bd8309df556`) as SCALE AUTHORITY ONLY —
explicit prompt language that the sign must extend well past her shoulders
and read proportionally larger on her than on a man. Job
`84696b99-06fc-4d05-9ead-c1b36dbc4b04`, 4:5, 2 credits. Output
`working/hero-still/freya-holding-sign-take02-cake.png`, measured QC in
`working/qc/stageB-annotated.png`.

**Take-02 result: scale ratio 2.32** (sign 845px / shoulders 365px) —
past the 1.93 target; reads correct-to-slightly-generous, within
pose/foreshortening noise (sign held toward camera, same as Alan's shot).
Lettering exact through both stages. Identity holds (warm brown eyes, no
hair-highlight drift, genuine smile). Setting landed in a genuine
workshop, closer to brand than take-01's. One continuity nit: the gold
ring appears on her left hand; the spec says right hand.

## Engineering-test verdict (agent-pass, not max-approved)

The full workflow chain now demonstrated end-to-end for a second
character: novel wording → printed onto the locked real product (exact) →
held by a consistent synthetic character at corrected scale. Total spend
this concept: 6 credits (take-01 2, Stage A 2, Stage B 2). Per
`../WEDDING_SIGN_VIDEO_RULES.md`, this validates nothing beyond the white
street-sign family — other products need their own proofs.

## Next action

Max reviews take-02 (and the Stage A product image). On his explicit yes:
assemble the DM-C017 four-view reference pack and run the one native video
generation (~72 credits). No video spend without that yes. The left/right
ring nit can be fixed in the same pass if he wants it fixed.
