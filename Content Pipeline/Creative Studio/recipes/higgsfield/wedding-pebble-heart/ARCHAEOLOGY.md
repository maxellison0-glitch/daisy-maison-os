# Wedding pebble heart - prompt archaeology

Status: asset 01 Higgsfield recipe recovered. Assets 03-04 provenance corrected
to the July OpenAI gift-box project. Asset 02 remains unresolved.

## Exact local targets

Source folder:
`../../../active/DM-C016-the-morning-of/assets/`

| Asset | Dimensions | SHA-256 | Archaeology state |
|---|---:|---|---|
| `01-main-open-heart.png` | 2048x2048 | `FB66FCFFA2FEF15BF5B352489697B61A3FD53EAA41DCA23FC53C8A94FF939927` | RECOVERED - see recipe below |
| `02-gift-box-heart.png` | 2048x2048 | `A9F2F6993DC9D4013554495BE0F8F336B98353B5A86C41DC1598B6865B299A7B` | Origin unresolved; Shopify re-encode only |
| `03-box-together-they-built-a-life.png` | 1254x1254 | `8181A683D435F70166C102036936D793C5FFDE8B831B3392D9E7A33BA5FCF8BA` | OpenAI gpt-image July mockup provenance recovered |
| `04-box-from-this-day-forward.png` | 1254x1254 | `7AD7D3E618922EAC522F3BE4E665E1394A1F5E83A2DA7B83F590768F1062EDD8` | OpenAI gpt-image July mockup provenance recovered |
| `05-product-reference-original.jpg` | 1140x1140 | `36C7DF238DE814B308F789A546E4035D39C0A73897C2A858D9EA0C8B0955D8A5` | CONFIRMED as the reference input of job `0e760551` (visual identity; Higgsfield media id `70fa28d5-704b-4263-94ed-2a14e1d30279`) |

## Recovered recipe - asset 01 (verified 22 July 2026)

Job `0e760551-d50b-4ced-b91e-7312e73972b5`, type image, status completed,
created 14 May 2026 17:53 UTC (matches the Shopify filename
`hf_20260514_175310_0e760551-d50b-4ced-b91e-7312e73972b5.png` exactly).

Verification: byte hashes differ because Shopify re-encodes uploads, but the
downloaded job output is 2048x2048 and visually identical to
`01-main-open-heart.png` (same "Dan & Rebecca" personalisation, pebble
placement, ribbon fold, linen creases, window light). The job's single
reference input is visually identical to `05-product-reference-original.jpg`
(the real hands-holding-the-heart product photo).

| Field | Value |
|---|---|
| Model | `nano_banana_flash` |
| Aspect ratio | 1:1 |
| Resolution | 2k (2048x2048) |
| Batch size | 1 |
| Reference input | one image, Higgsfield media id `70fa28d5-704b-4263-94ed-2a14e1d30279` = asset 05 |
| Reference elements | none |

Exact prompt:

> Take the exact heart plaque from the reference image — do not alter the
> shape, pebbles, ribbon, or any text. The heart plaque rests flat on a soft
> white linen surface, ribbon gently curled above it. Soft natural window
> light, subtle shadow beneath. Clean, minimal product photography. Shot on
> Sony A7 IV, 85mm f/1.8. No CGI, no rendering, no added props.

Recipe pattern: real product photograph in -> explicit product-immutability
instruction -> restage surroundings only (flat lay, linen, natural light) ->
photographic camera language -> explicit negative constraints ("No CGI, no
rendering, no added props"). This matches the DM-C014 rule set: the product
pixels are treated as truth and only the scene is generated.

## Corrected provenance - assets 03 and 04

These two gift-box images are not May Higgsfield outputs and must not be sought
in Higgsfield history.

Git commit `5e9b0e094713fe44ae7053546c9da1abd99f31f8`, dated 17 July
2026 16:56:57 +01, added the original product mockups:

- `projects/gift-box/artwork/mockups/03-together-giftbox-mockup.png`;
- `projects/gift-box/artwork/mockups/09-from-this-day-forward-giftbox-mockup.png`.

Decoded-image comparison against the Shopify copies is exact
(`gray_corr=1.00000000`, `gray_MAE=0.00000`); the file bytes differ because
Shopify re-encoded them.

Both preserved originals carry C2PA assertions naming:

- claim generator: `OpenAI Media Service API`;
- software agent: `gpt-image`, version `2.0`;
- digital source type: `trainedAlgorithmicMedia`;
- creation date: 17 July 2026.

The preceding concept commit is
`0f0112618275deacff7a7889dcb393f380051677` (16 July 2026). Exact prompt
recovery, if still useful, belongs in the bounded 16-17 July OpenAI/Codex task
history or the documented `E:\sean` working source, not Higgsfield.

## Unresolved provenance - asset 02

`02-gift-box-heart.png` contains no prompt, job ID or creation timestamp. Its
EXIF identifies Shopify processor `imagery4`; there is no exact duplicate among
workspace images. The safest next factual lookup is its Shopify MediaImage
record: media ID, `createdAt`, original filename and original source URL. That
timestamp may then bound a Higgsfield lookup. Do not assume 14 May solely
because asset 01 was made then.

## Known failed reconstruction lesson

Text and attractive lighting are insufficient identity checks. DM-C016 Take 2
preserved the lid motif but materially exaggerated the box's apparent size and
depth.
Future product identity sheets must include real dimensions, construction and
hand-relative scale before any agent review.

DM-C016's measured constraints now live in
`../../../active/DM-C016-the-morning-of/PRODUCT_IDENTITY.md`.
