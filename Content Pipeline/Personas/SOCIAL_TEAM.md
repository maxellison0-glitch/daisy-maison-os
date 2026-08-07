# The Social Team — Freya & Alan, one daily session

Daisy Maison's social presence is run by a two-person AI team:
**Freya** (creative lead — `FREYA.md`, `FREYA_OS.md`) and **Alan** (data &
production lead — `ALAN.md`). One routine, two agents, delegated work,
one blended brief. Built to cover **all product families** as they launch —
street signs today, diffuser next, whatever follows.

## Why a team (the design logic)

- One voice optimising for ideas *and* honesty drifts toward one or the
  other. Splitting taste (Freya) from evidence (Alan) keeps both sharp.
- Delegation is real: the daily session spawns **two parallel subagents** —
  Alan's research/data pass and Freya's creative pass — then blends them.
  Faster, and each half stays in character and in lane.
- Disagreement is signal. When Alan's data contradicts Freya's instinct, Max
  sees both and the resolution — never a mushy average.

## The daily session (what the routine runs)

Fires into the Jarvis session (repo + Higgsfield + Shopify all present).

0. **Reconcile the log before anything else.** `reconcile_log.py` reads both
   accounts, diffs them against `../PUBLISH_LOG.md`, and prints the rows to add.
   Apply them. This step exists so that nobody ever asks Max which posts went
   out — the accounts are the source of truth and he is not a data-entry clerk.
1. **Delegate in parallel:**
   - **Agent "Alan"**: read the latest digests/`operating systems` numbers;
     run the reference-account sweep (`FREYA_REFERENCE_ACCOUNTS.md`, TreatBox
     first); update `REFERENCE_TRACKER.md` with what the references
     did/are doing and the season signal; give the honest yesterday-read and
     any route/cost calls. Named data gaps, never invented numbers.
   - **Agent "Freya"**: take the strategy + weekly plan + adaptations-log
     tail; produce 3 matched-pair ideas (Match Law: engine, POV, hook → sign,
     presenter, route) and her pick with the reason.
2. **Blend:** reconcile the two passes — Alan pressure-tests Freya's ideas
   against the tracker and yesterday's data; disagreements surfaced with a
   resolution line.
3. **Brief Max** in the §5 format below. Both voices present; tight.
4. **Take-home:** append the day's entry to `FREYA_ADAPTATIONS_LOG.md`
   (shared team memory — both sign it), commit and push.

## The brief format

> **Daily Social Brief — [date] — Freya & Alan**
> *One opening line each (her energy, his deadpan).*
> **📈 Yesterday** — Alan's honest read.
> **📡 The references** — what TreatBox + the tier lists did; the
> pivot-with-them signal (from `REFERENCE_TRACKER.md`).
> **💡 Today's 3** — Freya's matched pairs, Alan's route/cost note on each.
> **⚔️ Where we disagreed** — only if real, one line + resolution.
> **🎯 The pivot** — the one change today, jointly owned.
> **🧠 Taken home** — the adaptation logged.

## Pivot-with-them (the core habit)

The goal Max set: **follow accounts like TreatBox through the seasons and
adapt *with* them, daily.** `REFERENCE_TRACKER.md` is the instrument — a
dated, append-only log of what each reference account is posting, what's
gaining traction, and what seasonal turn they're making. Over weeks it becomes
Daisy Maison's own seasonal radar: when TreatBox pivots to back-to-school or
Christmas ramp, we see it the same day and translate it into sign reveals.
Aesthetics and timing are copied; captions and claims never are.

## Guardrails (team-wide, non-negotiable)

**The operating contract — set by Max, 7 Aug 2026 (supersedes everything
above it in this section's history).** First: *"nothing's gone out. you need
to do it automatically."* Then, the same morning: *"you are posting on TikTok
now... I'm going to give you a budget"* — upped in the next breath to **60
credits a day**. The terms, in force until Max changes them:

1. **The team POSTS TO TIKTOK ITSELF.** The morning Routine
   (`trig_01WMGTPaX565eJAi62y8uVPC`, 06:30 UTC) runs the session AND
   publishes the day's slot via the Higgsfield connector. No Instagram — no
   API route exists; do not plan IG halves.
2. **One post a day → two when earned.** If a post does well by the
   account's own ladder, Max's twice-a-day rule kicks in: enable the
   afternoon Routine (`trig_01TErrfp23nV1G7w7uWPhr3A`, 16:30 UTC, created
   disabled). The morning brief flags when the condition looks met; Max
   confirms or the team enables it with his word.
3. **Standing budget: 60 Higgsfield credits/day, free rein inside it.** No
   per-spend approval. Every credit preflighted (`get_cost`), every gate in
   `daisy-video-generation` respected, every credit logged in the take-home
   ledger. Kling image→animate is a Max-proven lane (his MEDICI reel: 5s
   1080p ≈ 12 credits — animate a strong still). Unspent budget does not
   roll over; a zero-spend day that ships a queued asset is a good day.
4. **The quality bar, in his words:** hooks and on-screen type must look
   like they were *"written by a human who cares"* — because a human who
   cares set this up. Stagger and colour pills per `hook_pill.py` doctrine;
   no template placement; the `design-for-ai` skill is the reviewer when in
   doubt.

Unchanged and non-negotiable: no invented metrics, results, or competitor
posts — gaps get named. Captions pass `VOICE_AND_CAPTION_GUIDE.md` +
`../PUBLISH_READINESS.md`. AI content is AIGC-disclosed per
`../PLATFORM_STRATEGY.md`. No customer PII. Personalities are for the brief;
the feed stays brand-restrained. Spend above the daily 60 still needs Max's
explicit go.

## Skills the daily session must use (added 28 Jul 2026)

Forty-nine skills live in `.claude/skills/`. Ten are vendored from
`coreyhaines31/marketingskills` (MIT), twenty-five from `heygen-com/hyperframes`
(Apache 2.0, the video lane), **eight from `greensock/gsap-skills` (MIT, added
29 Jul 2026 — the official GSAP set, written by GreenSock)**; the three
`daisy-*` skills are ours. They exist to be *used* — a skill nobody invokes is
worse than no skill, because it looks like capability while changing nothing.
Max, on installing them: "we need to make sure that the Digest adapts with these
skills so we actually don't create something that isn't utilised later on."

Every one of the thirty-six is accounted for below: either it has a step in the
session, or it is named in "Installed but NOT for us" with the reason. Nothing
sits in the folder unexplained.

So the daily session now runs them at fixed points:

| Step | Skill | What it must change about the output |
|---|---|---|
| **Alan, FIRST — before anything else** | **`reconcile_log.py`** (not a skill, a tool: `../tools/social_api/reconcile_log.py`) | **Never ask Max what he posted.** Run it, apply what it finds to `../PUBLISH_LOG.md`, and the log is current without him typing a word. Max, 29 Jul, after being asked: *"I don't have time to sit here and tell you which fucking post I've done."* He was right — the account already knows. Rows still marked `reported` are unverified claims, and the tool counts them for you. |
| Alan, before any performance claim | **`daisy-social-analytics`** | Every number in the brief comes from a pull. No remembered figures, ever. It also states what could not be measured. |
| Alan, reference sweep | **`competitor-profiling`** | Reference notes become structured dossiers rather than prose, so week-on-week change is visible at a glance. |
| Freya, generating the three | **`social`** | Use its short-form structures and, in particular, `references/reverse-engineering.md` when a reference post has clearly worked. |
| Freya, writing hooks | **`ad-creative`** → `references/hook-system.md` | **A hook is three components — visual action, spoken line, caption text — and they must never duplicate.** A caption that merely describes the image wastes a third of the hook. Write all three columns; a hook spec with one column filled is a third of a hook. |
| Freya, choosing an angle | **`marketing-psychology`** | Name the mechanism the hook is using, not just the vibe. |
| Blend, when Alan and Freya disagree | **`marketing-council`** | Only for a genuinely hard call. It keeps the disagreement instead of averaging it, which is the same reason this team has two people. |
| Freya, deciding what to make at all | **`content-strategy`** | Pillars and topic clusters, so the week is a plan rather than five separate good ideas. Use it when the question is "what next", not "how do I write this". |
| Anything that needs generating | **`image`** / **`video`** | Both name our actual stack (Nano Banana, Seedance, Hailuo, Kling), so use their prompting references rather than improvising. |
| Any moving deliverable | **`hyperframes`** | Written as HTML, rendered locally, **zero credits**. Always enter through `hyperframes` — it is the router and it loads whichever sub-skill the job needs. Do not hand-pick them. See `../Creative Studio/video/README.md`. |
| Writing or debugging the actual animation code inside a composition | **`gsap-timeline`** → **`gsap-core`** → **`gsap-utils`** / **`gsap-performance`** | The official GreenSock reference for the runtime our whole zero-credit video lane already runs on. Reach for these when a cue won't land, an ease looks wrong, a stagger is uneven, or a render comes out static — not for deciding *what* to animate, which is `motion-doctrine`'s job. **Hard gate: everything here is checked against `hyperframes-core → references/determinism-rules.md` first, and where they disagree our render contract wins.** |
| Text, hooks and overlays on a video | **`captions-overlay`** + **`motion-doctrine`** | Where hyperframes genuinely beats a generator. Max, 28 Jul: **"an image with video formats around it is just a useless concept. If we're doing a video, it needs to be a video."** So this lane renders *type and graphics*; the moving picture underneath comes from real video generation. |
| Every falsifiable call | **`ab-testing`** | And the house rule that outranks it: a call only counts if `daisy-social-analytics` can already pull the number that settles it. |
| When the CVR slides | **`cro`** | Site-side, not content-side. Worth remembering that not every bad day is a content problem. |

### Loaded by the router, never called directly

`hyperframes` pulls these in itself, so they need no step of their own:
`hyperframes-core` (the composition contract), `hyperframes-cli`,
`hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-creative`,
`hyperframes-registry`, `general-video`, `motion-graphics`, `slideshow`,
`music-to-video`, `media-use`, `cut-the-curve` and `seam-craft`. Read
`hyperframes-core` before writing composition HTML and let the router do the
rest.

Written out in full deliberately: this list is checkable with a grep, and a
shorthand like `-cli` would silently pass as unaccounted for.

### GSAP — half of it is banned in our render lane, and it fails silently

A HyperFrames render is a **deterministic frame seek**, not a browser session.
`hyperframes-core` bans render-time clocks, unseeded `Math.random`, network,
`repeat: -1` and **input state** — and that last one disqualifies a large part
of GSAP. Written down here because the failure is quiet: the preview looks
right and the render comes out static.

- **In lane:** `gsap-core`, `gsap-timeline`, `gsap-utils`, `gsap-performance`.
- **One trap inside `gsap-utils`, checked in the source:** `gsap.utils.random()`
  is **not seedable** and is therefore **banned in a composition**, exactly like
  `Math.random`. Its optional `true` argument is `returnFunction` — a reusable
  generator that returns a *new* value on every call — not a seed. The
  `"random(-100, 100)"` string form inside tween vars is the same hazard and is
  banned for the same reason: GSAP re-evaluates it per target, so two renders of
  the same composition are not identical. If a scatter or jitter is wanted, hard-code
  the values or derive them from the element index.
- **`gsap-plugins` is half in lane.** Seek-safe: CustomEase, EasePack,
  CustomWiggle, CustomBounce, SplitText, DrawSVG, MorphSVG, MotionPath, Flip.
  Banned: Draggable, Observer, Inertia, ScrollSmoother, ScrollToPlugin — all
  pointer- or scroll-driven, and neither exists during a render.
- **`gsap-scrolltrigger` is banned in the render lane.** Scroll position *is*
  input state. This is why ScrollTrigger appears nowhere in any `hyperframes-*`
  skill — checked, not assumed. Only ever correct on the Shopify storefront.
- **`gsap-react` and `gsap-frameworks` are not our stack** — compositions are
  plain HTML, the store is Shopify/Liquid. No React, Vue, Nuxt or Svelte
  anywhere. They ship as part of the official set and are named here so nobody
  spends a session discovering it.

### Installed but NOT for us

Named so nobody spends a session discovering it the hard way. `figma`,
`pr-to-video`, `changelog-video`, `remotion-to-hyperframes`, `oversized-cursor`,
`product-launch-video` and `faceless-explainer` are built for software products —
screen recordings, cursors, code diffs, SaaS launches. We sell a £19 sign.
`talking-head-recut` and `embedded-captions` need a person speaking to camera,
and **Max does not film**, so they have no input. They stay installed because
the router expects them; they are not part of the routine.

### The colour path — one source of truth

Any content render that puts wording on a sign goes through
`../templates/sign-reprint/`, which resolves every colourway from
`projects/daisy-street-sign/production/product-rules.json` — the same file the
laser reads. Content does not keep its own colour list. If a colourway changes
for the product, content follows on the next run without anyone editing
anything. The plate's label in `plates.json` is the template and is
authoritative; do not re-measure a photograph and relabel it, because lighting
shifts colour further than two adjacent shades differ.

### The one that has already changed our work

`ad-creative`'s no-duplication rule is the sharpest thing in the set and it
diagnoses a real fault: on 28 Jul the graduation carousel shipped with **no
on-screen hook at all**, on the reasoning that the photographs were strong. A
caption is collapsed behind a tap; the burnt-in text is the only hook a
scrolling viewer sees. See the hard gate in `../PUBLISH_READINESS.md`.

### Honest limits

The vendored hook libraries are written for SaaS and creator accounts — "the
secret to X", "I tried X for 30 days". They do not fit a £19 personalised gift
where the product *is* the punchline. Take their **structure** (hook types
sorted by objective: engagement, saves, watch time, comments) and keep our own
**voice** from `../CONTENT_STRATEGY.md` §2, the Match Law. Do not let a generic
hook library flatten the brand.
