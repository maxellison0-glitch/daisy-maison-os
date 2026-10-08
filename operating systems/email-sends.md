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

Subscribed list size, 8 Oct 2026: 97,522 (Shopify Admin API). A full-list send
with no free allowance left = 97,522 × USD 1 / 1,000 = USD 97.52.
