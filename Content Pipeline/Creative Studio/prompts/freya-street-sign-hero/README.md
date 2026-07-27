# Freya street-sign hero — validated engineering case

**Scope: Freya only, stills only.** Max approved the take-02 result on 24
July 2026 ("that's definitely more realistic") and asked for this to be
saved as the engineering prompt. It is validated for producing a
photorealistic still of Freya holding a Large Daisy Maison street sign at
correct physical scale, with arbitrary display-safe wording. It does NOT
validate video (only the white wedding-sign family has a validated video
workflow, DM-C017), and it is not evidence for other product families.

Full evidence and measurements:
`../../active/DM-C018-freya-synthetic-sign-turn/`

## The method (two stages, one variable each)

**Stage A — printing replacement on the locked real product.**
`cases/DM-C018-FREYA-CAKE/01-validated-printing-replacement.txt`
One reference: the real product-only photograph (the DM-C017 construction
pack front crop). One change: the printing. Model `nano_banana_pro`
(executes as `nano_banana_2`). 16:9. ~2 credits.

**Stage B — Freya holds the Stage A sign, scale-locked.**
`cases/DM-C018-FREYA-CAKE/02-validated-freya-hero-scale-locked.txt`
Three references, roles strict:
1. the Stage A output (product authority),
2. Freya's locked identity hero (job `368014cd-bd1a-402f-9d1e-cebbea50c60e`),
3. the real human-scale frame (`instagram-DPjdseCDbDR` frame 240) as
   SCALE AUTHORITY ONLY.
4:5. ~2 credits.

## The scale gate (why this case exists)

The first attempt had pixel-exact lettering and a ~13-15% undersized sign
— caught by Max against Alan's Bond hero, confirmed by measurement.
Numeric check is mandatory before lettering QC:

- Measure sign-width : shoulder-width in pixels.
- Alan (male) benchmark: **1.63**. Freya target: **≥ 1.9** (same physical
  sign on ~18% narrower shoulders). Take-02 measured **2.32** — pass.
- A real photo of a person holding the product, supplied as an explicit
  scale-authority reference, is what fixed it in one take.

## Known nits and open items

- The signature gold ring drifted to her left hand in take-02 (spec:
  right hand). Acceptable for engineering; fix in prompt if it matters
  for a production still.
- Setting drift is benign: take-02 landed in a warm wood workshop that
  Max explicitly liked — treat that setting as preferred, not accidental.
- Wording used in the validated case is "GO AWAY (UNLESS YOU'VE BROUGHT
  CAKE)" — an engineering probe with no audited SVG behind it. Production
  stills for real orders should still source wording from the audited
  sign system.
