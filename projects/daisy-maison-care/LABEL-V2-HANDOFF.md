# Claude / Fable handoff — Daisy Maison Care collagen label V2

- Prepared: 17 August 2026
- Owner: Max / Daisy Maison
- Product: Nutribl `PL-489`, 300 g unflavoured marine collagen powder
Status: V1 is technically complete and has been sent to Nutribl, but Max has not approved its visual direction.

## Start here in Claude Code

From the repository root:

```powershell
Set-Location 'projects/daisy-maison-care'
claude
```

Claude Code will load `CLAUDE.md`, which points back to this brief. Ask it to execute the V2 label handoff and stop at the approval gate.

## The task

Redesign the label so the tub works as Daisy Maison Care's hero product in advertising and at Shopify thumbnail size. V1 contains the required information, but it feels too programmatic, too boxed and not close enough to the existing Daisy Maison visual identity.

The V2 label should feel:

- recognisably Daisy Maison;
- premium but warm, not clinical or luxury-cosmetics generic;
- minimal at first glance, with the compliance density moved to the side panels;
- human-set and editorial rather than algorithmically symmetrical;
- distinctive enough that the jar is memorable in a feed or product grid;
- calm, trustworthy and suitable for an established gifting brand extending into daily care.

Max specifically wants the website sage **`#B0AF9B`** used meaningfully.

## Do not begin by decorating V1

First create three low-resolution front-panel studies, assess them at thumbnail size, and then develop the strongest direction into the complete wrap label. The purpose is to reset the visual hierarchy, not just recolour the existing rounded rectangle.

Recommended concepts:

1. **Sage Editorial — recommended**
   - A solid but light `#B0AF9B` front field, warm-paper side panels and charcoal typography.
   - Exact Daisy Maison wordmark at the top.
   - Large, optical serif setting of `DAILY MARINE COLLAGEN` with an asymmetric line break.
   - One compact proof line: `10 g collagen · 29 servings`.
   - No decorative badge and no geometric flower.

2. **Quiet Apothecary**
   - Warm paper as the dominant front, one generous sage band or offset sage block.
   - More editorial whitespace and one fine botanical or ingredient line.
   - Must not drift into generic pharmacy packaging.

3. **Human Botanical**
   - Sage and warm paper with one intentionally imperfect, hand-drawn botanical mark.
   - The drawing must be original, restrained and optically placed—never a repeated petal rosette or AI-style mandala.

Create a contact sheet showing all three front-panel studies on the actual jar, recommend one, and continue with the recommended concept unless a serious usability problem appears.

## What successful collagen packs are doing

These are references for strategy, not artwork to copy.

| Brand | Evidence of traction | What the pack does | Transferable lesson |
| --- | --- | --- | --- |
| [Bare Biology Skinful](https://www.barebiology.com/products/skinful-pure-marine-collagen-powder) | £39.95, 4.8 rating and roughly 1,100 reviews on the brand site | White cylindrical tub, large whitespace, grey type and a loose teal watercolour face illustration | One human illustration and plain-spoken typography can make a clinical supplement feel warm and ownable. The illustration is a brand cue, not filler. |
| [Vital Proteins Collagen Peptides](https://www.hollandandbarrett.com/shop/highlights/bestsellers/) | Listed as a Holland & Barrett bestseller with roughly 2,479 reviews | Saturated blue wrap, large white product name, highly visible grams-per-serving proof | A single dominant colour and one large quantitative proof survive tiny ecommerce thumbnails. |
| [Ancient + Brave True Collagen](https://ancientandbrave.earth/products/true-collagen-powder) | 4.9 rating; the brand states 400,000+ customers | Refillable glass jar with a black label, restrained copy and an unmistakable illustrative emblem | A distinctive artefact, strong contrast and ritual language create premium memory without filling the front with claims. |
| [Applied Nutrition Marine Collagen](https://www.hollandandbarrett.com/shop/highlights/active-nutrition-bestsellers/) | About 1,000 reviews in a mass-market bestseller environment | Sports-nutrition hierarchy: brand, product, flavour/dose, high contrast | The first three seconds need brand, product category and proof. Everything else is secondary. Do not copy its sports aesthetic. |
| [Dose & Co collagen powder range](https://www.hollandandbarrett.com/shop/vitamins-supplements/supplements/collagen-silica/?t=format%3Apowder) | Multiple products listed as bestsellers with hundreds of reviews | Friendly wellness colour, simple naming and familiar tub format | Softer colour can still command a shelf when the typography is direct and the colour is consistent across the range. |

Research conclusion: successful packs tend to have **one ownable colour, one dominant product name, one proof point and one human brand cue**. V1 has too many equally weighted devices: a rounded panel, a rosette, a capsule outline, multiple centred lines and boxed side tables. Simplify the front aggressively.

## Thumbnail and advertising hierarchy

Judge the front face at 250 px tall and in a square Shopify crop. A customer should recognise, in this order:

1. Daisy Maison;
2. marine collagen;
3. 10 g per serving;
4. the sage pack colour.

The front should not require the customer to read the descriptive sentence. Move the full `Powdered Food Supplement...` description to a smaller supporting position or the side panel while keeping `Food Supplement` clearly present on the front.

Recommended front content only:

- Daisy Maison wordmark;
- `CARE` sub-brand;
- `DAILY MARINE COLLAGEN`;
- `10 g collagen per serving`;
- `UNFLAVOURED`;
- `300 g · 29 servings`;
- `FOOD SUPPLEMENT`.

The authorised vitamin claims, directions, ingredient declaration, tables and cautions belong on the side panels.

## Daisy Maison V2 design system

Use this palette unless a production test demonstrates a problem:

- Primary sage: **`#B0AF9B`** — the memorable front-face colour.
- Warm paper: `#F4EFE7` — side panels and breathing space.
- Ink: `#262923` — primary text; avoid pure black.
- Blush: `#D8BDB0` — one very small accent only, if it earns its place.
- White: `#FFFFFF` — only where contrast is needed.

Suggested colour ratio on the visible front face:

- sage 55–70%;
- warm paper 20–35%;
- ink 5–10%;
- blush no more than 3%.

Nutribl advises against very dark solid backgrounds because of print streaking. `#B0AF9B` is light enough to be the dominant field; do not replace it with a dark olive block.

Typography and composition:

- Use the exact Daisy Maison logo asset; recolouring is allowed, distortion is not.
- Start with Georgia or a restrained editorial serif for the product name and Arial for legal copy, because those are available in the existing build.
- `projects/daisy-scroll-story/theme/assets/daisy-times-regular.woff2` is available as an exploratory brand-adjacent display face, but use it only if it renders cleanly and improves the label. Do not force it into legal text.
- Avoid pill outlines, perfect concentric geometry, centred stacks of seven lines, faux seals and generic wellness icons.
- Use optical alignment rather than mathematical centring everywhere.
- Hairline rules are acceptable on the side panels; boxed tables should be used only where they materially improve numeric reading.
- A tiny, low-contrast paper grain on the sage field is acceptable if it survives print cleanly. Do not add a conspicuous digital texture.

## What makes it feel human

- Let one element sit slightly off-axis or off-centre with deliberate visual tension.
- Use one confident serif scale jump instead of many medium font sizes.
- Keep generous negative space around the product name.
- If using illustration, use one irregular botanical stroke with non-repeating curves; no radial flower generator.
- Hand-adjust tracking and line breaks after rendering—do not rely only on programmatic centring.
- Let the side-panel information feel typeset like a small editorial leaflet, not a spreadsheet export.
- View the design on the jar after every major iteration. The curved pack hides the left and right edges of the nominal front panel.

## Production specification — hard constraints

Source: [Nutribl self-design instructions](https://support.nutribl.com/support/solutions/articles/9000143837-can-we-design-our-own-labels-for-private-label-)

- Finished label: **200 × 100 mm**.
- Supplied artwork: **204 × 104 mm** including 2 mm bleed on every edge.
- Required production format: high-quality **RGB JPG**.
- Required production dimensions: **4819 × 2457 px** at 600 dpi.
- Minimum text size: **5 pt**; target 5.2 pt or larger for dense copy.
- Keep important text at least 4 mm from the exported artwork edges.
- Do not add trim marks, registration marks or an outer border.
- Product uses one wrap label.
- Final supplier filename must be **`PL-489$front.jpg`**.
- `fish` must remain bold in the ingredient declaration.
- All required cautions and best-before/batch wording must remain.
- Business operator details must remain Daisy Maison, Unit 6 Juniper Court, Thompson Road, Blackpool FY4 5QF, United Kingdom, with the orders email and website.

## Claims and copy safety

The authoritative copy is `source/PL-489_V3.docx`. V1's `artwork/build_label.py` already transcribes it.

Do not add claims about:

- reducing wrinkles;
- anti-ageing;
- plumper or younger-looking skin;
- hydration;
- treating joint pain or arthritis;
- preventing or curing a condition;
- collagen absorption superiority.

Use only the two Nutribl-supplied front-label claims:

- Vitamin C contributes to normal collagen formation for the normal function of skin, bones and cartilage.
- Riboflavin, biotin and niacin contribute to the maintenance of normal skin.

Relevant references:

- [Great Britain nutrition and health claims register](https://www.gov.uk/government/publications/great-britain-nutrition-and-health-claims-nhc-register)
- [ASA guidance on food and skincare claims](https://www.asa.org.uk/advice-online/food-skincare.html)

## Existing files and how V1 was made

Read these before building:

- `source/PL-489_V3.docx` — authoritative Nutribl copy.
- `source/daisy-maison-logo-white.png` — exact live-site wordmark.
- `source/nutribl-blank-jar.jpg` — supplier blank jar.
- `artwork/build_label.py` — V1 vector PDF builder using Python and ReportLab.
- `artwork/build_mockup.py` — V1 Pillow-based jar composite.
- `artwork/PL-489$front.jpg` — V1 supplier JPG, 4819 × 2457 RGB.
- `artwork/daisy-maison-daily-collagen-mockup.jpg` — V1 product mockup.
- `../../output/pdf/PL-489$front.pdf` — V1 proof PDF.
- `research-notes.md` — launch economics and compliance research.

V1 implementation stack:

- Python;
- ReportLab for the 204 × 104 mm vector PDF;
- Pillow for logo recolouring and the jar mockup;
- Poppler `pdftoppm` at 600 dpi for the exact supplier JPG.

You may reuse that stack or create an SVG-first V2 if it improves optical control. The output specification, exact copy and QA gates do not change.

## Required V2 deliverables

Create a new `artwork/v2/` directory. Do not overwrite V1.

1. `front-concepts.png` — three labelled front-panel studies shown at full size and thumbnail size.
2. `concept-rationale.md` — short comparison and chosen direction.
3. `build_label_v2.py` or an equivalent editable source.
4. `PL-489$front-v2-proof.pdf` — full wrap proof at 204 × 104 mm.
5. `PL-489$front.jpg` — final supplier candidate at exactly 4819 × 2457 RGB.
6. `daisy-maison-daily-collagen-v2-mockup.jpg` — advertising/product-page mockup.
7. `qa.md` — dimensions, colour mode, minimum font size, copy comparison, allergen check and visual inspection results.

Also produce front crops at approximately 250 px and 500 px tall to prove the hierarchy survives real ecommerce use.

## Acceptance criteria

- The tub is recognisably Daisy Maison before reading the small copy.
- `#B0AF9B` is the ownable front-face colour, not a token accent.
- The product name and 10 g proof remain readable in a small product card.
- The front has materially fewer visual devices than V1.
- The design does not resemble a generic AI wellness label.
- Every required word and number matches the current Nutribl source.
- No text is below 5 pt or inside the unsafe area.
- JPG is exactly 4819 × 2457, RGB, and named correctly.
- PDF and 600 dpi JPG render without clipping, overlap, garbled symbols or illegible contrast.
- The jar mockup looks plausible enough for a Shopify preview but is clearly treated as a pre-production mockup.

## Safety gates

- Do not overwrite or delete V1.
- Do not email V2 to Nutribl.
- Do not approve any supplier artwork.
- Do not place a stock order or spend money.
- Do not change the Shopify product image, status, inventory or live theme.
- Do not make V2 public.

Stop after the deliverables and ask Max to choose or approve the visual direction. Once approved, the final supplier JPG can replace the V1 submission and the Shopify mockup can be updated.
