# DM-C020 — The Correction, finished post

The first real video off the Alan + Freya office set. 4s, silent, 1080×1920.

Alan front, deadpan, holding `DAVE'S BAR` / *EST. 2019 - NO ENTRY WITHOUT
SNACKS*. Freya behind him holding the second sign from the same order:
`DAVE'S BAR` / *IT'S A SHED, DAVE*. The second sign is the punchline, so the
hook must not give it away.

---

## The footage

| | |
|---|---|
| Model | `seedance_2_0`, 4s, 720p, `mode: std`, `bitrate_mode: high`, silent |
| Start frame | `active/DM-C020-office-remodel/working/correction-01-daves-bar/outputs/take-02.png` (Max-approved) |
| Takes | 2 generated, **take-01 selected** |
| Credits | 36 (2 × 18) |
| Job ids | take-01 `5b4aba07-b5d3-4e5a-8733-ba7a3bb58c91` · take-02 `0c5395f2-f9ad-4873-97ad-6cc486ca70ff` |
| Raw | `raw/take-01.mp4`, `raw/take-02.mp4` |

**Why take-01.** Take-02 slowly pushes in — a camera move the prompt explicitly
forbade — and Alan's sign creeps toward the left edge as it does. Take-01 holds
the frame.

| Measured | take-01 | take-02 |
|---|---:|---:|
| Mean interframe delta (motion) | **1.59** | 0.87 |
| Closest edge gap, left / right | 112 / 68 px | 108 / 61 px |
| Framing gate | **PASS** | PASS |

Both wordings stay spelled correctly and readable on every frame of both takes.
That is the failure mode this format is most exposed to, and it did not happen —
because nothing rotates and nothing travels.

**The prompt lever that did it:** the motion brief was written as a list of
*small human actions* (an eye flick, a two-centimetre lift, weight shifting)
with the camera explicitly pinned, rather than as a camera instruction. Per
`OFFICE_SPEC.md`, constraints on the camera do not survive — so the camera was
described as not moving and all the motion was given to the people.

---

## The captions — two styles, rendered locally at zero credits

Both built to `Content Pipeline/VIDEO_CAPTION_SYSTEM.md`. Chromium renders a
transparent 1080×1920 PNG; ffmpeg composites it. No `drawtext`, no square
boxes, no Arial.

### Style A — TikTok native
TikTok Sans 800, white pill `rgba(255,255,255,0.94)`, `--ink` text, one burgundy
`#6E1B2D` keyword pill, 78px, fully rounded. Reads as the platform's own
caption. **Hook:** *same order. / both signs.*

### Style B — Documentary
Poppins 600, no pill, paper text with a 6px ink stroke via `paint-order`, 66px,
a short rule between the lines. Quieter, warmer, reads as a note rather than a
caption. **Hook:** *we just print / what they send.*

Style B's register is the one the account's best-performing post actually used —
`instagram-DPjdseCDbDR`, *"Customer of the year, probably"*, 11,889 views. The
brand reporting a customer, not selling to one.

### Placement

| Rail | y | Verdict |
|---|---|---|
| `top` | 270px | Clears the notch, sits in the top third. **Usable.** |
| `upper` | 430px | **Rejected — covers Alan's face.** Rendered only to prove it. |
| `low` | 1180px | Above TikTok's ~420px bottom UI band. **Usable.** |

Side inset 80px both edges, nothing below y=1500.

---

## Files

| | |
|---|---|
| `overlay.html` | the caption CSS, both styles |
| `render_overlays.py` | Chromium → 8 transparent overlay PNGs |
| `finish.py` | ffmpeg composite, upscales 720→1080 lanczos first |
| `finished/` | four cuts: A/B × top/low |
| `qc/CAPTION-STYLES.png` | six-up placement comparison |

`render_overlays.py` pins `executable_path` to
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome` — the bundled playwright
build is newer than the browser on this image and its default path is wrong.

---

## Not done

- Max has not picked a style, hook or placement.
- Nothing is posted. No caption copy written for the post body itself.
