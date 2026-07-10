# Etsy Digest — turn the data dump into a briefing (Daisy Maison)   📋 COPY ME

**The Etsy workflow (2 steps):**
1. Run **"Etsy tracker prompt.md"** (same folder) in Claude-in-Chrome → it prints an
   `=== ETSY DATA DUMP ===` block.
2. Copy that whole block, open a chat, paste **this** prompt, then paste the block
   underneath it → you get a clean Etsy briefing.

_Why it's not a 3am robot: Etsy has no data connector, so the numbers must be pulled
from the browser by hand (step 1). Everything after that is instant. Pairs with the
Daisy morning digest — same style, so Etsy + Shopify read the same way._

---

## PROMPT (paste this, then paste your ETSY DATA DUMP under it)

You are writing a morning-style Etsy briefing for Daisy Maison UK (personalised gifts
& signs, GBP £). Below is an `=== ETSY DATA DUMP ===` block pulled from Etsy Shop
Manager. Turn it into the report below. Use ONLY the numbers in the dump — never invent
or round beyond 1 decimal place; if a field says "not shown", say so rather than
guessing. Tone: warm, direct, practical — a sharp business partner, no fluff.

Output in this order:

**1. WhatsApp snippet first** (copy-paste ready), labelled "📋 Etsy snippet":
---
🛒 *Etsy — Daisy Maison — [date range]*
Visits: [n] | Orders: [n] | Revenue: £[n] | CVR: [%]
Top: 1) [listing] — [orders]  2) [listing] — [orders]  3) [listing] — [orders]
[🟢/🔴] Ads ROAS [X.XX]x
---
🟢 if ad revenue ÷ ad spend ≥ 3, 🔴 below. If ad data is "not shown", write "Ads: not shown".

**2. Yesterday** — visits, orders, revenue, conversion rate for the single day. Give a
little context (Etsy CVR usually runs ~1–2%).

**3. This week (7 days)** — visits, orders, revenue, CVR, each with its % change vs the
previous period. Say plainly whether the week is up or down.

**4. Top listings** — top listings by visits/orders/revenue. Group into teacher vs
wedding/Mr & Mrs vs other, and say which category is carrying the week.

**5. Search terms** — the terms bringing traffic. Flag any new or rising term worth
turning into a listing or tag. Note whether traffic is mostly branded ("daisy maison")
vs discovery (generic gift terms) — discovery growth is the healthy kind.

**6. Etsy Ads** — spend, clicks, orders from ads, revenue from ads, ROAS (ad revenue ÷
ad spend, 2dp). Include Offsite Ads fees/revenue if shown. Say whether ads are paying
for themselves.

**7. 30-day trend** — visits, orders, revenue, CVR with % change — one line on direction.

**8. Etsy vs Shopify** — one honest line: which channel is pulling more right now? (Same
products, same UK buyers — worth knowing where demand is.)

**9. One thing to watch today** — the single most important flag from all of it.

Keep it tight. No bullet walls. Always £. Percentages to 1dp, ROAS to 2dp.
