# Daisy Maison — Email Programme

*Built 6 Aug 2026. Six coded emails + master template, ready to paste into Shopify Email.
Nothing here is live — per house rules, nothing sends without Max's explicit go.*

---

## The idea that carries the whole programme

**The wording is the product** (`.claude/product-marketing.md`). So the signature
block of every email is a street sign rendered in pure HTML — white plaque, black
border, Fraunces type — and in the welcome email the sign says **the subscriber's
own first name** via Liquid. Their name, on their product, in their inbox, before
they've bought anything.

Psychology (from `marketing-psychology` skill): **endowment effect** (it already
feels like theirs), **IKEA effect** (personalisation = co-creation), and the
**Zeigarnik open loop** (a sign with your name on it that you don't own yet is an
unfinished task). No stock imagery required, crisp at any screen size, and it
*is* the brand — not decoration around it.

## Design system

| Token | Value | Source |
|---|---|---|
| Display font | Fraunces 600 (Apple Mail loads it; Georgia fallback everywhere else) | product-marketing.md |
| Ink | `#4A3A2C` | product-marketing.md |
| Ground | `#FAF6EE` | product-marketing.md |
| Muted / rules | `#8A7A68` / `#E8E0D0` | derived from ink+ground |
| Layout | 600px single column, one CTA per email, generous whitespace | premium email doctrine |

Voice: warm, dry, understated, never shouty. British spelling. No fake urgency —
the welcome nudge literally says *"We don't do fake countdown timers."* (That line
is doing psychological work: **pratfall/honesty signalling** builds the trust that
makes the *genuine* deadline — "your occasion has a date" — land harder.)

## The six emails

| # | File | Trigger | Sign reads | Psychology at work |
|---|---|---|---|---|
| 1 | `01-welcome-1-the-sign` | Signup, immediate | **{FIRSTNAME} LANE** | Endowment, reciprocity (code delivered), unity (family workshop story) |
| 2 | `02-welcome-2-occasions` | +2 days | IT'S THE THOUGHT | Social proof (9,000+ Mr & Mrs sold — verified), mimetic desire, occasion framing |
| 3 | `03-welcome-3-code-nudge` | +4 days | STILL 20% OFF | Commitment/consistency, honest urgency (occasion date, not timer), loss aversion (soft) |
| 4 | `04-abandoned-1-nearly-yours` | 1h after abandon | NEARLY YOURS | Zeigarnik (open loop), endowment ("your basket"), activation energy ("ten-second job") |
| 5 | `05-abandoned-2-fair-questions` | 24h after abandon | FAIR QUESTIONS | Objection pre-emption (the 3 documented objections), pratfall honesty, authority (workshop) |
| 6 | `06-occasion-one-year-down` | 11 months after wedding/anniversary purchase | ONE YEAR DOWN | Peak-end revival, availability heuristic, humour = brand liking |

Subjects/preheaders are in each file's hidden preheader div; suggested subjects:

1. *Your name looks good on this*
2. *Buying for an occasion? So is everyone.*
3. *Your 20% is still sitting here*
4. *You left this behind*
5. *Honest answers, in case you were wondering*
6. *It's nearly been a year*

**Deliberate discount discipline:** the abandoned flow contains **no discount**.
Cutting price on email one trains abandonment (second-order thinking / cobra
effect). If recovery underperforms after 4 weeks of data, test a code in email
2 only.

## What's verified vs. approximated

- Prices (£11.25 / £22.95), product images and handles: pulled live from Shopify 6 Aug 2026.
- "More than 9,000 times" for Mr & Mrs sign: verified ~9,270 units (Shopify, 28 Jul 2026) — understated deliberately.
- Sage accent `#7D8B6F` appears nowhere yet (emails use ink+ground only); if adding it, verify against the roundel asset first.
- **No invented reviews, metrics, delivery promises or countdowns anywhere.** House rule.

## Max's 20 minutes (the parts the API can't touch)

1. **Sender domain**: Settings → Notifications → Sender email → authenticate
   `daisymaison.co.uk` (add the SPF/DKIM DNS records Shopify shows). Do this
   first; it's what keeps us out of spam.
2. **Paste templates**: Marketing → Create campaign → Shopify Email → pick any
   template → switch to code view → replace with each file's contents.
3. **Automations**: Marketing → Automations → turn on *Welcome new subscriber*
   (3-email series, timings above) and *Abandoned checkout* (1h + 24h), choosing
   the pasted templates.
   ⚠️ In both abandoned emails, replace the `https://daisymaison.co.uk/cart`
   button link with the editor's **"Complete your checkout"** dynamic link so it
   deep-links to the customer's actual basket.
4. **Approve sends**: nothing goes out without your go, ever. That includes these.

## Segments (`segments.md`) and calendar (`calendar.md`)

The occasion-reminder flow needs buyer tagging — the Flow recipe and paste-ready
segment queries are in `segments.md`. The 12-month send calendar keyed to UK
gifting occasions (including the Christmas last-order-date sequence, the year's
single most valuable send) is in `calendar.md`.

## Measurement

North star: **email revenue as % of total revenue** — target 20–30% within 6
months (gift e-commerce norm; currently ~0%). Per send: revenue per recipient,
then open/click. Review in the morning digest weekly. If flows aren't at 10% of
revenue after 8 weeks, the welcome timing/subjects get iterated first — they're
the highest-volume flow.
