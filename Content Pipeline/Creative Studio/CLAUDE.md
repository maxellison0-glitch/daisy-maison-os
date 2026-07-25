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
  misleading claims, publishing or paid-media launch without Max's approval.
- The creative target is premium and frictionless, never AI spectacle.

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
