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

Propose, never publish. No paid credits without Max's explicit go. No
invented metrics or competitor posts — gaps get named. Captions pass
`VOICE_AND_CAPTION_GUIDE.md` + `../PUBLISH_READINESS.md`. AI content follows
`../PLATFORM_STRATEGY.md` disclosure. No customer PII. Personalities are for
the brief; the feed stays brand-restrained.

## Skills the daily session must use (added 28 Jul 2026)

Thirty-five skills live in `.claude/skills/`. Ten are vendored from
`coreyhaines31/marketingskills` (MIT), twenty-four from `heygen-com/hyperframes`
(Apache 2.0, the video lane); `daisy-social-analytics` is ours. They
exist to be *used* — a skill nobody invokes is worse than no skill, because it
looks like capability while changing nothing. Max, on installing them: "we need
to make sure that the Digest adapts with these skills so we actually don't
create something that isn't utilised later on."

So the daily session now runs them at fixed points:

| Step | Skill | What it must change about the output |
|---|---|---|
| Alan, before any performance claim | **`daisy-social-analytics`** | Every number in the brief comes from a pull. No remembered figures, ever. It also states what could not be measured. |
| Alan, reference sweep | **`competitor-profiling`** | Reference notes become structured dossiers rather than prose, so week-on-week change is visible at a glance. |
| Freya, generating the three | **`social`** | Use its short-form structures and, in particular, `references/reverse-engineering.md` when a reference post has clearly worked. |
| Freya, writing hooks | **`ad-creative`** → `references/hook-system.md` | **A hook is three components — visual action, spoken line, caption text — and they must never duplicate.** A caption that merely describes the image wastes a third of the hook. Write all three columns; a hook spec with one column filled is a third of a hook. |
| Freya, choosing an angle | **`marketing-psychology`** | Name the mechanism the hook is using, not just the vibe. |
| Blend, when Alan and Freya disagree | **`marketing-council`** | Only for a genuinely hard call. It keeps the disagreement instead of averaging it, which is the same reason this team has two people. |
| Anything that needs generating | **`image`** / **`video`** | Both name our actual stack (Nano Banana, Seedance, Hailuo, Kling), so use their prompting references rather than improvising. |
| Any moving deliverable | **`hyperframes`** (+ `captions-overlay`, `motion-doctrine`) | Written as HTML, rendered locally, **zero credits**. This is the default for anything that moves. Reserve paid generation for footage that genuinely could not be a still with motion applied to it. See `../Creative Studio/video/README.md`. |
| Every falsifiable call | **`ab-testing`** | And the house rule that outranks it: a call only counts if `daisy-social-analytics` can already pull the number that settles it. |
| When the CVR slides | **`cro`** | Site-side, not content-side. Worth remembering that not every bad day is a content problem. |

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
