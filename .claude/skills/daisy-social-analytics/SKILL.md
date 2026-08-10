---
name: daisy-social-analytics
description: "When the user wants to know how @daisymaison is actually performing on Instagram or TikTok, or wants a post's real numbers. Also use when the user mentions 'how did that post do,' 'engagement,' 'likes,' 'followers,' 'is it working,' 'did it perform,' 'check the account,' 'our numbers,' 'competitor numbers,' 'what are TreatBox doing,' 'reach,' 'views,' 'analytics,' or asks whether content is landing. Use this BEFORE any strategy argument about what to post — every claim about performance must come from a pull, never from memory. For deciding what to make next, hand off to social or content-strategy. For designing a test, see ab-testing."
metadata:
  version: 1.0.0
---

# Daisy Maison social analytics

Read the real numbers for @daisymaison on Instagram and TikTok. Both tools are
in this repo, both work with no login, no Meta app and no paid connector.

**The rule this skill exists to enforce: never reason from a remembered number.**
On 28 Jul 2026 three weeks of strategy rested on "Bond was our best post." It was
7 likes. One unauthenticated request settled it. If you are about to say a post
did well, pull it first.

## The tools

Both live in `Content Pipeline/tools/social_api/`.

```bash
cd "Content Pipeline/tools/social_api"

python3 ig_public.py profile --save              # ours
python3 ig_public.py profile --user treatbox     # any public account
python3 tiktok_public.py profile --save          # ours
```

`--save` writes a dated snapshot to `ig-snapshots/` or `tiktok-snapshots/`.
Always use it. The series is worth more than any single pull, and on TikTok the
series is the *only* way to get a daily number at all.

## What each one can and cannot see

| | Instagram | TikTok |
|---|---|---|
| Followers | yes | yes |
| Per-post likes | **yes**, last 12 | **no** |
| Per-post comments | **yes**, last 12 | **no** |
| Views | only on some videos | no |
| Reach, saves, shares, profile visits | no — needs the Meta token | no |
| Cumulative lifetime likes | no | **yes** — this is the useful one |

**TikTok per-post data: SOLVED 28 Jul 2026. The paragraph below used to say it
was impossible. It was wrong.**

```bash
python3 tiktok_posts.py posts --user daisymaison --limit 12 --save
python3 tiktok_posts.py look  --url <tiktok video url>      # SEE the post
```

`yt-dlp`'s TikTok extractor reads the same metadata the web player uses and
returns **per-post view counts, like counts, captions and dates with no login**.
Measured the day it was added, on @daisymaison: nine posts, views 3–796.

`look` goes further and closes the gap this skill could not: it **downloads a
post and lays its frames out as a contact sheet**, so a competitor's content can
be judged on how it looks, not only on what it earned. `ig_public.py` returns
numbers and captions and never images; this does images.

Two things that will bite:

- **Never install `curl_cffi` / yt-dlp's impersonation extra.** It performs its
  own TLS handshake and this container's agent proxy resets it — every request
  dies with `curl: (35) Recv failure`. It was installed once, broke every pull,
  and was removed. yt-dlp's native networking works.
- **A `0` like count means "not returned", not "no likes."** It came back
  missing on 3 of 9 posts and real on the rest. View counts were present on
  every post. Quote views; call a missing like count missing.

*What the old approach could do, kept because it still works as a cross-check:*
diff `hearts_total` between two daily `tiktok_public.py` snapshots for total
likes earned in between. If more than one post went live in that window the
number cannot be attributed to either, and you must say so.

## The numbers that actually decide something

1. **Engagement rate against followers.** `(likes + comments) / followers`.
   1–3% is healthy. Anything near zero is a distribution problem and no hook
   will fix it. `ig_public.py` prints this for you.
2. **The per-follower comparison across platforms.** As of 28 Jul: Instagram
   23,535 followers → 4–7 likes (~0.03%). TikTok 183 followers → 33.4 lifetime
   likes per video. TikTok reaches non-followers; Instagram does not currently.
   That gap, not the creative, is the biggest lever on this account.
3. **The delta, not the level.** A single pull tells you where you are. Two
   pulls tell you whether anything you did mattered.

## Reading the Instagram output correctly

- **The first rows may be pinned posts.** The API does not flag them, so read
  the dates — anything out of chronological order at the top is pinned, and its
  numbers reflect months of accumulation, not a day's performance.
- **A missing view count is not zero.** Views come back on some video posts and
  not others. Absent means unknown. Never log it as a result.
- **Twelve posts is the ceiling** for one request.

## Rate limits — this is the part people get wrong

Instagram will 429 an IP that asks repeatedly, and **a 429 lasts hours, not
minutes.** Measured on 28 Jul: one instaloader run burst several requests to
page through history, tripped a 429 inside a minute, and that block was still in
force fifty minutes and three attempts later. It cost the entire day's
competitor reads.

So:

- **One account per day, one request each.**
- **Never use a library that pages on your behalf** (instaloader, scrapers).
  The convenience is exactly what spends the budget.
- If you get a 429, stop. Do not retry in a loop. Come back tomorrow.
- Pull ours first. Competitors are a bonus, ours is the job.

## Workflow

1. Pull ours on both platforms with `--save`.
2. Compare against the previous snapshot. Report the delta, not just the level.
3. Cross-reference `Content Pipeline/PUBLISH_LOG.md` — which posts were live in
   that window, and does the log's claimed result match what you just measured?
   Correct the log if it does not. The log has been wrong before.
4. State every gap explicitly. No reach, no saves, no shares, no TikTok
   per-post. A named gap is worth more than a confident guess.
5. If a falsifiable call is open, settle it — or say plainly that it cannot be
   settled and why. On 28 Jul two consecutive calls died unmeasurable because
   they were written against numbers nobody could pull. **A call only counts if
   the number that settles it is one this skill can already fetch.**

## Guardrails

Analytics only — this skill reads, it doesn't post. Never invent a metric, a
competitor post or a result — name the gap instead. No customer PII in anything written to
the repo.
