# Instagram trial reels — the distribution fix

Max sent [this](https://www.youtube.com/watch?v=t1-XAN6AyOs) — *"Claude + Trial
Reels = Cheat Code"*, Ash Harris, 16 Jul 2026, 49,080 views — and said *"we have
to do this as well. It makes so much sense."*

He is right, and it is the most important thing in this repo right now, because
it attacks **the one problem that no amount of creative fixes.**

---

## 1. Why this matters more than anything else we are working on

Measured, not remembered:

| | |
|---|---|
| Instagram followers | **23,535** |
| Likes per recent post | **4–7** |
| Engagement rate | **~0.03%** |
| TikTok followers | 183 |
| TikTok views per recent post | 229–796 |

`daisy-social-analytics` already names the diagnosis: *"Anything near zero is a
distribution problem and no hook will fix it."* A 23,535-follower Instagram
account returning single-digit likes is not being shown to its own followers.

**A trial reel goes to non-followers only.** That is precisely the audience our
account can still reach. Every hour spent making the sign funnier is spent on
the wrong axis while a dead follower base is the bottleneck.

---

## 2. The three basics

1. **At least 3 grid posts a week.** The claim in the video is that >12 posts a
   month puts an account in a different algorithmic category. Sourced as *"word
   on the street"* from creators with Meta partnerships — **treat it as
   unverified**, but the cost of posting three times a week is nil.
2. **Maximum 5 trial reels a day.** Above that risks a reach-limit notification.
   Five is the number multiple large creators converge on.
3. **Cross-post to Facebook.** In the video's own data, 1.1M of 3.1M views and
   4,000 followers came from Facebook **without ever posting there** — purely
   cross-posted trial reels.

**The mechanic that makes the whole thing work: trial reels and the grid are
separate systems.** The same file posted to both is not treated as duplicate
content.

---

## 3. Phase 1 — recycle the winners we already have

Post existing grid winners straight to trial reels. Same file. It gets a second
run at reaching people who have never seen it.

**We have winners sitting idle.** `instagram-DPjdseCDbDR` — *"Customer of the
year, probably"* — did **11,889 views** against a recent baseline of 4–7 likes.
That post has never been given to a non-follower audience.

To run the same asset several times, change the first 2–3 seconds:

| Variation | Note |
|---|---|
| New text hook over the same base | the main lever |
| Zoom to 1.02× | visually identical |
| Speed to 1.02× | preferred over slowing down |
| Slow to 0.98× | warps voice — avoid |

Four hooks × four methods = 16 runs off one proven asset. **This is the same
economics as the overlay lane already in `daisy-video-generation`: the footage
is the expensive part, the hook is free.** We are already set up for it —
`render_overlays.py` + `finish.py` produce a new hook variant in about a minute
at zero credits.

Two further notes from the video: trial reels hit your **immediate location**
first, so they can be used to bias a geography; and after **60 days** an old
trial-reel winner can be run again.

---

## 4. Phase 2 — test every hook before the grid sees it

Film everything after the hook once, export it as one brick with captions
attached, then put A/B/C/D hooks on the front and post them a few minutes apart.
The grid then only ever sees a winner.

**The same caption text on all four is fine.** What must differ is the visual in
the first 2–3 seconds — the on-screen text, the framing, or the colour.

Claimed spreads between hooks on identical footage: up to **16×**.

**This is exactly what we built today and did not have a use for.** The
Correction has one hook — *same order. / both signs.* — and a second written but
unused: *we just print / what they send.* Two more would make a full A/B/C/D.

---

## 5. Promoting a winner — the part that is easy to get wrong

**Play A — push the trial reel through to the grid** (Settings → manage trial
reels). Carries its existing comments and likes across as social proof. Use when
the format is unusual or serves a different audience than our followers.

**Play B — post the file fresh to the grid.** Use when it is an obvious fit for
our own audience. Two separate rockets: the trial reel keeps running while the
grid post starts warm.

### The 48-hour rule
Push through within **48 hours** and it reaches followers' feeds as a normal
grid post. It does not matter if comments have gone quiet.

### The 25% rule
If a trial reel is still climbing, do not wait past the point where a day adds
**less than 25%** more views. 10,000 on day four → 12,000 on day five means it
is dying and the moment has passed.

**The failure that produced these rules:** a first trial reel did 40,000 views
in two days, was left for a week, and when finally pushed to the grid **got one
like.** Timing, not creative, was the whole difference.

---

## 6. What we do with it

| | |
|---|---|
| 1 | Post `instagram-DPjdseCDbDR` (11,889 views) as a trial reel. Costs nothing, uses an asset we own. |
| 2 | Build 4 hooks for The Correction, post as A/B/C/D trial reels a few minutes apart |
| 3 | Apply the 48-hour / 25% rule, push the winner to the grid |
| 4 | Get to 3 grid posts a week |
| 5 | Turn on Facebook cross-posting |
| 6 | Snapshot before and after with `ig_public.py` and `tiktok_posts.py` — this is a falsifiable call and it should be settled with numbers |

**Publishing is Max's.** Nothing here posts anything.

---

## 7. What is evidence and what is claim

The numbers in §1 are ours, pulled today. **Everything in §2–§5 is one
creator's account of their own results** — 480 → 21,000 followers, 3.1M views,
100 posts in 97 days, self-reported, with a course and a lead magnet attached.
The mechanics (separate systems, non-follower targeting, manage-trial-reels) are
Instagram features and checkable. The thresholds — five a day, 48 hours, 25%,
60 days, 12 posts a month — are **his observed heuristics, not documented
platform behaviour**, and we should hold them as such until our own snapshots
either support them or don't.

That is the honest frame: the *strategy* is sound because it targets our actual
bottleneck. The *numbers* are someone else's until we have our own.
