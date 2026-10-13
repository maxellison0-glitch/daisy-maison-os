# DM-CARL-EMILY emoji sign — square website images, 13 Oct 2026

State: **agent-pass** on C1e, C2, C3e. NOT max-approved, not uploaded to Shopify.

Target: a new square image for the Mr & Mrs street sign listing
(`mr-mrs-personalised-street-sign-gift`) showing the colour-emoji
personalisation (bouquet before line 2, champagne bottle after it).

## Max's verdict mid-batch — logged as it was spoken

> "look at our main images none of them look like that. no humans for this"

Website main images are **the sign on its own in a styled setting** — wall,
shelf, mantel, gatepost, fence — never a person. The held-format rules in
`REFERENCE_PACK.md` / `VERDICTS.md` are for social content, not listing images.
Also logged in `reference-masters/VERDICTS.md` (Round 4).

## Source

A real finished customer sign photographed on the packing bench by Max
(`CARL & EMILY / 💐 CONGRATULATIONS ON YOUR WEDDING DAY 17.10.2026 🍾`).
Cropped to the sign only, which removes the Shopify order printout and the
packing bench. The crop is the only input that carries the printing.

| Input | SHA-256 | Higgsfield media |
|---|---|---|
| Original upload (not committed — 3072², bench + order sheet in frame) | `c2208258a25e8031c69240d1aeaf8dea36da55e2289709325b792e798ac9c166` | — |
| `ref1-real-sign-CARL-EMILY-crop.jpg` (3000×880) | `1c4a3fbd5f77278bd406180c5970bed3552e939e10449e8e97657fe0bd12a4d9` | `7b9dae8e-cba3-4c21-94d6-54b1b69c0b0d` |
| `reference-masters/street-sign-BLACK-on-white-MASTER.jpg` (rounds 1 only) | `588121fe08ebd7db366119f057e4c50d31e5151c3e587657ebbe2333740c8b4c` | `47f198d8-5ef1-47c4-981e-54d89667fa4c` |

The names and date are a real customer's wording. First names and a date only,
no surname, address or contact — inside the "display wording when safe" rule,
but Max should decide before it goes on a public listing.

## The main-image recipe, recovered from the live jobs

Pulled from Higgsfield job params of the live featured images (0 credits):

| Live main image | Job | Model | Refs |
|---|---|---|---|
| Taylor & Travis, wall above shelf | `f9284022-d4b5-4cd0-b2bf-989ba67640b0` | `nano_banana_flash` 1:1 2k | one style/scale ref |
| The Potter Family, mantel | `6692efb2-306d-4050-b27a-435d003c18bb` | `nano_banana_flash` 1:1 2k | product + "image 2 is for a size reference only" |
| Grandma's Garden, white garden wall | `9e29e5ac-1037-427d-8be1-e69fd43bc54f` | `nano_banana_flash` 1:1 2k | product |
| David & Victoria, white wall | `a6d7a1d5-0d0b-456b-bbb2-db5527cc3e20` | `nano_banana_flash` 1:1 2k | product + Taylor & Travis as size ref |

Pattern: "Take the exact street sign from the reference image — do not alter…"
→ "the exact size is 57x12 cm" → one existing main image as size/scene
reference → scene + props → "Sign is the hero — fully visible, sharp,
completely legible. No letters cropped. Flat matte acrylic, no shine, no
glare. Shot on Sony A7 IV, 50/85mm f/1.8, film grain, no CGI."

**`nano_banana_flash` no longer exists on Higgsfield** (13 Oct: "unknown
model"). `nano_banana_pro` stood in; its jobs report as `nano_banana_2`.

## Jobs — 10 generations, 20 credits

Nano Banana Pro at 2k is **2 credits per image**, confirmed in the account's
transaction log. The `get_cost` preflight for `count: 2` returned `2`. That
figure is per image, not per pair, so it reads as half the true price. Quote
from a completed job's transaction, as `daisy-video-generation` already warns.

### Round 1 — rejected / discarded

| File | Job | Verdict |
|---|---|---|
| `A1-table.png` | `e80a4129-d2c7-4a5d-be4b-412e0147ff29` | **reject** — sign redesigned to ~2.5:1 to fit the easel, sans font, line 2 wrapped |
| `A2-table.png` | `40cdd904-e164-46aa-b7f6-6b63968ae384` | **reject** — sign redrawn near-square, three-line layout |
| `B1-held.png` | `6003ec0a-d74a-425e-a3cf-7d6e0bd5db36` | **discard** — sign exact, but a person (Max: no humans) |
| `B2-held.png` | `139bb776-2c85-436c-8c26-8d4f91000266` | **discard** — as B1 |

Lesson: asking for a tabletop easel in a square frame made the model reshape
the sign to suit the prop. The wall / mantel formats of the live mains never
did. Prompts: `prompt-A-reception-table.txt`, `prompt-B-held-reception.txt`.

### Round 2 — the main-image recipe

Ref 1 = the real sign crop; ref 2 = the live main image named below, for size
and scene proportions only.

| File | Job | Size ref | Verdict |
|---|---|---|---|
| `C1-shelf.png` | `30a54812-f7e2-4b68-a4a2-2a1aade48429` | Taylor & Travis | superseded by C1e — bottle read "THAMPAGNON" |
| `C2-mantel.png` | `634ffebb-ec58-4a7e-9cb6-50919a0d69fe` | Potter Family | **agent-pass** |
| `C3-console.png` | `6445067b-e21b-4c2a-a625-40b64ad18aa5` | David & Victoria | superseded by C3e — real Moët & Chandon label |
| `C4-venue.png` | `b6239348-a7f0-4152-88da-0616c41fdd5d` | Dad's Bar & Grill | **reject** — "EMLY", and guests in the background |
| `C1e-shelf-unbranded.png` | `23a9f7de-5c39-4bf2-8ecc-1920efcfa56a` | edit of C1 | **agent-pass** |
| `C3e-console-unbranded.png` | `a10fbf44-b23c-4977-8fbc-ffdebc0f452c` | edit of C3 | **agent-pass** |

Prompts: `prompt-C1-shelf.txt` … `prompt-C4-venue.txt`, `prompt-label-edit.txt`.

### Checked on every agent-pass

- "CARL & EMILY" and line 2 character-exact; heart touching the ampersand.
- Both emojis present, correct (bouquet before, champagne bottle after), not enlarged.
- Line 2 small, single line, regular weight.
- No mounting holes (`SIGN_HOLES=0` rule).
- Full sign in frame, shaped ends intact, no people, no third-party branding.

Not checked against a Max verdict: prop scale. Flutes and bottles read a
little small against a 57cm sign on all three, as they do on the live
Taylor & Travis and David & Victoria mains.

Images are gitignored (`Content Pipeline/**/*.png|jpg`); the job IDs above
re-download them from Higgsfield.
