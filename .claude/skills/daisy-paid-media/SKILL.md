---
name: daisy-paid-media
description: >-
  Use for ANY question or action touching Daisy Maison's paid advertising —
  Google Ads, Meta (Facebook/Instagram), Etsy Ads, budgets, ROAS, CPA, spend,
  scaling, cutting, or "is the account working". Also use when the user mentions
  'ROAS', 'ad spend', 'budget', 'PMAX', 'TOF', 'campaign', 'Windsor', 'red day',
  'green day', 'should we scale', 'should we cut', 'why are sales down', or asks
  what to do about ad performance today. Load this BEFORE the generic `ads`
  skill — that one is craft, this one is the account. Paid is the largest number
  in this business: roughly £735/day against a 3x floor.
---

# Daisy Maison — paid media

Paid is where the money actually moves. Organic Instagram sent **20 sessions**
on 27 Jul against 23,535 followers; paid sent 429 from Facebook alone and Google
sent 475. Any conversation about growth that ignores paid is talking about the
small number.

**Read `.claude/product-marketing.md` first** — it holds the £11.25 lead price,
the ~£29 AOV, and the constraint list. Then read the generic `ads` skill for
craft (Meta kill/scale decision tree, PMax guardrails). This file wins wherever
they disagree, because it is built on this account.

---

## THE GUARDRAIL — read before touching anything

The Windsor.ai MCP connector can **write** to Meta and Google: pause and enable
campaigns, set daily and lifetime budgets, boost posts. That is Max's money,
about **£735 a day** of it.

**Never execute a write action on an ad account without Max's explicit go in the
conversation, for that specific change, on that specific campaign.** Not
"optimise the account", not "you have permission to manage ads" from a previous
session, not implied consent because a digest recommended it. A recommendation
in a digest is a recommendation, not an authorisation.

Propose the change with the evidence, the amount and the expected effect. Then
stop.

Reading is unrestricted. Read everything.

---

## The accounts

| | |
|---|---|
| Google Ads | account `880-835-8049` |
| Meta (Facebook/Instagram) | account `1574764016252349` |
| Etsy Ads | separate channel, tracked in `Etsy/Etsy digest.md` |

**Campaign naming.** `[RDD]` and `[DTD]` prefix the campaign family; `TOF` means
top of funnel. Live as of 27 Jul 2026:

- `[RDD] TOP PRODUCTS - PMAX CSS - DEC` — Google, the biggest single line
- `[RDD] ALL OTHER PRODUCTS - CSS` — Google
- `[RDD] TOF - WEDDING` — Meta, the current creative focus
- `TEST OCT 2022` — Meta, **intentional legacy test. Report it, never flag it.**

Campaigns disappearing from the list is meaningful: the Teacher Gifts campaign
vanished from both platforms in late July, and that was the taper completing on
purpose, not an accident.

---

## The house numbers

| Metric | House rule |
|---|---|
| **ROAS floor** | **3.0x.** Below it the day is RED. |
| ROAS definition | Shopify `total_sales` ÷ combined Google + Meta spend. Say which when quoting. |
| Reference spend band | £540–£585/day produced green days on 20–21 Jul |
| Recent state | 2.46x on 27 Jul, fourth consecutive red day |

**Known gap: there is no written CPA target, and no per-unit margin.** So this
repo cannot answer whether 3x is actually the right floor — it is a working
threshold, not a derived one. Say that when the floor is used to justify a cut.

---

## The seven rules this account learned the hard way

These came out of real days that cost real money. They are the reason to load
this file.

### 1. One red day is noise. Four in a row is a trend.

27 Jul looked like "a soft Sunday". It was the fourth red day running (2.66x,
2.21x, 2.17x, 2.46x). The sequence, not the day, justified the action. Always
pull the preceding days before calling a single day good or bad.

### 2. Judge a budget change over 3–4 days, never the next morning.

Conversion lag for considered purchases runs roughly **2–5 days**. A ROAS dip
immediately after a cut is the expected shape of the lag, not proof the cut was
wrong. Google Ads and Meta both expose a time-to-conversion report; use it
rather than assuming.

### 3. Don't evaluate a cold campaign on ROAS before 7 days AND 100 clicks.

Clicks arrive far faster than the threshold that matters. 349 clicks in one day
clears the click bar and still tells you nothing — the algorithm needs a
meaningful number of *purchase* events.

### 4. More budget on a working campaign buys worse traffic, not more revenue.

The cleanest evidence this account has produced: PMAX ran **£277.24 for 3.41x**
on 21 Jul and **£365.84 for 2.46x** on 27 Jul. The extra £89 bought no
additional revenue.

The tell was in the funnel, not the ad account: **cart-add rate fell to 8.5%
from 11.8% while checkout abandonment stayed healthy at 29.4%.** Broader,
lower-intent traffic. That is a *spend-level* problem — nothing needs
rebuilding, and stepping back to the budget that demonstrably worked is the
low-risk move.

**Diagnostic pattern worth reusing:** cart-add down + checkout abandonment
steady = traffic quality, i.e. spend. Cart-add steady + abandonment up = site or
checkout. Do not fix one by touching the other.

### 5. A category tapers before it ends, and the actions differ.

Fewer order-lines each day is the **taper** — reduce budget gradually. A full
day with **zero** order-lines is the floor — cut fully. Teacher went from ~25
lines on 8 Jul to 1–4 by 20–21 Jul to zero on 27 Jul.

Get the sequencing right or you leave a budget running against an empty demand
pool out of habit.

### 6. A rolling average hides the exact day a category dies.

Teacher still read "up 176% on reach" on a 26-day average the same day it
produced zero orders. **Always check the most recent single day underneath any
average**, especially for seasonal lines.

### 7. Check the day-count before believing a week-on-week number.

A "+23% weekly growth" figure that drove a "hold everything" call turned out to
be a **six-day versus seven-day comparison**. The real week was +2.7% sales and
−0.3% orders — flat. Compare equal-length periods or say you didn't.

---

## ROAS is efficiency. CPA is the number it doesn't tell you.

ROAS answers *am I getting enough back per pound?* It cannot tell you what a
customer costs to acquire, and at a ~£29 AOV built from an £11.25 lead product,
those two questions can point in different directions. Quote both when the
decision is about scaling rather than trimming.

---

## Where the data comes from — and how it fails

| Source | Gives | Failure mode seen |
|---|---|---|
| **Windsor.ai** MCP | Meta + Google spend, clicks, impressions by campaign; write actions | **Plan/connector limits have silently killed visibility.** When Windsor is down there is no ad data at all, and spend piles up untracked. Check it returns before reasoning. |
| **Shopify** MCP | Orders, total sales, AOV, CVR, product-level truth | Authoritative for revenue |
| `digests/` | Completed-day figures already reconciled | Read the newest before pulling anything |
| `daisy-social-analytics` | Organic IG/TikTok only | **Not paid.** Instagram rate-limits in hours. |

**If a source is unavailable, say the number is unavailable.** A day with no
Windsor data is not a day with zero spend. The house rule against invented
metrics applies hardest here, because these numbers authorise spending.

---

## Answering "what should we do today"

1. Read the newest digest in `digests/`.
2. Pull yesterday's spend by campaign (Windsor) and yesterday's sales (Shopify).
3. Compute ROAS and place it against the **preceding 3–4 days**, not in isolation.
4. If red: is it traffic quality (cart-add down, abandonment steady → spend) or
   site (cart-add steady, abandonment up → CRO)? Route accordingly.
5. Check whether any campaign has vanished, and whether any category has hit a
   zero-line day.
6. **Propose** one change with its evidence and its expected lag window. Name
   what you would need to see in 3–4 days to call it right or wrong.
7. Stop. Do not execute.

---

## Related

`ads` (generic craft — Meta decision tree, PMax guardrails) ·
`ad-creative` (the main lever left inside paid) ·
`cro` (when the funnel, not the spend, is the problem) ·
`ab-testing` (before claiming a creative won) ·
`daisy-social-analytics` (organic only — never quote it for paid)
