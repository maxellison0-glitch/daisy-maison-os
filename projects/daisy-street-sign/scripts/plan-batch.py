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

SUPPORTED_SKU = "36961"
SUPPORTED_HANDLE = "mr-mrs-personalised-street-sign-gift"
SUPPORTED_SIZES = {"large", "medium", "small"}


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
            is_sign = sku == SUPPORTED_SKU or handle == SUPPORTED_HANDLE
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
                if record["size"] == "Large" and not record["line1"]:
                    record["review"] = "Missing Line 1 personalisation"
                else:
                    record["review"] = ""
                eligible.append(record)
            else:
                record["reason"] = "sign line has no unfulfilled quantity"
                excluded.append(record)
    return eligible, excluded


def manifest(eligible: list[dict], excluded: list[dict]) -> dict:
    groups = defaultdict(list)
    for record in eligible:
        key = f"{record['size']} / {record['colour']}"
        groups[key].append(record)
    batches = []
    for key in sorted(groups):
        records = groups[key]
        for index in range(0, len(records), 3):
            batch_records = records[index : index + 3]
            batches.append({
                "batch": f"B{len(batches) + 1:03d}",
                "template": key,
                "positions": [dict(record, position=position) for position, record in enumerate(batch_records, 1)],
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
        lines += [f"## {batch['batch']} - {batch['template']}", "", "| Position | Order | Line 1 | Line 2 | Review |", "|---:|---|---|---|---|"]
        for item in batch["positions"]:
            lines.append(f"| {item['position']} | {item['order']} | {item['line1']} | {item['line2']} | {item['review'] or 'OK'} |")
        lines += ["", "Status: **REVIEW REQUIRED**", ""]
    lines += ["## Safety", "", "This plan does not generate artwork, change Shopify, or send anything to a printer.", ""]
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
