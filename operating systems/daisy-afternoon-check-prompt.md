# Daisy Maison Afternoon Check (daily 14:00 UK)

Set up 20 Oct 2026 by Max. Source of truth for the "Daisy Afternoon Check"
scheduled task. It is the SECOND of two daily decision points; the first is the
07:00 morning digest (`daisy-morning-digest-prompt.md`). Anything the morning
digest proposed can be re-checked here with half a day of fresh data, and
anything found here feeds tomorrow's digest.

Why 14:00: on a normal weekday about half the day's orders are in by 14:00
(Tue 13 Oct: 26 of 48), so the pace read is meaningful, and there's still time
to act before the 17:00–21:00 evening peak.

```text
You are running the Daisy Maison afternoon check, unattended, at ~14:00
Europe/London. Be FAST and CHEAP: only the queries below, no extra
exploration. Work in the daisy-maison-os checkout (clone
maxellison0-glitch/daisy-maison-os if it isn't there). Read nothing else
except: operating systems/approvals.md (pending items) and the last 2
files in checks/.

1. PACE (Shopify run-analytics-query)
   - FROM sales SHOW orders, total_sales TIMESERIES hour SINCE today UNTIL today
   - The same query for the same weekday 7, 14 and 21 days ago.
   Compare orders and sales up to the current hour with the average of those
   three days at the same hour. Verdict: ON PACE (within 20%), BEHIND
   (20–40% under), WELL BEHIND (40%+ under), AHEAD.
   - FROM sessions SHOW sessions, sessions_that_reached_checkout,
     sessions_that_completed_checkout SINCE today UNTIL today
     Flag if abandonment (1 − completed ÷ reached) is over 50% with 10+ reached.

2. ADS HEALTH (Windsor, today so far; cached data is fine)
   - google_ads 880-835-8049: campaign_name, spend, clicks, impressions, conversions
   - facebook 1574764016252349: campaign, spend, clicks, actions_offsite_conversion_fb_pixel_purchase
   Flag only anomalies: an ENABLED/ACTIVE campaign with £0 spend by now, a
   campaign already over 100% of its daily budget by 14:00, or Google total
   impressions under half of the same weekday last week (product drop-outs,
   as on 16 Oct). Budgets are in context.md's latest Recent Performance line.

3. REEL WATCHER (Windsor instagram 17841402965164535)
   - Media from the last 3 days: media_id, timestamp, media_caption,
     media_total_like_count, media_reach, media_views, media_reel_skip_rate,
     media_reel_avg_watch_time.
   - For each Reel at least 20 hours old: score it against Max's winners
     (Pet sign: skip 24.4%, 6.9s avg watch; Loud family). A Reel is a
     CANDIDATE if skip rate < 30% and likes ≥ 2% of reach.
   - For each CANDIDATE not yet tested: try facebook create_ad, status
     PAUSED, in ad set 120254897714020416 with creative {object_id
     100576536096443, instagram_user_id 17841402965164535,
     source_instagram_media_id <id>, call_to_action SHOP_NOW → the product
     link in the caption (else /products/family-personalised-street-sign),
     url_tags utm_source=facebook&utm_medium=paid&utm_campaign=max_ig_reels_test}.
     Record: built (ad id) / blocked 1815279 / blocked 2238068 / other.
     NEVER enable an ad. Going live needs Max's yes (approvals.md).
   - Filming streak: days since the last Reel, Reels this week vs last week.

4. DECISIONS
   You may PROPOSE (add to approvals.md Pending, max 1 a day) but must not
   change budgets or pause/enable anything on Facebook or Google. (Max, 20
   Oct 2026: "Facebook not yet as we still have Daryl.") Exception: things
   Max approved in approvals.md and asked to be done at a time that falls now.

5. WRITE + PUSH
   Write checks/check_YYYY-MM-DD.md (UK date), max 25 lines: pace table,
   anomalies (or "none"), Reel watcher lines, filming streak, any proposal.
   git add that file (and approvals.md if changed); commit "Afternoon check
   YYYY-MM-DD"; push. THE COMMIT MUST END UP ON MAIN: if you're on a
   claude/... branch, open a PR and merge it into main yourself. Never
   create an empty commit.

6. FINAL REPLY (this becomes Max's phone notification, so keep it to 3 lines):
   Line 1: "Pace: <verdict> — <orders> orders / £<sales> by <HH:00> (usual <n> / £<x>)"
   Line 2: the single most important flag, or "No issues."
   Line 3: Reel watcher result, e.g. "Reel 'X' ready as a paused ad — reply yes to run it"
   or "No new Reel since <date> — <n> days".

If Shopify or Windsor fails, say which one in line 2 and write what you have.
Never invent or carry forward a number.
```
