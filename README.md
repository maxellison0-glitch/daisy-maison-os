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

This repository is the single source of truth for Daisy Maison's operating
context. It does not depend on MaxOS or any other repository — clone it
directly to its own top-level folder on every computer you use, and use it
from there.

### One-command sync (recommended)

On each computer, run this any time you start or finish working:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\sync.ps1
```

This pulls the latest from GitHub first (fast-forward only — it will stop and
tell you if there's a conflict rather than guess), then commits and pushes
anything you changed locally, so the next computer that runs it gets your
update. To only pull (e.g. at the start of a session, before you've made any
changes yet):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\sync.ps1 -PullOnly
```

### Manual sync (what the script does)

Before a run:

```powershell
Set-Location "$env:USERPROFILE\AA Daisy Maison OS"
git pull --ff-only
```

After an automation changes durable context:

```powershell
git add -A
git commit -m "Update Daisy operating context"
git push
```

If pull or push reports a conflict, stop and report it. Never commit connector
credentials, `.env` files, tokens, exports containing customer data, or payment
details.

## Design Project Routing

The Mr & Mrs street-sign system has one canonical project and one Jarvis entry:

```text
Project:    %USERPROFILE%\AA Daisy Maison OS\projects\daisy-street-sign
Automation: %USERPROFILE%\AA Daisy Maison OS\workflows\starred\daisy-street-sign-automation.md
```

The automation Markdown is the only street-sign document exposed as a primary
Jarvis orb. Its sections provide the smaller context orbs. Generator code,
assets, tests, references, and outputs stay inside the project and are loaded
only when an agent is producing signs or improving the automation.

Do not recreate `production-lab`, experiment briefs, handoff copies, or
agent-specific artwork folders.

## Organic Content Routing

The canonical planning and production entry point for Daisy Maison organic
Instagram, Facebook, and TikTok content is:

```text
%USERPROFILE%\AA Daisy Maison OS\Content Pipeline\README.md
```

Use that pipeline for ideas, briefs, approvals, scheduling, and performance
learning. The existing `projects/social-prompts/PROMPT.md` remains the specialist
prompt for turning a real product photo into a polished social image; it is not
a separate content workflow.
