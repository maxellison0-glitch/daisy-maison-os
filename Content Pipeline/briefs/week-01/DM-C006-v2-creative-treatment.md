# DM-C006 v2 — From Name to Real

## Creative decision

The earlier fireplace composite is rejected. It looked like a synthetic product
mock-up and weakened trust.

The replacement advert shows the actual purchase idea:

1. exact Daisy Maison artwork is personalised on screen;
2. `WINDSOR` is selected and replaced with `POTTER`;
3. the completed deterministic artwork match-cuts to genuine footage of the
   same physical `POTTER` sign.

Higgsfield may animate a verified product-source image when the sign design and
lettering remain accurate and stable and Max approves the result as realistic.
The selected Potter wedding video passes that human realism check. Higgsfield
must not freely invent or redraw an unverified product.

**Emotion:** quiet wedding-gift certainty.

**Product proposition:** their name is what turns it from a sign into their
gift.

## Recommended Take A — The Edit

Target length: 13–14 seconds. Master format: 9:16, composed crop-safe for 4:5
and 1:1.

| Time | Picture and animation | On-screen copy | Sound |
|---|---|---|---|
| 0.0–0.8s | Exact `MR & MRS WINDSOR` sign is already visible. A caret blinks beside the surname; the atmospheric plate moves very subtly behind it. | `It starts with their name.` | Warm room tone; one restrained music pulse. |
| 0.8–1.5s | `WINDSOR` is selected in one natural interaction. Coral highlight is confined to the input/UI layer, not the sign artwork. | — | Soft selection tick. |
| 1.5–1.8s | One backspace clears the selected surname. Heart, date and sign structure remain stable. | — | One tactile key sound. |
| 1.8–3.8s | `POTTER` types at varied human cadence. The exact sign re-renders and re-centres on every keystroke. | `Make it theirs.` | Six quiet mechanical keystrokes, each frame-synchronised. |
| 3.8–5.2s | UI fades. Finished `MR & MRS POTTER` artwork holds long enough to read. Slow 3% push-in continues. | — | Music lifts, then briefly suspends. |
| 5.2s | Hard geometry-matched cut from exact artwork to the real physical Potter sign. No morph and no dissolve. | — | Digital ambience stops; real room tone begins on the cut. |
| 5.2–10.5s | Genuine footage: light moves across the surface, then a hand lifts or settles the sign. A close detail proves the heart, print and finish. | `Made for them.` | Real handling sound and restrained music. |
| 10.5–13.5s | Real sign remains hero. Daisy Maison end lock-up. | `Add their names.` / `daisymaison.co.uk` | Clean musical resolution. |

No spoken voice is required for the first test. It must work muted.

## Challenger takes

### Take B — Proof First

- 0–2s: open on a genuine macro of the physical Potter sign.
- Copy: `Made for one couple.`
- Reverse match-cut into the digital artwork.
- Show the Windsor-to-Potter edit.
- Return to the same real sign.
- CTA: `Make it theirs.`

This tests whether immediate authenticity is a stronger hook than the
personalisation interaction.

### Take C — Silent Type

- No copy until the end card.
- Selection tick, backspace, six keys, hard cut, physical handling sound.
- End card only: `Daisy Maison` / `Add their names.`

This tests whether the mechanism is satisfying enough without explanatory
copy. Take A should be tested first; its winner should then face one challenger,
not both at once.

## Selected Higgsfield reveal

Use completed video job `243720fe-a504-4585-9613-0b306ec86d68` as the first
Potter reveal candidate.

- Model: `minimax-2.3-fast` / Minimax Hailuo
- Format: vertical 1080 × 1934
- Duration: 5.9 seconds
- Motion: locked camera; a single soft breeze through the florals; a distant
  wedding guest crosses the background.
- Full-resolution review: the main lettering and `I DO DAY · 1ST MAY 2026`
  line remain stable. Max judged the complete moving shot realistic enough.
- Local reference copy:
  `Content Pipeline/drafts/DM-C006/reference-review/minimax-243720fe/download/video.mp4`

Do not generate replacements merely because the asset is AI-assisted. First
assemble the advert and judge the transition in context. Only generate another
plate if the cut exposes a specific visual problem.

## Optional atmosphere-only fallback

If a replacement becomes necessary, generate the atmospheric plate without the
product:

> Vertical 9:16 cinematic background plate. English country-garden wedding at
> golden hour, heavily defocused; creamy bokeh from out-of-focus white and
> blush flowers with soft sage foliage moving gently in a light breeze; warm
> low backlight, subtle lens bloom, muted ivory, sage and honey palette. Very
> shallow depth of field with nothing in sharp focus. Large calm negative space
> throughout the central safe area. Near-static camera with only a 3–4 percent
> slow push-in and no cuts. Photorealistic high-end commercial cinematography,
> restrained fine film grain. No people, faces, hands, text, letters, signs,
> plaques, rectangular objects, tables or products.

Generate several takes because text-like shapes, rectangles, conspicuous camera
motion or overactive flowers are automatic rejects. In the composite, the plate
should be softened and mixed over Daisy cream so it reads as living atmosphere,
not as a location in which the digital sign supposedly exists.

## Exact-product rules

- Deterministic SVG/Pillow artwork remains the sole product image before the
  reveal.
- The interaction UI, artwork, copy, background, grain and CTA stay on separate
  layers.
- Every letter change must trigger the renderer and correctly re-centre.
- The final reveal sign must carry the same surname, date and layout as the
  final digital frame. If the selected safe/demo asset changes, change both
  halves together.
- No fake review, price, dispatch, stock or speed claim.

## Match-cut mechanics

1. Export the completed digital sign frame first; it is the geometry master.
2. Display it as a low-opacity onion-skin while filming the physical sign.
3. Match the four outer edges within roughly 16 pixels at 1080-wide, scale
   within 2 percent and rotation within 1 degree.
4. Continue the same slow push-in across both halves in post.
5. Add matching fine grain to the digital half before the cut.
6. Lift exposure slightly over the two frames before the cut and settle it over
   the two frames after; never overlap the two sign images.
7. Let the sound world switch from UI to real room tone on the exact cut frame.

If the edge match misses, use the insurance shot: a real hand crosses the frame
and places the physical sign. Hide the hard cut behind the hand. Do not ship a
nearly convincing morph.

## Optional real-footage fallback — under ten minutes

- Wipe the phone lens; shoot 4K/25fps; lock exposure, white balance and focus;
  use window light and turn off overhead lights.
- **3 minutes:** locked front-on match frame against a cream/neutral surface,
  aligned to the exported digital frame. Hold for ten seconds.
- **2 minutes:** same setup, with a hand placing the sign into the exact aligned
  position. Capture two takes for transition insurance.
- **2 minutes:** slowly tilt or lift the sign so light rakes across its printed
  surface and edges.
- **2 minutes:** close detail on `POTTER`, the heart and the date; allow slight
  natural handheld movement.

## Modular organic-to-paid package

- Archive: clean picture master plus separate music, UI/foley and optional VO
  stems.
- Organic: TikTok, Instagram Reels and Facebook Reels at 9:16.
- Paid candidates: Meta 9:16, 4:5 and 1:1; TikTok 9:16.
- Keep all essential text clear of the top 14 percent and bottom 20 percent.
- Paid CTA variants: `Add their names` and `Make it theirs`.
- Do not use `Personalise yours in 60 seconds` unless the live journey is timed
  and verified.

## Ruthless approval gates

1. The animated artwork must match the real product and live personaliser.
2. On a 50-percent overlay, the digital and real sign edges must meet tolerance;
   otherwise use the hand-occlusion cut.
3. Typing must feel human and every sound must land on the visual change.
4. For an AI-assisted product reveal, inspect the full-resolution sequence for
   changing letters, borders, heart, date, mounting geometry or material. Max's
   human realism judgement remains the final visual gate.
5. On a muted phone held at arm's length, `POTTER` must be readable before the
   cut and the physical object must be unmistakably real immediately after it.

## Current dependency

The selected Higgsfield Potter reveal is now available locally and accepted by
Max as realistic enough. The next dependency is the exact deterministic
Windsor-to-Potter interaction and a convincing cut into that video. A separate
real clip is fallback insurance, not a blocker for the first complete master.
