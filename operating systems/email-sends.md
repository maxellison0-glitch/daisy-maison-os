# Email sends log

One row per Shopify Email campaign. The morning digest uses this file to
work out each send's real cost (see the EMAIL rule in
`daisy-morning-digest-prompt.md`). Fill in **Recipients** from Shopify →
Marketing → the campaign's "Sent" number. Fill in **Billed** when the Shopify
bill line is known; it overrides the calculated figure.

Billing: 10,000 free emails per calendar month, then USD 1 per 1,000
(USD 0.65 per 1,000 past 300,000). Abandoned-checkout emails are free.

| Send date | Campaign (utm_campaign) | Recipients | Free left before send | Calculated cost | Billed | Source |
|---|---|---|---|---|---|---|
| 2026-10-07 | Our pebble pictures just got a glow up ✨_221538943315 | not yet known | not yet known | — | ~£38 (Max, estimate) | Max, 8 Oct 2026 |

Subscribed list size, 8 Oct 2026: 51,545 email subscribers (Shopify Admin
API, customer segment `email_subscription_status = 'SUBSCRIBED'`; total
customers incl. unsubscribed is 97,522). A full-list send with no free
allowance left = 51,545 × USD 1 / 1,000 = USD 51.55, which fits Max's ~£38.
CORRECTION 8 Oct 2026: this line first said 97,522 subscribers. That was
all customers, because the `customersCount` filter was silently ignored.
