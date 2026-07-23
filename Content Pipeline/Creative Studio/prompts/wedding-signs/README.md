# Wedding Sign Engineering Prompt Workflow — case library

This library currently records the proved white wedding-sign family only. A
case is proven only when the personalised sign is physically credible and
exact in the untouched native video—not merely when its wording can be mapped
in post.

Read `../../WEDDING_SIGN_VIDEO_RULES.md` and
`../../WEDDING_SIGN_ENGINEERING_PROMPT_WORKFLOW.md` before using this library.

Coloured signs with black text, coloured signs with coloured text and
non-wedding signs are unvalidated future lanes. Do not place them under proven
cases until each has passed its own complete still-to-video human approval.

## Proven cases

| Case | Models | Human result |
| --- | --- | --- |
| [`DM-C017-JANNAWAY v03`](cases/DM-C017-JANNAWAY/VALIDATED_CASE.md) | Nano Banana 2 + Seedance 2.0 | Max rated the untouched native video 8.5/10 for realism; finished eight-second Reel verified |

## Rejected learning cases

| Case | Models | Rejection |
| --- | --- | --- |
| [`DM-C017-JANNAWAY v02`](cases/DM-C017-JANNAWAY/CASE.md) | Nano Banana 2 + Seedance 2.0 | Composited source reference; forbidden face overlay; visible white/border seam; sign too thick; black reverse |

## Current engineering map

- Select a real incoming sign idea or a clearly labelled safe invention.
- Build the exact SVG from the audited LightBurn-derived system first.
- Give the image model the SVG for content truth and a real Daisy Maison sign
  photograph for material/construction truth.
- Generate 4-8 inexpensive image candidates.
- Do not paste the SVG onto a candidate. A human must approve one coherent
  image in which the exact artwork already reads as the physical sign.
- Before video, supply real printed-front, back-to-edge, front-to-edge and
  white-back references. The two transition views lock the thin profile; the
  back view prevents an invented reverse.
- Use the video model for one continuous performance while requiring the sign
  to remain native and unchanged.
- If any letter, colour, border, thickness, white reverse, shape, material,
  hand interaction or shadow changes, reject and regenerate.
- Never use a whole-panel, border, lettering-only, tracked, corner-pinned or
  homography replacement on the product surface.
- Finish only with hook, CTA, captions, whole-shot colour and sound outside the
  sign.
- Compare the untouched native take with real Daisy Maison footage at normal
  phone playback speed as well as frame by frame.

Use [`CASE_TEMPLATE.md`](CASE_TEMPLATE.md) only after another complete result
passes human product-realism review. Do not populate it halfway through
production.
