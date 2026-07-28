# Breaking out of the small audience — what the numbers actually say

Written 28 July 2026, from a real pull (`tools/social_api/ig-snapshots/daisymaison-2026-07-28.json`),
not from memory. Instagram was rate-limited on the day this was written, so these
are the 28 Jul figures and nothing newer.

Max, 28 Jul: *"one of the things we're struggling with is that no one's
consistently been following our Instagram... we're stuck in this smaller boat of
an audience."*

He is right, and the pull says it more sharply than that.

## 1. The account went dark for 233 days, and that is the whole story

| Posted | Likes | Comments | Views |
|---|---:|---:|---:|
| 2025-05-04 | 113 | 11 | 2,483 |
| 2025-06-16 | 43 | 0 | 128 |
| 2025-10-08 | **101** | 2 | **11,889** |
| *— 233 days of silence —* | | | |
| 2026-05-29 | 0 | 2 | – |
| 2026-05-30 | 0 | 0 | – |
| 2026-05-31 | 2 | 0 | – |
| 2026-06-01 | 2 | 1 | – |
| 2026-06-17 | 2 | 0 | – |
| 2026-07-16 | 0 | 0 | – |
| 2026-07-25 | 7 | 0 | – |
| 2026-07-26 | 6 | 0 | – |
| 2026-07-27 | 4 | 1 | – |

**Before the gap: 86 likes per post. After it: 2.6.** A 33× collapse across a
break, not across a change in what was being made.

This matters because it is the difference between "our content is bad" and "our
account is dormant". The second one is fixable by doing one thing repeatedly.
The first would need a new brand.

## 2. The best post this account has ever made is a sign turning round

`DPjdseCDbDR`, 8 October 2025 — **11,889 views**, nearly 5× the next best, and
the caption was four words: *"Customer of the year, probably."*

It is a real Daisy Maison sign, filmed on a phone, turning continuously from its
white back through the thin edge to the printed front. No generation. No spend.

That is the same reel the DM-C017 construction reference pack was cut from, and
it is the format Max named unprompted as the best bet:

> *"it'll probably be our streets and turnaround videos, because there are just
> so many concepts you can be cheeky, romantic, and sentimental with."*

His instinct and the only view count we have agree. Two caveats worth keeping
honest: it converted at 0.8% likes-per-view against 4.6% for the May post, so it
reached far more people and moved fewer of them; and it is one post, not a
pattern. It is still the strongest signal on the account.

## 3. What to actually do, in leverage order

### a. Recover the turnaround references — DONE, 28 Jul 2026

The four physical views the video rules demand (front, front-to-edge,
back-to-edge, white back) were **missing from the repo** — only the markdown
describing them survived. That is why DM-C019 had to be a lift rather than a
turn, and why DM-C019 is boring.

**They are back.** Not off Instagram — the public endpoint was rate-limited (429)
when this was attempted, and the cooldown is measured in hours. They came out of
**git history**, where the blobs were still reachable from an older commit even
though the files had left the working tree. Restored with `git cat-file`, and all
five recorded SHA-256 hashes re-verified byte for byte: the source video and each
of the four frames match exactly.

They are now force-added past `.gitignore` (2.4 MB) so they survive the next
merge. `REFERENCE_PACK.md` records how they were lost and why nothing flagged it.

**Gate 2 is satisfiable again, so the next sign video can turn** — and the turn
is the format the only view count we have actually likes.

### b. Stop paying 54 credits a video

`seedance_2_0` at 1080p/std costs **54**. `seedance_2_0_mini` at 720p/fast costs
**15** — measured with `get_cost`, not estimated. TikTok re-encodes everything to
roughly 720p anyway, so the extra resolution is being thrown away by the platform
we most want to win on.

Daily posting at 54 credits is ~1,620 a month. At 15 it is ~450. **Cadence is the
cure and cost is what stops cadence**, so this is the change that makes the cure
affordable.

### c. One paid take, many free posts

The footage is the only part that costs money. The hook, the caption, the
sign-off and the timing are HTML, and hyperframes re-renders them locally for
**zero credits in about 45 seconds**.

So one good turnaround take is not one post. It is one asset that ships repeatedly
with a different hook each time — cheeky, then romantic, then sentimental, which
is exactly the range Max described. Budget per *post* drops by however many hooks
a take can carry.

### d. Push TikTok, not Instagram, as the front door

This is the actual escape from the small boat, and it is worth being precise
about why.

| | Instagram | TikTok |
|---|---|---|
| Followers | 23,535 | 183 |
| Recent mean likes | 2.6 | 33.0 lifetime average |
| Posts | 12 in 15 months | 166 videos |

Instagram is a **follower graph** — a dormant list of 23,535 people who no longer
get shown our posts, and reach has to be earned back through them. TikTok is an
**interest graph** — it shows a video to strangers regardless of follower count.
183 followers earning 33 likes a video is not a worse account than 23,535 earning
2.6; it is a healthier one.

We do not need a warm audience on TikTok. That is the whole point. Higgsfield
exposes `tiktok_publish`, so the post step is automatable end to end once a take
passes QC — though **publishing still needs Max's explicit go every time**.

### e. The comment-to-sign loop — the warm-audience builder, at zero credits

The cheapest engagement we can manufacture honestly: someone comments a wording,
and we make that exact sign.

It costs nothing, because it never touches a video model:

1. `projects/daisy-street-sign/artwork/build.py` renders the exact wording — the
   same audited geometry the laser uses.
2. `Content Pipeline/templates/sign-reprint/` colours it from the laser's own
   `product-rules.json` and drops it into an approved plate.
3. hyperframes renders the still or carousel locally.

Every reply is a personalised artefact for a named commenter, which is the thing
most likely to make that person comment again. Repeat commenters are what a warm
pool actually is.

**Boundary, and it is a hard one:** this pasted-face route is the approved method
for *stills* only. `WEDDING_SIGN_VIDEO_RULES.md` Gate 3 forbids product-surface
replacement in generated video, and that rule exists because it produced a
visibly pasted panel once already. Stills yes, video never.

## 4. What this does not claim

- No per-video TikTok numbers. That endpoint is signed; the tool refuses to
  guess and so does this document. Account-level deltas only.
- Instagram view counts exist only on the three 2025 posts. Every 2026 post
  returns `null` for views, so the 2026 collapse is measured in **likes**, and
  reach is inferred from it rather than observed.
- One reel at 11,889 views is a signal, not a proven format. It should be
  treated as the best hypothesis available, and tested.
- Nothing here is published. Publishing needs Max's explicit go, every time.
