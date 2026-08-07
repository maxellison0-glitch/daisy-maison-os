#!/usr/bin/env python3
"""Append one row per printed sign unit to state/printed.log.

Run this immediately after run-batch.ps1 -SendToPrinter succeeds, with the SAME
go manifest. The log is why a printed-but-not-yet-fulfilled order does not come
back onto tomorrow's bed: plan-batch.py --printed-log subtracts these rows from
Shopify's unfulfilled quantities.

Row format (tab-separated):
    date  order  lineItemId  sku  size  line1

Counting semantics: plan-batch counts rows per lineItemId, so an accidental
double append cannot un-print anything - it only holds the sign back harder,
and --redo overrides it. Manual entries log lineItemId 'manual' and are never
subtracted (they have no stable id to match).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

try:
    from zoneinfo import ZoneInfo
    LONDON = ZoneInfo("Europe/London")
except Exception:  # zoneinfo data missing - date only, so UTC is close enough
    LONDON = None

HEADER = "# signauto print log - one row per printed sign unit\n# date\torder\tlineItemId\tsku\tsize\tline1\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("go_json", type=Path, help="the go manifest that was produced and sent")
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--date", default=None, help="override run date (YYYY-MM-DD)")
    args = parser.parse_args()

    date = args.date or datetime.now(LONDON).strftime("%Y-%m-%d")
    manifest = json.loads(args.go_json.read_text(encoding="utf-8"))

    rows = []
    for batch in manifest.get("batches", []):
        for p in batch.get("positions", []):
            order = str(p.get("order", "")).lstrip("#").upper()
            rows.append("\t".join([
                date,
                order,
                p.get("lineItemId") or "manual",
                str(p.get("sku", "")),
                str(p.get("size", "")),
                str(p.get("line1", "")),
            ]))
    if not rows:
        print("No positions in the go manifest - nothing logged.")
        return 2

    existing = args.log.read_text(encoding="utf-8") if args.log.exists() else ""
    dupes = sum(1 for r in rows if r in existing.splitlines())
    args.log.parent.mkdir(parents=True, exist_ok=True)
    with args.log.open("a", encoding="utf-8") as fh:
        if not existing:
            fh.write(HEADER)
        for r in rows:
            fh.write(r + "\n")
    print(f"logged {len(rows)} printed unit(s) to {args.log}"
          + (f" ({dupes} looked like duplicates of existing rows - harmless, but check"
             " you did not log the same run twice)" if dupes else ""))
    print("Now commit and push state/printed.log so every machine agrees on what is printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
