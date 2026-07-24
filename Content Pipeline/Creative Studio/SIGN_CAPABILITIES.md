# Sign capabilities — what we can synthetically make

Owner-approved reference (Max, 24 July 2026) for what Daisy Maison street
signs the content system can produce with Alan and Freya. Split honestly
into VALIDATED (ran through the two-stage proof with evidence) and
DECLARED (owner-confirmed capability, cheap to prove when first needed).

Physical product truth (from live listings + repo):
- Small 29 × 8.5 × 0.3 cm, Large 57 × 12 × 0.3 cm, 3 mm acrylic, UV inks,
  Large has two mounting holes. The Large is the content hero size.
- Thin pale physical edge; printed border is front-face artwork, reverse
  is plain white (locked by the DM-C017 construction pack).

## Colours — the official five

Source: live Shopify listings ("My Valentine", "Retirement": "5 colours")
and the official swatch chart, archived at
`active/DM-C018-freya-synthetic-sign-turn/working/colour-test/colour-swatch.jpg`:

| Colour | Note |
|---|---|
| Black | Standard; the wedding family runs a broad black band |
| Grass | Mid green |
| Sage | Pale grey-green |
| Blue | Muted steel-blue — deliberately dusty; reads close to grey (Max's own read of the proven result; that's true to the swatch, not drift) |
| Grey | Mid grey |

Border + lettering carry the colour; the field is cream/off-white across
the five. **Validated:** Blue, end-to-end (recolour of the real photo →
Freya hero), with one flag: the border band rendered slightly slimmer
than the black original. **Declared, untested:** the other three
non-black colours (same method, ~2 credits each to prove); field/
background colour changes (e.g., a grey field — and the Christmas range
already ships red-field signs, so field recolour is a real product
pattern, not an invention). One cheap Stage A probe each when first
needed.

## Design rules (owner-stated, 24 July 2026)

- **The red heart on the ampersand** is the signature for Valentine's
  signs, wedding signs, and the humorous novelty family. Listing rule on
  My Valentine: heart appears on the '&'; if no '&' in the wording, heart
  appears after the text. Evidence note: the real snacks sign runs
  heartless with no '&' — plain novelty signs can go without.
- Letterforms: Times-style serif capitals, main line + smaller second
  line. Never substitute a sans-serif — proven failure mode, see the
  colour-chain FAIL evidence.
- Wedding family: broad black band (exact geometry audited in
  `WEDDING_SIGN_ENGINEERING_PROMPT_WORKFLOW.md`). Coloured range: thinner
  outline border per the swatch.

## Who can hold it

| Character | Stills | Video |
|---|---|---|
| Alan | ✅ validated (DM-C017 hero) | ✅ validated, white wedding family only (8.5/10 native turn) |
| Freya | ✅ validated (DM-C018, saved prompt case) | ❌ not yet — one ~72-credit gated proof away |

Scale gate (mandatory, numeric, before lettering QC): sign-width :
shoulder-width — male benchmark **1.63**, Freya target **≥ 1.9** (measured
2.2–2.4 on passing takes). Method + fix: a real photo of a person holding
the product as an explicit scale-authority reference.

## Wording

Arbitrary display-safe wording proven (the "GO AWAY (UNLESS YOU'VE
BROUGHT CAKE)" case). Production stills for real orders still source
wording from the audited SVG system, and customer names/dates follow the
existing display-safety rules (no addresses/contact/payment data, ever).

## The recipe

Two stages, one variable each, ~4–6 credits per finished character still:
1. Printing change (wording and/or colour) on the locked real product
   photo.
2. Character hero from that sign + identity reference + human-scale
   reference.

Prompt cases: `prompts/freya-street-sign-hero/` (Freya; includes the
coloured-sign variant with the mandatory typeface/colour locks) and
`prompts/wedding-signs/` (Alan/wedding family). Known model quirk: the
signature ring lands on Freya's left hand regardless of instruction —
pick takes accordingly rather than fighting it.

## Hard boundary

Video validation does not transfer by analogy — each new combination
(Freya video, coloured-sign video, non-sign products) needs its own
gated proof per `WEDDING_SIGN_VIDEO_RULES.md`. Publishing anything still
requires Max's explicit approval per the Content Pipeline gates.
