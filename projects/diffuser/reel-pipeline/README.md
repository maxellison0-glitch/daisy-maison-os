# Diffuser reveal reel — pipeline

Reproducible build of `../reveal-carousel/DM-diffuser-reveal-reel.mp4` (1080×1920, ~6.5s).

- **Base motion:** the 3 matched stills (`../reveal-carousel/01,02,03`) cover-cropped to 9:16,
  slow push-in (ffmpeg zoompan 1.0→1.10), 0.5s cross-dissolves.
- **Captions:** `render_captions.py` (Playwright + pre-installed Chromium) renders the three
  overlays from `captions.json` using the caption system in `Content Pipeline/VIDEO_CAPTION_SYSTEM.md`
  — TikTok Sans / white pill / burgundy `#6E1B2D` keyword. Fonts bundled in `fonts/` (OFL).
- **Composite:** each caption alpha-faded in/out on the beat, overlaid on the base.
- Chromium path: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. ffmpeg via imageio-ffmpeg.

On-screen throughline (Freya · Alan): **one → theirs → only** — beat 3 completes the hook's sentence.
Silent master — add licensed audio per platform at post time. Gates before publishing: PII tag,
AI-content disclosure, audio licensing (see VIDEO_CAPTION_SYSTEM.md "Caveats").
