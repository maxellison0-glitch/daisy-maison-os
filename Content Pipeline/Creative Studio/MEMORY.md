# Useful creative memory

This is the distilled memory worth carrying between agents. It is not a
transcript and should remain short.

## What worked

**DM-C006 - From Name to Real** is the current quality baseline. The clean
street-sign personalisation and real wedding reveal worked because it was
frictionless, immediately understandable and product-led.

Master:
`../drafts/DM-C006/exports/DM-C006-P1-MASTER-ORG-9x16-hookA-v3.mp4`

Do not endlessly rebuild it. Test only one meaningful variable at a time, such
as the opening hook, tactile keystrokes, sound, sentiment or paid CTA.

## What we learned

- Product truth outranks spectacle.
- Frictionless is Daisy Maison's premium creative identity.
- Personalisation is inherently watchable.
- One symbolic match cut can carry an entire advert.
- Sentiment, tactile sound, craft and gifting ritual are separate levers; every
  advert does not need all of them.
- Organic content is advert research. Winning hooks should convert into paid
  variants without rebuilding the core visual.
- AI may animate a verified scene only when the product remains exact. It must
  never redraw a different product and pretend it is real.
- Agent attention is narrower than Max's global visual judgment. A frame can
  have correct text, hands and light while still depicting the wrong physical
  product. Check dimensions, construction and scale first.
- The repeatable system is human-directed: agents prepare and pre-filter
  batches; Max selects the winner. `agent-pass` never means `max-approved`.
- Every Max-approved Higgsfield output must retain its exact prompt, model,
  references, generation IDs and selection reason in `recipes/` so the system
  learns across tools and copied folders.
- A still image with a rotating overlay is not a video proof. For street signs,
  the person, hands, wrists and plaque must perform genuine continuous motion.
- **No sign overlays.** Never replace a whole panel, border or lettering on
  generated video, even with exact LightBurn-derived artwork. The sign must be
  native to the approved source state and remain unchanged through video
  generation. If it changes, reject and regenerate.
- DM-C017 proved why: its replacement face was a visibly different white from
  the physical border. It did not share the scene's reflections, falloff,
  blur, edge thickness or contact shadows, so humans immediately read it as a
  pasted-on graphic. Lettering metrics and continuity checks passed while the
  advert still looked fake.
- The useful part of the street-sign split remains: use 4-8 cheap Nano Banana 2
  stills for identity, anatomy, exact sign geometry and material before buying
  video. The chosen still and native video must already contain the final sign.
- Higgsfield's Windows `.cmd` wrapper can truncate multiline prompts and lose
  later references/flags. Call the bundled native `vendor\hf.exe`, flatten the
  prompt to one argument, quote the cost, and inspect returned job JSON.
- Automated QC must include a human physical-integration gate at normal phone
  playback speed. Border colour discontinuity, pasted-on white, inconsistent
  material response or a moving composite seam is a hard rejection.
- Never send a composited exact-face still into video generation. First create
  one coherent image from the exact SVG plus a real product photograph, then
  require human approval of that image.
- For street-sign prompt engineering, make one real printed sign the single
  manufactured-object authority and permit one change only: its printing. The
  SVG owns the replacement wording/art; the real photograph owns border,
  silhouette, holes, material, proportions, lighting and hand contact. Splitting
  those truths across prose and separate references lets the model redesign the
  product.
- Test the locked-product instruction with 4-8 identical inexpensive image
  runs before adding synthetic Max, pose or video motion. This separates
  product-prompt repeatability from identity and animation faults.
- Every street-sign video needs real front, two opposing edge/three-quarter and
  back reference views. The side views lock the genuinely thin pale edge; the
  back reference locks the real white reverse. The black border is front
  artwork, not a thick black slab. Missing construction views block video
  spend.
- DM-C017 v02 remains a rejected overlay/construction learning case: its source
  reference was composited, its turn became too thick and Seedance invented a
  black back. DM-C017 v03 separately validated the corrected white wedding-sign
  method. Max rated its untouched native video 8.5/10. The proven recipe is
  `WEDDING_SIGN_ENGINEERING_PROMPT_WORKFLOW.md`; never mix its approved inputs
  with the rejected v02 assets or claim that it proves coloured/non-wedding
  sign families.

## Ideas worth keeping

- Real typing or personalisation becoming the physical product.
- A private message or voice note explaining why the gift matters.
- Gift-box artwork match-cutting to its physical counterpart inside.
- Pebble hearts held in the hand, tactile unboxing and truthful recipient
  emotion.
- Pebble family members assembling into the finished framed picture.
- Craft proof: materials, edges, checking and packing.

## Parked, not abandoned

**Family Is a Gift:** baby bird on the family gift-box lid cuts to the matching
pebble child. Resume only when the matching family box and heart exist together
in one truthful master photograph.

**Phone personaliser transition:** strong idea, but only resume with a genuinely
tracked screen or controlled practical plate. Never float an unsynchronised
website overlay over a moving generated phone.

## Longer-term system

Once the production standard is repeatable, aim for one or two posts per day.
Use organic response as the testing layer, then add modular paid endings, safe
zones and rights-clean audio to the winners. The original working subscription
ceiling was approximately £150 per month; Higgsfield, ElevenLabs and an avatar
are optional tools, not the strategy.
