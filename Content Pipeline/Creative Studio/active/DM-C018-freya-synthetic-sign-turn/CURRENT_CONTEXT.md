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

## Max approvals, 24 July 2026

Max approved take-02 ("that's definitely more realistic") and asked for the
method to be saved as the Freya engineering prompt — done:
`Content Pipeline/Creative Studio/prompts/freya-street-sign-hero/`. He also
explicitly likes the wood-workshop background — treat it as the preferred
setting. Video spend still requires a separate explicit yes.

## Border-colour test (Max's ask: "have we tried changing border colours?")

The saved colours were found on the live Shopify store, not in the repo:
the "My Valentine" and "Retirement" street-sign listings offer **5
colours**, and the official swatch chart (`Mow-It-Swatch-Final-copy-1`,
saved to `working/colour-test/colour-swatch.jpg`) names them:
**Grass, Sage, Blue, Grey, Black** — border and lettering in the colour on
a cream field. Note the coloured range's real border is a thinner outline
than the wedding sign's broad band.

**Stage A2 — recolour the locked real photo to swatch Blue (one change):**
- First submission (job `28df9e22-c102-4256-b556-c76a87bbeda9`, 2 cr) went
  out WITHOUT the swatch attached — prompt referenced "reference image 2"
  but only one media was passed. Logged as a process error; output kept
  only as stray evidence.
- Corrected run: swatch uploaded (media
  `47c10ac9-aec5-4746-b46f-cdf49c275b17`), job
  `7d1f061c-809b-4ead-b4a0-4419c8dae28f`, 2 cr. **PASS with one flag:**
  colour matches the swatch steel-blue, wording/letterforms/scene exact;
  border band reads slightly slimmer than the black original — drifted
  toward the swatch's thin-border geometry despite instruction. Output:
  `working/colour-test/stageA2-blue-sign.png`.

**Stage B2 — Freya holds the blue sign (first attempt): FAIL.**
Job `4053b659-af5a-40ee-ae76-ee6e46191660`, 2 cr. Scale passed (~2.4) and
wording characters correct, but: typeface substituted (bold rounded
sans-serif replaced the locked serif), colour saturated toward royal blue,
and identity drifted (reads adjacent-to-Freya, not Freya). Diagnosis:
chaining a generated sign into a second generation compounded drift in a
way the cake chain didn't — plus single-take variance. Output kept as
failure evidence: `working/colour-test/stageB2-freya-blue-FAIL.png`.

**Stage B2 retry — PASS.** Job `69661359-0bbf-41ea-836e-9b4b00feaecb`,
2 cr, with explicit typeface/colour/identity locks added ("MUTED
STEEL-BLUE... NOT royal blue", "ELEGANT SERIF CAPITALS... do not
substitute any bold, rounded, sans-serif font", "must read as the same
individual person"). Serif letterforms held, muted blue held, identity is
genuinely Freya, scale ≈ 2.28, workshop setting. Output:
`working/colour-test/stageB2-freya-blue-take02-PASS.png`. The explicit
negative-space language is what fixed it — saved as prompt case
`prompts/freya-street-sign-hero/cases/DM-C018-FREYA-CAKE/03-validated-freya-hero-coloured-sign.txt`.

**Standing model quirk:** the signature gold ring has now landed on her
LEFT hand in three consecutive Stage B generations despite explicit
right-hand instructions. Treat as a known nano_banana_2 tendency; if the
ring hand matters for a production still, plan to fix it at selection
time (choose takes where hands are occluded) rather than fighting the
model.

## Honest scope statement (Max asked: "then we have the full workflow?")

After this test, the demonstrated STILLS capability for the Large street
sign is: arbitrary display-safe wording ✓, correct physical scale ✓,
fronted by Alan ✓ (DM-C017) or Freya ✓ (this concept), coloured printing
at the product stage ✓ (Stage A2, one flag). Carrying a coloured sign
through the character stage is NOT yet clean — first attempt failed.
VIDEO remains validated only for the white wedding-sign family (DM-C017);
coloured-sign video and other product families still need their own
proofs per `../WEDDING_SIGN_VIDEO_RULES.md`.

## Next action

QC the Stage B2 retry. Then Max's call on: (a) which wording/colour combo
to take to the four-view pack and the one ~72-credit native video, and
(b) whether the blue-chain result is worth further engineering now or
parks behind the white-sign video test.
