# Product Marketing Context — Daisy Maison

**Every marketing skill in `.claude/skills/` opens by looking for this file.**
Ten of them name it explicitly. Until 28 Jul 2026 it did not exist, so each one
started from zero and asked Max questions the repo could already answer.

Written 28 July 2026 from live sources, not memory: Shopify Admin API for the
catalogue and prices, `digests/digest_2026-07-27.md` for performance,
`projects/daisy-street-sign/production/product-rules.json` for colourways.

**Rule for maintaining it:** every number here is dated and sourced. If you
cannot source a claim, do not add it — add it to *Known Gaps* instead. A
confident invented number in this file becomes a confident invented number in an
advert.

---

## Product Overview

Daisy Maison is a **UK family business selling personalised gifts**,
manufactured in-house. Shopify store, `daisymaison.co.uk`, GBP, UK-based.

It is **not a one-product company**, which is the most common mistake made when
reasoning about it:

| Line | Price from | Notes |
|---|---:|---|
| **Personalised street signs** | **£11.25** | The flagship. Laser-cut, made to order, any wording. |
| Pebble hanging hearts / decorations | £14.95–£15.95 | A large second line — anniversary, birthday, new home, Christmas, friendship, Mum |
| Gift boxes | £3.95–£4.95 | Small and large, sentiment artwork |
| Add-ons / upgrades | £3.00–£10.95 | Size upgrades, large heart, bundle offers |

The street sign is the volume driver. Its Shopify variant carries roughly
**9,270 units sold** against the Mr & Mrs listing alone.

### The single most useful commercial fact

**The lead product is £11.25 but the average order is about £29.**

Computed from four consecutive completed days in `digest_2026-07-27.md`:

| Date | Total sales | Orders | AOV |
|---|---:|---:|---:|
| 22 Jul | £1,646.79 | 58 | £28.39 |
| 23 Jul | £1,686.06 | 56 | £30.11 |
| 24 Jul | £1,523.28 | 55 | £27.70 |
| 25 Jul | £1,482.98 | 48 | £30.90 |

So customers routinely buy **more than one sign, or a sign plus upgrades**. The
low headline price is the hook; the basket is nearly 3× it.

**Consequences for advertising:** never optimise as if the order is worth
£11.25, never write copy that makes a single sign feel like the whole purchase,
and treat multi-buy and upgrade paths as the actual product.

### The physical product

Thin rigid sheet, shaped ends, printed front with a black perimeter border,
**plain white reverse**, mounting holes. It is *not* a thick slab and the back
is *not* black — verified against real footage in
`Content Pipeline/Creative Studio/active/DM-C017-synthetic-sign-turn/.../REFERENCE_PACK.md`.

**Eight colourways, and never hard-code them.** The laser reads
`projects/daisy-street-sign/production/product-rules.json` and so must anything
else, through `Content Pipeline/templates/sign-reprint/colourways.py`. A second
copy of the list has already been wrong once, on both names and hexes.

---

## Target Audience

UK gift buyers. Evidenced by what actually sells and what campaigns exist:

- **Weddings and anniversaries** — the current paid focus; `[RDD] TOF - WEDDING`
  is the live Meta campaign, and "wedding gifts for bride and groom" is a new
  converting search term
- **Couples and new homes** — Mr & Mrs, "our home"
- **Parents and family** — Mum, family Christmas, birthdays
- **Seasonal/occupational gifting** — the teacher category ran and closed in
  July 2026; Christmas lines exist in the catalogue year-round

Buying occasion is the segment, not demographics. The category is
**considered-purchase gifting**: people buy for a date, which is why conversion
lag is real and why categories taper and end.

---

## Problems & Pain Points

The customer is not solving a functional problem. They are solving a social one:
*I want to give something that looks like I thought about it, without spending a
lot or leaving it too late.*

Personalisation is the whole value. A named sign cannot be bought anywhere else
by definition, which is why the wording — not the object — is the product.

---

## Competitive Landscape

**Known Gap.** TreatBox is the one competitor the repo names and monitors.
`competitor-profiling` and `daisy-social-analytics` can build the rest; nobody
has. Do not assert a competitive position beyond TreatBox without doing it.

Structurally the pressure is Etsy and NOTHS sellers — Daisy Maison's own listing
copy carries `#etsyuk` and `#noths` hashtags — plus the wider UK
personalised-gift market.

---

## Differentiation

1. **Made in-house.** Not a dropshipper or a print broker — there is a laser and
   an audited artwork pipeline (`projects/daisy-street-sign/`). Real
   manufacturing photographs exist and are the strongest asset the brand owns.
2. **Any wording at all.** The generative constraint is nearly zero, which is
   what makes comment-to-sign and reply-with-a-sign possible at no cost.
3. **Price against a gift that looks expensive.** £11.25 entry into a category
   where a personalised gift usually reads as £25+.

---

## Objections

- "Will it look cheap?" — the honest answer is the manufacturing footage
- "Will it arrive in time?" — considered-purchase gifting is deadline-driven
- "Will the personalisation be spelled right?" — mitigated by showing real orders

**Known Gap.** These are inferred from the category and the catalogue, not from
customer research or support tickets. Run `customer-research` against real
reviews and emails before quoting them as fact.

---

## Customer Language

The account's single best-performing post ever was a real sign reading
**"YOU'RE NOT WELCOME (UNLESS YOU'VE BROUGHT SNACKS)"**, captioned *"Customer of
the year, probably."* — 11,889 views, roughly 5× anything else.

That is the register the audience rewards: **dry, British, self-deprecating,
slightly rude**. Not sentimental, not salesy. The product is funny because a real
person ordered it and meant it.

`Content Pipeline/PUBLISH_LOG.md` is meant to capture exact audience phrasing
from comments so it can become the next batch of hooks. Use it.

---

## Brand Voice

Warm, dry, understated, never shouty. British spelling throughout —
*personalised*, not *personalized*.

Visual identity, used across every rendered asset:

| | |
|---|---|
| Font | Fraunces 600 |
| Ink | `#4A3A2C` |
| Ground / pill | `#FAF6EE` |
| Mark | Circular sage roundel, "DAISY MAISON · HOME OF PERSONALISED GIFTS", DM monogram |
| Strapline | Personalised street signs |

---

## Proof Points

Use only these. They are verified.

- ~9,270 units sold on the Mr & Mrs street sign listing (Shopify, 28 Jul 2026)
- One reel at 11,889 views (Instagram, 8 Oct 2025)
- Made in-house in the UK
- Instagram followers 23,535 (28 Jul 2026) — but see the warning below

**Never state a price, delivery time, review count or result that has not been
checked against Shopify or a live pull on the day.** Prices move; this file will
go stale.

---

## Goals & Current State (28 July 2026)

### Paid is the business; organic is not — yet

| | |
|---|---:|
| Daily ad spend (27 Jul) | **£735.05** (Google £431.40, Facebook £303.65) |
| ROAS | **2.46x** — below the 3x floor, **fourth red day running** |
| Site CVR | 4.06% |
| Checkout abandonment | 29.4% |
| Cart-add rate | 8.5%, down from 11.8% |

Traffic on 27 Jul: Search 40.2% (475, all Google), Social 38.0% (449 — Facebook
429, **Instagram 20**), Direct 20.5% (242).

**Read those two Instagram numbers together: 23,535 followers producing 20
sessions.** The organic Instagram audience is dormant — mean likes fell from 86
before a 233-day posting gap to 2.6 after it. Facebook traffic is almost
entirely *paid*.

So: **money is made on paid; organic social is a repair job in progress**, and
TikTok is the chosen way back in because it is an interest graph rather than a
follower graph. See `Content Pipeline/DISTRIBUTION_PLAN.md`.

### Where the leverage is, in order

1. **Paid efficiency.** £735/day at 2.46x against a 3x floor is the largest
   number in the business. One point of ROAS dwarfs anything organic can do this
   quarter. → `daisy-paid-media`, then `ads`.
2. **Ad creative.** Creative is the main lever left inside paid — see
   `ad-creative`, and note the brand already has proof that dry humour and real
   manufacturing footage outperform polish.
3. **Organic rebuild.** Cadence, cheaply. → `social`, `DISTRIBUTION_PLAN.md`.

---

## Hard Constraints — these are not preferences

- **Max does not film. Ever.** No new footage, no presenter to camera. Every
  moving asset is generated, rendered from HTML, or cut from footage already
  owned.
- **Organic social posts: autonomous.** The social posting routine generates
  and publishes directly — no approval step, no briefs, no PRs. Just post.
- **Paid media: propose only.** No paid credit spend without Max's explicit go.
- **No customer PII in published assets.** A real surname *as sign wording* is
  the product and is fine. An invoice, address, order number, contact detail or
  a real customer's face is never fine, and a real customer's face never goes
  into a generator.
- **Never invent a metric, result, competitor post, price or delivery time.**
  Name the gap instead. This has been the single most valuable house rule.
- **Never touch `projects/daisy-street-sign/production/` or `source/`.** That is
  the laser and print path; changing it changes what ships to a customer.

---

## Known Gaps

Things a skill might reasonably want that genuinely are not established. Do not
fill these from imagination.

- **Competitors beyond TreatBox** — never profiled
- **Objections** — inferred from category, not from customer research
- **Target CPA** — the digests reason in ROAS; no CPA target is written down,
  and CPA is the number ROAS does not tell you
- **Margin per unit** — so "is 3x actually the right floor?" cannot be answered
  from this repo
- **Email and SMS** — one email session in a day's traffic; no programme evident
- **Per-video TikTok analytics** — the endpoint needs a signed request
