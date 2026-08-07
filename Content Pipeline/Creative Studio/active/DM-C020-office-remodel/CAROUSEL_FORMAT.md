# The office carousel — the format that worked, made repeatable

Locked 30 Jul 2026, after DM-C020-POST-1 went out and got real engagement off
**two credits**. Max: *"this concept of using images with different lines, line 1
and line 2, and an on-screen hook is cheap for us to do... You've got a lot of
engagement from literally two credits."*

This file is the recipe. Freya & Alan run it the same way every time so the next
batch does not re-learn what this one paid for.

---

## What the format IS

A photo carousel. Each slide: **one sign, held in the office**, Alan deadpan in
the foreground, **an on-screen hook pill that reacts to that specific sign's
Line 1 / Line 2**. Nothing moves. It costs one generation per sign plus a
zero-credit local render for the pills (`../../../tools/hook_pill.py`).

Three things point at the same joke — this is the whole engine:

1. **Line 1** — the name (THE WILSONS, DAD'S BAR)
2. **Line 2** — the small print under it (FIRST CHRISTMAS HERE · 2026)
3. **The on-screen hook** — a dry human reaction to what Line 1 + Line 2 add up
   to (*"it's July"*)

The hook is not a caption and not a description. It is what a person says looking
at the sign. *"it's July"* on a first-Christmas sign. *"so… closed?"* on OPEN
WHEN IT'S NOT RAINING. If the hook merely repeats the sign, the slide is dead —
see `../../PUBLISH_READINESS.md` on the three-component rule.

## The frame

- **Alan foreground, deadpan, holding the sign at a slight diagonal** (the hold
  Max approved: `ideas-B-bargrill/take-02`, media `a64fdcbd-9a42-4702-9c3f-b4eae8a4c7a2`).
- **Freya can cross behind him mid-stride** on a slide or two — the two-hander.
  Reference: `cast-D-twohander-packing-bay/`. It reads as a real workshop where a
  colleague walked into the shot, which is the thing no stock photo can buy. Do
  not use it on every slide; it is a punctuation mark, not the default.
- **A different office room per slide.** Nine plates exist (`working/plate-*`).
  No two consecutive slides share a room — `../../PUBLISH_READINESS.md` frame gate.

## The pills — handled by the tool, not by hand

`../../../tools/hook_pill.py` burns the hooks in: staggered position (top / low,
never the middle band over the face and sign), one production colourway per
slide, WCAG-AA text colour computed per fill. Colour comes off **what the sign
is** (garden bar → grass, Christmas → burgundy), declared per slide — not
sampled, because a beige workshop only ever samples back to beige.

---

## The two traps that quietly wreck a batch

Both are **reference-sourcing** problems, not prompt problems. You cannot fix
either with a sentence in the prompt.

### Trap 1 — Line 2 is inflating

Real Daisy Maison signs have a second line roughly **a fifth the height of the
main line**, tucked under it. Our recent generations have been rendering it big —
half the main line — because they reference *earlier generations* where it was
already too big. Each generation compounds it.

**Fix: reference the real product for the line-2 proportion, never our own
output.**
- Non-wedding signs → `Content Pipeline/Creative Studio/reference-masters/street-sign-BLACK-on-white-MASTER.jpg`
- Wedding signs → the Mr & Mrs reference below (it has the correct small line 2
  *and* the heart).

Max, 30 Jul: *"line 2 is getting quite big. Our actual street signs do not look
like that... We just need to be careful where we're referencing these photos
from to keep it neat."*

### Trap 2 — Mr & Mrs signs need the red heart, and text alone won't make it

On a real Mr & Mrs sign a **small red heart replaces the dot over the ampersand**
(`MR ❤ MRS`). The generator will not produce that from wording alone — it needs a
reference image that already carries the heart.

**Fix: for any Mr & Mrs / wedding sign, add the real product photo as a
reference:** `projects/daisy-street-sign/references/mr-mrs-live-product-reference.jpg`
(MR ❤ MRS WINDSOR / FROM THIS DAY FORWARD… — brown-on-cream, correct heart,
correct tiny line 2). Also `projects/daisy-street-sign/artwork/assets/heart.png`
is the isolated heart if a cleaner cutout is wanted.

Max, 30 Jul: *"any of those should have a red heart, so use a red heart reference
image... or otherwise it just won't work."*

---

## Colour — use the whole sheet, not just black

Max: *"don't be afraid to use different colours from the baked-in sheet that we
have with the correct colourways."* The real colourways live in
`projects/daisy-street-sign/production/product-rules.json` and are the same
values the laser cuts: black `#010101`, sage `#9AA192`, grass `#68893C`, blue
`#799CAA`, lightsage `#BEC0A9`, blush `#EBC3C3`, duskypink `#CB9CA5`, plus
brown-on-cream for weddings. A sign generated in sage or blush is still a real
product; defaulting every sign to black is what makes a feed look flat.

The pill colour and the sign colour are chosen together per slide, both from this
sheet.

---

## The series: "Reviewing your signs"

Max's framing, 30 Jul: *"we can have a pool sign and literally say 'Reviewing
your signs, day one.'"*

It reframes the whole format as a **recurring series** — Alan (and Freya)
reacting to signs, the way the account's best-ever post worked (documentary, not
advert; the customer wrote the joke, the brand just held it up — see
`IN_OFFICE_CONTENT.md` §6).

**The sourcing rule that makes it sustainable:** ideally react to a real ordered
sign. When there is no good real one to show, **invent the on-screen hook first —
the funniest reaction that would land — then make the sign that earns it.** The
hook leads; the sign is built to it. This is explicitly delegated: *"If we can't
find any good signs to review, you can literally think of it yourself, think of
the actual on-screen hook that would work, and then make a sign for that."*

Never invent a real customer, a real order detail, or a metric. The sign wording
is fiction we own; a claim about a specific buyer is not (see the standing PII /
no-invented-claims rules).

---

## The build checklist (per carousel)

1. Write the three slides as Line 1 / Line 2 / hook, each a thing someone would
   actually hand over (the rule that killed "day 4 of 42").
2. Pick a colourway per sign from the sheet; pick the pill colours to match.
3. Assign a different room per slide; decide which one slide (if any) gets Freya
   crossing behind.
4. Generate each sign with **two references**: the room plate + the hold
   authority (`a64fdcbd`). For wedding signs **add the Mr & Mrs real product**
   ref. For everything else, if line 2 drifts big, add the black-on-white real
   master as the line-2 authority.
5. Two takes per sign, keep the one that holds the arm line (scale is still a
   lottery — `IN_OFFICE_CONTENT.md` §7). Filter before showing Max, not with him.
6. Burn hooks with `hook_pill.py --slide IMG "hook" COLOURWAY`.
7. Caption + post. Music: attach a CML track at publish (photo carousels take a
   track through the API — proven on POST-1). Log it in `../../PUBLISH_LOG.md`
   before it goes out.

## Cost

One generation per new sign (~1–2 credits at 2k, two takes ≈ 2–4). A three-sign
carousel is ~6–12 credits all in, pills and caption free. Signs already generated
(Wilsons, Dad's Bar, Garden Tavern) are reused, not re-made — unless line 2 needs
the real-product fix, in which case they are re-generated once, correctly.
