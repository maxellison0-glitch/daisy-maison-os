# Video from HTML — the zero-credit motion lane

Every video in here is written as an HTML file and rendered to MP4 locally. No
generation credits, no footage, no camera. **Max does not film, so the only
motion this brand can afford at volume is motion applied to stills it already
owns** — a push-in on an approved plate, a hook that arrives, an end card that
lands. That is what this lane is for.

Built on [HyperFrames](https://github.com/heygen-com/hyperframes) (Apache 2.0),
vendored into `.agents/skills/`.

## What it replaced

Before this, an on-screen hook was a PNG burnt into a still by a Python script
(`house-carousel/build.py`) — static, one frame, no timing. On 28 Jul a
carousel shipped with **no hooks at all**, because burning them in was a manual
export step that got skipped. Max: *"zero on screen hooks can't expect them to
perform well."* Text that lives in a composition file cannot be forgotten at
export, because it *is* the export.

## Running it

```bash
source "Content Pipeline/tools/video/setup-render-env.sh"   # once per container
cd "Content Pipeline/Creative Studio/video/<project>"
npx hyperframes check                                        # gate - do not skip
npx hyperframes render --quality high --output out.mp4
```

`check` is not a formality. On the first composition written here it caught a
real seeking bug — an exit tween on a clip element with no hard kill, which
leaves stale visibility when the renderer seeks non-linearly rather than plays
forward. It also runs WCAG AA contrast on every text layer, which is the
cheapest possible guarantee that a hook is legible on a phone in daylight.

## The format

1080×1920, cream (`#FAF6EE`) top and bottom bands, photo full-width between.

The bands are **not** letterbox — they are the account's own colour, and they
exist because our plates are 3:4. Cropping 3:4 to 9:16 removes 177 px from each
side, and on a Daisy plate that is the ends of the sign. The product is the
thing that must survive the crop, so the frame gives way instead.

The hook rides the **top** band. TikTok puts its own UI along the bottom and
right; the top carries only a gradient.

## Writing a composition

Brand tokens, matching the pill treatment Max approved on the diffuser carousel:

| | |
|---|---|
| Font | Fraunces 600 (`projects/diffuser/reel-pipeline/fonts/`) |
| Ink | `#4A3A2C` |
| Pill | `rgba(250,246,238,.96)`, radius 999px, `0 6px 22px rgba(30,25,20,.28)` |
| Ground | `#FAF6EE` |

Vendor GSAP into `assets/` rather than loading the CDN — a render that depends
on the network is a render that fails on the day the proxy is unhappy.

### The hook is three components, not a line

From `.claude/skills/ad-creative/references/hook-system.md`: visual action /
spoken line / caption text, and **they must never duplicate each other.** Our
videos are silent, so we have two slots — the photograph and the caption — and
wasting one by having the caption describe the picture is the single most
common way a post dies.

Worked example, `DM-SUMMER-COUNTDOWN`:

- **Visual:** the sign reads THE SUMMER HOLIDAYS / DAY 4 OF 42.
- **Caption:** "Six weeks off school." → "We're counting."

The caption never says what the sign says. It opens a loop; the product closes
it. A caption reading "The summer holidays" would have thrown the slot away.

## Standing constraints

- Propose, never publish. Nothing here goes live without Max saying so.
- No customer PII. A surname as sign wording is product; a date, an address or
  an order number is not.
- Only the five real colourways: BLACK, GREY, SAGE, GRASS, BLUE.
- Never state a price, a delivery time or a result that has not been verified.
