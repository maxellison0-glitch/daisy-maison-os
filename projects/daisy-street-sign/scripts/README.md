# Street-sign batch planner

`plan-batch.py` is the read-only planning stage for production. Give it a JSON
export containing Shopify orders and it will:

- keep only supported Mr & Mrs street-sign lines with `unfulfilledQuantity > 0`;
- extract size, colour, and personalisation fields;
- group matching physical templates;
- split each group into three-position batches; and
- write a JSON manifest and human-readable Markdown review sheet.

It does not call Shopify, generate artwork, modify orders, or send anything to a
printer. The next stage can consume an approved manifest and call
`artwork/build.py` for each position.

Example:

```powershell
python scripts\plan-batch.py .\shopify-orders.json --out-dir D:\Daisy-Production\Street-Sign-Batches\2026-07-15
```

The current supported renderer is the Large Mr & Mrs template (`SKU 36961`).
Medium, Small, and colour-specific templates should be added only after their
physical production templates are validated.
