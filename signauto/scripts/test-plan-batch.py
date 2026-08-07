#!/usr/bin/env python3
"""Planner and state-loop tests. No printer, no Shopify, no PowerShell needed.

Run from the repo root:  python scripts/test-plan-batch.py
Every behaviour the morning run depends on is asserted here; run this after any
edit to plan-batch.py, select-beds.py, log-printed.py or product-rules.json.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIXTURE = SCRIPTS / "fixtures" / "signauto-cases.json"
PY = sys.executable

passed = 0


def check(cond, label):
    global passed
    if not cond:
        print(f"FAIL: {label}")
        sys.exit(1)
    passed += 1
    print(f"  ok: {label}")


def run(*argv, expect=0):
    proc = subprocess.run([PY, *map(str, argv)], capture_output=True, text=True)
    if proc.returncode != expect:
        print(f"FAIL: {' '.join(map(str, argv))} exited {proc.returncode}, expected {expect}")
        print(proc.stdout)
        print(proc.stderr)
        sys.exit(1)
    return proc.stdout


def plan(tmp, *extra):
    out = tmp / "plan"
    run(SCRIPTS / "plan-batch.py", FIXTURE, "--out-dir", out,
        "--printed-log", tmp / "printed.log", *extra)
    return json.loads((out / "batch-plan.json").read_text(encoding="utf-8"))


def positions(data):
    return [p for b in data["batches"] for p in b["positions"]]


def by_order(data, name):
    return [p for p in positions(data) if p["order"] == name]


with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)

    print("plan-batch: fresh plan")
    data = plan(tmp)
    pos = positions(data)
    # DM90001 L1, DM90002 S2, DM90004 flagged-in, DM90006 S1, DM90007 S2, DM90008 S1
    check(data["eligibleCount"] == 8, f"8 eligible units (got {data['eligibleCount']})")
    check(len(by_order(data, "#DM90001")) == 1, "re-SKU'd Mr & Mrs plans")
    fam = by_order(data, "#DM90002")
    check(len(fam) == 2, "family quantity 2 takes two slots")
    check(fam[0]["colour"] == "sage" and fam[0]["review"] == "", "family colour read, unflagged")
    check(fam[0]["line2"] == "", "blank family Line 2 stays blank")
    broken = by_order(data, "#DM90004")
    check(len(broken) == 1 and "Missing Line 1" in broken[0]["review"], "attribute-less sign flagged, not dropped")
    check("upgrade" in broken[0]["review"], "orphan upgrade cross-check flags")
    att = "\n".join(data["needsAttention"])
    check("36955" in att, "unclassified grandparent sign in NEEDS ATTENTION")
    check("DM90005" in att and "bundle" in att, "bundle order in NEEDS ATTENTION")
    check("XT-627-SUM" not in att and "XT-626-SUL" not in att, "helper upgrades never flagged as signs")
    check(not any(p["order"] == "#DM90005" for p in pos), "bundle order not planned")
    check(not any("NOT A SIGN" in p["line1"] for p in pos), "pebble line ignored")
    check(by_order(data, "#DM90001")[0]["review"] == "", "matched Large upgrade: no flag")
    sizes = {b["template"] for b in data["batches"]}
    check(sizes == {"Large", "Small", "Unknown"}, f"bed sizes {sizes}")

    print("plan-batch: --skip")
    data = plan(tmp, "--skip", "dm90008")
    check(not by_order(data, "#DM90008"), "skip removes the order (case/hash-insensitive)")
    check(any(e["order"] == "#DM90008" and "skipped" in e["reason"] for e in data["excluded"]),
          "skip is recorded, not lost")

    print("plan-batch: multi-file dedup")
    out2 = tmp / "plan2"
    run(SCRIPTS / "plan-batch.py", FIXTURE, FIXTURE, "--out-dir", out2,
        "--printed-log", tmp / "printed.log")
    dup = json.loads((out2 / "batch-plan.json").read_text(encoding="utf-8"))
    check(dup["eligibleCount"] == 8, "same order on two pages counts once")

    print("printed.log loop: partial + full subtraction, then redo")
    (tmp / "printed.log").write_text(
        "# header\n"
        "2026-08-06\tDM90006\tgid://li/90006-1\tST-001-MR\tSmall\tMR & MRS PRINTED\n"
        "2026-08-06\tDM90007\tgid://li/90007-1\tST-001-MR\tSmall\tMR & MRS TWICE\n",
        encoding="utf-8")
    data = plan(tmp)
    check(not by_order(data, "#DM90006"), "fully printed line held back")
    check(any(e["order"] == "#DM90006" and "already printed" in e["reason"] for e in data["excluded"]),
          "held-back line visible in excluded")
    twice = by_order(data, "#DM90007")
    check(len(twice) == 1 and twice[0]["orderedQuantity"] == 1, "1 of 2 printed -> 1 slot remains")
    check("already printed" in twice[0]["review"], "partial print noted for the human")
    data = plan(tmp, "--redo", "DM90006")
    check(len(by_order(data, "#DM90006")) == 1, "--redo overrides the log")

    print("select-beds: flag gate")
    (tmp / "printed.log").write_text("", encoding="utf-8")
    data = plan(tmp)
    out = run(SCRIPTS / "select-beds.py", tmp / "plan" / "batch-plan.json",
              "--out", tmp / "go-all.json", expect=2)
    check("REFUSED" in out and "DM90004" in out, "flagged position blocks the whole go")

    print("select-beds: clean subset + loading map + bed mapping")
    data = plan(tmp, "--skip", "DM90004")
    out = run(SCRIPTS / "select-beds.py", tmp / "plan" / "batch-plan.json",
              "--out", tmp / "go.json")
    check((tmp / "go.json").exists(), "go manifest written")
    check("bed01-large" in out and "bed02-small" in out, "bed numbering matches run-batch order")
    check("MR & MRS TEST" in out and "POS 1" in out, "loading map lists positions")
    go = json.loads((tmp / "go.json").read_text(encoding="utf-8"))
    check(all(not p["review"] for b in go["batches"] for p in b["positions"]),
          "go manifest carries no flags")
    b1 = run(SCRIPTS / "select-beds.py", tmp / "plan" / "batch-plan.json",
             "B001", "--out", tmp / "go-b001.json")
    gob1 = json.loads((tmp / "go-b001.json").read_text(encoding="utf-8"))
    check(len(gob1["batches"]) == 1 and gob1["batches"][0]["batch"] == "B001", "subset selects exactly B001")

    print("log-printed: the anti-reprint memory")
    run(SCRIPTS / "log-printed.py", tmp / "go.json", "--log", tmp / "printed.log",
        "--date", "2026-08-07")
    logged = (tmp / "printed.log").read_text(encoding="utf-8")
    check(logged.count("2026-08-07") == 7, f"7 units logged")
    check("DM90001" in logged and "gid://li/90001-1" in logged, "rows carry order + lineItemId")
    data = plan(tmp, "--skip", "DM90004")
    check(data["eligibleCount"] == 0, "everything printed -> next plan is empty")
    check(sum(1 for e in data["excluded"] if "already printed" in str(e.get("reason", ""))) >= 4,
          "printed lines all held back")

print(f"\nAll {passed} checks passed.")
