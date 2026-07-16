# Daisy Maison — Social Content Prompts

Purpose: a growing library of proven Nano Banana Pro 2 (Higgsfield) prompts for
turning raw Daisy Maison product/workshop photos into Instagram-ready images,
so Claude doesn't have to reinvent a prompt from scratch every time.

## How this works

1. Max drops a product/workshop photo in chat and asks for a social-ready
   version.
2. Claude checks `prompts/` for a technique that fits the shot (flat-lay/shelf,
   single product on plain background, lifestyle scene, etc.) and adapts it to
   the specific items in frame and any text that has to survive unchanged.
3. Claude hands back a ready-to-paste prompt — usually two-pass (background/
   lighting first, then a light touch-up) — for Max to run in Higgsfield Nano
   Banana Pro 2.
4. Once a prompt is confirmed to work, Claude saves the source photo + final
   prompt(s) under `examples/`, and updates/adds a technique file under
   `prompts/` if it's a new situation.

## Rules

- Always preserve exact product text/copy verbatim — printed words on
  ceramics, boxes, labels, cards, etc. are fixed graphic elements, never
  reworded, re-lettered, or re-translated.
- Prefer two-pass prompts (background/lighting pass, then touch-up pass) over
  one big instruction — this is the fix for the "aesthetic prompt melts the
  text" failure mode seen on 2026-07-16.
- Keep `prompts/` entries reusable/generic (placeholders for the exact product
  list and exact text); keep `examples/` entries fully filled-in and dated so
  they double as a working reference library.
- If Max reports a prompt didn't hold up, update the relevant `prompts/` file
  and note the failure in the matching `examples/` entry rather than silently
  dropping it.

## Structure

- `prompts/` — reusable prompt templates by shot type.
- `examples/` — dated folders pairing a real source photo with the exact
  prompt(s) used for it and the outcome, once known.
