# Tracker Change Log

Use this file to record stock-tracker rule changes so Claude and Codex stay aligned.

## 2026-07-09

- Created shared tracker context folder.
- Added packaging rules from Codex stock reference.
- Confirmed small street signs use larger Mail Lite envelopes.
- Confirmed East of India matchboxes fit D/1.
- Confirmed East of India tealights: up to 2 fit D/1.
- Confirmed small pebble hearts fit D/1 and should not be treated as framed pebble pictures.
- Created placeholder files for exact Claude and Etsy prompts.
- Added easier envelope wording: Small / Medium / Large envelope settings, mapped to D/1, F/3, and H/5 supplier codes.
- Imported exact Claude `daisy-maison-stock-report` prompt into `claude-current-prompt.md`.
- Created Codex takeover prompt for East of India stock reporting.
- Created `east-of-india-stock-state.md` as Codex persistent state for Etsy tracking and special cases.
- Created active Codex automation `daisy-maison-east-of-india-stock-report`, scheduled daily at 7:00am Europe/London.

## 2026-07-10

- Added working Daisy delivery pricing for Standard, DPD ship-to-shop 24-hour,
  DPD Express next-day, and DPD Super home 24-hour options.
- Kept VAT, insurance, the spoken `0.6` adjustment, and the prior GBP 3.94 /
  approximately GBP 0.80 Express wording explicitly as unresolved assumptions.
- Added photo-confirmed DPD pricing and corrected Super from the earlier spoken
  GBP 9.99 / GBP 3.70 figure to the written GBP 9.95 / GBP 3.66 figure.
- Added Highland and Islands Royal Mail 48HR conditional Letter, Frame, and
  Sign pricing from the handwritten reference; the extra GBP 8.95 Letter note
  remains explicitly ambiguous.
