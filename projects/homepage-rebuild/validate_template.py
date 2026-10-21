"""Check a JSON template against the theme's section schemas and the store's data.

python3 validate_template.py index.json --theme-dir <dir with sections/*.liquid> \
    [--before index.before.json] [--files files_inventory.json] [--collections collections.json] \
    [--products all_products.json] [--extra-file name.jpg ...]

Checks: every setting id exists in the section/block schema; select/radio values are legal;
ranges are in bounds and on the step grid; checkboxes are booleans; block types exist;
max_blocks and the 25-section limit hold; block_order/order match their dicts;
image_picker values point at real Files; collection and product links point at live handles.
Sections identical to --before are skipped (they were valid when Shopify saved them).
"""
import argparse
import json
import re
import sys
from pathlib import Path


def load_template(path):
    return json.loads(re.sub(r"^\s*/\*.*?\*/", "", Path(path).read_text(encoding="utf-8"), flags=re.S))


def load_schema(theme_dir, section_type):
    text = (Path(theme_dir) / "sections" / f"{section_type}.liquid").read_text(encoding="utf-8")
    m = re.search(r"{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}", text, flags=re.S)
    return json.loads(m.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("--theme-dir", required=True)
    ap.add_argument("--before")
    ap.add_argument("--files")
    ap.add_argument("--collections")
    ap.add_argument("--products")
    ap.add_argument("--extra-file", action="append", default=[])
    a = ap.parse_args()

    tpl = load_template(a.template)
    before = load_template(a.before)["sections"] if a.before else {}
    files = set(a.extra_file)
    if a.files:
        files |= {f["filename"] for f in json.load(open(a.files))}
    live_cols = None
    if a.collections:
        data = json.load(open(a.collections))
        rows = data if isinstance(data, list) else data.get("collections", data.get("nodes", []))
        live_cols = {c["handle"] for c in rows if c.get("publishedOnlineStore", c.get("published", True))}
        live_cols.add("best-sellers")  # created 23 Sep 2026 for this rebuild
    live_products = None
    if a.products:
        data = json.load(open(a.products))
        rows = data if isinstance(data, list) else data.get("products", data.get("nodes", []))
        live_products = {p["handle"] for p in rows if p.get("status", "ACTIVE") == "ACTIVE" and p.get("onlineStoreUrl", True)}

    errors, checked = [], 0

    def check_value(where, sdef, value):
        t = sdef["type"]
        if t in ("select", "radio"):
            opts = [o["value"] for o in sdef["options"]]
            if value not in opts:
                errors.append(f"{where}: {value!r} not in {opts}")
        elif t == "range":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"{where}: range needs a number, got {value!r}")
                return
            lo, hi, step = sdef["min"], sdef["max"], sdef.get("step", 1)
            if not lo <= value <= hi:
                errors.append(f"{where}: {value} outside {lo}..{hi}")
            elif abs(((value - lo) / step) - round((value - lo) / step)) > 1e-9:
                errors.append(f"{where}: {value} not on step {step} from {lo}")
        elif t == "checkbox":
            if not isinstance(value, bool):
                errors.append(f"{where}: checkbox needs true/false, got {value!r}")
        elif t == "image_picker" and value:
            name = value.replace("shopify://shop_images/", "")
            if not value.startswith("shopify://shop_images/") or (files and name not in files):
                errors.append(f"{where}: image {value!r} not found in Files")
        elif t == "url" and isinstance(value, str) and value.startswith("shopify://"):
            kind, _, handle = value[len("shopify://"):].partition("/")
            if kind == "collections" and live_cols is not None and handle not in live_cols:
                errors.append(f"{where}: collection {handle!r} is not a live collection")
            if kind == "products" and live_products is not None and handle not in live_products:
                errors.append(f"{where}: product {handle!r} is not an active product")
        elif t == "collection" and value and live_cols is not None and value not in live_cols:
            errors.append(f"{where}: collection {value!r} is not a live collection")

    sections, order = tpl["sections"], tpl["order"]
    if sorted(order) != sorted(sections):
        errors.append("order does not list exactly the sections")
    if len(sections) > 25:
        errors.append(f"{len(sections)} sections (limit 25)")

    for key, sec in sections.items():
        if before.get(key) == sec:
            continue
        if sec["type"] == "apps":
            continue
        schema = load_schema(a.theme_dir, sec["type"])
        sdefs = {s["id"]: s for s in schema.get("settings", []) if "id" in s}
        for sid, val in sec.get("settings", {}).items():
            checked += 1
            if sid not in sdefs:
                errors.append(f"{key}.settings.{sid}: no such setting in {sec['type']}")
            else:
                check_value(f"{key}.settings.{sid}", sdefs[sid], val)
        blocks = sec.get("blocks", {})
        if blocks or "block_order" in sec:
            if sorted(sec.get("block_order", [])) != sorted(blocks):
                errors.append(f"{key}: block_order does not match blocks")
        mb = schema.get("max_blocks")
        if mb is not None and len(blocks) > mb:
            errors.append(f"{key}: {len(blocks)} blocks, max_blocks is {mb}")
        btypes = {b["type"]: b for b in schema.get("blocks", [])}
        for bkey, blk in blocks.items():
            if blk["type"] not in btypes:
                errors.append(f"{key}.{bkey}: block type {blk['type']!r} not in {list(btypes)}")
                continue
            bdefs = {s["id"]: s for s in btypes[blk["type"]].get("settings", []) if "id" in s}
            for sid, val in blk.get("settings", {}).items():
                checked += 1
                if sid not in bdefs:
                    errors.append(f"{key}.{bkey}.{sid}: no such block setting in {sec['type']}/{blk['type']}")
                else:
                    check_value(f"{key}.{bkey}.{sid}", bdefs[sid], val)

    for e in errors:
        print("ERROR", e)
    print(f"{checked} settings checked across {len(sections)} sections; {len(errors)} error(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
