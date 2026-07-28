# Diffuser — website image batch (2026-07-24)

Restaged website images generated from the clean, red-tinge-free source
photos with Nano Banana Pro (2k, 4:5), label-locked. Every take was QC'd by
zooming the label; only takes with pixel-faithful text are kept here.

## Kept (label verified — "HOME BY / DAISY MAISON / DS / THE ONE AND ONLY")
| File | Shot | Source | Name-safe? |
|---|---|---|---|
| 01-hero-seamless-A | primary listing hero, seamless warm-white | bottle-hero (6246) | ✅ no name |
| 02-hero-seamless-B | hero alt, tighter reeds | bottle-hero (6246) | ✅ no name |
| 03-hero-putty-boutique | boutique hero, wood + linen | bottle-hero (6246) | ✅ no name |
| 04-lifestyle-home | on a shelf, linen + wood | bottle-hero (6246) | ✅ no name |
| 05-giftset-flatlay | top-down open + closed box, eucalyptus | giftset-flatlay (6243) | ⚠ tag name |
| 06-openbox-threequarter | open box, three-quarter, linen | openbox-3q (6245) | ⚠ tag name |
| 07-giftbox-lifestyle | bottle on gift box, plaster console | giftbox-lifestyle (6250) | ⚠ tag name |

## QC notes
- **Label fidelity held** on the clean sources — the sharp, red-tinge-free
  photo gave the model a legible label to preserve. The 4 bottle-only heroes
  are pixel-perfect and carry **no customer name** → safe for the listing now.
- **One reject + retry:** the first `giftbox-lifestyle` take shrank the bottle
  and garbled the label ("H&DE DJ", "THE ONE AND UNTE"). Re-ran with an
  explicit "keep the label large and crisp, do not shrink the bottle"
  instruction → `07` passed. Lesson: when the product sits small in a lifestyle
  frame, the label degrades; force size/position in the prompt or crop tighter.
- **Customer name (PII):** shots 05–07 show the handwritten kraft tag
  "With love, Shelby & Sean x". If that's a real order, re-shoot with a neutral
  tag before any public listing — we never AI-edit the text to change it.
    The 4 name-free heroes have no such issue.

## Not yet done (needs a Max decision)
- **Second label design:** photos IMG_6252/6253 show a different personalised
  label — "HOME BY DAISY MAISON / HOME WITH THE *Smiths* / EST. 2005". Same
  restage workflow applies once we pick a website sample surname/year.
- **Ribbon colourways:** IMG_6251 shows the white box in **blush, lavender,
  charcoal, powder-blue**. A restaged "choose your colour" lineup is a strong
  extra listing image.
