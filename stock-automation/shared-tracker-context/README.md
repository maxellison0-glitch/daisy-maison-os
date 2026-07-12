# Daisy Maison Shared Tracker Context

Created: 2026-07-09

This folder is for sharing context between the existing Claude automation and the new Codex automation.

## Goal

Rebuild the current Claude stock tracker in Codex while keeping one shared operational context for:

- Shopify packaging stock usage.
- Packaging product rules.
- Supplier pricing and reorder logic.
- Future Etsy order tracking.

## Active Codex Automations

| Automation ID | Purpose | Schedule |
| --- | --- | --- |
| `daisy-maison-east-of-india-stock-report` | Codex takeover of Claude East of India stock report. | Daily 7:00am Europe/London |
| `daisy-maison-packaging-stock-usage-daily-report` | Packaging usage and reorder report. | Daily 7:30am Europe/London |

## File Roles

| File | Role |
| --- | --- |
| `shared-stock-context.md` | Human-readable source of truth shared by both trackers. |
| `claude-current-prompt.md` | Paste the exact current Claude automation prompt here. Do not rewrite it until captured. |
| `etsy-current-prompt.md` | Paste the Etsy prompt here so it can be adapted into the same stock workflow later. |
| `codex-rebuild-prompt.md` | Codex automation prompt rebuilt from the shared context and the Claude prompt once provided. |
| `codex-east-of-india-stock-report-prompt.md` | Codex takeover prompt for the Claude East of India stock-report automation. |
| `east-of-india-stock-state.md` | Persistent state for Etsy coverage, Etsy logs, mappings, extra accessories, thermal labels, and exclusions. |
| `tracker-change-log.md` | Record rule changes, corrections, and dates so both trackers stay aligned. |

## Important Rule

Do not let Claude-only or Codex-only assumptions drift. Any corrected packaging rule should be copied into `shared-stock-context.md`, then reflected in both automation prompts.
