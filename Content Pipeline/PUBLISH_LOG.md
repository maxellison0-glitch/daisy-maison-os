# Publish and Learning Log

**One row per platform per post.** A post that went to both Instagram and
TikTok gets two rows. This makes a missing or duplicate publish obvious at a
glance, which is the entire job of this file.

**Rebuilt 29 Jul 2026.** The previous version had five separate entries mashed
onto a single line with `||` separators, and logged Bond twice with two
different result figures. Nothing was lost in the rebuild — the content of
every old row is preserved below, in `LESSONS.md` where it was a lesson rather
than a record.

## How to fill it in

- **Source** is not optional. `measured` (pulled from an API), `reported`
  (Max said so — no URL or number captured), or `not captured`.
- Never write a number from memory. On 28 Jul three weeks of strategy rested
  on a remembered figure that turned out to be 7 likes.
- A row goes in **when the post goes out**, not when we get round to it.

---

## TikTok — @daisymaison

Views measured **30 Jul 2026** at `--limit 20` via
`tools/social_api/tiktok_posts.py`, snapshot at
`tools/social_api/tiktok-post-snapshots/daisymaison-2026-07-30.json`.
Account: **184 followers, 168 videos.**

**MEDIAN OF ALL 19 POSTS: 478 VIEWS.** Not 262. The 262 figure quoted on 29 Jul
came off a 12-post window and was an artefact of the truncation - every
falsifiable call written against "beat 262" was calibrated on a sample that cut
off above 3,422. Corrected here rather than quietly.

| Views | Content ID | Post |
|---:|---|---|
| **9,400** | - | "When a customer order lines up too perfectly with Sabrina's..." |
| **6,500** | - | "Autumn in a matchbox the sweetest little surprise..." |
| **4,574** | - | "Parenting tip #1: Lower your standards" |
| 3,422 | - | "You know it's nearly Christmas when these start flying out" |
| 1,507 | - | "Okay fine... maybe I'm not a wizard. But my house is" |
| 1,115 | - | "Tell me this doesn't feel like autumn in a box" |
| 897 | - | "real customer order btw (can't even be mad tho)" |
| 799 | - | "We didn't realise these surnames actually existed..." |
| 532 | - | "POV: Planning feels easier when you start with the board." |
| 478 | - | "The calm before the Christmas chaos" |
| 455 | - | "Experience 5 years, skill level Day 1" |
| 403 | - | "Do you guys think this was intentional or not..." |
| 262 | DM-CAT-HOUSE | "Cat owner can relate to this" |
| 244 | DM-HOUSE-QUIZ | "Which one's your house? Comment your number" - 27 Jul |
| 244 | DM-C017-JANNAWAY | "Nobody ever guesses" (PILL cut) - 28 Jul |
| 237 | DM-DIFFUSER-TEASE | "Not on the site yet - this one goes live this week" - 27 Jul |
| 229 | - | "The gown goes back. This doesn't." - 28 Jul |
| **7** | - | "Drop your wording in the comments and we'll make it" - 28 Jul |
| **5** | DM-C020-CORRECTION | "Dave ordered the sign. Someone else ordered the correction." - 29 Jul |

**What the full ladder says that the truncated one hid.** The top three are
9,400 / 6,500 / 4,574 - nearly 3x the figure we thought was our ceiling. All
three are third-party: a real customer order colliding with a trending song, an
autumn seasonal, and a parenting joke. **Not one of the top three is an advert
for a sign.** Two of the top six are autumn/seasonal, which partly rehabilitates
the seasonal lane that looked like a one-post fluke at 3,422.

**And every single thing this system has published sits in the bottom seven:**
229, 237, 244, 244, 262, 7, 5. The best pre-system post did 9,400. That is the
finding, and it is not a hook problem - it is the same account.

**The Correction did 5 views**, the worst post on the account, below the 7-view
live commission. It went out 29 Jul and was missing from this log until the
reconciler was fixed to actually re-pull instead of reading yesterday's cache.

Post dates are blank where the reader returns no timestamp. Not guessed - and
the `--days` window therefore cannot filter TikTok, which is why older inventory
appears here rather than being excluded.

---

## Instagram — @daisymaison

Likes measured 28 Jul 2026 via `tools/social_api/ig_public.py`, snapshot at
`tools/social_api/ig-snapshots/daisymaison-2026-07-28.json`.
Account at that read: **23,535 followers.** Instagram does not return view
counts on recent posts, so reach cannot be separated from seen-and-ignored.

| Date | Content ID | Post | Result | Source | URL |
|---|---|---|---|---|---|
| 29 Jul | DM-C020-CORRECTION | "Dave's Bar" / "It's a shed, Dave" | pending | **reported** — Max posted from his phone | not captured |
| 29 Jul | DM-HOUSE-QUIZ | 5-slide house carousel | pending | **reported** — Max | not captured |
| 27 Jul | DM-DIFFUSER-TEASE | "Not launched yet — this one goes live later this week" | **4 likes, 1 comment** | measured | [DbSiVvdDV4r](https://www.instagram.com/p/DbSiVvdDV4r/) |
| 26 Jul | DM-CAT-HOUSE | "POV: you thought it was your house" | **6 likes** | measured | [DbQPrf7Nyv9](https://www.instagram.com/p/DbQPrf7Nyv9/) |
| 25 Jul | DM-C018-BOND | "Some jobs call for a tuxedo" | **7 likes, 0 comments** | measured | [DbNj6tzt2Ff](https://www.instagram.com/p/DbNj6tzt2Ff/) |
| Oct 2025 | — | Pinned reel | **11,889 views** | measured | [DPjdseCDbDR](https://www.instagram.com/p/DPjdseCDbDR/) |

**The URL column is what makes this self-maintaining.** `reconcile_log.py`
joins on the Instagram shortcode, so a row without a URL is a row the
reconciler cannot match and will keep re-reporting as missing. The three URLs
above were recovered by the reconciler itself on 30 Jul — they were never
captured at post time because Max posts from his phone, and that is exactly the
problem the tool exists to solve.

**The shape of the problem, in one place:** 7 / 6 / 4 likes against 23,535
followers is about **0.03%**, against a healthy band of 1–3%. May and June sit
at 0–2, so the decay predates every creative decision we have made. The pinned
October reel holds 11,889 views — distribution exists and is simply not being
granted now.

---

## Built and queued — not out yet

Added 30 Jul 2026. A post that is built but unposted was previously invisible in
this file, which is how the Correction went missing for a day. It sits here until
it goes out, then it moves up into a platform section with a real number.

| Content ID | Shape | Planned route | Built |
|---|---|---|---|
| DM-C020-POST-1 | 3-slide 4:5 carousel — THE SUTTONS / THE MERCERS / THE WILSONS | Instagram carousel + TikTok photo carousel | 30 Jul, 0 credits |
| DM-C020-POST-2 | 2-slide 4:5 carousel — THE GARDEN TAVERN / DAD'S BAR, plus a silent 5.2s 9:16 cut | Instagram **trial reel** (needs the video, a carousel cannot be a trial reel) + TikTok | 30 Jul, 4 credits of generation, 0 to build |

Both are photo posts of Alan holding a sign at a diagonal in the office, one room
per slide, five different rooms across the two posts. That satisfies the frame
diversity gate in `PUBLISH_READINESS.md` **between the slides** but not between
the two posts — they share subject count, camera height and format. Post 2 should
not follow post 1 on the same platform on the same day.

## Not posted, and why

| Content ID | Status |
|---|---|
| DM-C019-SUMMER-HOLIDAYS | **KILLED 29 Jul.** Max killed the concept on merit 28 Jul. The burnt-in "DAY 4 OF 42" is also wrong — England/Wales broke up 20–23 Jul, so 29 Jul is day 7–10; "DAY 4" needs a Sunday 26 Jul start no UK nation has. Number is inside the generated sign face, so uncorrectable without regeneration. |
| DM-SUMMER-COUNTDOWN | **KILLED 29 Jul.** Weaker letterboxed cut of the same dead concept. |
| DM-JANNAWAY-reel-BOLD | Held. Same footage as the PILL cut already on TikTok — a re-treatment, not new inventory. |
| DM-BOND-reel-BOLD / -PILL | Held. Bond ran on Instagram 25 Jul. Never run on TikTok — that slot is still open and free. |

---

## Result notes

Record only the metrics that change the next creative decision:

- Hook/hold: did people stay after the opening?
- Consumption: watch time, completion, carousel continuation, or rewatches.
- Intent: saves, shares, comments, profile visits, or useful clicks.
- Audience language: exact questions, objections, recipient types, and occasions
  mentioned in comments.
- Next move: kill, revise the hook, extend into a series, or remake using a new
  product/occasion.

Never store customer names, messages, addresses, order numbers, or screenshots
containing personal data here.
