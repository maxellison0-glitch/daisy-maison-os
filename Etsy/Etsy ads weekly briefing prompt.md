# Etsy Ads — Weekly Briefing Prompt (Daisy Maison)

**The workflow (2 steps):**
1. Run **"Etsy ads weekly analysis prompt.md"** in Claude-in-Chrome → it prints an
   `=== ETSY ADS ANALYSIS ===` block.
2. Copy that block, open a chat, paste **this** prompt, then paste the block underneath
   it → you get a weekly Etsy Ads briefing with decisions.

---

## PROMPT (paste this, then paste your ETSY ADS ANALYSIS block under it)

You are writing a weekly Etsy Ads briefing for Daisy Maison UK (personalised gifts &
signs, GBP £, ad spend in USD $). Below is an `=== ETSY ADS ANALYSIS ===` block pulled
from Etsy Ads Manager. Turn it into the report below. Use ONLY the numbers in the block
— never invent or round beyond 1 decimal place. Tone: ruthless, data-first, no fluff.

Output in this order:

**1. Headline** — total 7-day spend, orders from ads, ROAS, green/red call (green at 3x+).
One sentence: are the ads paying for themselves this week?

**2. Per-listing league table** — sort all promoted listings by 7-day ROAS (highest first).
For each: listing title (shortened), spend, clicks, orders, ROAS, CPC. Mark each as:
- WINNER (ROAS 3x+)
- MARGINAL (ROAS 1x–3x)
- LOSER (ROAS below 1x or zero orders on meaningful spend)
- TOO NEW (under $15 spend, not enough data)

**3. Budget allocation verdict** — which listings deserve MORE budget and which should be
depromoted or paused. Use the 7-day per-listing data. The question is: would the next
dollar produce more revenue on listing A or listing B? A listing with 0 orders on $50+
spend is a cut signal. A listing with 3x+ ROAS on capped spend is a scale signal.

**4. CPC analysis** — average CPC across all listings. Flag any listing where CPC is 2x+
the account average (you're overpaying for those clicks). Flag any listing where CPC is
unusually low but ROAS is also low (cheap clicks, wrong audience).

**5. 7-day vs 30-day trend** — compare 7-day ROAS to 30-day ROAS. Is performance improving
or declining? Same for spend level — is budget increasing or flat?

**6. Offsite Ads** — are offsite ads profitable? If fees exceed revenue, flag it. If you're
eligible to opt out and they're losing money, say so.

**7. Search terms** — if search term data was captured, which ad-triggering terms are
converting and which are burning spend with zero orders?

**8. The three decisions this week** — the three specific changes to make right now:
promote/depromote/adjust budget/change strategy per listing. Be decisive — pick it, don't
offer options.

Keep it tight. Always £ for revenue, $ for ad spend. Percentages to 1dp, ROAS to 2dp.
