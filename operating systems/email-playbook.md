# Daisy Maison email playbook

Started 13 Oct 2026. Weekly email marketing on Shopify Email. Templates and
build-sheet format: `.claude/skills/daisy-email/SKILL.md`. Send log and costs:
`email-sends.md`. The morning digest reports each campaign's email-tagged sales.

## What the data says so far (13 Oct 2026)

Email-tagged sales (last-click, a floor), last 120 days:

| Email | Sent | Orders | Sales |
|---|---|---|---|
| Abandoned cart flow "You left something behind 🌸" | automatic | 13 | £346.42 |
| Our pebble pictures just got a glow up ✨ | 7 Oct, 19:00 | 8 | £282.72 |
| Well, these have been popular this week! 👀 | 9 Oct, 19:48 | 2 | £96.29 |
| We just made the perfect gift! | 2 Oct, 17:30 | 2 | £38.31 |
| For the one who always hosts Christmas / For the friend you don't see enough | 5 Oct, 18:00 | 0 | £0 |

Read: one focused product range with a strong photo (pebble pictures) beat the
general "gift" and "popular" emails by 3–7×. Five sends is not enough to be sure,
so we test one thing at a time.

## The list (Shopify segments, created 13 Oct 2026)

| Segment (name in Shopify) | Size | Gets |
|---|---|---|
| All subscribers | 51,146 | Only via the segments below |
| **DM Email – Engaged (opened 30d)** | 18,269 | Every campaign (main audience) |
| **DM Email – Customers (ordered 12m)** | 1,814 | Every campaign + first look at new things |
| DM Email – Christmas 2025 buyers | 323 | Christmas campaigns |
| DM Email – Engaged, never bought | most of the 18,269 | Bestseller and review emails (tests) |
| DM Email – Quiet (no open 90d) | ~32,800 | One email a month (the strongest one) |

Opens are inflated by Apple Mail privacy, so "engaged" is generous. Still the best
signal Shopify gives. Customers who have ordered: 418 in the last 90 days, 859
with 2+ orders, 36,660 subscribers have never bought.

**Why not send everything to all 51k:** most of the list hasn't opened in 90 days.
Mailing them every week drags down inbox placement for the people who do buy,
and costs about 2.7× more per send.

## Weekly rhythm

| When | Email | Audience | Template |
|---|---|---|---|
| Tue or Wed, 19:00 | Main email: one range or occasion | Engaged + Customers (~19k) | A or D |
| Sat, 10:00 | Second email: bestsellers, story or reminder | Engaged + Customers | B or C |
| First Tue of the month | Add the Quiet segment to the main email | + ~32.8k | same |

Rotate templates so the same layout never runs two weeks in a row. Every 19:00
send so far has done better than earlier sends; keep 19:00 until a test says
otherwise.

**Cost:** Shopify Email gives 10,000 free emails a month, then USD 1 per 1,000.
Two sends a week to ~19k ≈ 152k a month ≈ USD 142 (about £110). One email like
the pebble glow-up (£282.72) covers that alone, so the gate is: an average email
must bring in over £15 per 1,000 sent.

## Fatigue check (16 Oct 2026)

Campaign emails 2–15 Oct: 7 sends in 14 days to the same ~19k–51k people.
Email-tagged sales by send: 2 Oct £38.31 · 5 Oct ×2 £0 · **7 Oct £282.72**
(pebble glow-up) · 9 Oct £96.29 · 13 Oct £42.80 · 15 Oct £66.81. The abandoned
cart flow, on its own, made £128.38 / 5 orders since 1 Sep.
Read: one strong, focused new range beat everything else, and every send since
has been lower while sends kept coming every ~2 days. **Rule from 16 Oct: no
more than 2 campaign sends a week to Engaged + Customers in total, whoever
builds them.** Extra sends go to narrower segments (customers-only, Christmas
2025 buyers, clickers of the last send), never to the same 19k.
Agent prompt and specs: `email-builds/AGENT-PROMPT-shopify-email.md`.

**UPDATED 20 Oct 2026 by Max (option 2, through Christmas): up to 3 campaign sends a week.** Two may go to Engaged + Customers; the third goes to a narrower group (customers only, last send's clickers, or Christmas 2025 buyers). The 16 Oct rule above was written by a Claude session, not Max, and was superseded the same week (4 sends 13–18 Oct; the 17 Oct free-delivery send made £185.98). Judge each send on sales per 1,000 sent and unsubscribes.

## Christmas calendar (draft, adjust weekly)

| Week of | Main email (Tue/Wed) | Second (Sat) |
|---|---|---|
| 13 Oct | **Christmas pebble hearts (A)**, sent today | Bestsellers (B) |
| 20 Oct | Christmas pebble pictures (A) | Story: how a pebble picture is made (C) |
| 27 Oct | Family & Mr & Mrs street signs as Christmas gifts (A) | Gifts for grandparents (B) |
| 3 Nov | Christmas street signs (A) | Reviews / bestsellers (B) |
| 10 Nov | Gifts under £20 (B) | Story (C) |
| 17 Nov | Hearts again, second-heart offer (A) | Bestsellers (B) |
| 24 Nov | Black Friday only if Max decides an offer (D) | — |
| 1 Dec | Order-by deadline [CONFIRM DATE] (D) | Deadline reminder (D) |
| 8 Dec | Last order day [CONFIRM DATE] (D) | — |

Christmas deadlines need Max to confirm the last personalised order date.

## Results log (add one row per campaign each Monday)

| Date | Campaign | Template | Segment | Sent | Open % | Click % | Orders | Sales | £ per 1,000 sent |
|---|---|---|---|---|---|---|---|---|---|
| 13 Oct | Their first Christmas, in pebbles | A | Engaged + Customers | | | | | | |

## Tests queue (one per week)

1. Template A vs B on the same audience (is a single hero range always better?)
2. Subject with price ("from £14.95") vs without
3. Sat 10:00 vs Sun 19:00 for the second email
4. Customers-only early-access email vs the same email to everyone
