# THE LITTLE MADAM — three wall styles

Same clip, same locked sign, three different walls. Max: *"I want to take that
exact format, but I want a different background. I don't like the colour."*

| File | Wall |
|---|---|
| `MADAM-A-warm-white.mp4` | soft warm white |
| `MADAM-B-cool-grey.mp4` | cool chalky grey |
| `MADAM-C-deep-clay.mp4` | deep clay plaster |

1080×1934, 24fps, 6.46s, silent. Contact sheet: `MADAM-three-styles-QC.jpg`.
Builder: `Content Pipeline/templates/sign-in-situ/wall-restyle-reel.py`.

**Cost: zero credits.** The room was not regenerated. The wall's hue and
saturation are replaced and its VALUE is kept, so every gradient, the sunlit
patch top-right and the contact shadow under the cat house all survive — it
reads as the same room painted a different colour, not as a flat fill.

Wording swapped for free too: THE LITTLE MADAM / SHE RUNS THIS HOUSE, printed
onto the plate by the reprint engine. `MADAM-plate-reprinted.png`.

## What changed from the cat master

1. **The string is painted out.** Max: *"I don't like that we've overlaid it."*
2. **The wall is restyled** — three options rather than the sage.
3. **The end card no longer sits over the cat house.** It is up on the wall at
   y=300, and the last frame is held 1.25s so it can actually be read.

## Four bugs found and fixed here — all worth keeping

1. **String fit followed the sign, not the string.** Fitting rows 20..950 spans
   the sign at y 516..696, and the lettering is a far stronger ridge than a
   string. The render came back with the string still in it *and* a clean streak
   painted beside it. Fit on bare wall only (y 30..470).
2. **The string SWINGS.** It is a feather toy, not a taut line — 65px of travel
   at y300 across the clip, and the tilt reverses (frame 60 at x=586 on a −0.044
   slope, frame 62 at x=593 on +0.010). One fitted line cannot cover it; it is
   re-fitted every frame, carrying the previous line forward if a fit fails.
3. **The wordmark master is a cream CARD, not transparent lettering** (alpha is
   214/255 across the whole plate). Composited on a repainted wall it reads as a
   pasted rectangle, and on the warm-white style it nearly vanishes. The
   lettering is now keyed out of the card and laid down as white type with a soft
   shadow, which sits correctly on all three walls.
4. **A band of the old sage survived down the left of every frame.** The wall
   left of the door is in shade: its hue drifts 45°→125° down its length while
   its saturation falls to 0.08, so the main hue lobe *and* the saturation gate
   both gave it partial weight. A narrow second lobe came back blotchy for the
   same reason. It needed one flat wide lobe — full membership across hue
   35..135 on a lower saturation knee, inside x < 260. The cat house sits at hue
   19–24 and the door frame at 17, so the boundary lands on hue rather than on a
   hand-drawn edge.

Earlier, related: a strong wall colour came back blotchy because gaussian hue
membership gave partial weight across the sunlit patch (hue 39.5 there vs 47 in
shade). Membership is clipped-linear, flat across the wall's whole hue span.

## The sign is still locked

Measured on the output: **0px drift** in the sign interior across the whole
clip. It is the approved plate's pixels on every frame, composited through a
feathered mask, not the model's.

## Captions

"We've settled who owns this house." → "It's in writing now."

LAUGH engine, native white bold, mask-reveal up / mask away down, never a fade.

## Open

Max picks one and posts it. Nothing here has been published.
