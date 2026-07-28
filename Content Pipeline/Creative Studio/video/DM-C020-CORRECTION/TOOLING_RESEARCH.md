# What's worth installing, and what we already own

Max, 28 Jul 2026, asked for a proper survey before building anything else:
*"GitHub skills: video effects, graphics effects, sound effects, photoshop
effects… On competitors, again, let's go to GitHub… Let's do some proper
research. Let's get this right and then implement them directly into this
project so we don't just waste time."*

**First pass of this file concluded "almost nothing needs installing." Max:
*"disappointing, no external skills added."* He was right and the survey was
too thin — it searched for *Claude skills* and stopped, when the useful thing
was ordinary open-source tooling. Second pass added four packages and one of
them broke a limit this repo had written down as permanent.** Section 0 is the
result; the rest is the original survey, still accurate on its own terms.

---

## 0. INSTALLED, and what each one bought

| Package | What it unlocked | Verified |
|---|---|---|
| **`yt-dlp`** | **per-post TikTok views, likes, captions, dates — with no login** | 9 posts off @daisymaison, views 3–796 |
| **`yt-dlp`** | **downloading any public post so its frames can be LOOKED at** | pulled the Bond turnaround, 5-frame sheet |
| `gallery-dl` | Instagram/TikTok media fetch, second route if yt-dlp's breaks | installed, 1.32.8 |
| `pedalboard` | real audio effects (Spotify's lib) for sound design beyond raw SFX | installed, 0.9.24 |

**The headline: `daisy-social-analytics` stated flatly that TikTok has no
per-post data and that a per-post TikTok figure must never be quoted. That is
now false, and the skill has been corrected.** `yt-dlp`'s extractor reads the
same metadata the web player uses. New tool:
`Content Pipeline/tools/social_api/tiktok_posts.py`.

**It also closes the gap section 4 called unclosable.** `look` downloads a post
and renders a contact sheet, so a competitor's content can be judged on how it
*looks*, not only on what it *earned*.

**Two failures worth keeping:**
- **Do not install `curl_cffi` / yt-dlp's impersonation extra.** It does its own
  TLS handshake and this container's agent proxy resets it — every request died
  with `curl: (35) Recv failure`. Installed, broke everything, removed.
- **`rembg` did not install cleanly** (needs an onnxruntime extra). Not pursued,
  because nothing currently needs background removal.

**A `0` like count means "not returned", not "no likes"** — missing on 3 of 9
posts, present on the rest. Views were present on every post.

---

---

## 1. Sound effects — SOLVED, and it was already here

`.agents/skills/media-use` is installed and its doctor reports
**19 bundled SFX assets available** with no network and no login:

```
sparkle  key-press  typing  whoosh  whoosh-cinematic  whoosh-short  chime
error  glitch-1/2/3  impact-bass-1/2  notification  click  click-soft
pop  riser  ping
```

Three of them are now in the video. Nothing was downloaded and nothing was
generated.

**The one real gotcha, measured not guessed.** These mp3s carry leading silence
before their transient:

| file | length | transient at |
|---|---:|---:|
| `whoosh-short.mp3` | 0.57s | **0.123s** |
| `pop.mp3` | 0.72s | **0.117s** |
| `click-soft.mp3` | 0.37s | 0.052s |

`adelay` positions the *file*, not the *sound*. Delay by the cue and every hit
lands ~0.12s late, which reads as sloppy sync rather than as a bug. **Always
subtract the file's own transient offset.** `build_v2.py` does this and the
onsets now measure at exactly 0.25 / 1.35 / 2.20 against a 0.25 / 1.35 / 2.20
intent.

## 2. Music — blocked here, and the platform is the better answer anyway

**Local generation is not possible in this container.** No GPU
(`nvidia-smi` absent), 4 CPUs, 15GB RAM. The 2026 open-source options all need
one:

| Model | Licence | Why not |
|---|---|---|
| [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) | open | needs CUDA/Metal; <2s/song on an A100, unusable on 4 CPU cores |
| MusicGen (Meta Audiocraft) | commercial-use OK | GPU, multi-GB weights |
| [YuE](https://github.com/multimodal-art-projection/YuE) | Apache 2.0, credit required | GPU |
| Stable Audio Open | **non-commercial research licence** | licence alone rules it out for a shop |

`media-use` also exposes a **10,000+ track BGM catalog** via the HeyGen CLI —
but that needs `heygen auth login --oauth`, an interactive browser sign-in this
session cannot perform. **That is the one genuinely worth setting up**, and it
needs Max at a keyboard once.

**Even with all that working, the trending sound picked at upload is the better
call for TikTok** — the platform boosts its own audio and a bundled bed does not
get that. Music is for the cases where the post must work silent-first.

## 3. Video / graphics / "Photoshop" effects — nothing worth adding

Surveyed the current lists — `awesome-claude-skills`, `awesome-claude-code`,
`rohitg00/awesome-claude-code-toolkit`, `daymade/claude-code-skills` — and the
one directly on-topic repo:

**[wilwaldon/Claude-Code-Video-Toolkit](https://github.com/wilwaldon/Claude-Code-Video-Toolkit)** (MIT).
Contains Remotion, Manim, a YouTube clipper, Playwright screen recording and an
ffmpeg skill. **Verdict: do not install.**
- No sound-effect generation, no music, no caption animation, no competitor
  research — all four things actually wanted.
- Its captions are **ffmpeg `drawtext`**, which is precisely the flat,
  square-cornered, Arial look `VIDEO_CAPTION_SYSTEM.md` was written to replace.
  Installing it would be a downgrade.
- Remotion is React-to-MP4; this repo already standardises on HyperFrames.

**We already have the effects lane and it is bigger than anything on offer:**
`.agents/skills/` carries `hyperframes-*` (core, animation, keyframes,
creative, registry, cli), `motion-graphics`, `motion-doctrine`, `cut-the-curve`,
`seam-craft`, `media-use`, `embedded-captions` and `captions-overlay`. The gap
was never tooling. It was that none of it had been pointed at this video.

For raster work, PIL + ffmpeg filters already cover it — `build_v2.py` does
sub-pixel slides, eased scaling, rotation and alpha ramps in ~150 lines with no
new dependency. **A free Photoshop was not needed; a timeline was.**

## 4. Competitor research — the blocker is not tooling

`Content Pipeline/tools/social_api/ig_public.py` already reads any public
Instagram profile with no login: followers, post count, and the last twelve
posts with likes, comments and captions.

**The blocker is Instagram's rate limit.** A competitor pull on 28 Jul returned
429 immediately, which per `daisy-social-analytics` lasts hours. Installing a
scraper makes this *worse*, not better — the skill's own measured finding is
that library scrapers page on your behalf and burn the day's budget in seconds.

**And there is a limit worth naming plainly: the tool returns numbers and
captions, never images.** It can say what a competitor's post *earned*. It can
never say whether it *looked* better. Answering "are competitors more aesthetic
than us" needs eyes on their grids — a different job, and one no scraper does.

## 5. What actually got implemented today

| | |
|---|---|
| `ffmpeg` symlinked to `/usr/local/bin` | `media-use` and every other skill assume it on PATH; it only existed inside `imageio_ffmpeg` |
| `build_v2.py` | full per-frame timeline: staggered pills, eased slides, SFX with transient compensation, optional loop ramp |
| `pills.html` | pills rendered as separate transparent PNGs so they can be animated independently |

## 6. The one thing that needs Max

**`heygen auth login --oauth`**, once, to unlock the 10k-track BGM catalog and
the TTS path in `media-use`. It is the only item in this survey that is both
worth having and impossible to do from here.
