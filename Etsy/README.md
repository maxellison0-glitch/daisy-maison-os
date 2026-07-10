# Daisy Maison — Etsy Folder

This folder connects your Etsy store data to both Claude (Cowork) and ChatGPT.

---

## Files

| File | Purpose |
|---|---|
| `Etsy Store Context.md` | Shared context doc — fill this in once, both AIs read it |
| `ChatGPT System Prompt.md` | Paste into ChatGPT custom instructions |
| `CSV Templates/Etsy Listings Export Template.csv` | Export your Etsy listings here monthly |
| `CSV Templates/Etsy Orders Export Template.csv` | Export your Etsy orders here monthly |
| `CSV Templates/Etsy Analytics Export Template.csv` | Export your Etsy search term / analytics data here |

---

## Monthly Workflow

1. Export CSVs from Etsy Stats (takes ~2 minutes)
2. Save them to `/CSV Templates/` replacing the templates
3. Open Claude (Cowork) and say: "Analyse my latest Etsy data"
4. OR paste the CSV into ChatGPT — it already has the system prompt context

---

## How to Export from Etsy

- **Listings:** Shop Manager → Listings → (filter Active) → Download CSV
- **Orders:** Shop Manager → Orders & Shipping → Download CSV
- **Search terms / analytics:** Shop Manager → Stats → (select date range) → Export
