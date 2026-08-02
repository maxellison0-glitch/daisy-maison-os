# DM-C014 — Claude / Codex collaboration log

A running record of the two agents working the concept in turns. Newest at the
bottom. Decisions that stick get promoted into `CURRENT_CONTEXT.md`.

## Setup

- Codex CLI: gpt-5.6-sol, reasoning effort high, sandbox `workspace-write`.
- Wrapper: `.collaboration/invoke-codex.ps1` (concept shim) → workspace wrapper.
- Fix applied by Claude: workspace wrapper now pipes the prompt via **stdin**
  (`codex exec … -`) instead of as a command-line arg, because `codex.cmd`
  routes through cmd.exe which truncated the multiline context packet at the
  first newline. Verified end-to-end with a tail-marker echo test.

## Turn 1 — Claude builds the first cut

- Built deterministic 3-shot 9:16 animatic from the single master photo.
- v1 → v2: corrected feature centroids (hearts 822,955; pebbles 482,772),
  chose the full-gift reveal ending, tightened the match cut.
- Deliverables: silent master + 720p mobile copy + contact sheet + cut blend.

## Turn 2 — Codex reviews (session 019f8653)

Codex ran its own pixel-level centroid analysis (System.Drawing luminance
sampling) and returned six ranked, numeric findings:

1. Match cut off by ~38px right / 35px high → move `PEBBLES` to **(494,761)**.
2. Scale can't match (hearts 90×44, pebbles 73×112) — solve position, keep H=600.
3. Tighten runtime to **8.5s** (48/72/105/30 frames).
4. Remove the Shot B micro-settle — the decisive frame must not wander.
5. Not final-resolution: 3.2× upscale softens lettering; needs hi-res original
   before delivery. No crop falsifies the product.
6. Sound: **ADD** — room tone ~−34 LUFS + one dry 80–120ms stone tick ~−20 dBFS
   on the cut. No music/reverb.

## Turn 3 — Claude applies the review (v3)

- Applied all six. Rendered v3 (255 frames / 8.5s). Blend confirms the hearts
  and pebbles now co-locate dead-centre at the cut.
- Sound-on proof muxed to Codex's spec — measured −33.9 LUFS / −19.5 dBFS peak.
- Deliverables: `DM-C014-P1-MASTER-9x16-v3.mp4`,
  `DM-C014-P1-MOBILE-720x1280-v3.mp4`, `DM-C014-P1-SOUND-9x16-v3.mp4`.

## Turn 4 — Phase 2 kickoff (elevation)

Max asked the two agents to push toward a benchmark-grade result: reference real
premium companies, use each other as research agents, and max out Higgsfield's
advantages while keeping the product pixel-true. Claude opened benchmark
research; Codex tasked as second research agent + elevation planner.

## Turn 5 — Codex researches + specs the elevation (session 019f8664)

Codex agreed v3 is "perfect enough to ship as the muted first-cut validation"
and caught Claude's draft grade as over-processed. Accepted finishing spec:

- Easing → smootherstep `6t^5-15t^4+10t^3`, `t=frame/(len-1)` for exact endpoints.
- Luma-only tone curve, 8-bit anchors 0>2 32>34 64>68 128>132 192>193 224>221
  255>248; saturation 0.97; **no RGB warming** (source is already warm).
- Vignette: -0.08 stop at corners, smoothstep from 65% radius.
- Grain: monochrome zero-mean sigma=32, 1.5% opacity, 3-frame rolling average.
- Camera breath: none (gimmicky; risks lettering shimmer).
- Higgsfield: only a locked, abstract warm-linen light field composited solely in
  the synthetic-BG margins (mask eroded 24px, feathered 20px on bg side, luma
  excursion <=6/255, <=18% opacity). If the seam shows at all, drop Higgsfield.

Rejected (Codex): floating bokeh/dust/sparkles, blanket warmth, fake handheld,
visibly crawling grain — the "luxury beige" cliche.

## Turn 6 — Claude implements the benchmark finishing (v4)

Implemented Codex's spec faithfully in numpy (exact luma curve, vignette, grain)
plus smootherstep easing in the geometry. Product pixels untouched. Rendered the
v4 benchmark master (silent + sound + mobile).

## Turn 7 — Codex verifies v4 (session 019f867e)

Codex confirmed render_v4.py implements every spec item correctly, flagged only
two visually-immaterial edge cases (pure-black not lifted to luma 2; the first two
frames average fewer grain plates), found no regression vs v3, and gave the
verdict: **"v4 is the benchmark muted master to show Max."** The hi-res original
remains the only true blocker to a final delivery master.

## Turn 8 — Max's verdict: REJECTED (22 July, morning)

Max rejected the deterministic animatic outright: "looks like one of those
Chinese adverts… you've literally zoomed into an image, zoomed out, and then
zoomed out again… pixelated… stretched a square image into a reel." Correct on
every count. The crop-pan approach is dead. New mandate: foundation-first —
build the base assets properly, get them approved, then real motion. Higgsfield
tools were also missing from the session; Max fixed the connector (full
generation suite now live). 2K is the master ceiling (social delivers 1080p).

## Turn 9 — Codex directs the redo (session 22/07)

Codex direction, accepted in full: keep the match cut as the spine (95%);
build THREE separately composed 9:16 stills — lid macro, pebble macro, hero
wide (98%); camera-only motion (slider 3-5%, arc <=2 deg, dolly <=3%), never
"ribbon sways / box opens" prompts (90%); frame-level truth test with 8-12
takes per shot budgeted; no text on the proof (97%); biggest risk = accepting
attractive motion that falsifies the product (99%).

## Turn 10 — Claude builds the foundation (22 July)

- bytedance 2K upscale: REJECTED by truth test (rewrote all lettering as
  gibberish, invented pebble texture). 2 credits to learn the model is unusable.
- nano_banana_2 prompted restoration (full text inventory spelled out):
  lid zone letter-perfect and sharper — ACCEPTED for Shot A only; pebble
  contours/tree/date drifted — REJECTED for B/C. Lesson: prompted text-aware
  editors preserve print far better than blind upscalers, but never feed them a
  guessed reading of handwriting (it can write the guess onto the product).
- Base canvas: outpainted 9:16 margins + original square re-composited over the
  interior (identity diff = 0). AI pixels exist only outside the photograph.
- Three stills built with the match cut baked in (hearts and pebbles both at
  frame position 0.50, 0.62). Max approved with notes; wants the full workflow.
- Motion: seedance_2_0 plan-gated (403, needs Pro/Ultimate). Fell back to
  kling3_0 pro (8.75 credits/clip, silent, camera-only prompts) — three takes
  submitted from the approved stills.

## Turn 8 (superseded numbering) — Claude delivers

Finalised v4 (silent + sound + 720p mobile), built a private case-study artifact,
and updated CURRENT.md + CURRENT_CONTEXT.md. Higgsfield image/video generation is
not exposed in this non-interactive session, so the margin-atmosphere idea is
documented for a future interactive pass rather than faked. Ready for Max.
