# The Correction — the post

**Approved by Max, 28 Jul 2026:** Style A, bottom pills.
*"I like A, with probably the bottom pills… I think that looks good. It doesn't
cover their faces."*

| | |
|---|---|
| File | `APPROVED/DM-C020-the-correction-FINAL.mp4` |
| Cover | `APPROVED/cover.jpg` |
| Spec | 1080×1920, 4.04s, 24fps, h264, silent |
| On-screen hook | *same order.* (white pill) / *both signs.* (burgundy pill), y≈1180 |
| Brand tag | Daisy Maison wordmark on a cream tag, top-right, rotated -7°, pops in at **2.20s** and holds |

**Why the tag pops at 2.20s and not at the top.** The bottom of the frame is
taken by the two pills, so the tag goes top-right where it covers neither face
and clears both platforms' UI. It arrives *after* Freya's sign has been read —
a brand mark landing before the joke competes with it; landing after it signs
it. It overshoots to ~1.10 and settles, rotating from -15° to -7° as it lands,
so the angle reads as deliberate rather than as a crooked paste.

The cream `#F5F1E8` is the sign panel's own colour, which is why it sits on the
footage instead of on top of it. Built in `logo_tag.py` from
`reference-masters/daisy-maison-WORDMARK-v2.png` — PIL only, no generation.

Silent by design. Both platforms autoplay muted and the joke is entirely
visual — there is nothing for audio to carry. Add a trending sound at upload if
the platform pushes one; do not mix one in here.

---

## Caption copy

**Primary — use this one:**

> He ordered one sign. She ordered the correction.
>
> Personalised street signs, any wording, made in our unit.

It tells the story the video does not have time to, names the product plainly,
and the second line is the only selling in it. No claim, no price, no delivery
promise.

**Alternates, same register:**

- *We printed both. We said nothing.*
- *Two signs, one order, one very specific point being made.*

**Do not use:** anything framing this as a real named customer's order, any
delivery time, any discount. It is Alan and Freya on our own set — the joke
works without pretending it is documentary evidence.

---

## Per-platform

| | Instagram Reels | TikTok |
|---|---|---|
| Hook position | y≈1180 clears Reels' ~360px UI band | clears TikTok's ~420px band and the right-hand rail |
| Caption | primary, full | primary, trimmed to the first line |
| Tags | `#personalisedgifts #streetsign #homebar #giftsforhim` | same, plus whatever is trending that day |
| Cover | `cover.jpg` — both signs readable in the grid | n/a |

The same 4s cut serves both. Per the zero-credit overlay lane, one take carries
several hooks: re-running `render_overlays.py` with new copy and `finish.py`
gives another post off this footage for nothing.

---

## Status

Cut, approved, and **not posted.** Publishing is Max's call.
