# Freya & Alan — Daily Automation (how it actually runs)

The daily social session is a Claude **Routine** — `Freya & Alan — Daily
Social @daisymaison` (trigger `trig_01WMGTPaX565eJAi62y8uVPC`) — visible and
manageable at claude.ai → Routines from any device (work laptop, work PC,
phone).

## The architecture that works
- **Fires into the persistent Jarvis session** (self-bind), not a fresh
  session. Lesson learned 24 Jul: a fresh-session routine created from inside
  a coding session gets **no repo access and no connectors** — the first run
  failed exactly that way. The bound session already holds the cloned repo,
  git, Higgsfield and Shopify, so the team wakes up with all tools live.
- **Schedule:** daily 07:30 UK (`30 6 * * *` UTC in BST; shift to `30 7` on GMT).
- **Trade-off accepted:** self-bind routines don't send completion push/email
  — the brief lands in the Jarvis conversation itself, with full continuity.

## What each run does
Per `SOCIAL_TEAM.md`: pull the branch → both personas boot → **parallel
subagents** (Alan: numbers + reference sweep + `REFERENCE_TRACKER.md` entry;
Freya: 3 matched-pair ideas) → blend + surface real disagreements → Daily
Social Brief in both voices → take-home entry appended to
`FREYA_ADAPTATIONS_LOG.md` → commit + push.

## Guardrails
Propose only — no publishing, no paid credit spend without Max's explicit go.
No invented metrics or competitor posts; gaps are named. Captions pass the
voice guide + `PUBLISH_READINESS.md`; AI content follows
`PLATFORM_STRATEGY.md` disclosure. No customer PII.

## Managing it
Pause/resume/retime/edit from claude.ai → Routines, or just ask in-session.
If this session is ever retired, recreate the routine bound to its successor
(or from the Routines UI with repo + connectors attached).
