#!/usr/bin/env python3
"""Gate between a reviewed plan and run-batch.ps1.

Takes plan/batch-plan.json and the batch IDs the operator approved (none =
all), refuses anything a human has not resolved, and writes the go manifest.

This is the ONLY sanctioned way to feed run-batch.ps1 from a plan, because it
is where three guarantees live:

1. No flagged sign gets through. A position with a non-empty review note is a
   question, and questions are answered by people, not printed over.
2. Bed numbering is pinned. run-batch.ps1 groups by size and numbers beds
   bed01, bed02... - this script reproduces that grouping and refuses to
   proceed if the mapping would not be 1:1 with the plan's batches, so the
   loading map it prints is the loading map the PDFs will have.
3. What the operator approved is exactly what runs. The go manifest carries
   only the selected batches, verbatim.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# The loading map echoes customer text; a cp1252 Windows console must never
# crash the gate over an emoji.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan_json", type=Path)
    parser.add_argument("batches", nargs="*", metavar="BATCH",
                        help="batch IDs to produce, e.g. B001 B003; none = all")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--allow-flagged", action="store_true",
                        help="let flagged positions through anyway (a human has decided)")
    args = parser.parse_args()

    plan = json.loads(args.plan_json.read_text(encoding="utf-8"))
    all_batches = plan.get("batches", [])
    if not all_batches:
        print("Plan has no batches - nothing to select.")
        return 2

    by_id = {b["batch"]: b for b in all_batches}
    wanted = [w.upper() for w in args.batches] or list(by_id)
    unknown = [w for w in wanted if w not in by_id]
    if unknown:
        print(f"No such batch in the plan: {', '.join(unknown)}. Known: {', '.join(by_id)}")
        return 2
    selected = [by_id[w] for w in wanted]

    flagged = [(b["batch"], p) for b in selected for p in b["positions"] if p.get("review")]
    if flagged and not args.allow_flagged:
        print("REFUSED - these positions carry review flags a human has not resolved:")
        for batch_id, p in flagged:
            print(f"  {batch_id} pos {p['position']}: {p['order']} \"{p['line1']}\" -> {p['review']}")
        print("Resolve them (re-plan with --skip, fix product-rules.json, or a manual entry),")
        print("or pass --allow-flagged if a human has looked and says print anyway.")
        return 2

    # Reproduce run-batch.ps1's grouping (by size, alphabetical, order preserved
    # within a size) and check every chunk equals one selected batch. Within one
    # plan each size has at most one part bed and it is last, so this holds
    # whenever whole batches are selected - this check is the tripwire in case
    # that ever stops being true.
    ordered = sorted(selected, key=lambda b: (b["template"].lower(),
                                              all_batches.index(b)))
    per_size: dict[str, list] = {}
    for b in ordered:
        per_size.setdefault(b["template"].lower(), []).append(b)
    for size, group in per_size.items():
        for b in group[:-1]:
            if not b["full"]:
                print(f"REFUSED - {b['batch']} is a part bed but not the last {size} bed "
                      "selected; bed numbering would not match the plan. Select it alone "
                      "or re-plan.")
                return 2

    args.out.write_text(json.dumps({
        "source": str(args.plan_json),
        "generatedAt": plan.get("generatedAt"),
        "batches": ordered,
    }, indent=2), encoding="utf-8")

    print(f"go manifest: {args.out}  ({sum(b['slotsUsed'] for b in ordered)} sign(s), "
          f"{len(ordered)} bed(s))")
    print()
    print("LOADING MAP - beds print in this order; positions fill from POS 1:")
    for bed_no, b in enumerate(ordered, 1):
        size = b["template"].lower()
        fill = "FULL" if b["full"] else f"PART {b['slotsUsed']}/{b['perBed']}"
        print(f"\nbed{bed_no:02d}-{size}  (= plan {b['batch']}, {fill}) "
              f"-> PDF bed{bed_no:02d}-{size}.pdf, jig bed{bed_no:02d}-{size}-jig.pdf")
        for p in b["positions"]:
            print(f"  POS {p['position']}: {p['order']}  {p['colour']:<10} {p['line1']}"
                  + (f"  /  {p['line2']}" if p.get("line2") else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
