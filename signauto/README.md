# signauto

Daisy Maison street signs: unfulfilled Shopify orders → print-ready beds on the
Mimaki UJF-6042MkII, run by an AI agent taking one-word commands from whoever is
standing at the printer.

**This repo is the only copy of the street-sign system.** It moved here from
`daisy-maison-os/projects/daisy-street-sign` on 2026-08-06, on Max's instruction,
so any capable AI model can be pointed at one small repo and start work.

## The morning, in full

1. Open an AI session on the printer PC in this repo (it needs Shopify access
   and a terminal). Say **`print`**.
2. The agent pulls every open sign order itself, plans the beds, and tells you:
   how many signs today, each bed's contents position by position, which
   invoices to print for packing, and anything that needs a human decision.
   Nothing is generated yet. **You decide, it types** — there is no manual
   order-picking in Shopify and no typing of order numbers.
3. Say **`go`** (or `go B001 B002` to hold part beds back, `skip DM…` to drop
   an order). The agent builds all artwork, sends the bed PDFs to RasterLink's
   hot folder, records every sign in `state/printed.log`, and prints you the
   loading map.
4. You: load blanks into the paper jig per the map → RasterLink: RIP and Print
   at 0,0, **600x900 VD / 12 pass** → press **ENTER** on the printer panel.
   Repeat per bed. Fresh jig needed? Say **`jig medium`**.

The full command set and every rule the agent follows: **`AGENT.md`** (one page —
that file IS the automation; edit it to change the workflow).

## What keeps this safe

- Anything odd — unclassified SKU, missing personalisation, size/upgrade
  mismatch, unknown colour — is **flagged and refused, never guessed**. The
  refusal lists live in the plan; `scripts/select-beds.py` is the gate.
- `state/printed.log` remembers what has physically been printed, so orders
  awaiting dispatch don't reprint tomorrow. It is committed after every run.
- The printer never starts on its own: the head-heater fault means every job
  waits for a human ENTER press. See `docs/OPERATIONS.md`.

## Fresh PC setup

```powershell
git clone https://github.com/maxellison0-glitch/signauto
cd signauto
python -m pip install -r requirements.txt
python artwork\verify-heart-placement.py
powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 -OrdersJson scripts\fixtures\run-batch-orders.json -OutDir .\_check
python scripts\test-plan-batch.py
```

Needs: Windows PowerShell 5.1, Python 3.13 (numpy, pillow, shapely, fonttools),
Chrome or Edge, RasterLink7 with hot folder `C:\MijCtrl\Hot\UJF6042MkII` (only
for the final send), and a Shopify connection to `daisymaisonuk.myshopify.com`.
No USB drive: every blank contour is committed.

## Day one (first real run)

- The printed log starts empty, so the first `print` lists **every** open sign
  order, including any already made by hand and sitting on the shelf. Check the
  list against the shelf once: `skip` what exists physically, then `go`. From
  then on the log carries the memory.
- Medium and Small are software-verified but have never come off the machine:
  print the jig and dry-fit a real blank before their first customer bed.

## Map

| Where | What |
|---|---|
| `AGENT.md` | the agent runbook — commands, rules, the whole workflow |
| `docs/OPERATIONS.md` | machine manual: printer, RasterLink, per-stage repair routes |
| `production/` | run-batch runner, stage scripts, `product-rules.json`, `bed-layout.json` |
| `scripts/` | `plan-batch.py`, `select-beds.py`, `log-printed.py`, tests + fixtures |
| `queries/orders.graphql` | the one Shopify query (the date bound lives here) |
| `state/printed.log` | what has been printed (committed; the anti-reprint memory) |
| `artwork/`, `source/` | generator, locked design assets, blank contours |

## Not yet built

- **Etsy.** Etsy sign orders still run by hand. The clean route is an Etsy
  connector feeding the same planner (its manual-array input already accepts
  typed entries as a stopgap: see `docs/OPERATIONS.md`).
- The RasterLink RIP-and-Print click (no CLI; a GUI-automation pattern exists —
  see `docs/OPERATIONS.md`).
- The ENTER press will stay manual until the head heater is repaired.
