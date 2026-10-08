# Email sends log

One row per Shopify Email campaign. The morning digest uses this file to
work out each send's real cost (see the EMAIL rule in
`daisy-morning-digest-prompt.md`). Fill in **Recipients** from Shopify →
Marketing → the campaign's "Sent" number. Fill in **Billed** when the Shopify
bill line is known; it overrides the calculated figure.

Billing: 10,000 free emails per calendar month, then USD 1 per 1,000
(USD 0.65 per 1,000 past 300,000). Abandoned-checkout emails are free.

| Send date | Campaign | Recipients | Billed cycle | Cost | Source |
|---|---|---|---|---|---|
| 2026-10-02 17:30 | We just made the perfect gift! | not visible via API | 7 Sep–7 Oct bill | share of £8.95 | Shopify bill 7 Oct (Gmail) |
| 2026-10-05 18:00 | For the one who always hosts Christmas | not visible via API | 7 Sep–7 Oct bill | share of £8.95 | Shopify bill 7 Oct (Gmail) |
| 2026-10-05 18:00 | For the friend you don't see enough | not visible via API | 7 Sep–7 Oct bill | share of £8.95 | Shopify bill 7 Oct (Gmail) |
| 2026-10-07 19:00 | Our pebble pictures just got a glow up ✨ | not visible via API | 7 Oct–7 Nov bill | unknown until 7 Nov bill | Max said ~£38 (estimate) |

**Billing evidence (checked 8 Oct 2026):** Shopify bills arrive from
billing@shopify.com on the 7th, in GBP, with a "Messaging" line. 7 Sep bill:
Messaging £0.00. 7 Oct bill (cycle 7 Sep–7 Oct): Messaging **£8.95** for the
three sends above, about £2.98 a send on average (estimate, equal split). That's
far below £38, so either the sends went to segments well under the full list,
or most of them used the 10,000 free emails. Shopify's API shows each send
(marketingEvents) but not how many people it went to.

**How the digest costs a send:** use the Messaging line on the bill that covers
it, split across that cycle's sends in proportion to recipients if known,
otherwise equally (mark as estimate). Until that bill arrives, use the last
cycle's average cost per send, marked as an estimate.

Subscribed list size, 8 Oct 2026: 51,545 email subscribers (Shopify Admin
API, customer segment `email_subscription_status = 'SUBSCRIBED'`; total
customers incl. unsubscribed is 97,522). A full-list send with no free
allowance left = 51,545 × USD 1 / 1,000 = USD 51.55, which fits Max's ~£38.
CORRECTION 8 Oct 2026: this line first said 97,522 subscribers. That was
all customers, because the `customersCount` filter was silently ignored.
