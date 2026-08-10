---
name: daisy-audio
description: "Trending audio for Daisy Maison video - find what is trending on TikTok, measure it, and cut the edit to its beat. Use when a video is silent, when picking a sound for a post, when animation cues (pills, logo pop, cuts) need to land on the beat instead of on typed-in numbers, when asked about music, sound, audio, trending sounds, BPM, or 'what song should this use', and when deciding how long a cut should be so it loops cleanly. Also covers what we are and are not licensed to embed."
metadata:
  version: 1.0.0
---

# Daisy Maison audio

Two problems, one tool: `Content Pipeline/tools/audio/trend_audio.py`.

The obvious problem was that our videos were silent. The bigger one was that
every animation cue was a number somebody typed because it looked about right.
On a feed watched with sound on, a cue 80ms off the beat reads as cheap and the
viewer cannot say why.

## YouTube audio: BLOCKED from this container. Do not re-run the search.

Measured 28 Jul 2026. Search and metadata work fine. The **media stream** is
refused by every player client:

| client | result |
|---|---|
| default, `web_embedded` | `HTTP 403 Forbidden` |
| `web`, `ios` | "Sign in to confirm you're not a bot" |
| `tv`, `mweb` | requested format not available |

This is YouTube blocking a datacenter IP, **not a missing flag**. A JS runtime
is present and wired up — `--js-runtimes node:/opt/node22/bin/node` clears the
deprecation warning — and changes nothing. The only fix is real YouTube
cookies, which are a credential and do not belong in this repo or container.

**TikTok downloads work.** That is the route that is open, and it is also the
better one — see below.

## What Max actually wants: real songs people recognise

Stated 28 Jul, twice, after the first version of this skill got it wrong:
*"The right audios make the difference between a good video and a bad video.
Using real songs that people recognise actually helps so much."* The TikTok
Commercial Music Library is **not** that. He has never heard of those tracks and
has rejected them outright. Do not offer them as the answer again.

**Do not argue TikTok sound-attachment at him.** The "a muxed file isn't
attached to a sound so you lose discovery" point is technically true and he does
not care: *"you think I care about TikTok commercial sounds? I don't care if
TikTok thinks we have a sound or not."* It is not the question being asked.

### Why it isn't already solved

Two separate blockers, and conflating them is what made the first answer bad:

1. **YouTube download is blocked from this container** (table above). Technical.
2. **Baking a commercial recording into Daisy Maison's marketing is a rights
   problem** — that's the business exposed, so no rip-the-charts pipeline gets
   built here. Say this once, plainly, and move to the fix. No sermon.

Note these pull against each other: the in-app picker is licensed *because it
goes through the platform*, which needs a human in the app — the exact thing
autonomy removes. Baking the file in is what removes the human, and that's the
uncovered use. That tension is the real problem, not the 403.

### The routes that actually get him it

| | |
|---|---|
| **Account category** | Business accounts get a restricted music catalogue on both IG and TikTok — label deals don't extend to commercial use, so you get library filler. Creator accounts typically get the full recognisable library. Most likely single cause of *"these sounds are shit"*. Untested — `ig_public.py` does not surface account type, so this needs checking in-app. |
| **A licence we hold** | Lickd licenses real chart music for creator/commercial use. That's the only route that is both recognisable **and** autonomous, because we'd own the right to embed the file. Epidemic / Artlist are cheaper but are library music — i.e. the thing he's rejecting. |

**Everything in this tool works on any audio file and does not care where it
came from.** `cues` emits timing numbers, not audio — it carries no licence and
survives this argument entirely. The missing piece is the right to use a track,
not the ability to handle one.

`fetch` downloads previews **to measure them**, never to redistribute — hence
the `.gitignore` on `library/`. `bed` genuinely embeds audio and needs a track
we hold rights to.

## Use it

```bash
cd "Content Pipeline/tools/audio"

# START HERE - what sound is on posts that actually performed
python3 trend_audio.py sounds --users daisymaison competitor1 --limit 12

# pull audio off a TikTok/IG post (works); search YouTube (download does not)
python3 trend_audio.py grab --url "https://www.tiktok.com/@x/video/123"
python3 trend_audio.py grab --query "upbeat indie instrumental"

# 1. call the tiktok_music_trending MCP tool, pipe its JSON in
python3 trend_audio.py chart --save

# 2. pull previews so they can be measured
python3 trend_audio.py fetch --top 20

# 3. measure
python3 trend_audio.py analyse --all

# 4. the payoff — cues that land on the beat
python3 trend_audio.py cues --track "finally-you-are-here" --dur 4.04 --events 3
```

## Reading `analyse`

Nobody here can hear a track, so "does this slap" is not answerable from this
seat. **Say that plainly rather than implying a taste judgement.** These are
answerable and they change the edit:

| Column | What it decides |
|---|---|
| `bpm` | whether a 4s cut is a whole number of bars |
| `lift` | where the intro ends. Trim to here, not to 0:00 |
| `busy` | onsets/sec. Above ~5 it fights two captions in a 4s cut |
| `bright` | spectral centroid Hz. Low = warm, high = bright/busy. The brand is *"premium and frictionless, never AI spectacle"*, so this is a real filter |
| `<-- clean` | the cut is a whole number of bars, so it loops with no musical seam |

`lift` uses the **95th percentile**, not the max. The first version thresholded
against the max — a single snare crack — so tracks never reached their own loud
section and `lift` came back empty on 15 of 20. If it regresses, that's why.

## What our own account is already using — measured 28 Jul 2026

`sounds --users daisymaison` over 9 posts:

| views | sound | artist |
|---:|---|---|
| 796 | Mission Possible | Zé Maré |
| 478 | Golden Hour | Tarwensi |
| 403 | original sound | DaisyMaison |
| 243 | Ok I Like It | Milky Chance |
| 241 / 236 / 229 | Luxury, Elegance, Refined | Ted D'souza, Dani |

**Do not read a sound→views causal line off this table.** The first version of
this skill put *Mission Possible* next to 796 views in a way that implied the
sound did it. Max, correctly: *"That's the Mr. and Mrs. Bond video. Of course we
know that did better because it was a better video. It wasn't an audio."* The
sound is fully confounded with video quality, and the best post here is our best
video. Nine posts cannot separate the two and neither can ninety.

What the table **is** good for: knowing what we've already used, so we stop
reaching for *Luxury, Elegance, Refined* a fourth time by default. That's a
repetition check, not a performance finding.

## TikTok chart tracks — measured 28 Jul 2026

Off a 20-track slice of the TikTok trending chart, three cut cleanly to 4.0s:

| Track | bpm | bars in 4.0s | bright | busy |
|---|---:|---:|---:|---:|
| Acoustic guitar, warm and gentle sounds — Veil music | 117.5 | 1.96 | 1357 | 3.2 |
| Aesthetic — BoominBeats | 117.5 | 1.96 | 1460 | 2.9 |
| Finally You Are Here — BCD Studio | 123.0 | 2.05 | 1507 | 2.8 |

**A result worth keeping:** on *Finally You Are Here* the grid puts our three
events at 0.35 / 1.35 / 2.35. The hand-typed values in `build_v2.py` were
0.25 / 1.35 / 2.20 — within ~100ms of a real 123bpm grid. The eyeballed timing
was close, not wrong. The tool's value is that it is now *checkable*, and that
picking a different track re-derives the whole timeline instead of leaving cues
stranded against a new tempo.

## Rules

- **Re-pull the chart before building a week on it.** Trending moves; a saved
  chart is a dated snapshot and `chart --save` says so.
- **Never claim a track is trending from memory.** Pull it, or name the gap.
- **Beat detection is an estimate.** If a cue looks wrong on the frame, trust
  the frame.
- Organic social posts publish autonomously. Paid media needs Max's go.
