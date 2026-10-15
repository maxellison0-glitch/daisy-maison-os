# Daisy Maison — Checkout Audit (6 Aug 2026)

*Audit of the checkout flow, the new mandatory fields (phone number, postcode), abandonment behaviour, and how the flow compares to standard UK e-commerce practice. All store statistics pulled live from Shopify on 6 Aug 2026.*

---

## TL;DR

1. **The mandatory phone field is not visibly hurting completion.** Checkout completion has *improved* from ~58% (May–Jun) to ~65% (Jul–Aug). ~96% of recent orders carry a shipping phone number. Keep it — but only if we actually use it for delivery notifications; otherwise industry evidence (Baymard: 14% of users abandon when phone is required without explanation) says make it optional.
2. **The real friction is not the form — it's the shipping cost reveal.** Nearly every abandoned checkout in the sample had a *fully completed* address, phone and postcode. People finish the hard part, see the total, and leave. We charged **£9,941 in shipping on £51,985 total sales (30d)** — ~£5.60 per order on a **£23.81 AOV** — and the free-shipping threshold is **£50, more than double AOV**, so effectively nobody reaches it.
3. **228 abandoned checkouts in 30 days (~£5.5k of intent)**, most with full contact details captured — a recovery-email goldmine if the automation is actually on.
4. Postcode being mandatory is a non-issue (every UK checkout requires it). The lever is **address autocomplete / postcode lookup**, which UK shoppers expect — confirm it's enabled in Settings → Checkout.

---

## 1. The funnel — real numbers (last 30 days, 7 Jul – 6 Aug)

| Stage | Sessions | Rate |
|---|---|---|
| Sessions | 30,608 | — |
| Added to cart | 3,255 | 10.6% of sessions |
| Reached checkout | 2,375 | 73.0% of carts |
| Completed checkout | 1,537 | **64.7% of checkouts** |
| Overall conversion | — | **5.02%** |

- **Checkout abandonment: 35.3%** of sessions that reach checkout leave without buying (~28 sessions/day).
- **Post-cart abandonment: 52.8%** — well *better* than the Baymard global average of ~70% cart abandonment. The funnel is healthy by industry standards; the opportunity is incremental, not a fire.
- Orders (sales data): 1,775 orders, £51,985 total sales, £23.81 AOV, £9,941 shipping charges.

### By device (30d, reached → completed)

| Device | Sessions | Reached checkout | Completed | Completion |
|---|---|---|---|---|
| Mobile | 27,624 (90.2%) | 2,168 | 1,410 | **65.0%** |
| Desktop | 2,430 | 167 | 95 | **56.9%** |
| Tablet | 554 | 41 | 32 | 78.0% |

Desktop completes *worse* than mobile — unusual (desktop normally converts better). Sample is small (167 checkouts), but worth a manual test-purchase run on desktop to rule out a layout/payment issue.

### Trend (weekly checkout completion, completed ÷ reached)

May: 49–61% → June: 57–61% → **July: 65–66%** → early Aug: 62%.

Completion has been *improving* through the period in which the new mandatory fields were live. Whatever conversion softness exists (overall CVR fell from the June peak of 7.9% weekly to ~4.5–5.2%) is **upstream of checkout** — sessions→cart rate, i.e. traffic quality / paid mix territory — not checkout friction.

---

## 2. Mandatory fields audit

### Phone number (newly mandatory)

Evidence from the last 50 orders:
- **~96% have a shipping phone number** — consistent with the field being required. (The couple of nulls are staff/draft orders and likely express-wallet checkouts, which can bypass the standard form.)
- Formats are **wildly inconsistent**: `07…`, `+447…`, `447…` (no plus), and versions with spaces. If this number feeds courier SMS/WhatsApp notifications (Royal Mail, Evri etc.), un-normalised formats like `447481144734` can silently fail. Worth normalising at export or via the fulfilment app.

Industry evidence ([Baymard](https://baymard.com/blog/explain-phone-number-field)): **14% of users abandon checkout when a phone number is simply required**; the fix is to explain *why* it's needed ("for delivery updates"). On our plan (Shopify, not Plus) we can't add microcopy to the checkout field — the options are only required / optional / hidden.

**Verdict:** our own data shows no completion damage, so keep it **required only if the number is genuinely used for delivery notifications**. If it isn't, set it to optional — we'd be paying a known industry tax (up to ~14%) for data we don't use. Either way, decide based on use, and note the date the setting changed so future funnel dips can be attributed correctly.

### Postcode

- Mandatory postcode is **universal in UK e-commerce** — Shopify cannot ship a UK order without one, nor can any competitor. This field is not a differentiator or a friction source by itself.
- The differentiator is **address autocomplete / postcode lookup**. UK shoppers are trained (Amazon, ASOS, Next, virtually every retailer) to type a postcode and pick their address. Shopify has a free built-in address autocomplete toggle: **Settings → Checkout → Address collection preferences → "Use address autocomplete"**. Confirm it's on — it's the single cheapest way to shorten the form on a 90% mobile audience.
- **Validation gap observed:** an abandoned checkout contained postcode `IV1 1ID` — an impossible UK postcode (the letters C, I, K, M, O, V never appear in the final two positions). Shopify's format check is loose, so bad postcodes can flow into orders → failed deliveries → refunds. Low frequency, but if delivery failures ever spike, an address-validation app is the fix.

### Field count vs benchmark

Shopify's hosted checkout asks for: email, first name, last name, address1, address2 (optional), city, postcode, phone = **8–9 fields**. Baymard's ideal is 12–14 *elements* total (average US site: 23). **We are already leaner than the benchmark** — there is no case for structural form changes.

---

## 3. Where people actually abandon

Sampled the 25 most recent abandoned checkouts (of **228 in the last 30 days**):

- **~90% had a complete shipping address including phone and postcode.** These are not people scared off by form fields — they finished the form, advanced to shipping/payment, and left.
- Cart values £11–£48, clustering at £22–34 — i.e. **below the £50 free-shipping threshold**, so all of them were staring at a ~£3–6 shipping line on a ~£25 order when they quit.
- Almost all have a captured email and/or phone → fully recoverable audience.

**At ~£25 average abandoned value, 228 abandons ≈ £5,500/month of expressed intent.** Industry recovery emails typically win back 5–15%: **£300–800/month** on autopilot.

**Action:** confirm the abandoned-checkout email automation is actually live (Shopify Admin → Marketing → Automations), and that it sends at ~1h + ~24h. We could not verify this via API.

---

## 4. Shipping cost — the structural friction

- Shipping charged in 30d: **£9,941** across 1,775 orders ≈ **£5.60/order** on a £23.81 AOV → customers pay a **~24% surcharge** at the exact moment of maximum hesitation.
- Free-shipping threshold: **£50** (announced on-site) vs £23.81 AOV. A threshold customers can't realistically reach doesn't drive basket-building — it just advertises that they're paying for shipping.
- This matches the #1 industry abandonment cause: **39–48% of shoppers cite unexpected extra costs/shipping** as their reason for abandoning ([Statista](https://www.statista.com/statistics/1228452/reasons-for-abandonments-during-checkout-united-states/), [Baymard via ContentSquare](https://contentsquare.com/guides/cart-abandonment/stats/)).

**Recommended test (highest-value item in this audit):**
- Drop the free-shipping threshold to **£30–35** — reachable with one add-on (mounting strips, second sign, microfiber cloth when it launches). This converts the shipping line from pure friction into an AOV lever, feeding the existing add-on strategy in `revenue-levers.md`.
- Alternative to A/B: bake ~£3 into product prices and advertise "Free UK delivery" sitewide. Higher risk (price perception on ads/Etsy comparisons), so test threshold first.
- Show shipping cost *earlier* (cart page estimate) so the checkout reveal isn't a surprise.

---

## 5. How the flow compares to other websites

| Practice (UK norm) | Big UK retail (Amazon/ASOS/Next pattern) | Daisy Maison today |
|---|---|---|
| Guest checkout by default | ✅ standard | ✅ Shopify default |
| Steps | 1-page or 3-step express | ✅ Shopify 3-step, best-in-class baseline |
| Postcode lookup / address autocomplete | ✅ universal | ❓ verify toggle is on |
| Phone required | Usually optional **or** explained ("for delivery updates") | Required, no explanation possible on our plan |
| Express wallets (Apple Pay / Google Pay / Shop Pay / PayPal) top of checkout | ✅ universal | Shopify Payments + PayPal confirmed in order data; **verify Apple/Google Pay and Shop Pay toggles are on** — 90% of traffic is mobile, where wallets convert best |
| Shipping cost visible before checkout | ✅ increasingly standard | ❌ revealed at checkout; £50 free-ship threshold out of reach |
| Free-ship threshold vs AOV | typically set ~20–40% above AOV | **210% of AOV** |
| BNPL (Klarna/Clearpay) | common at £30+ baskets | Not present — fine at £24 AOV, not worth the fee load |

Because checkout is Shopify-hosted, the structure is already what most UK small retailers use — the deltas are all **configuration** (autocomplete, wallets, threshold), not build work.

---

## 6. Bugs & data-quality observations

1. **Invalid postcode accepted** (`IV1 1ID`) — loose validation; watch failed-delivery rate.
2. **Phone formats un-normalised** (`07…` / `+447…` / `447…` / spaces) — risk to courier SMS notifications; normalise in fulfilment flow.
3. **A small % of paid orders have no phone despite the mandatory setting** — express-wallet path can supply different fields. If ops relies on "every order has a phone", it doesn't — build the exception into the dispatch process.
4. **Desktop completion (56.9%) below mobile (65.0%)** — small sample; do one manual desktop test purchase to rule out a real defect.
5. `revenue-levers.md` said "Checkout friction: no known issues" — now superseded by this audit (updated in the same commit).

---

## 7. Ranked recommendations

| # | Action | Effort | Expected impact |
|---|---|---|---|
| 1 | Lower free-shipping threshold to £30–35 and promote it in the announcement bar + cart | Config | Attacks the #1 abandonment cause; feeds AOV strategy. Even +3pts completion ≈ +70 orders/£1.7k/mo |
| 2 | Verify abandoned-checkout email automation is live (228 abandons ≈ £5.5k/mo intent) | Config check | £300–800/mo recovered |
| 3 | Confirm address autocomplete is ON (Settings → Checkout) | Toggle | Shorter mobile form for 90% of traffic |
| 4 | Confirm Shop Pay + Apple Pay + Google Pay enabled and dynamic checkout button shows on cart | Toggle | Wallet checkouts skip the form entirely — sidesteps the whole mandatory-field question |
| 5 | Decide phone policy: keep required **iff** used for delivery SMS; else optional | Decision | Avoids the ~14% "unexplained required phone" tax if unused |
| 6 | Show shipping estimate on cart page | Small theme edit | Removes the surprise at checkout |
| 7 | Normalise phone formats for courier notifications | Ops | Fewer silent SMS failures |
| 8 | One desktop test purchase to explain the 56.9% desktop completion | 10 min | Rules out a real bug |

### What this audit could NOT read via API (verify in Admin → Settings → Checkout)
- Exact phone-field setting (required/optional) and **the date it changed**
- Address autocomplete toggle state
- Express wallet / dynamic checkout button toggles
- Abandoned-checkout email automation status

---

*Sources for external benchmarks: [Baymard — phone field](https://baymard.com/blog/explain-phone-number-field), [Baymard cart-abandonment stats via ContentSquare](https://contentsquare.com/guides/cart-abandonment/stats/), [Statista — US checkout abandonment reasons](https://www.statista.com/statistics/1228452/reasons-for-abandonments-during-checkout-united-states/), [checkout abandonment statistics roundup](https://www.amraandelma.com/checkout-abandonment-statistics/). Store data: Shopify Admin API + ShopifyQL, pulled 6 Aug 2026.*
