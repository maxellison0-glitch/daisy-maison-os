# Daisy Morning Digest - Work PC Handoff

Source prompt: `operating systems/daisy-morning-digest-prompt.md`.

## Migration state

Prepare the digest on the always-on work PC, then disable the old home-hosted
copy only after one successful test run. Never leave two active 07:00 digests.

## Required local source

```text
%USERPROFILE%\AA Daisy Maison OS
```

Private repository:

```text
https://github.com/maxellison0-glitch/daisy-maison-os
```

The large `%USERPROFILE%\context.md` Daisy theme workspace is not required for
this analytics digest. Load or migrate it separately only for theme/code work.

## Work-PC bootstrap

Clone the repository into `%USERPROFILE%\AA Daisy Maison OS`.
If the folder already exists, do not clone over it. Open it and run
`git pull --ff-only` instead.

## Automation contract

- Use `operating systems/daisy-morning-digest-prompt.md` as the automation's source instructions.
- Run daily at approximately 07:00 Europe/London on the always-on work PC.
- Start by pulling `%USERPROFILE%\AA Daisy Maison OS` with `git pull --ff-only`.
  MaxOS is not needed for this job.
- Replace every old `C:\Users\maxel\...` path with `%USERPROFILE%\...`.
- Read Daisy files in this order:
  1. `operating systems\context.md`
  2. `operating systems\learnings.md`
  3. `operating systems\mounting-strips-price-test.md`
  4. `operating systems\etsy-latest.md`
  5. `title_optimisation_baseline.json` when the title tracker needs it
- Use the connected Shopify source for `daisymaisonuk.myshopify.com` and the
  Windsor Google Ads/Facebook Ads sources already named in the existing digest.
- Do not duplicate the hourly sales pulse. This digest is the deeper daily
  completed-day analysis and WhatsApp summary.
- Save every successful run to `digests\digest_YYYY-MM-DD.md` using the
  Europe/London run date, include the exact `Spend: £X | Sales: £Y | Orders: N`
  headline, and commit/push that artifact with the other intended Daisy updates.
- Commit and push only the daily digest plus any intentionally changed
  `operating systems\context.md` or `title_optimisation_baseline.json` files.
- Stop plainly on Git conflict, missing connector authorization, or data-source
  failure; never invent values.
- Do not read or commit secrets, tokens, `.env` files, customer exports, Shopify
  credentials, Windsor credentials, or payment data.

## Connector gate

Before activation on the work PC, verify that its Codex/Claude environment can
access:

- Shopify analytics for Daisy Maison UK
- Windsor Google Ads account `880-835-8049`
- Windsor Facebook Ads account `1574764016252349`

Connector authorization is machine/session-specific and is not transferred by
GitHub. Files and prompts sync through Git; connector logins do not.

## Cutover checklist

1. Clone/pull the private Daisy OS repository on the work PC.
2. Verify the five read-first files exist under `%USERPROFILE%`.
3. Verify Shopify and Windsor connectors on the work PC.
4. Run one manual digest test without sending or mutating external systems.
5. Confirm its context-file update commits and pushes successfully.
6. Activate the work-PC 07:00 automation.
7. Disable the old home-hosted 07:00 automation immediately.
