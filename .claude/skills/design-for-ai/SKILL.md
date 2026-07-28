---
name: design-for-ai
description: Visual design doctrine — typography, colour theory, proportion, composition, visual hierarchy, and the AI tells that make work look generated rather than authored. Use when designing or critiquing any visual output — a caption layout, a thumbnail, a page, an ad, a graphic — and especially when something "looks a bit AI" or "looks basic" and the reason needs naming rather than guessing. Also use for usability review, UX writing, data-viz choices, and design-system decisions. Vendored from ryanthedev/design-for-ai (MIT).
---

# design-for-ai — vendored 28 Jul 2026

Installed at Max's request. Upstream: **[ryanthedev/design-for-ai](https://github.com/ryanthedev/design-for-ai)**, MIT,
v4.2.0. Pinned commit in `UPSTREAM-COMMIT.txt`. Design principles derived from
*Design for Hackers* by David Kadavy.

**Why it's vendored rather than installed as a plugin.** The proper install is
two commands in an interactive session:

```
/plugin marketplace add ryanthedev/rtd-claude-inn
/plugin install design-for-ai@rtd
```

That path writes to a machine-local plugin cache. This container is ephemeral
and the write to `.claude/settings.json` that would make it persist was blocked
by the permission classifier, so the content is vendored into the repo instead —
tracked, versioned, and available to every future session with no fetch. If Max
runs the two commands above, the plugin version supersedes this copy and this
directory can be deleted.

---

## What to read, and when

### The one that matters most here: `references/visual/ai-tells.md`

Daisy Maison's standing creative rule is *"premium and frictionless, never AI
spectacle"* (`Creative Studio/CLAUDE.md`), and the most common rejection in this
repo is a variant of *"it looks basic"* or *"that's not real."* This file is the
vocabulary for that. It defines **AI slop** (technically competent, visually
generic), **design tells** (a visual pattern that reveals the absence of a
decision) and **convergent design** (independent systems producing identical
output because they optimise for the same safe defaults), then gives a detection
checklist and transformation patterns.

Read it before defending a layout, and read it when Max says something looks
generic and the reason needs naming rather than guessing.

### The rest

| Path | Use it for |
|---|---|
| `references/visual/chapter-03-typography.md` | type choices — the caption-font argument lives here |
| `references/visual/chapter-07-visual-hierarchy.md` | what the eye hits first; the "punchline is the smallest thing in the frame" problem |
| `references/visual/chapter-05-proportions.md` | sizing relationships, including sign-to-body scale |
| `references/visual/chapter-06-composition.md` | framing and balance |
| `references/visual/chapter-08-color-science.md`, `chapter-09-color-theory.md` | colourway decisions against the production palette |
| `references/visual/motion.md` | motion craft — pairs with `motion-doctrine` |
| `references/visual/design-dna.md`, `archetypes.md` | giving a brand a describable visual personality |
| `skills/usability/`, `skills/data-viz/`, `skills/clarify/`, `skills/prototype/` | the four bundled sub-skills |
| `commands/` | the upstream research → plan → mock → build workflow |
| `agents/design-review-agent.md` | the review pass |

---

## How it fits what's already here — read this before it causes a conflict

This repo already has strong, **Max-approved, evidence-backed** house rules.
Where the two disagree, **the house rules win**, because they were bought with
his rejections rather than inherited from a book.

| Ours | Status |
|---|---|
| `Content Pipeline/VIDEO_CAPTION_SYSTEM.md` | the caption spec. TikTok Sans 800, rounded pills, no `drawtext` |
| `Creative Studio/prompts/CHARACTER-LOCK-SYSTEM.txt` | the arm-line scale gate and the locks |
| `.claude/skills/daisy-video-generation` | the spend gates and reference discipline |
| `motion-doctrine`, `cut-the-curve`, `seam-craft` | motion law |

**One live conflict worth settling with it, not around it.** The caption spec
says TikTok Sans 800 in a rounded pill. The account's actual best-performing
post — the Bond turnaround, 796 views — uses a **serif in a cream pill**. Two
different house looks are in play and nobody has picked. `ai-tells.md` and
`chapter-03-typography.md` are the right tools for that argument, since it is
exactly a question of whether a choice is authored or defaulted.

**Do not let it override product truth.** Colourways, panel colour and
dimensions come from `projects/daisy-street-sign/production/product-rules.json`.
A design doctrine does not get a vote on what the product is.
