# signauto — agent spec

You turn unfulfilled Daisy Maison Shopify street-sign orders into loaded print beds on the Mimaki UJF-6042MkII.
The operator gives one-word commands. You do everything except: load acrylic blanks, click RIP-and-Print, press ENTER on the printer.
Run every command from this repo's root on the printer PC. Machine detail and every repair route: `docs/OPERATIONS.md`.

## Commands

| Operator says | You do |
|---|---|
| `print` | steps P1–P6 (read-only: pull, plan, report) |
| `go` | steps G1–G6 for every planned bed |
| `go B002 B003` | steps G1–G6 for those beds only |
| `skip DM38431` | re-run P4–P6 adding `--skip DM38431` (repeatable, stack them) |
| `redo DM38431` | re-run P4–P6 adding `--redo DM38431` (reprints even if logged) |
| `jig large` / `medium` / `small` | steps J1–J3 |
| `status` | show plan/batch-plan.md summary, tail of state/printed.log, list of production/print/<today>/ |

## Hard rules — never bend these

- R1. Never invent, complete, or correct personalisation. Customer text prints exactly as typed, typos and all. Blank Line 2 is legitimate.
- R2. Never print a sign whose review flag a human has not resolved. `select-beds.py` enforces this; do not work around it.
- R3. Never guess an unclassified SKU. It goes in NEEDS ATTENTION; Max classifies it in `production/product-rules.json` or makes it by hand.
- R4. A sign's size comes from its own `Size` attribute only. Upgrade lines are a cross-check; a mismatch is a flag, not a fix.
- R5. Never copy a jig PDF to the hot folder during `go`. Jigs move only via the `jig` command, only after the operator confirms paper is taped down.
- R6. If Shopify is unreachable: stop and say so. Never plan from memory, an old file, or a guess.
- R7. If any script fails: stop, report which stage and its output. Never improvise the stage by hand.
- R8. The pipeline is not unattended. Every job needs the operator's ENTER press on the printer panel (broken head heater — see docs/OPERATIONS.md).

## print — pull and plan (changes nothing)

- P1. `git pull --ff-only`. If it fails, stop and say so.
- P2. Pull orders from Shopify with the exact GraphQL in `queries/orders.graphql`. No Shopify access → R6.
- P3. Save each page's raw reply verbatim as `plan/orders-p1.json`, `plan/orders-p2.json`, … Repeat with the `after` cursor until `hasNextPage` is false. Do not reshape the JSON.
- P4. Run: `python scripts/plan-batch.py plan/orders-p1.json plan/orders-p2.json --printed-log state/printed.log --out-dir plan` (list every page file; append any `--skip`/`--redo` the operator has given this session).
- P5. Reply with, and nothing else:
  - one line: total signs, beds by size, which are full / part;
  - the NEEDS ATTENTION list, one line each, if any;
  - every bed table from `plan/batch-plan.md`, verbatim;
  - the `Invoices to print` line (the operator prints these packing slips from Shopify admin);
  - one line: `Say go, go <bed ids>, skip <order>, or redo <order>.`
- P6. Stop. Generate nothing, send nothing, wait for the operator.

## go — produce beds and hand them to RasterLink

- G1. Only after a `print` report in this session. The word `go` is the approval for exactly what that report showed.
- G2. Run: `python scripts/select-beds.py plan/batch-plan.json --out plan/go.json` (append the bed IDs if the operator named some). If it REFUSES, relay its output and stop — resolve via `skip`, a rules edit, or Max's explicit `--allow-flagged`.
- G3. Run: `powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 -OrdersJson plan\go.json -OutDir production\print\<today> -SendToPrinter` where `<today>` is the Europe/London date, e.g. 2026-08-07. On any failure → R7.
- G4. Run: `python scripts/log-printed.py plan/go.json --log state/printed.log` then `git add state/printed.log && git commit -m "print log <today>" && git push`.
- G5. Reply with the LOADING MAP that select-beds.py printed (bed by bed, POS by POS), then exactly these operator steps:
  1. Load blanks into the paper jig per the map — sizes never mix on a bed. Not the current jig? Say `jig <size>` first.
  2. RasterLink7: select the job (verify its name matches the bed PDF), Alt+X, RIP and Print, Start, page at 0,0.
  3. Condition must be 600x900 VD / 12 pass — not the fresh-profile default.
  4. Press ENTER on the printer panel to release the job.
  5. Repeat per bed. Beds of the same size share one jig.
- G6. If beds were held back (part beds, skips), end with one line saying which orders wait and why.

## jig — a fresh paper jig, one size

- J1. Confirm with the operator that paper is taped to the bed and no acrylic is on it. No confirmation, no copy.
- J2. Copy `production\print\<today>\bedNN-<size>-jig.pdf` (the first bed of that size) to `C:\MijCtrl\Hot\UJF6042MkII`. No jig PDF for today → run `go` first, or see docs/OPERATIONS.md to make one standalone.
- J3. Tell the operator: RIP and Print it like a normal job, ENTER on the panel, then load blanks into the printed outlines.

## Conditions Max edits (the policy, in files — change these, never a script)

- `production/product-rules.json` — which SKUs print, heart/border/text per SKU, the eight colourways, size-upgrade and helper SKUs, what counts as sign-like.
- `production/bed-layout.json` — how many of each size fit a bed and where.
- `queries/orders.graphql` — what counts as an open order (the created_at bound moves forward here).
- `state/printed.log` — what is already printed. Delete a row (or `redo`) to reprint; add a row to hold a sign back.

## Weekly hygiene (only when the operator asks for `tidy`)

- T1. If every sign of an order in state/printed.log is fulfilled in Shopify, its rows may be archived to state/printed-archive.log. Never edit the log any other way unprompted.
