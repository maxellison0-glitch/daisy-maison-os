# Social content prompt templates

Locked templates for the automated social posting workflow (TikTok, Instagram).

## The one rule that matters

**Never describe the product.** The reference image is the complete description.
Do not say what it is made of. Do not say what it looks like. Do not add
adjectives. The image you are passing as reference 1 is the product — the model
copies it. Any words you add will be wrong and will produce rejected output.

This rule exists because every time a prompt has described the product's material,
it has been wrong. "Wooden sign" — wrong. "Acrylic sign" — unnecessary. "Large
street sign" — the model invents its own version. The validated prompts that work
say: "Reference 1 is a real photograph of a Daisy Maison street sign — preserve
it exactly." That is all.

## Line 2 size gate

Line 2 (the subtitle) must be roughly one-fifth the height of line 1. The
real product is 59pt vs 11.5pt — a 5:1 ratio. The SVG generator (`build.py`)
enforces this by code. When Higgsfield does the print-edit, visually verify
after generation that line 2 reads as a small caption, not a second headline.
If it looks too big, reject and regenerate.

## Templates

- `FREYA-SOCIAL-HERO.txt` — Freya holding the sign in a new scene. Uses 3
  references: product photo, Freya identity lock, scale authority. Fill in
  `{{SCENE}}` with the setting description only (the room/location, NOT the
  product). Append the phone-snapshot block from `HOUSE-STANDARD-phone-snapshot.txt`.

## References for social content

| Reference | File | Role |
|---|---|---|
| Product (ref 1) | `reference-masters/street-sign-BLACK-on-white-MASTER.jpg` | The product. Never described, only copied. |
| Freya identity (ref 2) | `reference-masters/PLATE-summer-holidays-BLACK-freya-hallway-APPROVED.png` | Face, hair, freckles, ring. |
| Scale authority (ref 3) | `reference-masters/FREYA-holding-sign-BLUE-MASTER.jpg` | Size relationship only. |

## Scene descriptions — what goes in {{SCENE}}

The scene is the ONLY creative variable. Keep it short. Examples that work:
- "a bright sun-drenched modern kitchen, natural daylight, warm tones"
- "a hallway with heritage paint and pale oak flooring, natural light from a side window"
- "a garden terrace on a summer morning, soft light, greenery behind"

Do NOT put product descriptions in the scene. The scene is the room. The product
is reference 1.

## Interior style (locked 25 Jul 2026)

Modern UK upper-middle-class. Wide-plank pale European oak flooring, matte; soft
chalky stone-grey heritage paint above crisp white shaker panelling; brushed-brass
hardware; neutral oatmeal-linen soft furnishings. Calm, uncluttered, expensively
simple — architect-renovated family home. NOT a rustic cottage.

Negative: terracotta, quarry tiles, tartan, plaid, muddy boots, exposed beams,
clutter, patterned wallpaper, dated fittings.
