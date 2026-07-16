# Project Social Prompts

## Purpose

Canonical context orb for turning raw Daisy Maison product/workshop photos
into Instagram-ready social content prompts. Use this entry when Max drops a
product photo and asks for a social/aesthetic/IG version, or mentions Nano
Banana Pro 2, Higgsfield image edits, or social content prompts.

## How this works

1. Max attaches a product/workshop photo in chat.
2. Claude checks `projects/social-prompts/prompts/` for a matching technique
   and `projects/social-prompts/examples/` for a similar past shot, then
   tailors a ready-to-paste Nano Banana Pro 2 prompt to the specific products
   and text in this photo.
3. Default technique is the two-pass restyle in
   `projects/social-prompts/prompts/two-pass-text-safe-restyle.md`: a
   background/lighting pass, then a light touch-up pass. This exists because
   single "make it aesthetic" prompts tend to let the model redraw printed
   text on ceramics/signs/boxes — the failure mode Max hit on 2026-07-16.
4. Claude saves the source photo plus the exact filled-in prompt(s) under a
   new dated folder in `projects/social-prompts/examples/`, and updates the
   technique file if this shot revealed a new pattern.

## Hard rule

Never let a restyle prompt risk the product's actual printed/engraved text.
Always instruct the model to preserve it verbatim and treat it as a fixed
graphic element, not content to reinterpret.

## Source of truth

`projects/social-prompts/README.md` for the full workflow and rules.
