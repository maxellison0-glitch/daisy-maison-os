# Etsy Data Pull — Claude in Chrome prompt (Daisy Maison)

**How to use:** open Etsy (logged in) in Chrome, paste the prompt below into Claude in Chrome, let it run, then copy the `=== ETSY DATA DUMP ===` block it prints and paste it back into the Daisy Maison chat. I'll turn it into an Etsy morning digest. Run it whenever — 1–5×/week is fine; the rolling 7-day window means gaps don't break anything.

---

## Which one to run?

- **DAILY QUICK** (below) — ~30 seconds, just yesterday + the 7-day headline. Use most mornings.
- **FULL WEEKLY** (further down) — traffic sources, search terms, top listings, Etsy Ads, 30-day trend. Run 1–2×/week or whenever you want the deep read.

Both print the same `=== ETSY DATA DUMP ===` block, so either one drops straight into the digest — the daily version just leaves the deeper sections as "not pulled today".

---

## DAILY QUICK PULL (copy everything below this line)

You are pulling read-only analytics for my Etsy shop, Daisy Maison UK. **Do not change any settings, reply, edit listings, or click anything that alters shop state. Read and report only.** Currency is GBP (£). Report exact numbers as shown — never round or estimate; if a figure isn't visible, write "not shown". If I'm not logged in, stop and tell me.

1. Go to https://www.etsy.com/your/shops/me/stats. Set the range to a single day = **yesterday**. Capture Visits, Orders, Revenue, Conversion rate.
2. Switch the range to **Last 7 days**. Capture Visits, Orders, Conversion rate, Revenue (with the ± % change vs previous period Etsy shows), and note the exact dates the range covers.

Then print ONE fenced code block in exactly this structure, nothing outside it:

```
=== ETSY DATA DUMP — Daisy Maison ===
Pulled: <today's date + time>
Mode: DAILY QUICK
Etsy 7-day range shown as: <dates>

[LAST 7 DAYS]
Visits: <n> (<±%>)
Orders: <n> (<±%>)
Conversion rate: <%> (<±%>)
Revenue: £<n> (<±%>)

[TRAFFIC SOURCES — 7d]
not pulled today

[SEARCH TERMS — 7d, top 10]
not pulled today

[TOP LISTINGS — 7d, top 8]
not pulled today

[ETSY ADS — 7d]
not pulled today

[YESTERDAY — <date>]
Visits: <n> | Orders: <n> | Revenue: £<n> | Conversion rate: <%>

[LAST 30 DAYS]
not pulled today

[EXTRAS]
not pulled today

[NOTES]
Daily quick pull — deeper sections skipped. Run the full weekly for those.
=== END ===
```

---

## FULL WEEKLY PROMPT (copy everything below this line)

You are pulling read-only analytics for my Etsy shop, Daisy Maison UK, to feed a morning digest. **Do not change any settings, reply to anything, edit listings, or click anything that alters shop state. Read and report only.** Currency is GBP (£). Report exact numbers as shown on screen — never round or estimate, and if a figure isn't visible, write "not shown" rather than guessing.

Work through these steps in order. If I'm not logged in, stop and tell me. If a page layout differs from what's described, navigate the Shop Manager left-hand menu to find the equivalent (Stats, Marketing → Etsy Ads, Orders & Shipping) and pull the same fields.

**1. Stats — Last 7 days (primary window)**
Go to https://www.etsy.com/your/shops/me/stats and set the date range to **Last 7 days**. Etsy usually shows a % change vs the previous period next to each metric — capture both the value and the % change for:
- Visits
- Orders
- Conversion rate
- Revenue
- (also note the exact date range Etsy says this covers)

**2. Traffic sources (Last 7 days)**
On the same Stats page, open the traffic-sources breakdown ("How shoppers found you" / "Traffic"). List every source with its visits and % share, e.g. Etsy search, Direct & other traffic, Social media, Etsy Ads, Marketing & SEO, Etsy app & other Etsy pages.

**3. Search terms (Last 7 days)**
Find the "Search terms that brought visitors to your shop" list. Give me the top ~10 terms with their visit counts.

**4. Top listings (Last 7 days)**
From the listings/stats breakdown, give the top ~8 listings by visits, and for each (where shown): visits, orders, and revenue. Note which are teacher products and which are wedding / Mr & Mrs products.

**5. Etsy Ads (Last 7 days)**
Go to https://www.etsy.com/your/shops/me/advertising (Marketing → Etsy Ads). Set the range to Last 7 days and capture: ad spend, ad clicks, ad views/impressions, orders from ads, and revenue from ads. Then find Offsite Ads and capture offsite ad fees and offsite-attributed revenue if shown.

**6. Yesterday snapshot (single day)**
Back on Stats, switch the range to a single day = **yesterday**. Capture Visits, Orders, Revenue, Conversion rate for that one day.

**7. Last 30 days snapshot (trend context)**
Switch the range to **Last 30 days** and capture just: Visits, Orders, Revenue, Conversion rate (with % change vs previous period if shown).

**8. Extras (if quickly visible on the dashboard)**
New favourites/likes and new followers over the last 7 days, if surfaced. Skip if not easily found.

When done, print the results as ONE fenced code block in exactly this structure, filling every field (use "not shown" where unavailable). Do not add commentary outside the block.

```
=== ETSY DATA DUMP — Daisy Maison ===
Pulled: <today's date + time>
Etsy 7-day range shown as: <dates>

[LAST 7 DAYS]
Visits: <n> (<±%>)
Orders: <n> (<±%>)
Conversion rate: <%> (<±%>)
Revenue: £<n> (<±%>)

[TRAFFIC SOURCES — 7d]
<source>: <visits> (<%>)
... (all sources)

[SEARCH TERMS — 7d, top 10]
<term>: <visits>
...

[TOP LISTINGS — 7d, top 8]
<listing title> | visits <n> | orders <n> | revenue £<n> | [teacher/wedding/other]
...

[ETSY ADS — 7d]
Spend: £<n>
Clicks: <n>
Views: <n>
Orders from ads: <n>
Revenue from ads: £<n>
Offsite ad fees: £<n>
Offsite ad revenue: £<n>

[YESTERDAY — <date>]
Visits: <n> | Orders: <n> | Revenue: £<n> | Conversion rate: <%>

[LAST 30 DAYS]
Visits: <n> (<±%>) | Orders: <n> (<±%>) | Revenue: £<n> (<±%>) | Conversion rate: <%>

[EXTRAS]
New favourites (7d): <n or not shown>
New followers (7d): <n or not shown>

[NOTES]
<anything odd, missing, or a range that didn't match the request>
=== END ===
```
