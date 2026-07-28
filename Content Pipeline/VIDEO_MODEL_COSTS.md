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
