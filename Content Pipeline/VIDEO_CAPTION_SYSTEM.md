# Video Caption System — on-screen text for Reels & TikTok

**Status:** proposal, ready to ship. Written for our own Playwright + Chromium
caption renderer (HTML/CSS composited over video with ffmpeg/libass), so every
value below is CSS-replicable. Nothing here posts, buys, or signs up for
anything — it's a spec.

**What this replaces:** the current finish scripts render captions with ffmpeg
`drawtext` — Arial Bold, `box=1:boxcolor=black@0.30` with square corners and a
heavy black border (see
`Creative Studio/active/DM-C017-synthetic-sign-turn/working/batches/video/v03-native-approved-pair/finish_native_reel.py`,
lines 89–119). That is *exactly* the flat, square-cornered, slightly-dated look
Max flagged on the old "Mr & Mrs" video: generic system font, hard border,
right-angle box. This system throws that out and moves to rounded pill captions
in a real native font, rendered in the browser where we have full control.

Research pass: 24 July 2026. Sources cited inline and listed at the bottom.

---

## 1. The caption style spec

### 1.1 Font — the single most important call

**Primary: TikTok Sans** (Google Fonts / TikTok's own GitHub, SIL Open Font
License 1.1). This is *literally* the typeface TikTok uses across its own app UI
and branding. TikTok open-sourced it in July 2025 specifically so creators can
use it in external editors; it's free for commercial use, supports 75 languages,
and the only restrictions are the normal OFL ones (don't sell the font file,
don't rename a modified copy "TikTok Sans", keep the licence text with any
embed). Nothing reads more *native and current* to the platform than the
platform's own font — and because it's a real, professionally-drawn typeface
(Grilli Type / Contrast Foundry / Type Network), it never reads "AI-made" or
template-generic the way a novelty font does. Use weight **800 (ExtraBold)** for
captions, **900 (Black)** for one-word hero hits.

**Warm alternate: Poppins** (Google Fonts, OFL). Slightly rounder, softer
letterforms than TikTok Sans — use this variant when a piece wants the
friendlier, "bubblier" register (gift-reveal, family/wedding warmth) rather than
the crisp TikTok-native register. Weight **600–700**. Poppins is geometric and
premium without being the single most over-used caption font on the internet.

**Safe fallback: Montserrat** (Google Fonts, OFL). Only as a system fallback in
the font stack if a glyph is missing — not a first choice. It's competent but
it's the "default creator font," so leaning on it is part of what makes captions
look same-y. Keep it in the stack, off the stage.

**Deliberately not used:** Arial / Helvetica (the current dated look), Bebas Neue
(all-caps condensed reads shouty and 2019), Impact, and anything with a "hand-
written" or "quirky" novelty feel — those are the fonts that date a video and
read AI-made.

> Rounded *feel* comes from the pill box + heavy weight, not from a childish
> rounded font. That's how current creators get "bubbly and grounded" while
> still looking premium.

### 1.2 Colours (on-palette: black / burgundy / white)

| Token | Hex / value | Use |
|---|---|---|
| `--ink` | `#0E0E0E` | Black caption text (on white/light pill). Near-black, not pure `#000`, to sit naturally over video |
| `--paper` | `#FFFFFF` | White caption text (on dark/burgundy pill or over dark footage) |
| `--pill-white` | `rgba(255,255,255,0.94)` | White pill fill — the default caption box |
| `--pill-dark` | `rgba(14,14,14,0.80)` | Dark frosted pill fill — for light/busy footage |
| `--burgundy` | `#6E1B2D` | Brand burgundy — keyword-highlight pill fill (white text on it) |
| `--burgundy-pop` | `#8A2338` | Slightly brighter burgundy for a keyword rendered as *text* (not a pill) so it stays legible over video |

No grey. Text is always `--ink` or `--paper`; the only accent is burgundy. That
is the whole palette — restraint is the brand.

### 1.3 Pill / rounded-box treatment

- **Corner radius:** single-line captions and word-pops → **fully rounded**
  (`border-radius: 999px` — a true pill). Two-line blocks → **`22px`** rounded
  rectangle (still soft, never square).
- **Padding:** `0.24em` top/bottom, `0.60em` left/right (at a 64px caption that's
  ~15px / 38px). Enough breathing room to read as a deliberate "grounded" box,
  not a tight sticker.
- **Background opacity:** `0.94` for the white pill (near-solid, premium, high
  contrast), `0.80` for the dark frosted pill. Add `backdrop-filter: blur(6px)`
  on the dark pill so busy footage behind it reads as soft frost, not mush.
- **Shadow (subtle, not "drop-shadow mush"):** one soft, tight box-shadow on the
  pill only — `0 4px 14px rgba(0,0,0,0.16)`. This lifts the pill off the video a
  hair. **No text-shadow when a pill is present** — the pill is the contrast, so
  a text shadow on top is exactly the blurry "mush" to avoid.
- **Stroke:** none on pill captions. Only the no-pill hero word (§1.5) gets a
  crisp stroke, via `paint-order: stroke`, never a blurred outline.

### 1.4 Size, weight, placement, safe margins (9:16, 1080 × 1920)

- **Body caption:** `font-size: 62px`, weight `800`, `line-height: 1.12`,
  `letter-spacing: -0.01em`. Max **2 lines**, 3–5 words per line.
- **Hook / top line:** `font-size: 78px`, weight `800–900`.
- **One-word hero hit:** `font-size: 132px`, weight `900`, `letter-spacing:
  -0.02em`.
- **Case:** sentence case or Title Case — **not** shouty all-caps. All-caps is
  part of the dated/aggressive look; reserve caps for a single short hero word if
  ever.
- **Safe margins:** side inset **80px** each edge (keep text inside x: 80–1000).
  Vertical safe band **y: 250 → 1430** (matches the y=360–1430 primary-copy zone
  already set in `PLATFORM_STRATEGY.md`). Bottom-anchored captions sit around
  **y ≈ 1180–1300** so they clear the platform UI: TikTok's right-hand action
  rail + caption/handle overlay eats roughly the bottom **420px** and the left
  ~just above it; Instagram Reels eats roughly the bottom **360px**. Never place
  copy below y=1500.

### 1.5 The "pop-on word" / auto-caption style

This is the current native default on both platforms — speech transcribed and
revealed **word-by-word (or short phrase), the spoken word highlighted as it's
said** ("karaoke"). Our version, on-brand:

- Base transcript sits in a **white pill, `--ink` text**, one short phrase at a
  time.
- The **active/spoken word** gets the **burgundy pill** (`--burgundy`, white
  text) *or* flips to `--burgundy-pop` coloured text — one keyword lit at a time,
  never a rainbow.
- Motion: each phrase **scale-pops in** from `0.86 → 1.0` over ~120ms with a
  slight ease-out; no bounce, no spin, no typewriter. Understated motion is the
  premium tell.
- Keep it to **one highlighted keyword per phrase** — the word that carries the
  meaning ("*surname*", "*same day*", "*their reaction*").

---

## 2. Drop-in CSS for the Playwright renderer

Copy-paste ready. Bundle the two `woff2` files locally in the renderer's fonts
dir (download TikTok Sans from Google Fonts or `github.com/tiktok/TikTokSans`,
Poppins from Google Fonts) and `@font-face` them — don't depend on a live CDN at
render time.

```css
@font-face {
  font-family: "TikTok Sans";
  src: url("./fonts/TikTokSans-ExtraBold.woff2") format("woff2");
  font-weight: 800; font-style: normal; font-display: block;
}
@font-face {
  font-family: "TikTok Sans";
  src: url("./fonts/TikTokSans-Black.woff2") format("woff2");
  font-weight: 900; font-style: normal; font-display: block;
}
@font-face {
  font-family: "Poppins";
  src: url("./fonts/Poppins-SemiBold.woff2") format("woff2");
  font-weight: 600; font-style: normal; font-display: block;
}

:root {
  --ink: #0E0E0E;
  --paper: #FFFFFF;
  --pill-white: rgba(255, 255, 255, 0.94);
  --pill-dark: rgba(14, 14, 14, 0.80);
  --burgundy: #6E1B2D;
  --burgundy-pop: #8A2338;

  --caption-font: "TikTok Sans", "Poppins", "Montserrat", system-ui, sans-serif;
  --warm-font: "Poppins", "TikTok Sans", "Montserrat", system-ui, sans-serif;
}

/* 1080x1920 stage. Everything positioned inside the safe band. */
.stage {
  position: relative; width: 1080px; height: 1920px;
  font-family: var(--caption-font);
  -webkit-font-smoothing: antialiased; text-rendering: geometricPrecision;
}

/* Horizontal safe zone: 80px each side. */
.caption-layer {
  position: absolute; left: 80px; right: 80px;
  display: flex; flex-direction: column; align-items: center; gap: 14px;
  text-align: center;
}
.caption-layer.bottom { top: 1180px; }   /* clears TikTok/Reels UI */
.caption-layer.top    { top: 250px;  }

/* --- Default caption: white pill, black text --- */
.pill {
  display: inline-block;
  font-weight: 800;
  font-size: 62px;
  line-height: 1.12;
  letter-spacing: -0.01em;
  color: var(--ink);
  background: var(--pill-white);
  padding: 0.24em 0.60em;
  border-radius: 999px;              /* 22px for guaranteed 2-line blocks */
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16);
  max-width: 100%;
}
.pill.block { border-radius: 22px; }  /* multi-line variant */

/* --- Dark frosted variant: white text, for light/busy footage --- */
.pill.dark {
  color: var(--paper);
  background: var(--pill-dark);
  -webkit-backdrop-filter: blur(6px);
  backdrop-filter: blur(6px);
}

/* --- Hook (top line) --- */
.pill.hook { font-size: 78px; }

/* --- Keyword highlight: burgundy pill, white text --- */
.kw {
  color: var(--paper);
  background: var(--burgundy);
  padding: 0.12em 0.34em;
  border-radius: 999px;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
/* Alt: keyword as coloured text only (no pill), still legible over video */
.kw-text { color: var(--burgundy-pop); }

/* --- One-word hero hit (no pill): crisp stroke, never a blur --- */
.hero-word {
  font-weight: 900;
  font-size: 132px;
  letter-spacing: -0.02em;
  color: var(--paper);
  -webkit-text-stroke: 3px rgba(14, 14, 14, 0.85);
  paint-order: stroke fill;          /* stroke behind fill = crisp edge */
}

/* --- Pop-on word animation (understated scale, no bounce) --- */
@keyframes wordPop {
  from { opacity: 0; transform: scale(0.86); }
  to   { opacity: 1; transform: scale(1.0); }
}
.word {
  display: inline-block;
  animation: wordPop 120ms ease-out both;
}
.word.active { /* the spoken word: light it burgundy */
  color: var(--paper);
  background: var(--burgundy);
  padding: 0.10em 0.30em;
  border-radius: 999px;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}

/* Warm register (gift/wedding reveals): swap the font family on the pill */
.pill.warm { font-family: var(--warm-font); font-weight: 600; }
```

Minimal markup examples:

```html
<!-- Bottom caption with a burgundy keyword -->
<div class="caption-layer bottom">
  <span class="pill">Street signs with your actual <span class="kw">surname</span></span>
</div>

<!-- Word-by-word pop-on (active word lit) -->
<div class="caption-layer bottom">
  <span class="pill">
    <span class="word">Packed</span>
    <span class="word active">same&nbsp;day</span>
  </span>
</div>

<!-- One-word hero hit over the reveal moment -->
<div class="caption-layer" style="top:820px">
  <span class="hero-word">theirs.</span>
</div>
```

---

## 3. External tools shortlist (the real apps creators use)

Verdict up front: **keep our own CSS pipeline as primary** — it's the only route
that gives us exact burgundy, exact pill radius, zero watermark, zero per-video
cost, and it already fits the Playwright/ffmpeg infra we built. The tools below
matter as a **backup** and as a reference for the look.

| Tool | Look it produces | On-brand fit | Rough cost (2026) | Fits our workflow? |
|---|---|---|---|---|
| **CapCut** | The definitive native TikTok/Reels caption look; huge library of pill/word-pop styles; now supports **TikTok Sans** | Good — can get very close to our spec by hand, but brand burgundy + exact radius is fiddly to lock per video | **Free**, no watermark on export (mobile & desktop) | Manual, off-pipeline; great as a backup or for one-offs |
| **Submagic** | Best-in-class animated word-by-word "creator" captions, one-click styled | Good look, weak brand-precision — palettes are preset-driven, not our exact hex | ~**$12/mo** Starter, ~$23/mo Pro (annual) | Off-pipeline, subscription; the "if we ever want fancy animation without building it" option |
| **Captions (the app)** | Polished mobile-first auto-captions, strong "talking-head" styles | Fine, but mobile-only and less brand control; billing friction | ~**$10–25/mo** | Off-pipeline, mobile; not a fit for a repo-driven workflow |
| **Veed** | Clean browser captions, team/collab features | Neutral; corporate-clean rather than warm-native | ~**$10–24/mo** (watermark on free) | Browser-based, team tool; overkill for us |
| **Typito** | Template/brand-kit driven lower-thirds & captions | Brand-kit is nice, but templates read more "marketing video" than native-native | ~**$16–50/mo** | Off-pipeline; not native enough |
| **Canva** | Has caption/text + Brand Kit; good for static/carousel too | Decent for stills; caption animation is generic | ~**$13/mo** Pro | We already may use it for carousels; not for Reel captions |
| **Native in-app (IG/TikTok caption tool)** | The *most* native look by definition; TikTok "Classic" style | Most-native, least control — no burgundy, no brand lock, and it re-encodes | **Free** | Last-resort only; also risks the platform stamping its own styling |

**Recommendation:**
- **Primary → our own Playwright/CSS renderer** using §1–2. Full brand control,
  on-palette, no watermark, no cost, version-controlled with the rest of the
  pipeline.
- **Backup → CapCut (free)**. When the pipeline is unavailable or a piece needs a
  fast hand-edit, CapCut + TikTok Sans + a white pill + black text + a burgundy
  keyword gets us ~90% of the look at zero cost and no watermark.
- Park **Submagic** as the only paid tool worth a trial *later*, and only if we
  decide we want animated word-pop that's more elaborate than the understated
  scale-in built into our CSS.

---

## 4. Do / Don't — tuned to Daisy Maison

**Do**
- White pill + `--ink` black text as the default; dark frosted pill only when
  footage is too light/busy for white.
- One **burgundy** keyword per phrase — the word that carries the meaning.
- TikTok Sans ExtraBold (native register) or Poppins SemiBold (warm register).
- Fully-rounded pills; `22px` radius for any 2-line block.
- Understated scale-in pop (0.86→1.0); one soft box-shadow on the pill.
- Sentence/Title case; 3–5 words a line; max 2 lines.
- Keep copy in y: 250–1430, 80px side margins; bottom captions at y≈1180–1300 to
  clear the UI.

**Don't**
- No **grey** text, ever. Only ink / paper / burgundy.
- No square-cornered boxes, no hard black border (that's the retired
  `drawtext` look).
- No blurred text-shadow "mush" behind pill text — the pill *is* the contrast.
- No all-caps shouting, no Arial/Helvetica/Bebas/Impact, no novelty or
  "handwritten" fonts.
- No rainbow of highlighted words, no bounce/spin/typewriter animation, no karaoke
  in three colours.
- No TikTok watermark carried onto a Reel/Short (already the house rule in
  `PLATFORM_STRATEGY.md`) — render from the clean master.
- Don't let a keyword pill and a hero word fight in the same frame; one focal
  element at a time.

---

### Sources checked

- TikTok for Developers — *TikTok Sans: Now a Free and Open-Source Font*
  (developers.tiktok.com/blog/tiktok-sans-open-source) — confirms OFL 1.1, free
  commercial use, on Google Fonts + GitHub.
- `github.com/tiktok/TikTokSans` — the official font repo (verified as the
  download/licence source; not deep-inspected file-by-file).
- CapCut — *10 Best Subtitle Fonts for Captions* (capcut.com/resource/subtitle-font).
- SendShort — *8 Best Fonts for TikTok: Subtitles & Text (2026)*.
- Reelwords — *Best Fonts for Captions (Reels, TikTok, Shorts) + Exact Settings*
  (note: gives font list and principles but **no** pixel/radius/opacity numbers —
  the concrete values in §1 are our own spec, not lifted from it).
- Blitzcut — *TikTok Caption Font: The Exact Fonts Used by Top Creators (2026)*.
- Caption-tool comparisons: aivideocut.com, designrevision.com, caption-x.com,
  zapcap.ai, quso.ai (pricing is directional 2025–2026 and will drift — treat as
  ballpark, re-check before any trial).

*Couldn't independently verify:* exact current subscription prices for every tool
in §3 (they change often and vary by annual/monthly and region) — figures are the
ranges reported across the comparison articles above, not confirmed on each
vendor's live pricing page. No competitor post metrics were used or invented.

— Freya · Alan

---

## First reel — DS gift reveal hook

**The piece:** DS "THE ONE AND ONLY" personalised reed diffuser, candlelit
gift-reveal, ~6s, three matched beats — (1) closed white blush-ribbon box +
handwritten tag, (2) box open, wood-wool straw + diffuser nestled, (3) diffuser
standing, candle + fairy-light glow throughout. Warm, cosy, premium, real.
This is the **first scheduled post**, so the hook has to be right, not clever.

### Freya's take (the scroll-stopper for frame 1)

Frame 1 is a closed box and a handwritten tag — that's an *emotional*, curiosity
frame, not a spec frame. So the hook should trade on a true feeling, land in
under ~1.7s, and quietly set up the payoff. Candidates:

1. **"The one that doesn't end up in a drawer."** — dry, British, a universal
   truth (everyone owns the drawer of forgotten gifts), and "the one" secretly
   seeds the product's own label, *The One and Only*.
2. **"Not another candle."** — punchy, sets a contrast the reveal pays off (it's
   a diffuser, and a personalised one), but it undersells the warmth.
3. **"Handwritten tag. So you know it wasn't a last-minute one."** — leans into
   the literal frame-1 detail and our "show the working" rule, but it's a beat
   too long for a 6s opener.

**Freya's pick → #1, "The one that doesn't end up in a drawer."** It's on-voice
(understatement over hype), it's a genuine shared truth so it earns the stop
honestly, and the word "one" rhymes forward into the payoff label. (Note: I've
deliberately avoided "regift" — it smuggles in gift-as-a-verb, which our own
cheat sheet bans.)

### Alan's take (retention, and what actually earns the save)

Two things bank on this reel: it needs a curiosity gap the *last* frame closes
(retention/completion), and it needs to be save- and send-worthy, because that's
IG Reels' top non-follower lever (DM sends) and a gift idea is inherently
sendable. My candidates, from the numbers angle:

1. **"For the couple who has everything."** — the classic high-save gift-solve
   frame (it's already hook #7 in the playbook); a direct "tag the person buying
   for them" trigger.
2. **"Closed box → this, in six seconds."** — pure retention, promises a payoff
   by the end. Risk: "wait for it" framing reads a bit dated/gimmicky, which is
   exactly the register Max is trying to leave behind.
3. **"This is what 'personalised' should actually look like."** — sets a
   standard the last frame (their name on the label) delivers.

**Alan's pick → #1**, but I'll concede the *on-screen* slot. Freya's line is the
stronger scroll-stop for an emotional frame-1; the "couple who has everything"
utility does more work in the **caption**, where saves are actually banked. So
my pick moves to the caption, not the overlay. That's the honest split, not a
fake consensus.

**Match Law — satisfied, and unusually tightly.** Opening hook "the **one** that
doesn't end up in a drawer" ↔ closing frame: the diffuser standing, lit, on
display — literally the opposite of a drawer — under its own label, *The **One**
and Only*. The hook word and the payoff word are the same word. That's the
tightest match we can get; the closing frame doesn't just pay the hook off, it
completes its sentence. Green light from me.

### Joint conclusion — postable-tomorrow spec

**On-screen text (pop-on friendly, one burgundy `#6E1B2D` word each):**

| Beat | Frame | On-screen line | Burgundy word | Timing (6s) |
|---|---|---|---|---|
| 1 | Closed box + tag | **The one that doesn't end up in a drawer** | **one** | 0.0 – 2.0s (line fully on by ~1.5s, hold on tag) |
| 2 | Open, nestled in wood-wool | **Handmade, and actually theirs** | **theirs** | 2.0 – 3.9s (rides the open/nestle motion) |
| 3 | Diffuser standing, glow | **The one and only 🤍** | **only** | 3.9 – 6.0s (text resolves *into* the product label over the DS monogram; hold last ~0.5s for the save) |

Throughline: **one → theirs → only.** By beat 3 the on-screen caption has become
the product's actual name, sitting over the glowing DS monogram — the overlay and
the object say the same thing at the payoff.

Render notes: white pill + `--ink` text on all three (warm footage, so white
pill reads premium; if the candle glow blows out the pill on beat 3, switch that
one to `.pill.dark`). Beat 1 and 2 bottom-anchored (`caption-layer bottom`,
y≈1180); beat 3 can sit slightly higher (y≈1000) so it frames the standing
bottle, not the base. Understated `wordPop` only — no bounce.

**Caption (Freya):**
> Some gifts get opened once and forgotten in a drawer. This one gets a spot on
> the shelf — and stays lit. A personalised reed diffuser, handmade to order,
> with the wording that's actually theirs. 🤍
>
> If you're buying for the couple who "have everything", this is the one that
> lands. Which name would you put on it? 👇

**First comment (hashtags kept out of the caption, Alan):**
> #personalisedgifts #reeddiffuser #homefragrance #giftreveal #weddinggift
> #anniversarygift #thoughtfulgift #giftideas #uksmallbusiness #giftinspo
> #homedecor #newhomegift

*(10–12, niche + reach mix; drop into the first comment so the caption stays
clean. Re-wrap per platform — TikTok leans the caption toward search intent
("personalised reed diffuser gift idea"), Instagram toward the DM-share prompt.)*

### Caveats before this renders (propose-only)

- **PII — the tag.** The DS gift shots carry a handwritten kraft tag
  *"With love, Shelby & Sean x"* — flagged in `projects/diffuser/README.md` as
  possibly a **real order**. If beat 1 shows that tag legibly, do **not** publish
  as-is: re-shoot / re-label with a neutral or clearly-sample tag first (and we
  never AI-edit a name onto a real bottle). Safest render: keep the tag soft /
  partly out of focus so it reads "handwritten and personal" without publishing a
  real customer's name.
- **AI disclosure.** The DS images are AI-restaged (Nano Banana Pro, surroundings
  only). If any beat is AI-generated, apply each platform's AI-content disclosure
  before publishing, per `PLATFORM_STRATEGY.md` — compliance step, not optional.
- **Audio.** Pick warm/cosy licensed audio *per platform* — TikTok-original
  commercial tracks are frequently unlicensed on Meta and can get the Reel muted.
- **Not sponsored / no fabricated claims.** No invented review, no "back in
  stock", no delivery promise in the caption.

— Freya · Alan
