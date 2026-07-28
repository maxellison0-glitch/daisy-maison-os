# Publish Readiness — is this actually good enough to post?

This is the standard that turns "I generated something" into "I judged it."
Every piece of generated or edited content — Freya's stills, Max's synthetic
clips, product video, carousels — passes through this before it can move to
`Ready for approval` in `PRODUCTION_QUEUE.md`. This is a working evaluation
tool, not a taste statement: it produces one of three verdicts, and EDIT
always names the specific fix, never "try again and hope."

## The decision protocol

**PASS** — Meets every dimension below at production quality. Move to
`Ready for approval` for Max's sign-off (see `README.md`'s approval gates).

**EDIT** — One or more specific, nameable flaws. Diagnose which dimension
failed, apply the matching fix below, regenerate only what needs it. Never
regenerate the whole asset blind when the flaw is localised.

**KILL** — The concept, the reference, or the generation method itself is
wrong, not just one output. Stop spending credits on it. Change the method
or drop the concept. Log why, so the same dead end isn't re-walked.

An agent verdict is never the final word — it filters obvious failures so
Max's attention goes to genuine judgment calls, not technical faults. This
mirrors the rule already locked for product video: `agent-pass` is never
`max-approved` (`Creative Studio/MEMORY.md`).

## The seven dimensions

### 1. Hook (first frame / first 1-2 seconds)

Does it stop the scroll with sound off? Is the value proposition or
curiosity legible instantly, with no context? Weak hooks are the single
biggest reach killer — TikTok/Reels ranking leans hard on whether people
stay past the first second.

- **Fail mode:** slow build, logo/branding first, or a hook that's true but
  not specific ("check this out" vs "which one would you choose").
- **Fix:** re-cut the opening or rewrite the on-screen hook line. This is
  almost always an edit, not a regeneration — see `VOICE_AND_CAPTION_GUIDE.md`
  hook bank.

### 2. Technical & product fidelity

For product video/images: does the real product survive exactly, per
`Creative Studio/WEDDING_SIGN_VIDEO_RULES.md` and the equivalent rules for
any other product line? Border, proportions, material, construction,
wording — pixel-exact where it matters.

- **Fail mode:** any product-surface drift (overlay seam, wrong thickness,
  invented material, changed wording) — **and wrong whole-object scale**,
  which passes every lettering check while still depicting a different
  product. Proven live on DM-C018: Freya's first sign take had pixel-exact
  wording but rendered the sign ~13-15% undersized against her body; Max
  caught it by eye, measurement confirmed it.
- **Check scale first, and check it numerically when a person holds the
  product:** measure sign-width-to-shoulder-width in pixels and compare
  against a known-good reference (Alan's Bond hero ratio is 1.63; the same
  physical sign on narrower female shoulders needs ~1.9+). Two minutes in
  a script, catches what lettering QC structurally cannot — see
  `Creative Studio/active/DM-C018-freya-synthetic-sign-turn/working/qc/`.
- **Fix:** per the wedding-sign rules — reject and regenerate from an
  approved source image. Do not patch a drifted product shot; a human
  perception failure isn't fixable by editing around it. For scale
  specifically, a real photo of a person holding the product, supplied as
  an explicit scale-authority reference, fixed it in one take on DM-C018.

### 3. Identity & character consistency

For anything featuring Max or Freya: is it recognisably the same person as
the locked reference? Check the specific "tell" details first — they're the
fast, reliable signal (see `Personas/HIGGSFIELD_CHARACTER_BUILD.md`'s
consistency toolkit): the signature accessory, freckle pattern, hair colour,
face shape.

- **Fail mode:** identity drift — different bone structure, added/removed
  freckles, hair colour or styling that wasn't in the locked hero, an
  accessory that vanished or changed.
- **Fix:** if it's one detail (hair colour drifted, ring missing), regenerate
  that shot with the specific correction named explicitly in the prompt —
  don't assume the model "remembers" the spec. If several shots in a batch
  drift the same way, the generation *method* is the problem, not the
  individual shots — see the worked example below.

### 4. Brand tone & "no AI spectacle"

Does it look like it belongs in the same photographic and emotional world
as Daisy Maison's real product photography — warm, matte, boutique,
frictionless? Or does it read as generic AI/influencer output — glossy skin,
fake tan, an "editorial" intensity that doesn't match the brand?

- **Fail mode:** airbrushed symmetry, oiled/dewy skin sheen, styling more
  "fashion campaign" than "approachable social lead," an intensity of
  expression that doesn't match the locked persona voice.
- **Fix:** this is often a generation-pipeline issue, not a prompt-wording
  issue — see the worked example below for a real case where the fix wasn't
  available as a settable parameter and required strengthening the prompt's
  explicit negatives instead.

### 5. Caption & voice

Does the caption match the fronting character's locked voice
(`Personas/MAX.md` or `Personas/FREYA.md`) and the shared playbook
(`Personas/VOICE_AND_CAPTION_GUIDE.md`)? Is every claim in it true?

- **Fail mode:** generic hype language, an American cadence, a fabricated
  personal-life claim, a claim about stock/price/delivery that hasn't been
  verified against the live site.
- **Fix:** rewrite against the playbook's templates. This is always a fast
  edit — never a reason to reject the visual asset.

### 6. Platform fit

Right aspect ratio, right length, right pacing and on-screen-text
convention for where this is actually going — see `PLATFORM_STRATEGY.md`.
A technically perfect asset built for the wrong platform's grammar
under-performs regardless of quality.

- **Fail mode:** a slow, polished IG-style edit posted natively to TikTok
  (or vice versa); text outside the safe zone once platform UI is
  accounted for; wrong duration for the platform's sweet spot.
- **Fix:** re-cut the platform-specific version. The pipeline already
  produces one master concept adapted per platform — this dimension checks
  that adaptation actually happened, not just got copy-pasted.

### 7. Predicted performance signal

Higgsfield's `virality_predictor` tool gives a real, automated read on hook
strength, retention risk and predicted engagement. Run every near-final
candidate through it before presenting for approval. Treat it as one input,
not the verdict — it catches things human eyes skim past (pacing lulls,
weak retention windows) but it doesn't know the brand, the product truth
rules, or whether a claim is honest. A high score with a dimension-1-6
failure is still a KILL or EDIT.

## Worked example: the Freya Stage 2 batch, 23 July 2026

This ran the protocol for real, so it's kept here as the reference case.

Ten reference-expansion images were generated from the locked hero
(candidate-03) using Higgsfield's reference-image-conditioned path. QC
against dimension 4 failed across the batch: deeper fake tan, oiled skin
sheen, added hair highlighting not in the hero, and a "fashion campaign"
intensity replacing the locked warm expression — a textbook brand-tone
failure, not a one-off bad seed.

Diagnosis before any fix was attempted: the tool's own prompt-enhancer was
rewriting the prompt on this specific generation path, injecting language
like "sun-kissed... healthy glow" and "editorial" that fought the explicit
brief. First fix attempt — pass `enhance_prompt: false` — was silently
rejected by the tool ("Soul 2.0 does not support this parameter"). That
ruled out the clean fix. Second attempt — strengthening the prompt's
explicit negatives ("no fake tan, no glossy influencer sheen, matte skin not
oiled or dewy") — measurably improved several shots even though the
enhancer kept firing regardless, confirmed by comparing the actual pixels
before and after, not the tool's own text description of what it made.

Verdict: **partial pass**. A few shots hold the brand's real look and are
usable; several still drift enough that the batch should not be used to
train a persistent Soul identity without a human look first. Logged as a
standing finding in `Personas/HIGGSFIELD_CHARACTER_BUILD.md` rather than
quietly accepted — this generation path has a structural bias worth knowing
about before the next batch, not a one-time fluke to shrug off.

## What this rubric explicitly refuses to do

- Treat "the automated check passed" as equivalent to "post this." Pixel
  provenance and correct metrics cannot overrule a human-perceived failure —
  this principle is already proven the hard way on product video and
  applies identically here.
- Accept a KILL-worthy method problem patched into a PASS by cherry-picking
  the least-bad output from a flawed batch. If the method is wrong, fix the
  method.
- Let "fully automated" mean "unreviewed." See `AUTOMATION.md` for exactly
  where the human checkpoint stays and why.

## Hard gate: every published still carries an on-screen hook

Added 28 Jul 2026. Max: *"zero on screen hooks can't expect them to perform
well."* He was right and it cost a live post.

**No still, carousel slide or photo post ships without burnt-in hook text.** Not
"usually". Not "unless the photograph is nice". The caption is not the hook — on
TikTok and Reels the caption is collapsed behind a tap, so a product photograph
with no text on it is a scroll-past no matter how good the photograph is.

How it happened, so it doesn't again: the hooks for the graduation carousel were
written in the morning and then dropped at export, because the generated
photographs looked strong enough on their own. They weren't. The DM-HOUSE-QUIZ
and diffuser carousels both carried pills and both were built by the same
process — the difference was a silent decision made at the last step with no
gate to catch it.

The check, before any upload:

1. Open every frame. Is there hook text on it? If any frame has none, stop.
2. On a carousel, does slide 1 set up a loop that a later slide closes? Two
   pretty photographs side by side is not a carousel, it is two photographs.
3. Is the pill clear of the platform's UI - top ~120px, and on 9:16 the bottom
   ~450px where the caption and buttons sit?

Treat a missing hook exactly like a missing colourway check: it is not a taste
call, it is a fault, and the post does not go.
