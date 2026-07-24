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

## Decision

**Pending.** Awaiting Max's look before any video-generation spend.

## Next action

If approved: assemble the same reference-view requirements DM-C017 used
(front, both edges, back) and run native video generation. If not
approved: treat as a specific, nameable EDIT per `PUBLISH_READINESS.md`,
not a reason to abandon the approach — this take is close.
