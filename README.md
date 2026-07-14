# Daisy Maison OS

Private, versioned operating context for Daisy Maison automations and agents.
The repository deliberately excludes local archives, design assets, spreadsheets,
and scratch material that the daily digest does not need.

## Canonical location

Clone this repository to:

```text
%USERPROFILE%\AA Daisy Maison OS
```

Automation prompts must use `%USERPROFILE%` rather than a hard-coded Windows
username. This makes the same prompt work for `C:\Users\maxel` at home and
`C:\Users\customer` at work.

## Sync contract

Before a run:

```powershell
Set-Location "$env:USERPROFILE\AA Daisy Maison OS"
git pull --ff-only
```

After an automation changes durable context:

```powershell
git add -- "operating systems/context.md" "title_optimisation_baseline.json"
git commit -m "Update Daisy operating context"
git push
```

If pull or push reports a conflict, stop and report it. Never commit connector
credentials, `.env` files, tokens, exports containing customer data, or payment
details.

## Design Project Routing

The Mr & Mrs street-sign artwork has one canonical project only:

```text
%USERPROFILE%\MaxOS\projects\daisy-street-sign
```

Do not recreate `production-lab` or agent-specific artwork copies in this Daisy
operating-context repository. The approved generator and outputs live under the
MaxOS project's `artwork\` folder.
