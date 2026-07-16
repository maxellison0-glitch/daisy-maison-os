# Two-Pass Text-Safe Aesthetic Restyle (Nano Banana Pro 2)

**Use for:** raw workshop/backstage photos of Daisy Maison products that carry
printed or engraved text (ceramic plaques, street signs, boxes, cards, etc.)
which must not change, being turned into Instagram-ready shots.

**Why two passes:** a single "make this aesthetic" prompt gives the model
license to redraw everything in frame, including small printed text — the
classic failure mode (first hit 2026-07-16 on a shelf flat-lay). Splitting
background styling from any touch-up keeps the model's hands off the product
text.

## Pass 1 — Background & Lighting Only

```
Edit this product photo. Do not touch, move, resize, recolor, or redraw
anything in the foreground/products — [LIST EXACT PRODUCTS AND ANY TEXT ON
THEM, VERBATIM]. Only replace the background: [DESCRIBE CURRENT BACKGROUND]
becomes [DESCRIBE TARGET BACKGROUND]. Add soft, warm natural light with
gentle realistic shadows. Remove or softly blur any background clutter.
Shallow depth of field, warm neutral pastel palette, minimal boutique
product-photography look. Photorealistic, no illustration/cartoon rendering,
no added logos or text.
```

## Pass 2 — Light Touch-Up (run only on Pass 1's output)

```
Make a light color-grade and crop pass only: warm the tones slightly, tighten
the crop to [DESCRIBE FRAMING], soften shadows. Do not alter any product, its
shape, its color, or any printed/engraved text in the image — treat
everything already in the photo as fixed.
```

## Notes

- If Nano Banana still touches the text, lower the edit strength/creativity
  slider if the tool offers one — full-strength is what melts small text
  first.
- Hard fallback if both passes fail: generate/aesthetic-ify an empty version
  of the same background+angle, then composite the original (untouched)
  product crop back on top in any photo editor. Zero risk to text because the
  product pixels never touch the model.
- Keep brand direction consistent across shots unless Max says otherwise:
  warm neutral/cream tones, soft natural light, minimal boutique styling, no
  harsh flash or saturated color.

## Filled examples

See `../examples/` for dated, fully filled-in prompts run against real photos
— check there first for a shot type close to what you're working on.
