#!/usr/bin/env python3
"""Create a reviewable street-sign production manifest from Shopify order JSON.

This is deliberately read-only: it never calls Shopify and never writes artwork.
The Shopify connector/API can export orders to JSON, then this script groups only
line items with an actually positive unfulfilled quantity.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SUPPORTED_HANDLE = "mr-mrs-personalised-street-sign-gift"
SUPPORTED_SIZES = {"large", "medium", "small"}

PROD = Path(__file__).resolve().parent.parent / "production"

# Which SKUs are street signs, and how many of each size fit on one bed, both come
# from the same JSON the production scripts read. Hardcoding either here is how a
# planner starts disagreeing with the machine: this script used to chunk every size
# into batches of 3, which silently halved Small's real 8-up capacity.
with (PROD / "product-rules.json").open(encoding="utf-8") as fh:
    PRODUCT_RULES = json.load(fh)
KNOWN_SKUS = set(PRODUCT_RULES["products"])

with (PROD / "bed-layout.json").open(encoding="utf-8") as fh:
    BED_LAYOUT = json.load(fh)
PER_BED = {
    name: int(cfg["cols"]) * int(cfg["rows"])
    for name, cfg in BED_LAYOUT["sizes"].items()
}


def text(value) -> str:
    return "" if value is None else str(value).strip()


def get(obj: dict, *keys, default=""):
    for key in keys:
        if isinstance(obj, dict) and key in obj and obj[key] not in (None, ""):
            return obj[key]
    return default


def attributes(item: dict) -> dict[str, str]:
    raw = get(item, "customAttributes", "custom_attributes", "properties", default=[])
    if isinstance(raw, dict):
        return {text(k).lower(): text(v) for k, v in raw.items()}
    result = {}
    for entry in raw or []:
        if isinstance(entry, dict):
            key = get(entry, "key", "name", default="")
            value = get(entry, "value", default="")
            if key:
                result[text(key).lower()] = text(value)
    return result


def attr_value(attrs: dict[str, str], *names) -> str:
    for name in names:
        wanted = name.lower()
        for key, value in attrs.items():
            if key == wanted or wanted in key:
                return value
    return ""


def size_for(item: dict, attrs: dict[str, str]) -> str:
    value = attr_value(attrs, "size", "sign size") or text(get(item, "size"))
    value = value.lower()
    for size in SUPPORTED_SIZES:
        if size in value:
            return size.title()
    title = text(get(item, "title", "name"))
    for size in SUPPORTED_SIZES:
        if re.search(rf"\b{size}\b", title, re.I):
            return size.title()
    return "Unknown"


def colour_for(item: dict, attrs: dict[str, str]) -> str:
    value = attr_value(attrs, "colour", "color", "sign colour", "sign color")
    return value or text(get(item, "colour", "color")) or "Unspecified"


def line_value(attrs: dict[str, str], line: int) -> str:
    if line == 1:
        return attr_value(attrs, "line 1", "line1", "personalisation", "personalization", "name")
    return attr_value(attrs, "line 2", "line2", "subtitle", "date", "text 2")


def order_items(order: dict):
    return get(order, "lineItems", "line_items", default=[])


def order_number(order: dict) -> str:
    return text(get(order, "name", "orderNumber", "order_number", "id"))


def eligible_records(payload: dict) -> tuple[list[dict], list[dict]]:
    orders = payload.get("orders", payload if isinstance(payload, list) else [])
    eligible, excluded = [], []
    for order in orders:
        for item in order_items(order):
            attrs = attributes(item)
            quantity = int(get(item, "unfulfilledQuantity", "unfulfilled_quantity", default=0) or 0)
            sku = text(get(item, "sku"))
            product = get(item, "product", default={}) or {}
            handle = text(get(product, "handle"))
            is_sign = sku in KNOWN_SKUS or handle == SUPPORTED_HANDLE
            if not is_sign:
                continue
            record = {
                "order": order_number(order),
                "customer": text(get(order.get("customer", {}) or {}, "displayName", "name", "email")),
                "lineItemId": text(get(item, "id")),
                "sku": sku,
                "size": size_for(item, attrs),
                "colour": colour_for(item, attrs),
                "line1": line_value(attrs, 1),
                "line2": line_value(attrs, 2),
                "quantity": quantity,
                "title": text(get(item, "title", "name")),
            }
            if quantity > 0:
                # Applies at every size. Line 1 is the sign; without it there is
                # nothing to print, whatever the size or the SKU.
                notes = []
                if not record["line1"]:
                    notes.append("Missing Line 1 personalisation")
                if record["size"] == "Unknown":
                    notes.append("Size not recognised - needs Small, Medium or Large")
                if sku and sku not in KNOWN_SKUS:
                    notes.append(f"SKU {sku} is not classified in product-rules.json")
                record["review"] = "; ".join(notes)
                eligible.append(record)
            else:
                record["reason"] = "sign line has no unfulfilled quantity"
                excluded.append(record)
    return eligible, excluded


def manifest(eligible: list[dict], excluded: list[dict]) -> dict:
    # One bed is one size at one colour: a bed is a single print run at one ink
    # setup, so mixing either would mean re-jigging mid-run.
    groups = defaultdict(list)
    for record in eligible:
        key = f"{record['size']} / {record['colour']}"
        # A line item ordered x3 occupies three bed slots, not one.
        for _ in range(max(1, int(record.get("quantity") or 1))):
            groups[key].append(record)
    batches = []
    for key in sorted(groups):
        records = groups[key]
        # Capacity comes from bed-layout.json, the same file make-jig.ps1 and
        # make-imposition.ps1 read - 3 Large, 3 Medium, 8 Small.
        per_bed = PER_BED.get(records[0]["size"].lower(), 1)
        for index in range(0, len(records), per_bed):
            batch_records = records[index : index + per_bed]
            batches.append({
                "batch": f"B{len(batches) + 1:03d}",
                "template": key,
                "perBed": per_bed,
                "slotsUsed": len(batch_records),
                "full": len(batch_records) == per_bed,
                # One position is one physical sign in one bed slot, so its
                # quantity is 1 by definition - the line item's own quantity was
                # already spent expanding it into these slots above. Leaving the
                # original here made run-batch.ps1 expand it a SECOND time and an
                # order for 2 came out as 4 signs on the bed.
                "positions": [
                    dict(record, position=position, quantity=1,
                         orderedQuantity=int(record.get("quantity") or 1))
                    for position, record in enumerate(batch_records, 1)
                ],
                "status": "REVIEW REQUIRED",
            })
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "Shopify order JSON supplied to plan-batch.py",
        "eligibleCount": sum(item["quantity"] for item in eligible),
        "eligibleLineItems": len(eligible),
        "excludedSignLineItems": len(excluded),
        "batches": batches,
        "excluded": excluded,
        "nextAction": "Human review required before artwork generation or printer handoff.",
    }


def markdown(data: dict) -> str:
    lines = [
        "# Street-sign production batch plan",
        "",
        f"Generated: {data['generatedAt']}",
        f"Eligible line items: {data['eligibleLineItems']} ({data['eligibleCount']} units)",
        f"Excluded sign lines: {data['excludedSignLineItems']}",
        "",
    ]
    if not data["batches"]:
        lines += ["## No production batches", "", "No sign line currently has `unfulfilledQuantity > 0`.", ""]
    for batch in data["batches"]:
        fill = "FULL BED" if batch["full"] else f"PART BED - {batch['slotsUsed']} of {batch['perBed']} slots"
        lines += [f"## {batch['batch']} - {batch['template']} ({fill})", "",
                  "| Position | Order | SKU | Line 1 | Line 2 | Review |", "|---:|---|---|---|---|---|"]
        for item in batch["positions"]:
            lines.append(f"| {item['position']} | {item['order']} | {item['sku']} | {item['line1']} | {item['line2']} | {item['review'] or 'OK'} |")
        lines += ["", "Status: **REVIEW REQUIRED**", ""]
    part = [b for b in data["batches"] if not b["full"]]
    if part:
        lines += [f"## {len(part)} part bed(s)", "",
                  "Printing a part bed wastes acrylic; holding it delays those orders. Max's call.", ""]
    lines += ["## Safety", "", "This plan does not generate artwork, change Shopify, or send anything to a printer.",
              "", "To turn an approved plan into print-ready PDFs:", "",
              "```powershell",
              "powershell -NoProfile -ExecutionPolicy Bypass -File production\\run-batch.ps1 `",
              "    -OrdersJson <out-dir>\\batch-plan.json -OutDir production\\print\\<date>",
              "```", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orders_json", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.orders_json.read_text(encoding="utf-8"))
    eligible, excluded = eligible_records(payload)
    data = manifest(eligible, excluded)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "batch-plan.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (args.out_dir / "batch-plan.md").write_text(markdown(data), encoding="utf-8")
    print(markdown(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
