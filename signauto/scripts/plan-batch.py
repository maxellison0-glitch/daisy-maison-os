#!/usr/bin/env python3
"""Create a reviewable street-sign production manifest from Shopify order JSON.

Deliberately read-only: never calls Shopify, never writes artwork. Feed it the
raw connector replies (one file per page) and it produces plan/batch-plan.json
for run-batch.ps1 plus plan/batch-plan.md for the human.

What it will not do, on purpose:
- print a sign whose SKU nobody classified (NEEDS ATTENTION instead)
- silently drop a line that looks like a sign (NEEDS ATTENTION instead)
- take a size from a Size Upgrade line (the sign line's Size attribute is
  authoritative; upgrades are a cross-check and a mismatch is a flag)
- re-plan a sign already in state/printed.log (printed but not yet fulfilled
  in Shopify stays out of tomorrow's bed unless --redo says otherwise)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# The review sheet echoes customer text to the console. On Windows the console
# is often cp1252, and one emoji in a Line 2 must not crash the plan - the files
# are the deliverable, the echo is a courtesy.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")


def read_json_any_encoding(path: Path):
    """PowerShell 5.1's '>' redirection writes UTF-16; other routes add a BOM.

    A saved connector reply must load whichever way it was written, or the
    morning stops on an invisible byte.
    """
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return json.loads(raw.decode("utf-16"))
    return json.loads(raw.decode("utf-8-sig"))

SUPPORTED_HANDLE = "mr-mrs-personalised-street-sign-gift"
SUPPORTED_SIZES = {"large", "medium", "small"}

PROD = Path(__file__).resolve().parent.parent / "production"

# Which SKUs are street signs, and how many of each size fit on one bed, both come
# from the same JSON the production scripts read. Hardcoding either here is how a
# planner starts disagreeing with the machine.
with (PROD / "product-rules.json").open(encoding="utf-8") as fh:
    PRODUCT_RULES = json.load(fh)
KNOWN_SKUS = set(PRODUCT_RULES["products"])
DEFAULT_COLOURWAY = PRODUCT_RULES.get("defaultColourway", "black")
HELPER_SKUS = set(PRODUCT_RULES.get("helperSkus", {}).get("skus", []))
BUNDLE_SKUS = set(PRODUCT_RULES.get("bundleSkus", {}).get("skus", []))
SIZE_UPGRADES = {k: v for k, v in PRODUCT_RULES.get("sizeUpgrades", {}).items()
                 if not k.startswith("_")}
SIGN_LIKE = PRODUCT_RULES.get("signLike", {})
SIGN_LIKE_PREFIXES = tuple(SIGN_LIKE.get("skuPrefixes", ["ST-"]))
SIGN_LIKE_PATTERN = re.compile(SIGN_LIKE.get("titlePattern", r"street\s*-?\s*sign"), re.I)

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
    """The customer's chosen border colour, or "" if the order carries none.

    Mr & Mrs orders carry no colour attribute at all - that product is always
    black - so this used to return the literal "Unspecified", which recolour-sign
    correctly refuses as an unknown colourway. The caller substitutes the default.
    """
    value = attr_value(attrs, "colour border", "colour", "color", "sign colour", "sign color")
    return value or text(get(item, "colour", "color"))


def line_value(attrs: dict[str, str], line: int) -> str:
    if line == 1:
        return attr_value(attrs, "line 1", "line1", "personalisation", "personalization", "name")
    return attr_value(attrs, "line 2", "line2", "subtitle", "date", "text 2")


def nodes(value):
    """Accept a plain list, or GraphQL's {"nodes": [...]} / {"edges": [{"node": ...}]}.

    The Shopify connector returns connection objects, not arrays. Iterating one of
    those yields its dict KEYS, so every line item quietly became the string
    "nodes" and a pull containing four real orders produced a plan with zero signs
    on it and no error at all.
    """
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        if isinstance(value.get("nodes"), list):
            return value["nodes"]
        if isinstance(value.get("edges"), list):
            return [e.get("node", {}) for e in value["edges"] if isinstance(e, dict)]
    return []


def order_items(order: dict):
    return nodes(get(order, "lineItems", "line_items", default=[]))


def order_number(order: dict) -> str:
    return text(get(order, "name", "orderNumber", "order_number", "id"))


def norm_order(name: str) -> str:
    """'#DM38431', 'DM38431' and 'dm38431' are the same order."""
    return text(name).lstrip("#").upper()


def is_sign_like(item: dict) -> bool:
    sku = text(get(item, "sku"))
    if sku in HELPER_SKUS:
        return False
    if sku.startswith(SIGN_LIKE_PREFIXES):
        return True
    title = text(get(item, "title", "name"))
    handle = text(get(get(item, "product", default={}) or {}, "handle"))
    return bool(SIGN_LIKE_PATTERN.search(title) or SIGN_LIKE_PATTERN.search(handle))


def load_orders(paths: list[Path]) -> list[dict]:
    """Merge one or more saved replies (pages), deduplicating whole orders by name.

    The same order can appear on two pages if new orders arrive between page
    requests and shift the pagination window. Orders are deduplicated by order
    name; the first occurrence wins.
    """
    merged, seen = [], set()
    for path in paths:
        payload = read_json_any_encoding(path)
        if isinstance(payload, dict) and "data" in payload:
            payload = payload["data"]
        orders = nodes(payload.get("orders", payload)) if isinstance(payload, dict) else nodes(payload)
        for order in orders:
            key = norm_order(order_number(order)) if isinstance(order, dict) else ""
            # A manual plain-array entry is a pseudo-order; it has no line items to
            # merge, so duplicates of it are kept as typed.
            if key and isinstance(order, dict) and order_items(order):
                if key in seen:
                    continue
                seen.add(key)
            merged.append(order)
    return merged


def load_printed(path: Path | None) -> Counter:
    """state/printed.log -> printed unit count per line-item id.

    One row per physically printed sign unit, tab-separated:
        date  order  lineItemId  sku  size  line1
    Rows whose lineItemId is 'manual' never subtract (manual entries have no
    stable id). Blank lines and lines starting with # are ignored.
    """
    counts: Counter = Counter()
    if not path or not path.exists():
        return counts
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        item_id = parts[2].strip()
        if item_id and item_id != "manual":
            counts[item_id] += 1
    return counts


def eligible_records(orders: list, printed: Counter, skip: set[str], redo: set[str]):
    eligible, excluded, attention = [], [], []
    for order in orders:
        if not isinstance(order, dict):
            continue
        items = order_items(order)
        oname = order_number(order)
        onorm = norm_order(oname)
        customer = text(get(order.get("customer", {}) or {}, "displayName", "name", "email"))

        # A plain-array manual entry is its own sign, not an order wrapper.
        if not items and get(order, "sku"):
            items = [order]
            oname = text(get(order, "order", default="")) or oname or "MANUAL"
            onorm = norm_order(oname)

        # --- first pass over the order: what is on it? ---
        upgrades: Counter = Counter()   # size -> unfulfilled upgrade units
        order_attention = []
        for item in items:
            sku = text(get(item, "sku"))
            unful = int(get(item, "unfulfilledQuantity", "unfulfilled_quantity",
                            default=get(item, "quantity", default=1)) or 0)
            if sku in SIZE_UPGRADES and unful > 0:
                upgrades[SIZE_UPGRADES[sku]] += unful
            if sku in BUNDLE_SKUS and unful > 0:
                order_attention.append(
                    f"{oname}: bundle line {sku} ({text(get(item, 'title'))}) means several"
                    " signs in one line item - plan this order by hand")

        expected_upgrades: Counter = Counter()
        order_signs = []
        order_held = 0  # sign lines held back (skip / already printed) this order

        for item in items:
            attrs = attributes(item)
            sku = text(get(item, "sku"))
            if sku in HELPER_SKUS or sku in BUNDLE_SKUS:
                continue
            quantity = int(get(item, "unfulfilledQuantity", "unfulfilled_quantity",
                               default=get(item, "quantity", default=0)) or 0)
            product = get(item, "product", default={}) or {}
            handle = text(get(product, "handle"))
            known = sku in KNOWN_SKUS
            if not known and not (handle == SUPPORTED_HANDLE or is_sign_like(item)):
                continue  # not a sign, not sign-like: genuinely out of scope

            colour = colour_for(item, attrs)
            record = {
                "order": oname,
                "customer": customer,
                "lineItemId": text(get(item, "id")),
                "sku": sku,
                "size": size_for(item, attrs),
                "colour": colour or DEFAULT_COLOURWAY.title(),
                "line1": line_value(attrs, 1) or text(get(item, "line1")),
                "line2": line_value(attrs, 2) or text(get(item, "line2")),
                "quantity": quantity,
                "title": text(get(item, "title", "name")),
            }

            if not known:
                # Sign-like but unclassified. Visible, never guessed, never planned.
                if quantity > 0:
                    attention.append(
                        f"{oname}: {sku or 'no SKU'} \"{record['title'][:60]}\" is sign-like but not"
                        f" classified in product-rules.json (Line 1: {record['line1'] or '-'};"
                        f" Size: {record['size']}) - classify it or make it by hand")
                continue

            if quantity <= 0:
                record["reason"] = "sign line has no unfulfilled quantity"
                excluded.append(record)
                continue

            if onorm in skip:
                record["reason"] = "skipped by operator (--skip)"
                excluded.append(record)
                order_held += 1
                continue

            # Already-printed subtraction from state/printed.log.
            done = 0 if onorm in redo else printed.get(record["lineItemId"], 0)
            if record["lineItemId"] and done >= quantity:
                record["reason"] = f"already printed ({done} unit(s) in state/printed.log)"
                excluded.append(record)
                order_held += 1
                continue
            partial_note = ""
            if record["lineItemId"] and 0 < done < quantity:
                record["quantity"] = quantity - done
                partial_note = f"{done} of {quantity} already printed; planning the remaining {quantity - done}"

            if record["size"] in ("Medium", "Large"):
                expected_upgrades[record["size"]] += record["quantity"]

            notes = []
            if partial_note:
                notes.append(partial_note)
            if not record["line1"]:
                notes.append("Missing Line 1 personalisation")
            if record["size"] == "Unknown":
                notes.append("Size not recognised - needs Small, Medium or Large")
            # Only worth flagging where the customer actually picks a colour.
            # Mr & Mrs is always black, so a missing colour there is normal.
            if not colour and PRODUCT_RULES["products"].get(sku, {}).get("border") == "customer":
                notes.append(f"No colour on the order line; defaulted to {DEFAULT_COLOURWAY}")
            record["review"] = "; ".join(notes)
            order_signs.append(record)
            eligible.append(record)

        # --- upgrade cross-check: the Size attribute said one thing, did the
        # money agree? Soft by design: a mismatch flags, it never resizes. ---
        if order_signs and not order_attention:
            for size in ("Medium", "Large"):
                if expected_upgrades[size] > upgrades[size]:
                    note = (f"size says {size} but the order carries {upgrades[size]}"
                            f" '{size} upgrade' line(s) for {expected_upgrades[size]} sign(s) - check the invoice")
                    for record in order_signs:
                        if record["size"] == size:
                            record["review"] = "; ".join(x for x in (record["review"], note) if x)
                elif upgrades[size] > expected_upgrades[size] and not order_held:
                    # order_held guard: a sign already printed or skipped still has
                    # its paid upgrade line on the order - that is not a mismatch.
                    note = (f"order carries a '{size} upgrade' line not matched by any sign's"
                            f" Size attribute - check the invoice")
                    for record in order_signs:
                        record["review"] = "; ".join(x for x in (record["review"], note) if x)
        attention.extend(order_attention)

    return eligible, excluded, attention


def manifest(eligible, excluded, attention) -> dict:
    # One bed is one SIZE. Colour does not split a bed: border colour is artwork,
    # not a machine setting, so the Mimaki prints a grass sign and a blush sign in
    # the same run with no re-setup. Only the physical blank changes the layout.
    groups = defaultdict(list)
    for record in eligible:
        key = record["size"]
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
            batch_records = records[index: index + per_bed]
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
        "eligibleCount": sum(int(item["quantity"]) for item in eligible),
        "eligibleLineItems": len(eligible),
        "excludedSignLineItems": len(excluded),
        "needsAttention": attention,
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
    if data["needsAttention"]:
        lines += ["## NEEDS ATTENTION - not planned, a human decides", ""]
        lines += [f"- {item}" for item in data["needsAttention"]]
        lines += [""]
    already = [e for e in data["excluded"] if str(e.get("reason", "")).startswith("already printed")]
    if already:
        lines += [f"{len(already)} sign line(s) held back as already printed per state/printed.log.", ""]
    if not data["batches"]:
        lines += ["## No production batches", "", "No sign line currently has `unfulfilledQuantity > 0`.", ""]
    for batch in data["batches"]:
        if batch["template"] == "Unknown":
            fill = "NOT PRINTABLE - size unresolved, a human decides"
        else:
            fill = "FULL BED" if batch["full"] else f"PART BED - {batch['slotsUsed']} of {batch['perBed']} slots"
        # Colour is a per-position column: one bed carries whatever colourways the
        # orders in it happen to use.
        lines += [f"## {batch['batch']} - {batch['template']} ({fill})", "",
                  "| Position | Order | SKU | Colour | Line 1 | Line 2 | Review |",
                  "|---:|---|---|---|---|---|---|"]
        for item in batch["positions"]:
            lines.append(
                f"| {item['position']} | {item['order']} | {item['sku']} | {item['colour']} "
                f"| {item['line1']} | {item['line2']} | {item['review'] or 'OK'} |"
            )
        lines += ["", "Status: **REVIEW REQUIRED**", ""]
    invoices = []
    for batch in data["batches"]:
        for item in batch["positions"]:
            if item["order"] not in invoices:
                invoices.append(item["order"])
    if invoices:
        lines += ["## Invoices to print", "", " ".join(invoices), ""]
    part = [b for b in data["batches"] if not b["full"]]
    if part:
        lines += [f"## {len(part)} part bed(s)", "",
                  "Printing a part bed wastes acrylic; holding it delays those orders. Max's call.", ""]
    lines += ["## Safety", "", "This plan does not generate artwork, change Shopify, or send anything to a printer.",
              "", "To gate and produce an approved plan:", "",
              "```powershell",
              "python scripts\\select-beds.py <out-dir>\\batch-plan.json --out <out-dir>\\go.json",
              "powershell -NoProfile -ExecutionPolicy Bypass -File production\\run-batch.ps1 `",
              "    -OrdersJson <out-dir>\\go.json -OutDir production\\print\\<date> -SendToPrinter",
              "```", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orders_json", type=Path, nargs="+",
                        help="one or more saved Shopify replies (pages) or a plain array")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--printed-log", type=Path, default=None,
                        help="state/printed.log; signs already logged there are held back")
    parser.add_argument("--skip", action="append", default=[], metavar="ORDER",
                        help="exclude this order from the plan (repeatable)")
    parser.add_argument("--redo", action="append", default=[], metavar="ORDER",
                        help="plan this order even if state/printed.log says it was printed")
    args = parser.parse_args()
    orders = load_orders(args.orders_json)
    printed = load_printed(args.printed_log)
    skip = {norm_order(o) for o in args.skip}
    redo = {norm_order(o) for o in args.redo}
    eligible, excluded, attention = eligible_records(orders, printed, skip, redo)
    data = manifest(eligible, excluded, attention)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "batch-plan.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (args.out_dir / "batch-plan.md").write_text(markdown(data), encoding="utf-8")
    print(markdown(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
