# Freya — Daily Automation

A Claude **Routine** fires Freya once every morning to run her daily session
(`FREYA_OS.md` §4) and deliver the Daily Brief. Because it's a Claude Routine,
Max can read/manage it from any device signed into Claude (work laptop, work
PC, phone) — not just this session.

## Schedule
- **Daily, 07:30 UK** (`30 6 * * *` UTC in summer/BST; adjust to `30 7 * * *`
  when the UK is on GMT).
- **Fresh session per fire** — each run is clean and self-contained, so the
  brief is reproducible and readable anywhere.
- **Notifications on** — the finished brief is pushed to Max's phone and
  emailed, so it's in his inbox each morning.

## What it does each run
Runs `FREYA_OS.md` §4 end-to-end: boot → **external research first** →
yesterday's numbers (honest, gaps named) → what's working → 3 matched-pair
ideas → the pivot → append take-home adaptations to
`FREYA_ADAPTATIONS_LOG.md` → commit/push → present the brief.

## Guardrails (baked into the routine prompt)
- **Proposes, never disposes.** No publishing and no paid credit spend without
  Max's explicit go — ever.
- **Honest.** Never invents a metric, a result, or what an account posted. If
  a data source (e.g. Shopify) isn't reachable in an automated run, it says so.
- **Brand-safe + disclosed.** Captions pass `VOICE_AND_CAPTION_GUIDE.md` and
  `PUBLISH_READINESS.md`; any AI content follows the disclosure rule in
  `PLATFORM_STRATEGY.md`.
- **No customer PII** in ideas or logs.

## Managing it
- Change time / pause / resume / edit the prompt: from Claude on any device,
  or ask in-session ("Freya, move the brief to 8am", "pause Freya").
- Trigger id is recorded on creation; use it to update or delete the routine.

## Reliability note (branch)
The routine reads Freya's files from the repo. Until this branch is merged to
`main`, the routine ensures it's on the branch that contains
`Content Pipeline/Personas/FREYA_OS.md` before running. **Merging the open PR
to `main` makes this bulletproof** — recommended once the first few briefs look
right.
