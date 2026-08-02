# Instructions for Claude

You are the active creative operator for one Daisy Maison advert. Before doing
anything, read `CURRENT_CONTEXT.md`, `CREATIVE_BRIEF.md`, `PRODUCTION_PLAN.md`
and inspect `assets/from-this-day-forward-master.jpg` at full size.

## Working rule

The photograph is the product truth. Do not regenerate, redraw, replace or
relabel any product element. Superseded by Max (22 July 2026): outpainting and
generative extension are approved for SURROUNDINGS ONLY (linen, margins, scene
beyond the original square); every original product pixel remains immutable.
Generative enhancement of product regions is allowed only if it passes a
letter-perfect frame-level truth test against the original (see
COLLABORATION_LOG.md Turn 10 for accepted/rejected precedents).

The deterministic crop-pan animatic approach was rejected by Max (22 July).
Current pipeline: approved base stills -> camera-only image-to-video motion ->
frame-level fidelity check -> assembly. Foundation first, then motion.

## Calling Codex as supervisor

When Max asks you to work with Codex, or when you want an independent technical
challenge before locking a material edit decision, invoke the real Codex CLI:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".collaboration/invoke-codex.ps1" "<context-rich review request>"
```

The wrapper calls the Daisy Maison workspace's official Codex wrapper in an
ephemeral read-only sandbox. State the objective, named source files, locked
decisions, rejected directions, exact question and whether edits are allowed.

- Never simulate Codex.
- Report whether the CLI call succeeded.
- Treat its answer as an independent opinion, not an automatic instruction.
- Do not ask Codex to call Claude back in the same review round.
- Cross-model review is read-only unless Max explicitly authorises shared
  implementation and assigns file ownership.
- Write accepted decisions into `CURRENT_CONTEXT.md`, not a raw transcript.
- Max has final authority.

## First task

Build or direct the silent three-shot technical animatic described in
`PRODUCTION_PLAN.md`. Do not expand the campaign or return to the family version
until Max approves or rejects this exact visual mechanism.

