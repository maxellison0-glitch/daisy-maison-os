# DM-C014 - From This Day Forward

Portable Daisy Maison content pipeline for one advert concept.

## Start here

1. Read `CURRENT_CONTEXT.md`.
2. Inspect `assets/from-this-day-forward-master.jpg` at full size.
3. Read `CREATIVE_BRIEF.md` and `PRODUCTION_PLAN.md`.
4. Build only the silent three-shot animatic described there.

This folder deliberately contains its own working context so it can be opened
directly in Claude Code or Codex without relying on the earlier conversation.

## Locked premise

The advert uses one truthful Daisy Maison wedding product photograph. The two
illustrated hearts on the box lid match-cut to the two real pebble people in
the acrylic heart. The source product does not change at any point.

The separate `Family Is a Gift` version remains a future concept. It requires
its own coherent family-product master photograph and must never be composited
onto this wedding product.

## Collaboration

- When this folder is opened in Claude, `CLAUDE.md` makes Claude the active
  creative operator and provides a local wrapper for a real read-only Codex
  review.
- When opened in Codex, `AGENTS.md` makes Codex load the same source of truth.
- Accepted decisions belong in `CURRENT_CONTEXT.md`; raw model transcripts do
  not.
- Max has final approval over every visual version.

## Source-of-truth asset

`assets/from-this-day-forward-master.jpg`

This is a byte-for-byte copy of the image supplied by Max. Never overwrite it.
Derivatives and exports should go in new `working/` and `exports/` directories.

