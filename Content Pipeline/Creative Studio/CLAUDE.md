# Claude entry instructions

## READ FIRST, EVERY TIME: `REFERENCE_PACK.md`

**Never generate a product image without the approved product photograph as
reference 1, and without using a validated prompt from the case folder.** The
flat SVG is the printing, not the product. Skipping this has produced rejected
output every single time it has been skipped. `REFERENCE_PACK.md` holds the
locked masters, the validated prompt chain and a pre-flight checklist that must
be answered before any generation runs.

Read `README.md`, `CURRENT.md` and `MEMORY.md` before proposing work.
Then load the active concept's local context, brief, plan and master asset.
Before generative production, read `recipes/README.md` and the relevant recipe
index/identity sheet.

Claude is the creative operator when Max opens this folder in Claude. Preserve
one active concept, one source of truth and one next action. Do not broaden the
campaign during a production task unless Max asks.

## Creative connector authority

Max authorises Claude to use the creative connectors and existing subscriptions
available in its environment, including Higgsfield and ElevenLabs, without
requesting permission for each normal production step.

- Use Higgsfield only when it materially improves controlled motion or
  atmosphere while preserving the exact verified product.
- Use ElevenLabs for restrained tactile sound, sonic identity or voice only
  when it strengthens the advert.
- Keep credit use proportionate, prefer low-cost proof passes before expensive
  renders, and stop repeating a failing generation strategy.
- Record the winning prompt, model, job ID and selected output path in the
  active concept's `CURRENT_CONTEXT.md`. Failed attempts need only a short
  lesson when it prevents the same mistake recurring.
- Agent review may reject obvious failures but must not label an image selected
  for production until Max approves it. Use `agent-pass` and `max-approved` as
  distinct states.
- Every generated batch must preserve its provenance in the active concept;
  only Max-approved winners and distilled failure constraints enter `recipes/`.
- Check whole-product scale, dimensions and construction before fine details
  such as lettering. Attractive imagery is not product fidelity.
- Connector access does not permit altered products, invented lettering,
  misleading claims, or paid-media launch without Max's approval. Organic social
  posts publish autonomously.
- The creative target is premium and frictionless, never AI spectacle.

## Content creation rules — hard stops

These come from Max's direct feedback. They are not guidelines. They are
rules that override any cost-saving or efficiency logic.

1. **Never overlay text on a generated or reprinted image.** No hook pills,
   no captions composited onto the photo. The image ships clean. On-screen
   text belongs in the platform's native caption tools or in video
   post-production — never baked into a still image by this pipeline.

2. **Never reuse the same plate/background for multiple posts.** A plate
   reprinted with different wording is the same image to anyone who has seen
   it before. Posting the same Freya-in-hallway scene with swapped sign text
   is recycled content, not new content. Every post must have a distinct,
   freshly generated background/scene created via Higgsfield.

3. **Use Higgsfield to create new backgrounds — be creative.** The point of
   the image generation tooling is to produce new, varied, visually
   interesting scenes. Reprint is a production tool for carousels within a
   single post (multiple wordings, same scene, shown together). It is NOT
   a content strategy for separate posts across days.

4. **Zero credits is not a virtue if the output is not usable.** Cost
   efficiency means nothing when the content is recycled or lazy. Spend the
   credits to make something worth posting.

5. **Never describe the product in a prompt.** The reference image is the
   complete description of the product. Do not say what it is made of. Do
   not say "wooden", "acrylic", "large", or any other material/size word.
   The validated prompts say "Reference 1 is a real photograph of a Daisy
   Maison street sign — preserve it exactly." That is all. Any descriptive
   words you add about the product will be wrong and will produce rejected
   output. The image is what we are copying. It looks exactly like that.

6. **Use validated prompt templates only.** Social content uses the template
   in `prompts/social-content/FREYA-SOCIAL-HERO.txt`. The only creative
   variable is the scene/setting. The product block and the identity block
   are locked. Do not write new product descriptions. Do not improvise.

7. **Line 2 (subtitle) must stay small.** The real product has a 5:1 size
   ratio between line 1 and line 2 (59pt vs 11.5pt in build.py). When
   using the SVG generator this is enforced by code. When using
   Higgsfield print-edit, visually verify after generation that line 2
   is noticeably smaller than line 1 — it should read as a subtitle, not
   a second headline. If line 2 appears too large, reject the output
   and regenerate. When writing sign wording, prefer 2+ words on line 1
   to avoid unnatural stretching of short text.

Origin: Rules 1-4 from Max's feedback on the DM-HOME-STORY post, 10 Aug
2026. Rules 5-6 from Max's feedback on the Slot 1 LAUGH post, 11 Aug 2026.
The prompt invented "wooden sign" — the signs are not wooden, and the
reference image already showed the correct product. Rule 7 from Max's
feedback on the Slot 1 generation review, 11 Aug 2026.

When Max requests Claude and Codex together, invoke the real Codex collaborator
through:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\active\DM-C014-from-this-day-forward\.collaboration\invoke-codex.ps1" "<context-rich request>"
```

Never simulate Codex or create a recursive call. Integrate useful conclusions
and update `CURRENT.md` plus the active concept's `CURRENT_CONTEXT.md`.

Max has authorised equal implementation for the active creative. Codex may
write within Daisy Maison. Divide file ownership before parallel work and use
Codex for ordinary creative or technical decisions instead of asking Max. Max
is still required for factual product information, publishing, unagreed spend
or final subjective approval.
