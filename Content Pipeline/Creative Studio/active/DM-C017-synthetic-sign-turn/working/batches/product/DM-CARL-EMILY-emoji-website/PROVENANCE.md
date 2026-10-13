# DM-CARL-EMILY emoji sign — square website images, 13 Oct 2026

State: **E3 is the current candidate**. Max picked the C2 mantel; round 3 restyled the room and round 4 replaced the white mantelpiece.
Not max-approved as final, not uploaded to Shopify.

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

## Jobs — 18 generations, 36 credits

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

Prop scale: flutes and bottles read a little small against a 57cm sign on
C1e and C3e, as they do on the live Taylor & Travis and David & Victoria
mains. Max confirmed it in round 3: "the others looked weird to me still".

### Round 3 — Max's pick, restyled

Max on C2: "this ones cute but it looks ai generated the flowers the
fireplace. Make it a tad warmer and more modern/uk at the same time. **Size is
bang on for realism** (the others looked weird to me still). Use this as the
ref image."

Diagnosis: C2 has two fireplaces, the one under the sign and a second one
burning across the room, plus a saturated florist-dome bouquet and two
identical champagne buckets. Those duplicates read as AI.

Edit of C2 (job `634ffebb`, passed by job ID at 2048px; Max's attachment was
a 1092px copy of the same image). `nano_banana_pro`, 1:1, 2k, count 4, 8
credits. Prompt: `prompt-D-mantel-restyle.txt`. It locks the sign, removes the
second fireplace, restyles the room as a renovated Victorian terrace in the
house interior style, uses a loose stoneware-jug arrangement and one bucket,
and adds real-world flaws.

| File | Job | Sign width / frame | R/B warmth | Verdict |
|---|---|---:|---:|---|
| `C2-mantel.png` (Max's pick) | `634ffebb-ec58-4a7e-9cb6-50919a0d69fe` | 67% | 1.465 | reference |
| `D1-mantel-restyle.png` | `5dd52274-daf1-4e0b-b9b1-6f4dadb86b60` | ~56% | 1.421 | reject: sign shrank |
| `D2-mantel-restyle.png` | `24c696b6-135d-42b3-bc8b-54081304e892` | ~55% | 1.274 | reject: sign shrank, cooler |
| `D3-mantel-restyle.png` | `c812b3be-4c4a-4674-9578-af6633066db7` | 68% | 1.381 | **agent-pass**: size held, sign exact |
| `D4-mantel-restyle.png` | `60481a76-df39-40ce-ac0b-924801475c40` | ~56% | 1.361 | reject: sign shrank |
| `D3w-mantel-restyle-WARM.png` | local grade of D3, 0 credits | 68% | 1.551 | **candidate** |

Lesson: "keep the same framing" did not hold on 3 of 4 takes. The model
pulled the camera back to show the new room. Measure sign width against the
frame on every restyle, because Max calls size by eye.

Lesson: asking the edit for "a touch warmer" made every take cooler. The new
dusk window brought blue in. Warmth is done locally and for free: a linear-light
white-balance shift (R ×1.08, B ×0.84, soft highlight shoulder) applied to the
whole frame. Sign panel goes from 196/179/171 to 203/179/158, a warm white
under lamp light. No layout or lettering is touched.
D3w SHA-256 `9783dc8f83f3436771ef78ef82f184badca9ffa634c5f2f3bdeb0dea1bfb6428`.

### Round 4 — the white mantelpiece goes

Max on D3w: "get rid of the ugly ass white mantelpiece i don't like it. Looks
uncanny to me"

Edit of D3w (uploaded as media `64bd3a0d-9373-4e0e-9a75-6d36247ee4cc`), so
the model inherits the warm grade. `nano_banana_pro`, 1:1, 2k, count 4, 8
credits. Prompt: `prompt-E-oak-beam.txt`. It swaps the white surround for a
chunky oak beam set into a plastered chimney breast, with a black wood
burner on a slate hearth below. The prompt states the sign's frame width
("about 68%") and says "do not pull the camera back". **All 4 held the
size** (~69%), against 1 of 4 in round 3 when no number was given.

| File | Job | Verdict |
|---|---|---|
| `E1-oak-beam.png` | `a41a0d2d-a23a-4bdf-ab4c-6f057ac528f0` | agent-pass: stove top stops under the beam, no flue |
| `E2-oak-beam.png` | `ff3b695a-0ed6-4e43-a1fd-1313bd1db6e0` | agent-pass: as E1 |
| `E3-oak-beam.png` | `de22224e-ea1d-4f07-bf51-c30d0eeeea7e` | **candidate**: whole stove on its hearth, flue stub rising behind the beam |
| `E4-oak-beam.png` | `50d1e2f4-c64e-44f3-bc90-6b4f2c71f351` | agent-pass: stove cropped by the bottom edge |

Every sign exact. Sign panel white measures the same as D3w (~235/197/167),
so no regrade. Whole-frame R/B rose to ~1.72 from the honey oak, not from
the light.

Images are gitignored (`Content Pipeline/**/*.png|jpg`); the job IDs above
re-download them from Higgsfield.
