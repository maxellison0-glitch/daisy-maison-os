# Skills

## Vendored — `coreyhaines31/marketingskills` (MIT)

Nine skills installed 28 Jul 2026 from
https://github.com/coreyhaines31/marketingskills, MIT licensed, copyright
retained in `LICENSE-marketingskills`. Chosen against problems this business
actually has rather than installed wholesale — the source repo has 49.

| Skill | Why it is here |
|---|---|
| `social` | TikTok/IG content, hooks, short-form scripting, social listening. The core one. |
| `content-strategy` | Deciding what to make, not just how to write it. |
| `marketing-psychology` | Why people buy. Feeds the hook work directly. |
| `ad-creative` | Hook writing and creative iteration **at scale** — we are hunting a format, and this is the discipline for it. |
| `video` | Names Seedance, Hailuo, Kling, Veo — literally our generation stack. |
| `ab-testing` | Falsifiable calls are already the house habit; this is the rigour behind them. |
| `competitor-profiling` | Structured competitor dossiers, which is what `REFERENCE_TRACKER.md` is reaching for. |
| `cro` | Site conversion. CVR slid three days straight to 3.85% on 27 Jul. |
| `marketing-council` | Multiple opposed expert lenses on a hard call, with the disagreement kept rather than averaged. |

Added 28 Jul 2026 from the same source:

| Skill | Why it is here |
|---|---|
| `ads` | Meta kill/scale decision tree and PMax guardrails. Paid is £735/day — the largest number in the business, and nothing installed covered it. Curated: **4 of its 10 references**, routing table edited to drop dead links. B2B/LinkedIn/lead-gen references deliberately skipped and the reasoning recorded in the file. |

Not installed, available in the source repo if wanted: SEO (several), email,
SMS, pricing, offers, launch, PR, referrals, influencer, ASO, attribution,
analytics (GA4/GTM focused — not our problem), and ~30 more.

## The keystone — `.claude/product-marketing.md`

**Not a skill. Read it before any of them.** Ten of the vendored skills open by
looking for a product-marketing context file; until 28 Jul 2026 none existed, so
every one of them started from zero and asked Max questions the repo could
already answer.

It holds the product lines and real prices (street sign **£11.25**, not the ~£19
that had been assumed in conversation for weeks), the **~£29 AOV** computed from
four completed days, the audience by buying occasion, the voice, the verified
proof points, the hard constraints, and — as importantly — a **Known Gaps**
section for everything that genuinely is not established.

Every number in it is dated and sourced. **If a claim cannot be sourced it goes
in Known Gaps, not in the file.** A confident invented number here becomes a
confident invented number in an advert.

## Ours — the three that encode what this business paid to learn

Written here because the generic skills are craft and these are the account.
Where they disagree with a vendored skill, these win.

| Skill | What it holds |
|---|---|
| `daisy-paid-media` | The guardrail (**never execute an ad-account write without Max's explicit go** — Windsor.ai can move ~£735/day of real money), the account IDs and naming, the 3x floor, and **seven rules learned the hard way**: one red day is noise and four is a trend; judge budget changes over 3–4 days against a 2–5 day conversion lag; no ROAS verdict before 7 days *and* 100 clicks; more budget buys worse traffic (PMAX £277→3.41x vs £366→2.46x) with the cart-add/abandonment diagnostic; taper vs zero-line floor; rolling averages hide the death day; check day-counts before believing a week-on-week number. |
| `daisy-video-generation` | The spend rules (`get_cost`, never estimate; default to the 15-credit tier, not the 54), the three gates, **the law of the end frame** (take 01 cost 54 credits to learn it), one-reference-per-question, and the QC gates including how the framing check finds the sign and why the obvious method silently answers the wrong question. |
| `daisy-social-analytics` | See below. |

## Ours — `daisy-social-analytics`

Written here because nothing off the shelf can do it: it drives `ig_public.py`
and `tiktok_public.py`, the two readers in
`Content Pipeline/tools/social_api/`, and encodes what each platform can and
cannot actually show us plus the rate-limit discipline that cost us a day's
competitor reads to learn.

**Use it before any argument about what to post.** Its whole reason for
existing is that on 28 Jul three weeks of strategy rested on a remembered
number that turned out to be 7 likes.
