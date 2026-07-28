# Voice & Caption Playbook

Shared by both characters. Use this alongside `Content Pipeline/README.md`'s
weekly mix and creative rules — this file is specifically about how things
are said, not what gets made. Usable immediately; it's a writing standard,
not a creative commitment that needs approval.

## Principles

1. First person, plain English, specific beats generic every time.
   "Laser-cut, hand-checked, packed same day" beats "quality you can trust."
2. Every caption earns its place: it teaches something true, invites a
   genuine reply, or tells a specific real story. If it does none of those,
   cut it.
3. Show the working. Say why a decision was made — why this font, why this
   box size. Reasoning builds more trust than a finished claim.
4. Two registers, one brand. Max = credibility through craft (process,
   quality, catching mistakes). Freya = credibility through taste
   (curation, choices, occasions). Don't blur them into one flat voice —
   see `MAX.md` and `FREYA.md`.
5. Hold the 70/20/10 mix already set in `Content Pipeline/README.md`: mostly
   useful/engaging, some proof/process, a little direct offer.
6. Never fabricate — reviews, stock, discounts, delivery promises, or (new)
   personal-life claims for either character. If it isn't true, it doesn't
   go in a caption.
7. British, not generic English-language internet. See the cheat sheet
   below.

## Hook bank

First line only — the rest of the caption has to earn what the hook
promises.

1. "POV: you just found out street signs can have your actual surname on
   them."
2. "Which one would you give the couple — 1, 2 or 3?"
3. "Here's what actually happens after you hit order."
4. "Three things I'd check before ordering any personalised sign."
5. "This took four minutes to make. Their reaction lasted a lot longer."
6. "Got this wrong the first time. Here's what changed."
7. "The couple already has everything. So what do you actually buy them?"
8. "Small, medium or large — here's what they really look like next to each
   other."
9. "Best man, groom, maid of honour — this one's for you if you're stuck."
10. "We don't do fake reviews. Just real orders, like this one."
11. "Nobody films this bit — checking every name spells right before it goes
    near the laser."
12. "A generic wedding gift would've been easier. Then we added their
    names."
13. "This order started as two names on a screen."
14. "Before you order anything personalised, read this."
15. "Not sponsored. Just genuinely the thing I'd buy."

Use these as structures, not scripts — the actual footage or product has to
earn the hook, same rule already set in `IDEAS.md`.

## Caption templates

**1. Hook → detail → payoff → soft CTA**
Line 1: hook. Line 2–3: one real specific detail (material, timing, a
decision made). Line 4: the small reveal or payoff. Close: a light question,
not a hard sell.

**2. POV / story**
Set a scene in second person ("You're stood there with the box, not sure
what to write..."). Deliver the emotional payoff in the middle. Close by
inviting their own story in the comments.

**3. Choice / carousel**
Pose the decision plainly. Give a light personal steer ("I'd go with two")
without pretending there's a wrong answer. Ask directly: comment 1, 2 or 3.

**4. Teaching / trust**
One useful, specific tip tied to a real detail from the shop — never generic
gifting advice. Close with a light, optional CTA. Never "link in bio NOW."

## UK voice cheat sheet

- Spellings: personalised, colour, favourite, jewellery, mum/nan/grandad,
  organise.
- Currency: always £, never $. "Quid" is fine in casual voice-note-style
  captions.
- Avoid Americanisms: gotten, "reached out," "gift" used as a verb, Mom,
  "so good you guys."
- Regional colour used sparingly, never gimmicky: Yorkshire coast towns,
  real UK seasonal occasions (school end-of-term for teacher gifts, not
  "back to school" US framing).
- Understatement over superlative hype: "properly lovely," "does the job
  beautifully," a knowing "no notes" beat "AMAZING!!! 😍😍😍."
- Emoji: 0–3 per caption, functional not decorative. One well-placed heart
  beats six.
- Self-deprecating humour welcome. Confidence stated plainly, never shouted
  in caps.

## What breaks authenticity

- A fabricated personal-life detail stated as literal fact (fake husband,
  fake hometown, fake wedding).
- The airbrushed, perfectly symmetrical "AI face" look — no texture, no
  asymmetry.
- A caption that suddenly reads like a press release.
- Freya being framed as the shop's owner or founder — that's Max, always.
- Inconsistent facts about her across posts (age, location, the signature
  accessory) — the locked bio in `FREYA.md` is the single source of truth.
- No prepared, honest answer if someone sincerely asks whether she's real.
- Hustle-culture CTAs ("DON'T MISS OUT," "LINK IN BIO NOW") — mismatched
  with a calm boutique brand.

## Taste gate — never rubber-stamp

This exists because we failed it. We shipped a v1 caption system and a v1 reel
that we *passed* — and Max's verdict was "still shit" and "AI slop." The deeper
failure wasn't the work, it was that we approved our own work instead of
critiquing it. That stops here. This gate is mandatory before anything renders
or ships.

**The rule:** review the work the way a human art director would tear it apart —
before it goes anywhere. Name what's mediocre, specifically. Then only pass work
you would genuinely be proud to post on your own account.

1. **"It does the job, I guess" is a FAIL, not a pass.** If your honest reaction
   is a shrug, it's rejected. The bar is "I'd be proud of this," not "this is
   defensible."
2. **Freya and Alan critique cold, and actually disagree.** The one who made it
   doesn't get to wave it through. The other reviews it like a stranger would,
   and says the unflattering thing out loud. A brief that shows fake consensus is
   a bug — if you agree, it has to be a *real* agreement you could each defend
   alone.
3. **Be specific or say nothing.** "Feels off" is useless. "The burgundy pill
   looks cheap, the white box fights the candlelight, the font is a TikTok
   default, and it's slapped dead-centre over the product" is a critique you can
   act on. Name the font, the hex, the placement, the frame.
4. **If neither of you can find a flaw, you're not looking hard enough.** That
   itself is the signal to slow down, not to ship.

### The "does this look like AI slop?" checklist (motion + realism)

Max's second verdict on v1: "still images turned into video and they weren't
still, they were vibrating." Captions are only half the job — if the underlying
motion screams AI, no typography saves it. Every clip passes this before it
ships. **The single standard: could this pass as filmed?** If not, it doesn't go.

- **(a) Vibration / jitter / shimmer on a shot that's meant to be static =
  REJECT.** ffmpeg `zoompan` on a still image jitters at the sub-pixel level and
  reads instantly as fake. A static shot must be *actually* static, or carry real
  motion — not a trembling still.
- **(b) Any warp, morph, wobble or drift on the product or its label between
  frames = REJECT.** The bottle, reeds and personalised text must stay
  pixel-stable. A label that breathes or letters that reflow is the worst
  possible tell on a brand whose whole promise is a precisely personalised object.
- **(c) Fake Ken-Burns pan/zoom that fools no one = REJECT.** A slow zoom across a
  flat still doesn't read as camera movement; it reads as a slideshow. Prefer,
  in order: (i) genuinely still footage held still; (ii) *real* image-to-video
  motion where the moving thing is something that should move — candle flicker,
  fairy-light shimmer, a wisp of scent-steam, shallow true parallax; (iii) a
  single, genuinely smooth, barely-perceptible push only if it's clean.
- **Motion belongs to the things that move.** In a candlelit reveal, the flame
  and the lights move; the bottle and the box do not. If everything is subtly
  swimming, it's slop.
- **When in doubt, hold the frame.** A clean static hero beats a wobbling
  "animated" one every time. Stillness reads as confidence and premium; jitter
  reads as cheap and synthetic — the exact "AI spectacle" the brand rules already
  forbid.

This gate applies to captions, motion, typography, colour and composition
alike. Passing it is the job. Rubber-stamping is not.
