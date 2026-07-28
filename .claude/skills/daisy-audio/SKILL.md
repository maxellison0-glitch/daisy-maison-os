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

## The licence line — this is the part to get right

TikTok's Commercial Music Library is licensed for use **on TikTok, through
TikTok**. That gives one clean route and one trap.

| | |
|---|---|
| **Route A — clean** | Attach the track at publish with `music_sound_id` (the `song_clip_id` from the chart). Nothing is downloaded, TikTok mixes it, and the platform boosts its own audio — which is the entire reason to use a trending sound. |
| **Route B — NOT covered** | Download a preview, mux it into an mp4, post that file to Instagram / the site / an ad. Different use, not granted by that licence. |

So `fetch` downloads previews **to measure them**. `cues` uses the measurement
and touches no audio at all — its output is timing numbers, which are ours and
carry no licence. Both are safe for either platform. `bed` genuinely embeds
audio and needs a track we hold rights to.

**For an Instagram-first cut, the answer is not "mux a trending sound."** It is
either a track we are licensed for, or the sound design we already have —
`media-use` ships 19 SFX and `build_v2.py` already places them frame-accurately.

## Use it

```bash
cd "Content Pipeline/tools/audio"

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

## Measured 28 Jul 2026

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
- **Propose, never publish.** Attaching a sound at publish is still publishing.
