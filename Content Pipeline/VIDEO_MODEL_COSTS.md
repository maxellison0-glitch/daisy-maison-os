# Video model costs & selection (Higgsfield)

Real preflight costs, pulled 2026-07-24. Per single 9:16 clip, silent
(we add audio/caption ourselves). Costs scale with duration / resolution /
audio — these are the low-spec baseline we should default to.

| Model | Baseline spec | Credits | Use it for |
|---|---|---|---|
| **Veo 3.1 Lite** | 4s, silent | **4** | Cheap ambient motion, batch tests |
| **Minimax Hailuo 2.3 Fast** | 6s, 768 | **4** | Natural physics, quick hero clips |
| **Seedance 1.5 Pro** | 4s, silent | **4.8** | Reliable motion, good default |
| **Kling 3.0 Turbo** | 5s, silent | **7.5** | Fast start-frame animation |
| **Seedance 2.0 Mini** | 5s, silent | **12.5** | Budget reference-driven |
| **Seedance 2.0** | 5s, silent | **22.5** | **Best identity/label lock** — premium only |

Higher tiers (Veo 3.1 ultra, Kling 3.0 pro/4k, Cinema Studio 3.0) exist but are
overkill for organic social. Don't reach for them without a reason.

## Seedance 2.0 in full — re-quoted 2026-07-28

Model tier and resolution are **separate axes**, and treating them as one thing
is why "Seedance 2.0" got remembered as a flat 54 credits. It isn't. Every row
below is a live `get_cost` quote, 9:16:

| Model | duration / resolution / mode | Credits |
|---|---|---:|
| Seedance 2.0 Mini | 6s / 480p / fast | **6** |
| Seedance 2.0 Mini | 6s / 720p / fast | **15** |
| Seedance 2.0 | 4s / 720p / std | **18** |
| Seedance 2.0 | 6s / 720p / fast | **21** |
| Seedance 2.0 | 6s / 720p / std | **27** |
| Seedance 2.0 | 6s / 1080p / std | **54** |

The 54 is **resolution, not the model** — and per rule 5 below, 720p is what
TikTok delivers anyway. Full Seedance at 720p/4s is 18 credits, three more than
Mini. Escalating for a pixel-locked label costs a few credits, not a fortune.

**`bitrate_mode: "high"` is free** — 27 either way at 720p/std, 54 either way at
1080p. Higher bitrate means less compression on fine printed detail. Default it
on; there is no reason not to.

**`generate_audio: false` saves nothing** (15 vs 15). Rule 6 stands on
unpredictability, not cost.

## Selection logic

1. **Does this even need video?** → run the Brief Gate first.
2. **Caption:** always our post overlay. Never buy model text-rendering.
3. **Motion model:** start at the 4–8 credit tier (Seedance 1.5 / Hailuo / Veo Lite).
   Only escalate to **Seedance 2.0 (22.5)** when the DS label / product must stay
   pixel-locked across the clip (reference-driven, `image_references` role).
4. **One shot, not three.** A 5s continuous ambient clip > a 3-clip cut.
5. **Resolution:** 720p is plenty for Reels/TikTok. 1080p only for feed hero.
6. **Audio:** generate silent, score with a licensed track in post; native
   model audio is unpredictable and costs more.

## Rough per-post budgets

- One captioned ambient hero clip (budget model): **~5 credits**
- Same on premium Seedance 2.0 (label-locked): **~22 credits**
- Still image / carousel frame: image-model cost only (cheapest path)

At ~1,169 credits on hand, cost is not the constraint — *purpose* is.
Preflight every job with `get_cost:true` before spending.
