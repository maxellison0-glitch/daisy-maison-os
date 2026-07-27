# Automation architecture — what runs itself, what doesn't

This is the answer to "fully automated within this workflow." Split
honestly into two tiers, because they carry very different risk.

## Tier 1: production and judgment — can run end-to-end

This is genuinely automatable now, and it's most of the actual work:

1. **Generate.** Pull from `IDEAS.md`/`PRODUCTION_QUEUE.md`, produce
   candidates via Higgsfield (images, video, captions) using the locked
   character and product references.
2. **Evaluate.** Run every candidate against `PUBLISH_READINESS.md`'s seven
   dimensions, including the automated `virality_predictor` pass.
3. **Diagnose and edit.** When something fails, name which dimension failed
   and apply the matching fix — a re-cut hook, a corrected identity prompt,
   a rewritten caption — rather than blindly regenerating the whole asset.
4. **Iterate.** Repeat until a candidate genuinely passes, or until the
   evidence says the concept/method itself is the problem (KILL — stop,
   don't sink more credits).
5. **Log.** Every generation's prompt, model, job ID and verdict recorded
   in the relevant concept folder, same discipline already proven on
   product video.

This loop does not need a human in it at every step. It needs a human at
the end of it.

## Tier 2: publish — stays a human checkpoint, deliberately

Final publish to the real public accounts is not automated, and this isn't
a placeholder limitation — it's the correct design, for two reasons that
both hold independent of each other:

**It's already this business's standing rule.** Every document in this
repo that touches production says some version of the same thing: nothing
is posted without Max's explicit approval, connector access "does not
permit... publishing... without Max's approval"
(`Creative Studio/CLAUDE.md`), a post moves to `Scheduled` only after
verification (`README.md`). This system doesn't override that; it feeds it.

**It's the actually-correct design regardless.** A wrong post going out
automatically to a real brand's public account — a fabricated claim, a
drifted character face, a tone-deaf moment — is a genuinely bad outcome
that full automation of Tier 1 makes *more* likely to reach that point
untouched, not less. The fix isn't removing the checkpoint; it's making it
fast. If Tier 1 is doing its job, Max's part shrinks to a quick look at
work that's already passed seven checks and a virality read — not sifting
raw generations himself.

## What "fully automated" concretely looks like once this is running

Max (or this session, prompted to run the pipeline) reviews a short queue
of finished, already-passing candidates with captions attached, and taps
approve or reject. That's the whole remaining manual step. Everything
upstream of that — ideation triage, generation, technical QC, brand-tone
QC, caption drafting, platform-specific re-wrapping, iteration on anything
that fails — already happened without him.

## Closing the loop to actual publishing

Two separate paths exist, both currently un-activated — don't touch either
without explicit instruction, since both are real public-facing actions:

- **The connector Max mentioned isn't built yet.** Disregarded per current
  instructions; this doc doesn't change that.
- **Higgsfield itself already exposes native TikTok publishing tools**
  (`tiktok_connect`, `tiktok_prepare_publish`, `tiktok_publish`,
  `tiktok_publish_status`) — discovered while building this system, not yet
  tested or connected to a real account. This may resolve part of the
  "connector isn't ready" gap sooner than expected, specifically for
  TikTok. Worth knowing about; not worth acting on until Max says so — an
  untested publish path to a live account is exactly the kind of action
  that needs a deliberate yes, not an assumed one.

Once either path is live, Tier 2 doesn't have to mean "Max personally clicks
publish in an app" — it can mean "Max approves in this workflow, and the
approved post is what actually gets scheduled." The checkpoint stays; the
friction around it doesn't have to.

## Known operational constraints (found by running this for real)

- Higgsfield's Max plan caps concurrent jobs at 8 — batch generation
  requests queue past that and need a second submission wave, not a
  failure to work around.
- The `soul_2` reference-image-conditioned generation path applies its own
  prompt enhancement that isn't fully suppressible via parameters (see the
  worked example in `PUBLISH_READINESS.md`) — budget for an extra QC pass
  specifically on brand-tone drift whenever a batch uses image references,
  not just plain text-to-image.
- Cost throughout this build has been trivial (low single-digit credits
  per batch against a 1,000+ credit balance) — credit spend is not the
  constraint on how far Tier 1 automation can run; judgment quality is.
