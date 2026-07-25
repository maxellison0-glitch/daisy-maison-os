# DM-MURPHY in-situ — the staging problem, solved (agent-pass)

## The route that failed, and why
First attempt followed `SIGN_IN_SITU_WORKFLOW.md` §3: generate an **empty room**,
then install the sign. Four empty boot-room plates were generated (6 credits) and
are effectively wasted. Max called it before more was spent:

> "You've literally shown me four free images of a hallway with no sign on it… if
> you just ask it to put it on the wall, it's just never going to put it on right."

He is right. Asking a model to mount a sign on a bare wall makes it invent the
placement, the scale AND the lighting — three independent chances to be wrong,
with no reference for any of them. The approved photograph works *because* a
person is holding the sign; stripping the person out discards the only thing
anchoring scale and contact.

## The route that worked, first attempt
Keep the person. Change the setting. This is the diffuser method already proven
in this repo — *"change ONLY the background"* — combined with the validated
print-edit.

- **Reference 1** — `reference-masters/street-sign-BLACK-on-white-MASTER.jpg`.
  LOCKED: sign silhouette, proportions, border width, shaped ends, mounting holes,
  material and edge; the person's body, clothing, forearms, hands, grip, sign
  height; contact shadows and finger occlusion; camera height, angle, framing,
  crop, lens, depth of field, exposure, grain.
- **Reference 2** — `MURPHY-black.svg` → PNG via `build.py`
  (`SIGN_COLOURWAY=BLACK SIGN_HEART=0`). Supplies printing only.
- **Two changes only:** the printing, and the room behind the person.

Jobs: `2c4f016d-03dd-48e3-abcc-89020df69ac0` (A),
`be02d3b2-673d-4cd9-8def-1911d9738450` (B). nano_banana_pro, 2k, 2-up, 4 credits.

## Verified
- Wording character-exact, both lines. No heart (correctly suppressed on an
  apostrophe-bearing line). Black colourway, real cream panel.
- Border reads broad and correct — closer to the master than the earlier colour
  edits managed.
- **Dog sits entirely below and beside the sign, never crossing it** — Alan's
  occlusion rule holds, which keeps the clip on the 4-credit tier later.
- Human + dog + sign together give the scale read Max originally asked for.

## Crop note (matters for Reels)
Both are 1792×2400 (3:4). A 9:16 crop takes width to 1350, losing 442px total.
**A survives it** — the sign has margin either side. **B's sign runs nearly edge
to edge and will clip.** So: A for 9:16 vertical, B for 4:5 feed where its larger
sign and more prominent dog are the stronger frame.

## Status
agent-pass, awaiting Max. This is now the route for every in-situ still; the
empty-room-then-install path in `SIGN_IN_SITU_WORKFLOW.md` §3 should be replaced
by it.
