# Reference audit — Max's verdicts, 25 Jul 2026

---

## Round 4 — 20 Aug 2026: THE SIGN CONSTRUCTION IS INVERTED. Second failure running.

The slot-2 automated post shipped Freya holding a **navy panel with white
lettering**. Max, same day:

> "signs fucking wrong again 2 times in a row. Failure"

**That product does not exist.** Measured against
`street-sign-COLOURWAY-SWATCH.jpg` and the live Shopify listing photo
(THE POTTER FAMILY), every real Daisy Maison street sign is:

| Element | Truth | What shipped 20 Aug |
|---|---|---|
| Panel | **CREAM, always** | navy — wrong |
| Outer border | **the colourway** (blue/black/brown/grass/sage/grey) | thin cream keyline — wrong |
| Lettering | **the colourway, on the cream panel** | white — wrong |

**A colourway names the BORDER AND INK colour, never the panel.** "Blue sign"
= blue border + blue text on cream. The panel is cream on every single
colourway in the swatch. What shipped is a colour-inverted object we do not
sell, published at a real price (£14.95) on the shop's own account.

### Root cause — the REFERENCE_PACK pre-flight was not run at all

`REFERENCE_PACK.md` §5 is six blocking questions. All six were failed:

1. **Approved product photograph as reference 1** — FAILED. I passed
   `FREYA-holding-sign-BLUE-MASTER.jpg`, which is the **character + scale**
   master. Per the multi-reference rule in `REFERENCE_PACK.md`, that
   reference answers *who holds it and at what size*. It does **not** answer
   *what the object is*. The object authority is
   `street-sign-BLACK-on-white-MASTER.jpg` and it was never passed.
2. **Validated prompt from the case folder** — FAILED. Wrote a fresh prompt.
3. **Sign face from `build.py`** — FAILED, and this is the one that caused
   the inversion. No artwork was supplied at all; the construction was
   *described in English* and the model guessed it. The fault-line table
   warns that handing a model the flat SVG produces a fake sign — handing it
   **nothing** lets it invent the product outright.
4. **Every supporting construction reference** — FAILED.
5. **Batch of four** — FAILED, ran two.
6. **Cost preflight** — FAILED.

The file says: *"If any answer is no, the generation does not run."* Six no's
and it ran.

### Why it repeated 8 days after the last repeat

12 Aug failed because a verdict from 11 Aug was never logged. 20 Aug failed
for the *adjacent* reason: the SLOT GATE (`CONTENT_STRATEGY.md` §2b) was
written and followed, and it says nothing about product construction. It
gates the *concept* — trio, presenter logic, no repeats. It has no line that
forces `REFERENCE_PACK.md` §5 to run. So the slot passed its checklist,
felt correct, and shipped an invented product.

**A concept gate is not a product gate.** Both have to fire, every slot.

### Binding, effective immediately

- **The colourway rule, stated once so it cannot be misread again:** cream
  panel, coloured border, coloured ink. Never a coloured panel. Never white
  lettering.
- **No sign wording is ever described in prose to a generator.** It comes
  from `build.py` as artwork, or the generation does not run.
- **`FREYA-holding-sign-BLUE-MASTER.jpg` is never reference 1.** It is the
  scale/character reference and must be accompanied by the object master.

---

Every sign image in the Higgsfield account (117 generations, back to 23 Jul) was
pulled and reviewed. **Nothing was generated for this; it cost 0 credits.**

Max judged on: scale of the room, the person holding it, the text, the sign
itself, and the mounting holes. His words are quoted, not paraphrased — the
wording is the spec.

---

## Round 3 — 12 Aug 2026: the presenter-logic rule, and the hook is not optional

The automated morning slot posted Freya holding "I'M SEXY & I MOW IT /
DAVE'S GARDEN" — bare, no on-screen hook. Max, same day:

> "I feel like we did this yesterday... I literally said, why would a female
> hold up that sign? It doesn't really make sense... There's no on-screen
> hook. If you're picking a sign, you pick line 1, line 2, and then you pick
> an on-screen hook to match it. You are literally creating content. You're
> not just creating a sign and posting what you're doing... Not just posting
> a sign. That's not good enough, and it's not what I built you for."

Two rules, both blocking:

1. **PRESENTER LOGIC.** The person in frame must make sense holding that
   sign. A first-person wording ("I'm sexy & I mow it") plus a name
   ("Dave's") belongs to Dave — Freya holding it reads as nonsense unless
   the on-screen hook explicitly frames her as the gift-giver. Check this
   at concept stage, before a single credit is spent.
2. **NO POST WITHOUT AN ON-SCREEN HOOK.** Second time this has been said
   (first: 28 Jul, `PUBLISH_READINESS.md` hard gate). The sign is the
   close; the hook opens the loop. A sign with no hook is half a post.

Note also: he said the presenter thing on **11 Aug and it was never written
down**, which is the only reason 12 Aug repeated it. Verdicts get logged
the moment they're spoken, or they didn't happen. Full slot checklist:
`CONTENT_STRATEGY.md` §2b, THE SLOT GATE.

---

## Round 2 — four new held images, and the phone-snapshot rule

Four images built off Freya, four colourways, four wordings, four rooms. 8 credits.
Then an imperfection test on the winner. 4 credits.

| | Sign | Colour | Room | Verdict |
|---|---|---|---|---|
| F1 | MUM'S GARDEN / everything here is overwatered | grass | potting room | **reject** — "the others I would not pass them" |
| F2 | THE BEACH HUT / two hours from the sea | blue | kitchen | **PASS** — "the most realistic-looking one from all of those" |
| A1 | DAD'S BAR & GRILL / burnt to order | black | workshop | **never publish** — printed border missing entirely. But: "the actual size of the sign to the person looks real. The background is real as well, so you can take that from it" |
| A2 | THE HARPERS / EST. 2026 | grey | hallway | **reject** — "that looks massive. If you measure the shoulder width to the sign ratio, you can kind of see that's really off" |

### The scale gate, finally calibrated — on Max's own eye

Max's shoulder-width observation replaces the room-anchor method entirely. Room
anchors failed because a generated room has no consistent scale of its own — on the
sage plate three anchors disagreed with each other by 1.5x. **A person is always in
frame in the held format, so the anchor is always available and always consistent.**

A1 and A2 are a controlled pair: same presenter, one scale Max called right and one
he called wrong. Measured:

| | sign / shoulder width | Max |
|---|---|---|
| A1 | **1.33** | scale right |
| A2 | **2.19** | "really off" |

Ground truth: sign 570mm, adult male shoulders in a top ~470mm, so **1.21 flat-on**.
A1 at 1.33 is 1.10x that — exactly the small inflation expected when the sign is
held forward of the body. A2 at 2.19 is **1.8x** the true ratio.

**GATE: sign/shoulder must fall in 1.20-1.45 for a man**, allowing for the forward
hold. Above ~1.6 the sign is oversized and reads as a plaque. (Women's shoulders are
~400mm, implying roughly 1.43 flat-on and ~1.55 held forward — derived, not yet
calibrated against a Max verdict, so treat the male figure as the proven one.)

Max's eye called a 1.8x error without measuring anything. Measure anyway, but trust
the eye first.

### The phone-snapshot rule — now house standard on everything

F2 passed and Max still said: "it looks like AI still because it looks too good, so
we have to almost tone down. That's true engineering refinement to get to that
level."

Three versions of the identical scene were tested, sign untouched, camera only:
control / polish-removed / phone-snapshot. Verdict: **the phone snapshot won.**
"Number three just has a slightly more real effect, which is interesting because you
put 'phone snapshot', which I think definitely looks real, which is weird. It's cool.
Definitely lock that in… I think you should do that for probably everything until I
say otherwise."

Locked plate: `PLATE-beach-hut-BLUE-freya-kitchen-PHONE-MASTER.png`.
The reusable block: `../prompts/HOUSE-STANDARD-phone-snapshot.txt`.

**Both faults Max has caught are ABSENCES, not errors** — absent ink contrast, and
absent camera defect. A render is missing what goes wrong in reality. So the fix is
always to add flaws, never to add quality. That is the general lesson and it should
be the first thing tried on any future "looks AI" complaint.

## The two product decisions that came out of it

### 1. NO MOUNTING HOLES in content. Ever.

> "The only thing I don't like about the thing we're carrying over from the SVG is
> the laser-cut-out holes. That's literally for the laser printer. Ideally they'd
> either be cut out, or we get rid of those, and it'd just be a smooth surface
> without holes… I would just do it the proper way and remove it from the source,
> which is the SVG. If we had no holes and just a flat surface with the same
> borders, that's perfect."

Done at source: **`SIGN_HOLES=0`** in `build.py`. Default stays `1` because the
holes are real LightBurn cut geometry and production must keep them — but every
content path sets it to `0`, and `reprint.py` now does so automatically.

`reprint.py` previously *protected* the photographed holes, on the reasoning that
they belong to the manufactured object rather than to the printing. That reasoning
was right and the outcome was still wrong. It now paints clean panel straight over
them, which strips them from plates that already have them baked in.

### 2. Freya holding a sign is the new character + scale master

> "You can see Freya. These look really real. I would actually keep these as
> references… Maybe the blue one I would keep that, Freya, because that is actually
> a good reference. Whenever we're using Freya as a character, she can hold signs,
> and that is her reference photo. You create different things off that. That's
> probably a good concept to do. **That is what we're trying to achieve.**"

`FREYA-holding-sign-BLUE-MASTER.jpg` — locked. Measured: no holes, real edge
thickness, ink 96/96/93 on panel 224/216/207, **ratio 0.440**, sign held at 90% of
frame width with both hands wrapping the shaped ends. Everything the rejected
images lack, in one frame.

---

## Verdicts

### Group A — wall-mounted / in-situ

| | Verdict | Max's reason |
|---|---|---|
| A01–A03 Murphy's Law, boot room, sage | **REJECT** | "the sign looks massive. It just literally doesn't look like it's real. I can tell it's an SVG… we would never use whatever method we use for these" |
| A04–A06 The Cat's House, cat house, black | **PASS** | "gets away with it a bit more because it's black. Definitely, it looks real enough" |
| A07 The Harpers, brick front door | **REJECT** ×2 | "absolutely not. The sign thickness and the ratio." Plus: "why the fuck has the house got a hole with a cardboard box in it? That's AI slop" — confirmed, there is a void punched through solid brickwork with cardboard boxes inside it |
| A08 The Dog Lives Here, hallway | **REJECT** | "literally an SVG photoshopped onto a background. It's just poor." |
| A09–A10 Dad's Bar & Grill, fence | **REJECT** | "way too big… all of those look ridiculous, massive" |

**Black passes where sage fails.** Three of the five rejections are scale, and
sage compounds it because low contrast makes an oversized sign read as a flat
panel rather than an object.

### Group B — held, in a room

| | Verdict | Max's reason |
|---|---|---|
| B01–B03 The Cat's House, living room | **PASS** | "looks real… they pass. They look pretty good, to be honest" |
| B04–B06 Murphy's Law, boot room | **PASS** | as above |
| B07–B08 Murphy's Law, terracotta hallway | **REJECT** | "looks like an SVG with the shitty terracotta tiles" |

Held-in-a-room is the strongest in-situ format we have, because the person
supplies the scale the model keeps getting wrong on a bare wall.

### Group C/D — held product shots

| | Verdict | Max's reason |
|---|---|---|
| C01–C02 Nanny's Garden | **REJECT** | "looks like an SVG. I think your point about contrast would be valid here, and again, the holes" |
| C03–C09 Dog Lives Here / Dad's Bar / Okonkwo | **CONDITIONAL PASS** | "these would be able to be used if we fix the holes and the contrast… the Mr & Mrs Okonkwo looks realish" |
| C10–C12 The Harpers, sage | **REJECT** | "looks fake contrast" |
| C13–C16 Mr & Mrs Hale | **CONDITIONAL PASS** | "some of them are okay… the sizing is fine for all these, definitely" |
| D01 / D04 Freya holding | **PASS — keep as reference** | "these look really real" |
| D02–D03 blue, held | **PASS on size** | "that's a great size" |
| D04–D05 Go Away | size note | "that's a bit big, actually" |

**Sizing is fine across the whole held group** — it is only the wall-mounted
group where scale collapses. Another argument for the held format.

---

## What this settles

1. **The tell is contrast plus holes plus scale**, in that order, and all three
   are now either fixed or gated. See `../../SIGN_CAROUSEL_ENGINE.md` §4b, §4c.
2. **Held beats wall-mounted** for believability, because a person anchors scale.
3. **Black beats sage** when the sign must read as an object.
4. **Sage is not a hero colourway.** Rejected on both plates it appeared on, for
   contrast, independently of size.

## Correction to my own gate

I wrote the ink-ratio gate as **0.12–0.24**. That range was measured on **black
only**, and as an upper bound it is wrong — the Freya blue master measures 0.440
and Max passed it as the best image in the set. Pale colourways legitimately sit
high.

**Corrected: the gate is a floor, not a window.** Ratio must be **≥ 0.11**. Below
0.08 is the vector-black signature. For black specifically, expect 0.12–0.24.
