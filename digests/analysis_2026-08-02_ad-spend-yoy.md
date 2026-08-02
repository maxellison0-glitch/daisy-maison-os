# Why are we spending so much compared to last year?

**Deep dive, 2 August 2026.** Requested after Daryl's WhatsApp message of 1 Aug.

Sources: Windsor.ai (Google Ads `880-835-8049`, Meta `1574764016252349`) for spend,
clicks, impressions and platform conversions. Shopify Admin/ShopifyQL for sessions,
orders and `total_sales`. Every figure below was pulled live on 2 Aug 2026. Nothing
here is carried over from a previous digest.

---

## The short answer

**We are not spending more than last year. We are spending 37.6% less.**

July 2025 total paid spend was **£32,829**. July 2026 was **£20,483** — £12,346 less.
Revenue fell almost exactly in step: £90,245 → £54,189, down 40.0%. ROAS barely moved
(2.75x → 2.65x).

The account has not become dramatically worse at turning money into revenue. It has
become dramatically worse at turning money into **visitors**.

| July, whole month | 2025 | 2026 | Change |
|---|---:|---:|---:|
| Spend | £32,829 | £20,483 | **−37.6%** |
| Clicks | 136,284 | 45,640 | **−66.5%** |
| Blended cost per click | £0.241 | £0.449 | **+86.3%** |
| Shopify total sales | £90,245 | £54,189 | −40.0% |
| Orders | 3,496 | 1,865 | −46.7% |
| AOV | £25.81 | £29.06 | **+12.6%** |
| ROAS | 2.75x | 2.65x | −3.8% |
| CPA | £9.39 | £10.98 | +17.0% |
| Revenue per click | £0.662 | £1.187 | **+79.3%** |

Read the last two rows together with the first three. Every visitor we buy is worth
**79% more** than last year. Every visitor we buy also costs **86% more**. Those two
almost cancel, which is why ROAS looks flat while the business is 40% smaller.

**£20,483 spent at last July's click prices would have bought 85,031 visitors. It bought
45,640.** The 39,391 missing visitors are worth roughly **£46,800 a month** at this
year's own revenue-per-click.

---

## Reconciling Daryl's numbers

Daryl's figures are correct. His comparison window is not.

He quoted "this day equivalent last year": 3 Aug 2025, £720 spend (£430 Google, £290 FB),
£2,600 revenue. Verified against the raw pulls — Google £429.29, Meta £291.94, total
**£721.23**; Shopify total sales **£2,601.98**. Exact.

The problem is *which* day. Meta spend in July 2025 was heavily front-loaded and tapering
hard all month:

| Meta spend, 2025 | £/day |
|---|---:|
| 1–15 Jul 2025 | £970 |
| 17–31 Jul 2025 | £469 |
| by 31 Jul 2025 | £241 |

By 3 Aug 2025 Meta was at the very bottom of that taper. Comparing today against the
single cheapest week of last summer makes today's spend look inflated. Compare the whole
month and the direction reverses completely.

This is house rule 7 in `daisy-paid-media` — *check the day-count before believing a
period comparison* — showing up again, in a slightly different costume.

---

## Where the money actually went: matched 7 days (27 Jul – 2 Aug)

Equal-length windows, both years, same calendar dates.

| | 2025 | 2026 | Change |
|---|---:|---:|---:|
| Spend | £4,618.23 | £4,280.70 | −7.3% |
| Clicks | 16,087 | 9,034 | −43.8% |
| Shopify sessions | 9,842 | 6,467 | **−34.3%** |
| **Cost per session** | **£0.469** | **£0.662** | **+41.1%** |
| Conversion rate | 4.69% | 4.41% | −6.0% |
| Cart-add rate | 11.18% | 9.87% | −11.7% |
| Revenue per session | £1.487 | £1.552 | **+4.4%** |
| Orders | 531 | 325 | −38.8% |
| ROAS | 3.17x | 2.35x | — |
| CPA | £8.70 | £13.17 | +51.4% |

**The website is not the problem.** Conversion rate is within noise of last year, revenue
per session is *up*, AOV is up 12.6%. On the 14-day window (20 Jul – 2 Aug) site CVR is
actually higher this year: 4.53% vs 4.43%.

Cart-add rate is the one funnel metric genuinely down (11.18% → 9.87%). Per rule 4 in
`daisy-paid-media` — cart-add down while checkout abandonment holds — that reads as
traffic quality, not site quality. It is a symptom of the spend problem, not a second
problem.

---

## The diagnosis: it is Meta creative, and it is measurable

Splitting the cost-per-click inflation by platform, matched 7 days:

| | Google 2025 → 2026 | Meta 2025 → 2026 |
|---|---|---|
| Spend | £2,334 → £2,755 (+18.0%) | £2,285 → £1,526 (−33.2%) |
| Impressions | 349,214 → 370,207 (+6.0%) | 481,440 → 362,649 (−24.7%) |
| Clicks | 4,443 → 4,231 (−4.8%) | 11,644 → 4,803 (−58.8%) |
| **CPM** (auction price) | £6.68 → £7.44 (**+11.3%**) | £4.75 → £4.21 (**−11.3%**) |
| **CTR** (creative pull) | 1.27% → 1.14% (−10.2%) | 2.42% → 1.32% (**−45.2%**) |
| CPC | £0.525 → £0.651 (+23.9%) | £0.196 → £0.318 (**+62.0%**) |

**This is the single most important table in the document.**

Meta's CPM *fell* 11%. The auction got **cheaper**. Media inflation is not the
explanation on Meta — we are paying 62% more per click into a market that is charging
11% less per impression. The entire gap is click-through rate, which halved.

CTR is creative. That is what CTR measures.

Google is a milder, more ordinary story: CPM up 11%, CTR down 10%, both contributing to
+24% CPC. Some of that is genuine auction inflation.

Decomposing the **blended** +86% cost per click:
- **+49 points** — within-channel inflation (mostly Meta CTR collapse)
- **+11 points** — mix shift away from Meta, which is still the cheap channel

Meta was 68.0% of spend in July 2025 and is 44.0% now. We moved budget from the £0.32
channel to the £0.65 channel, which makes the blended number worse on top of everything
else.

---

## What the ad accounts looked like last year vs now

This is the part Mum asked for directly, and it is the most actionable finding.

### Meta — 6 live campaigns became 2

**27 Jul – 2 Aug 2025, live and spending:**

| Campaign | Angle |
|---|---|
| `Frame MANUAL HIGH` | best performer — 2.7–3.1% CTR, CPC £0.13–0.19 |
| `Frame winner adv +` | Advantage+ version of the same winner |
| `Advantage+ wedding sale Campaign - Copy` | wedding, sale framing |
| `WEDDING JULY` | wedding, seasonal |
| `Wedding Targets` | wedding, interest-targeted |
| `Planner` | separate product line |

**27 Jul – 2 Aug 2026, live and spending:**

| Campaign | Spend (7d) | % of Meta | CPC | CTR | Platform ROAS | CPA |
|---|---:|---:|---:|---:|---:|---:|
| `[RDD] TOF - WEDDING` | £951.41 | 62% | £0.259 | 1.64% | 2.35x | £12.52 |
| `TEST OCT 2022` | £574.73 | **38%** | £0.507 | **0.82%** | 2.14x | £17.42 |

Two observations, both material:

1. **Six creative angles became one.** Last year ran a frame product, a planner and
   three distinct wedding treatments concurrently. This year runs wedding only. There
   is nothing left to rotate into when a creative tires — and the data says it has
   tired. `[RDD] TOF - WEDDING` CTR over the last fortnight: 1.43, 1.96, 2.09, 2.28,
   2.40, 1.98, 2.02, 1.85, 1.72, 1.69, 1.59, 1.43, 1.53, 1.54. It peaked on 24 Jul and
   has fallen every direction since. Its CPC went £0.202 → £0.308 across the same
   window. Reach fell from 35,529 people on 20 Jul to 19,478 on 2 Aug.

2. **`TEST OCT 2022` is now 38% of Meta budget.** The house note says report it, never
   flag it, so this is a report, not a flag: at £0.507 CPC it buys clicks at roughly
   **double** the price of `TOF - WEDDING`, at half the CTR, for a worse CPA (£17.42 vs
   £12.52). Last year it spent nothing. Whether that is intended at this scale is a
   question for Max and Daryl, not an inference for this document.

### Google — 7 campaigns became 2

**Matched 7 days, share of Google spend:**

| 2025 | Spend | Share | | 2026 | Spend | Share |
|---|---:|---:|---|---|---:|---:|
| `[RDD] ALL OTHER PRODUCTS` | £1,102.41 | 47.2% | | `[RDD] TOP PRODUCTS - PMAX CSS - DEC` | £2,345.85 | **85.2%** |
| `[CB] PMax: Street Signs` | £997.90 | 42.8% | | `[RDD] ALL OTHER PRODUCTS - CSS` | £408.71 | 14.8% |
| `[CB] PMax - Pebble Gifts` | £108.25 | 4.6% | | | | |
| `[RDD] Search-Brand Terms` | £63.71 | 2.7% | | | | |
| `[CB] PMax - Remarket` | £29.52 | 1.3% | | | | |
| `[CB] Shopping - Catch All` | £17.21 | 0.7% | | | | |
| `CB - Search - Wedding Stationary` | £14.72 | 0.6% | | | | |

**Two of the campaigns that disappeared were the two most efficient in the account:**

- `[RDD] Search-Brand Terms` — £63.71 spend, 176 clicks at £0.36, £448.88 platform
  conversion value. **7.05x.** Brand search is people typing "Daisy Maison" into Google.
  It is the cheapest, highest-intent traffic that exists.
- `[CB] PMax - Remarket` — £29.52 spend, £111.28 value. **3.77x**, above the house floor.

Together they were only £93/week, so this is not where the £12,000 went. But they were
the two buckets clearing the 3x floor comfortably, and neither exists now. 85% of Google
budget sitting in a single PMax campaign also means there is no structural way to shift
money toward what is working — PMax decides that internally, and the 27–29 Jul digests
already document it drifting past efficient spend.

---

## Product: the shop got wider, the advertising got narrower

The catalogue is not the constraint. Jun–Aug 2026 gross sales by line include:

| Product | Orders | Gross |
|---|---:|---:|
| Personalised Dad Gift Street Sign (BBQ) | 467 | £5,310 |
| Personalised Number Plate Sign | 385 | £4,720 |
| Personalised Football Stadium Street Sign | 403 | £4,579 |
| Personalised Laser Cut BBQ Sign | 54 | £1,377 |

Football, number plates and Dad/BBQ signs are doing real volume — roughly £14,600 across
two months — with **no campaign of their own on either platform**. Every live Meta pound
goes to wedding.

One line has genuinely collapsed: `Porcelain Handled Tea Light Holder - Good friends`
did **207 orders / £2,996 in 14 days** last year (≈£214/day, ~13% of daily revenue). It
is still active but did 53 orders / £753 across all of **June–August 2026** (≈£12/day).
That single line accounts for a meaningful slice of the YoY revenue gap on its own.

**Open question, not a finding:** revenue per order containing `Mr & Mrs Street Sign`
fell from £17.28 (2025, 255 orders) to £11.46 (2026, 218 orders). The 28 Jul 2026 digest
shows Mr & Mrs at exactly £11.25/order — one unit. That implies last year's orders carried
~1.5 signs each and this year's carry one. ShopifyQL does not expose unit counts per
product here, so this could equally be a price change. **It needs checking in the Shopify
admin before anyone acts on it** — if multi-buy really has halved, that is a second,
independent revenue problem sitting underneath the traffic one.

---

## What this says to do

Ordered by size of the number attached, not by ease. **These are proposals. Nothing has
been executed and nothing should be without Max's explicit go on the specific change.**

1. **Meta creative is the whole ballgame.** A 45% CTR fall against a *falling* CPM is not
   the market and is not the website. Last year the account carried six concurrent angles
   including a non-wedding product; today one angle carries everything and it has been
   decaying for nine days straight. The brand already knows what its audience rewards —
   dry, British, self-deprecating, and real manufacturing footage over polish
   (`product-marketing.md`, and the 11,889-view sign post). Rebuilding creative volume is
   the lever, and per the hard constraints it can be done without filming anything.

2. **Reinstate brand search on Google.** `[RDD] Search-Brand Terms` ran at 7.05x on £9/day.
   It is the cheapest win available and the smallest change on this list.

3. **Give football / number plate / Dad-BBQ signs their own campaigns.** £14,600 over two
   months with zero dedicated spend, in an account where the only Meta audience is
   saturating. This is the clearest untapped demand pool in the data.

4. **Ask Daryl directly about `TEST OCT 2022` at 38% of Meta budget** and about the two
   Google campaigns that were removed. Both are structural decisions this repo cannot
   see the reasoning for.

5. **Check the Mr & Mrs units-per-order question in Shopify admin** before treating it as
   real.

### What would tell us this read is right

If it is Meta creative: new angles should lift Meta CTR back toward 2%+ and pull Meta CPC
back under £0.25 within a week of launch, with sessions rising before revenue does. Judge
over 3–4 days minimum, never the next morning (rule 2), and do not evaluate any new cold
campaign on ROAS before 7 days *and* 100 clicks (rule 3).

If sessions rise and revenue does not follow, the read is wrong and the problem is further
down the funnel than this document places it.

---

## Known gaps in this analysis

- **No margin data**, so the 3x ROAS floor remains a working threshold, not a derived one.
  Whether 2.65x is actually loss-making is not answerable from this repo.
- **No CPA target** is written down anywhere, so "+17% CPA" cannot be scored against
  intent.
- Windsor's 2025 Google detail was pulled from 27 Jul; the 14-day matched window uses
  Shopify for both years and Windsor spend for the 7-day overlap. Both comparison windows
  are equal-length and same-calendar-date.
- Both chosen 7-day windows sit *below* their own month's daily average
  (£2,091/day vs July 2025's £2,911; £1,434/day vs July 2026's £1,748), so the matched-week
  figures understate both years roughly symmetrically.
- Etsy is excluded entirely — no fresh data in `Etsy/`.
