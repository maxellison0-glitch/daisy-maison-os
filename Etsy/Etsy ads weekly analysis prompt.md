# Etsy Ads — Weekly Analysis Prompt (Daisy Maison)

**How to use:** open Etsy (logged in) in Chrome, paste the prompt below into Claude in Chrome, let it run. Run once a week — the 7-day and 30-day windows give enough data to make real decisions.

---

## PROMPT (copy everything below this line)

You are pulling a detailed Etsy Ads analysis for my Etsy shop, Daisy Maison UK. **Do not change any settings, adjust bids, toggle listings on/off, or click anything that alters shop state. Read and report only.** Currency is GBP (£) for revenue and USD ($) for ad spend (Etsy bills ads in USD). Report exact numbers as shown — never round or estimate; if a figure isn't visible, write "not shown". If I'm not logged in, stop and tell me.

**Step 1 — Etsy Ads dashboard (7 days)**
Go to https://www.etsy.com/your/shops/me/advertising and set the date range to **Last 7 days**. Capture the top-level summary:
- Total ad spend
- Total clicks
- Total impressions/views
- Total orders from ads
- Total revenue from ads
- ROAS (revenue ÷ spend — calculate if not shown)
- Daily budget setting
- Number of promoted listings

**Step 2 — Per-listing ad performance (7 days)**
On the same page, find the listing-level breakdown. For EVERY promoted listing (not just the top few), capture:
- Listing title
- Ad spend
- Clicks
- Impressions/views
- Orders from ads
- Revenue from ads
- ROAS (calculate: revenue ÷ spend)
- CPC (calculate: spend ÷ clicks)
- Ad strategy/bid setting if shown (e.g. "Lower click cost", "Efficient spending", "Max clicks")

Sort by spend (highest first).

**Step 3 — Etsy Ads dashboard (30 days)**
Switch the date range to **Last 30 days** and capture the same top-level summary as Step 1 (spend, clicks, impressions, orders, revenue, ROAS).

**Step 4 — Per-listing ad performance (30 days)**
Same listing-level breakdown as Step 2, but for the 30-day window. Capture all promoted listings with the same fields.

**Step 5 — Offsite Ads**
Find the Offsite Ads section (usually under Marketing or a separate tab). Capture:
- Offsite ad fees charged
- Orders from offsite ads
- Revenue from offsite ads
- Whether Offsite Ads are opted in or out (and whether you're eligible to opt out)

**Step 6 — Search terms driving ad clicks (if visible)**
If the Ads dashboard shows which search terms triggered your ads, capture the top 10 by clicks with: term, impressions, clicks, orders, spend.

When done, print the results as ONE fenced code block in exactly this structure:

```
=== ETSY ADS ANALYSIS — Daisy Maison ===
Pulled: <today's date + time>

[7-DAY SUMMARY]
Period: <exact dates>
Daily budget: $<n>/day
Promoted listings: <n>
Total spend: $<n>
Total clicks: <n>
Total impressions: <n>
Total orders from ads: <n>
Total revenue from ads: $<n>
ROAS: <n>x

[7-DAY PER-LISTING (sorted by spend)]
<listing title> | spend $<n> | clicks <n> | impressions <n> | orders <n> | revenue $<n> | ROAS <n>x | CPC $<n> | strategy: <strategy>
...

[30-DAY SUMMARY]
Period: <exact dates>
Total spend: $<n>
Total clicks: <n>
Total impressions: <n>
Total orders from ads: <n>
Total revenue from ads: $<n>
ROAS: <n>x

[30-DAY PER-LISTING (sorted by spend)]
<listing title> | spend $<n> | clicks <n> | impressions <n> | orders <n> | revenue $<n> | ROAS <n>x | CPC $<n> | strategy: <strategy>
...

[OFFSITE ADS]
Opted in: <yes/no>
Eligible to opt out: <yes/no>
Fees charged (period): $<n>
Orders from offsite: <n>
Revenue from offsite: $<n>

[SEARCH TERMS DRIVING AD CLICKS — top 10]
<term> | impressions <n> | clicks <n> | orders <n> | spend $<n>
...
(or "not shown" if this breakdown isn't available)

[NOTES]
<anything odd, missing, or layout differences>
=== END ===
```
