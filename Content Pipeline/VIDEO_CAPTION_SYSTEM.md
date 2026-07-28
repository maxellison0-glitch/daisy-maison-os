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

> **Two registers — pick per piece.** §1–3's white-pill / TikTok-Sans system is
> the **native-creator register**: punchy process/UGC clips where reading fast
> matters more than mood. It is *not* the default for warm, editorial, candlelit
> pieces — for those, use the **warm-editorial register** (cream serif, top-third,
> no box) proven out in *First reel — DS gift reveal hook* below. The burgundy
> keyword pill is **retired for the warm-editorial register**; burgundy lives on
> the physical product and website, not as a caption chip on mood footage.

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

> **v2 — hard reset.** Max's verdict on v1: "still shit." He's right, and we own
> the deeper failure: we *passed* our own captions instead of critiquing them.
> This section is rebuilt from scratch against the new **Taste gate**
> (`Personas/VOICE_AND_CAPTION_GUIDE.md`). The copy (*one → theirs → only*)
> survived — it wasn't the problem. The **look** did not.

### Honest critique of v1 (we agree with Max, with reasons)

- **The burgundy `#6E1B2D` keyword pill "looks a bit shit" — agreed.** A saturated
  wine-coloured pill sitting on warm candlelit footage is two different worlds
  colliding: the footage is soft, tonal, low-contrast; the pill is a hard,
  high-saturation UI chip. It reads like a sticker slapped on a mood photo. On a
  reveal whose whole job is atmosphere, a solid coloured box is the single most
  atmosphere-killing thing you can add. **Retired for this aesthetic** (see below).
- **White pill + black text is "basic and doesn't match the aesthetic" —
  agreed.** It's the TikTok-default look. It's legible, which is why it's
  everywhere, and "everywhere" is exactly the problem for a premium boutique. A
  bright white box also punches a cold rectangle into a warm cream/amber frame —
  it fights the palette instead of belonging to it.
- **The fonts don't suit the video — agreed.** TikTok Sans / Poppins are correct
  for a *native-creator* register, which is the opposite brief to a *warm,
  editorial, premium* one. They're clean and modern; this world wants elegant and
  intentional. Right fonts, wrong film.
- **Placement is lazy — agreed, and this is the real lesson.** Dead-centre-bottom,
  slapped over the product, is the default you reach for when you *haven't decided*
  where text should go. In an aesthetic reveal the text should live in the frame's
  negative space and never cover the hero object. "Just learn where to place them"
  is the correct note.

Nothing here is "sure, it does the job." It doesn't. Rebuilt.

### What the research actually says (placement + type)

**Placement — premium/editorial, not generic-viral.**
- Aesthetic and luxury/lifestyle creators put text in the **top third or in
  deliberate negative space**, not centred over the subject — clearing the centre
  and upper area for type is the standard editorial move (MindStudio; CreatorFlow;
  DigitalZoomStudio, 2026).
- **Both-platform safe band (verified, 2026):** IG Reels safe area is ~1010×1280,
  inset **220px top / 420px bottom**; TikTok reserves **~130px top, ~484px bottom,
  ~140px right, ~44px left** (Kreatli; TryMyPost; ignitesocialmedia). The
  intersection that survives both, plus the right-hand action rail, is roughly
  **x: 96–940, y: 260–1420**. The old "centre-bottom y≈1180 over the product" sat
  technically inside that band but visually *on* the hero — safe ≠ good.
- Practical rule this gives us: **place text over the darkest, emptiest quadrant
  of each specific frame**, footage-aware, never over the bottle, the flame or a
  fairy light. Placement is a per-beat decision, not a fixed anchor.

**Type — what reads "expensive and intentional" vs "TikTok default."**
- Editorial/premium reels lean on either a **high-contrast display serif** or a
  **very refined, wide-tracked sans in small sizes**; minimal or no box; tonal
  rather than stark colour (Kimp; JustCreative; ym-graphix, 2026). Real
  Google-Fonts options, judged for *this* candlelit world:
  - **Fraunces** (OFL) — a "soft" high-contrast serif with an optical-size axis
    and a little warmth/wonk. **Fits best:** elegant and characterful without
    being cold, and the opsz axis keeps it crisp at display size on mobile. Our
    primary recommendation.
  - **Cormorant Garamond** (OFL) — gorgeous, delicate, genuinely luxurious.
    **Risk:** very fine strokes disappear over bright candlelight on a small
    phone; usable only large, with a scrim, and even then it's the legibility
    gamble of the set.
  - **Playfair Display** (OFL) — classic fashion-masthead high contrast.
    **Fits**, but it's become a slightly default "elegant" choice; fine as a hero
    word, less as a whole system.
  - **Jost** (OFL) — geometric, Futura-lineage sans. In light weight, ALL-CAPS,
    widely tracked and *small*, it's the "quiet fragrance-ad" look. **Fits** the
    minimal-luxury register and is the safest for legibility.
  - **DM Sans / EB Garamond** — good supporting players (a tracked sans subline
    under a serif hero), not leads.
  - **Not this world:** Didot/Bodoni (too cold/fashion-hard for cosy), Bebas
    (shouty), and anything rounded or novelty.
- **Colour:** stark `#FFFFFF` is part of what makes v1 basic. Go **tonal warm
  off-white / cream** so the text belongs to the candlelight instead of punching
  through it. **No box**; if a bright frame threatens legibility, use a
  *whisper* gradient/radial scrim, never a solid chip.

### Three distinct directions for THIS reel (render these as visual comparisons)

Copy is identical across all three — *one → theirs → only* — so the comparison is
purely about **look and placement**. Colours are new warm-palette tokens:
`--cream: #F5EFE6`, `--ivory: #FAF6EF`, `--warm-shadow: rgba(20,12,8,0.28)`.
**The burgundy pill is retired for this aesthetic** (burgundy stays where it
belongs — the physical product: label, ribbon, packaging — and on the website).

---

**Direction A — "Editorial Cream" (refined serif, top-third, no box).** *The
magazine-cover option.*
- **Font:** Fraunces, weight **500** (opsz ~72 if the axis is available), the
  final line in **italic 500** as a signature. `letter-spacing: +0.01em`.
- **Size:** 58px body; the beat-3 line 66px.
- **Colour:** `--cream #F5EFE6`. No fill.
- **Placement:** **top third, centred**, block top at **y≈300**, within x:
  120–960. Product lives in the lower two-thirds, untouched.
- **Box/scrim:** none by default; if candle blowout hurts a frame, add a top
  scrim `linear-gradient(180deg, var(--warm-shadow) 0%, transparent 44%)` only.
- **Animation:** slow **fade-up** — opacity 0→1 + translateY 14px→0 over
  **500ms** ease-out; fade-out 300ms. No scale, no pop.

**Direction B — "Fragrance Minimal" (light sans, small caps, lower-side).** *The
quiet-luxury option.*
- **Font:** Jost, weight **300**, **ALL CAPS**, `letter-spacing: +0.22em`.
- **Size:** small — **34px**. Understatement is the whole point.
- **Colour:** `--ivory #FAF6EF`. Optional 1px cream hairline rule above the line
  for editorial structure.
- **Placement:** **lower-left negative space, left-aligned**, x=**110**, baseline
  **y≈1360** (single line; clears TikTok's 484px bottom reserve and the right
  rail). Sits *beside/below* the product's empty space, never over it.
- **Box/scrim:** none. Relies on placement over a dark area for contrast.
- **Animation:** pure **fade**, 600ms. Zero movement — stillness is the flex.

**Direction C — "Cinematic Serif Pair" (serif hero + tracked sans subline).**
*The perfume-film option, most designed / highest risk.*
- **Font:** hero word in **Cormorant Garamond 600** at **104px**; subline in **DM
  Sans 400**, small caps, `+0.18em`, **30px**.
- **Colour:** both `--cream #F5EFE6`.
- **Placement:** **upper-centre**, hero baseline **y≈420**, subline **y≈520**.
- **Box/scrim:** soft **radial** scrim behind the hero
  (`radial-gradient(closest-side, var(--warm-shadow), transparent)`) — Cormorant
  is too fine to survive candlelight without it.
- **Animation:** hero **letter-spacing settle** (+0.06em → +0.02em) + fade over
  **700ms**; subline fades in at +150ms. Slow, filmic.
- **Flag:** two typefaces + a very fine serif = the highest legibility and
  "trying too hard" risk of the three. Include it in the comparison, but it has
  to earn its place.

### The argument, and the pick (real, not fake-agreed)

**Freya (taste):** Direction A. It's the one I'd actually be proud to post.
Fraunces in cream, up in the top third, no box — it reads like a real boutique
brand shot a little film, not like a creator ran auto-captions. It gets out of
the product's way and lets the reveal breathe, and the italic final line lands
*The one and only* like a signature under the glowing monogram. B is beautiful
but so quiet it risks saying nothing on the first post, when we still need to
*land* a hook. C is lovely and I don't trust it — two fonts is one more thing to
get wrong on day one.

**Alan (performance/realism):** I'll push back on A before I agree to it. My
worry isn't taste, it's **legibility at the conditions people actually watch in**
— small, sound-off, mid-scroll, over *flickering* candlelight. A high-contrast
serif in low-contrast cream is the exact combination that vanishes over a bright
flame, and if the hook can't be read in ~1.5s the completion curve dies and the
whole reveal is wasted. On pure numbers I'd take **B** (Jost is the most legible
and the most obviously premium-minimal) — but I accept B may under-hook a *first*
post. And one point that lands on *my* side of the table too: IG down-ranks
majority-text reels, so the minimal, get-out-of-the-way direction is also the
*algorithmically* correct one. Less text, placed well, is the performance call as
well as the taste call.

**Resolution — we pick Direction A, with Alan's guardrails baked in (not a
fake-agree):** Freya's direction wins because a *first* post has to have taste and
has to hook, and A does both. Alan's legibility objection is real and is fixed by
spec, not ignored: (1) Fraunces at **500, not a light weight**; (2) cream held at
full opacity, and the **top scrim is mandatory, not optional, on the candlelit
beats** (2 and 3) — a whisper of `--warm-shadow`, enough to guarantee contrast
over a flame without becoming a box; (3) text placed over each frame's **darkest
quadrant**, checked per beat; (4) hard legibility test before ship — **read it at
30% size, sound-off, on a phone**; if you can't, it fails. Alan genuinely wanted
B; he's conceding the direction *on the condition these hold*. If the 30% test
fails on beat 3, we fall back to B for the whole set rather than ship something
unreadable.

### Chosen spec — Direction A, per beat

| Beat | Frame | On-screen line (Fraunces 500 cream, top-third) | Placement | Timing |
|---|---|---|---|---|
| 1 | Closed box + tag | **The one that doesn't end up in a drawer** | top-third centred, y≈300; place over the darker upper area, clear of the tag | 0.0 – 2.0s, fade-up |
| 2 | Open, nestled | **Handmade, and actually theirs** | top-third centred, y≈300; **top scrim on** | 2.0 – 3.9s, fade-up |
| 3 | Standing, glow | ***The one and only*** (italic) | top-third centred, y≈300, sitting *above* the standing bottle so the eye runs text → glowing DS monogram; **top scrim on** | 3.9 – 6.0s, fade-up, hold last ~0.6s |

No burgundy on-screen anywhere. Throughline still **one → theirs → only**, and
beat 3's italic line *is* the product's own name — overlay and object say the
same thing at the payoff. Match Law: opening "the **one** that doesn't end up in a
drawer" ↔ closing "*The **one** and only*" over the lit, displayed bottle — the
hook word and the payoff word are the same word.

### Motion — must pass the AI-slop gate (this is why v1 was called slop)

The captions were only half of Max's verdict; the other half was "still images
turned into video and they weren't still, they were vibrating." Non-negotiable
for this reel, per the Taste gate motion checklist:
- **No ffmpeg `zoompan` / Ken-Burns on the stills.** A fake slow pan over a flat
  photo is exactly the tell. Either hold the frame genuinely still, or use *real*
  image-to-video motion.
- **Motion belongs only to what should move:** candle flicker, fairy-light
  shimmer, a faint drift of scent-haze. The **bottle, box, reeds and personalised
  label stay pixel-stable** — any warp/morph of the label is an instant reject on
  a personalisation brand.
- Standard: **"could this pass as filmed?"** If a beat wobbles, cut it or reshoot
  the motion; a clean static hero beats a vibrating "animated" one every time.

### Caption + first comment (unchanged — copy wasn't the problem)

**Caption (Freya):**
> Some gifts get opened once and forgotten in a drawer. This one gets a spot on
> the shelf — and stays lit. A personalised reed diffuser, handmade to order,
> with the wording that's actually theirs. 🤍
>
> If you're buying for the couple who "have everything", this is the one that
> lands. Which name would you put on it? 👇

**First comment (hashtags, Alan):**
> #personalisedgifts #reeddiffuser #homefragrance #giftreveal #weddinggift
> #anniversarygift #thoughtfulgift #giftideas #uksmallbusiness #giftinspo
> #homedecor #newhomegift

### Caveats before this renders (propose-only)

- **PII — the tag.** The DS gift shots carry a handwritten kraft tag
  *"With love, Shelby & Sean x"* — flagged in `projects/diffuser/README.md` as
  possibly a **real order**. If beat 1 shows that tag legibly, do **not** publish
  as-is: re-shoot / re-label with a neutral or clearly-sample tag first (we never
  AI-edit a name onto a real bottle). Safest: keep the tag soft / partly out of
  focus so it reads "handwritten and personal" without publishing a real name.
- **AI disclosure.** DS images are AI-restaged; apply each platform's AI-content
  disclosure before publishing, per `PLATFORM_STRATEGY.md`.
- **Audio.** Warm/cosy licensed audio, re-selected *per platform*.
- **No fabricated claims** — no invented review, stock or delivery promise.

### Research sources (this section)

- Kreatli — *Instagram Reels Safe Zone (2026)* & *TikTok Safe Zone (2026)*
  (kreatli.com/guides) — the 220/420 and 130/484/140/44 inset figures.
- TryMyPost — *IG Reels Safe Zones & Text Placement 2026*; ignitesocialmedia —
  *Safe Zones for TikToks and Instagram Reels*.
- MindStudio (*AI image gen for social* — clearing centre/top-third for text);
  CreatorFlow (*Instagram Aesthetic playbook*); DigitalZoomStudio (*Text overlays,
  2026*) — editorial/negative-space placement.
- Kimp, JustCreative, ym-graphix (2026) — luxury/aesthetic serif vs refined-sans
  type direction. Font *choices and rationale for this candlelit world are our
  own call*, not lifted from any single article.

*Couldn't independently verify:* on-screen behaviour of these exact fonts over
this exact footage at phone size — that's what the 30%/sound-off render test and
the visual A/B/C comparison are for. No competitor posts or metrics invented.

— Freya · Alan
