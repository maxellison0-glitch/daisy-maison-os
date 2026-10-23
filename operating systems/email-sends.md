# Email sends log

One row per Shopify Email campaign. The morning digest uses this file to
work out each send's real cost (see the EMAIL rule in
`daisy-morning-digest-prompt.md`). Fill in **Billed** when the Shopify
bill line is known; it overrides the calculated figure.

**HOW RECIPIENTS ARE KNOWN (Max, 17–19 Oct 2026): Claude, not Max.** Claude
picks the Shopify segment for every send and logs it here (Segment column)
before or on send day. The digest then counts that segment's members itself
and writes the number into Recipients. Never ask Max for a "Sent" number.
Count method (tested 19 Oct 2026): Admin GraphQL mutation
`customerSegmentMembersQueryCreate(input: {segmentId: "<gid>"})`, then query
`customerSegmentMembersQuery(id: "<returned id>") { done currentCount }` until
`done: true`. (The synchronous `customerSegmentMembers(query: ...)` form
rejects `shopify_email.opened MATCHES` segments, so use the segment ID.)
Counts are taken after the send, so mark them "≈ segment count <date>".
No segment logged = full subscribed list as the upper bound, marked ESTIMATE.

Segment IDs:
- DM Email – Engaged (opened 30d): gid://shopify/Segment/1186234859859 (18,116 on 19 Oct 2026)
- DM Email – Customers (ordered 12m): gid://shopify/Segment/1186234892627
- DM Email – Christmas 2025 buyers: gid://shopify/Segment/1186234925395
- DM Email – Engaged, never bought: gid://shopify/Segment/1186234958163
- DM Email – Quiet (no open 90d): gid://shopify/Segment/1186234990931
- Email subscribers (full list): gid://shopify/Segment/1072653762899

Billing: 10,000 free emails per calendar month, then USD 1 per 1,000
(USD 0.65 per 1,000 past 300,000). Abandoned-checkout emails are free.

| Send date | Campaign | Recipients | Billed cycle | Cost | Source |
|---|---|---|---|---|---|
| 2026-10-02 17:30 | We just made the perfect gift! | not visible via API | 7 Sep–7 Oct bill | share of £8.95 | Shopify bill 7 Oct (Gmail) |
| 2026-10-05 18:00 | For the one who always hosts Christmas | not visible via API | 7 Sep–7 Oct bill | share of £8.95 | Shopify bill 7 Oct (Gmail) |
| 2026-10-05 18:00 | For the friend you don't see enough | not visible via API | 7 Sep–7 Oct bill | share of £8.95 | Shopify bill 7 Oct (Gmail) |
| 2026-10-07 19:00 | Our pebble pictures just got a glow up ✨ | not visible via API | 7 Oct–7 Nov bill | unknown until 7 Nov bill | Max said ~£38 (estimate) |
| 2026-10-09 19:48 | Well, these have been popular this week! 👀 | not recorded | 7 Oct–7 Nov bill | £37.80 ESTIMATE (upper bound) | digest 10 Oct |
| 2026-10-13 19:00 (planned) | Their first Christmas, in pebbles | DM Email – Engaged (opened 30d) + Customers (12m), ~19,000 | 7 Oct–7 Nov bill | ≤ USD 19 est. | build sheet in email kit; segment as planned, not confirmed |
| 2026-10-15 19:30 | NEW! A launch-day treat for just you 🎁 | segment not logged → full list upper bound | 7 Oct–7 Nov bill | £37.36 ESTIMATE (upper bound) | digest 16 Oct |
| 2026-10-17 10:36 | Free delivery this weekend 🚚 | DM Email – Engaged (opened 30d), ≈ 18,116 (segment count 19 Oct) | 7 Oct–7 Nov bill | ≈ USD 18.12 ≈ £13.29 est. | segment chosen by Claude in chat 17 Oct; Max confirmed sent |
| 2026-10-18 18:00 | Free delivery ends midnight! 🎁 | segment not logged → full list upper bound | 7 Oct–7 Nov bill | £37.15 ESTIMATE (upper bound) | digest 19 Oct |
| 2026-10-21 19:00 | Their name on the front door this Christmas 🎄 | DM Email – Customers (ordered 12m), ≈ 1,748 (segment count 2026-10-22). CORRECTION 2026-10-22: Shopify shows **10,610 sent** (Max). The segment count was wrong for this send; the send went wider than the build-sheet segment. Max built it with his own prompt and new pebble items, not from the build sheet; the segments it went to aren't visible via API (Engaged = 18,060 and Customers = 1,748 on 22 Oct; neither matches 10,610) | 7 Oct–7 Nov bill | ~~≈ USD 1.75 ≈ £1.28 est.~~ ≈ USD 10.61 ≈ £7.78 est. | build sheet email-builds/2026-10-20-christmas-street-signs.md; sent per marketingEvents 21 Oct 18:00 UTC |
| 2026-10-22 18:30 | New from the workshop: six pebble designs ✨ | segment not logged → full list upper bound, Email subscribers ≈ 50,466 (segment count 2026-10-23) | 7 Oct–7 Nov bill | ≈ USD 50.47 ≈ £37.01 ESTIMATE (upper bound) | found in Shopify marketingEvents by digest 23 Oct; not in this log or a build sheet beforehand |
| 2026-10-24 19:00 (planned, moved from Thu 22 Oct so it doesn't hit the same people two nights running) | The gift 400+ couples chose this month 💍 (replaced "Your family, in pebbles, for Christmas" on 22 Oct, Max) | DM Email – Engaged (opened 30d), ≈ 18,116 (segment count 19 Oct) | 7 Oct–7 Nov bill | ≈ USD 18 ≈ £13 est. | approved by Max 20 Oct (A2); build sheet email-builds/2026-10-22-couples-bestsellers.md |

**Billing evidence (checked 8 Oct 2026):** Shopify bills arrive from
billing@shopify.com on the 7th, in GBP, with a "Messaging" line. 7 Sep bill:
Messaging £0.00. 7 Oct bill (cycle 7 Sep–7 Oct): Messaging **£8.95** for the
three sends above, about £2.98 a send on average (estimate, equal split). That's
far below £38, so either the sends went to segments well under the full list,
or most of them used the 10,000 free emails. Shopify's API shows each send
(marketingEvents) but not how many people it went to.

**Gmail is not to be used for this (Max, 8 Oct 2026).** The figures above were
read once from Gmail before that instruction; the digest must not repeat it.

**How the digest costs a send:** use the Messaging line on the bill that covers
it (when Max provides it), split across that cycle's sends in proportion to recipients if known,
otherwise equally (mark as estimate). Until that bill arrives, use the last
cycle's average cost per send, marked as an estimate.

Subscribed list size, 8 Oct 2026: 51,545 email subscribers (Shopify Admin
API, customer segment `email_subscription_status = 'SUBSCRIBED'`; total
customers incl. unsubscribed is 97,522). A full-list send with no free
allowance left = 51,545 × USD 1 / 1,000 = USD 51.55, which fits Max's ~£38.
CORRECTION 8 Oct 2026: this line first said 97,522 subscribers. That was
all customers, because the `customersCount` filter was silently ignored.
