# DM-C017 source provenance and cost record

Recorded: 23 July 2026

Status: DM-C017 v03 is a validated native engineering proof. The earlier
source composite and overlaid v02 outputs remain rejected evidence. Nothing is
published.

## Product and LightBurn source

| Source | SHA-256 |
| --- | --- |
| `projects/daisy-street-sign/artwork/build.py` | `0fa8a168613863f00cec42c0894c8d4e4c5a477f87dc47ee60ba02a04654c81b` |
| `projects/daisy-street-sign/artwork/assets/times.ttf` | `2cff2a03d8034801979dd6d16f09b9a825c3d710fcf068f2ebfbf0e1425c87cf` |
| `projects/daisy-street-sign/source/source-data.js` | `c16852abf80a6d13ce3bfac4b44f5bcd15279278efe7fbfcf976a8beaf120492` |
| Incoming order SVG `projects/daisy-street-sign/artwork/orders/DM37174.svg` | `6f1c2bd68f0c88bd717197f45c91c3efd43e960e7f39bba5fbb7cda5b67fdf45` |
| Incoming order PNG `projects/daisy-street-sign/artwork/orders/DM37174.png` | `01bacd1127fa747a851b83408ba582d0d2585260317ea3557c96442399b416a2` |
| Real physical reference photograph | `160cbfd81c434437628cbc98f9799bca22ca99dd8a3b91c0ec56a91aa62cfcd3` |

Product handle: `mr-mrs-personalised-street-sign-gift`.
Product GID: `gid://shopify/Product/9702132711763`.
Source SKU: `36961`.

Audited product truth:

- finished contour: 570 × 125 mm, 409 vertices;
- mounting holes: `(23.306, 63.735)` and `(546, 61.5)`, radius 2;
- LightBurn settings: speed 8, min/max power 75, two passes, blower on;
- Times New Roman regular, vertical scale 1.4;
- `#010101` frame/text, white panel, approved raster heart.

The generated SVG/PDF are exact visual sources. The workspace explicitly says
printer/RIP/nesting/laser handoff is not implemented and requires separate
office validation.

## Exact Jannaway face

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `assets/DM-C017-JANNAWAY-V02-sign-face.svg` | 136,830 | `e180b9e0a4a11825541d7c545fe01b534cf40bacc87c47383bc56fc2ea6b6184` |
| `assets/DM-C017-JANNAWAY-V02-sign-face.png` | 113,513 | `691c5ef8a68b7fc05e4971dd16d19c5c0af191c571080ca462bcd8563a50ce82` |
| `assets/DM-C017-JANNAWAY-V02-sign-face.pdf` | 138,905 | `1628f8a149312edca56216c0390cb7bdb52c5072804a48d5029407b57ce5456a` |

The PNG is 2280 × 500 RGBA. The PDF page is exactly 570 × 125 mm. The metadata
labels it as a visual source, not a production handoff file.

## Shopify demand

Shopify Admin was accessed read-only. The aggregation used order creation and
cancellation state plus line-item SKU, quantity, fulfilment, custom attributes
and product handle. No product, order or customer mutation occurred.

The retained aggregate covers 48 matching street-sign units among the sampled
latest 50 orders since 1 April 2026. Forty-three used the
`MR & MRS [SURNAME]` pattern and 44 contained a date. The Jannaway wording was
selected from existing incoming order artwork. No address, email, phone,
payment or other customer details were copied into this lane.

## Real Daisy Maison construction reference

Source Reel:
`https://www.instagram.com/daisymaison/reel/DPjdseCDbDR/`

The 10-second 1080 × 1920, 30 fps Daisy Maison Reel was downloaded for internal
product-reference/QC use. All 300 frames were decoded so thickness, reverse,
front artwork, hand contact and lighting can be inspected through one
continuous real turn.

| File | Source frame/time | SHA-256 |
| --- | --- | --- |
| `source/real-product-reference-pack/instagram-DPjdseCDbDR/daisymaison-reel-DPjdseCDbDR-video.mp4` | 300 frames / 10.00 s | `c160fd4795e63afe277b440b45b2527544d7a099bd2502d13b2da88324a070b9` |
| `source/real-product-reference-pack/instagram-DPjdseCDbDR/selected/01-front-frame-240-t08.000.jpg` | 240 / 8.000 s | `f584d777445a1abfdb3a436f8044aada4dd921bff200eb5ecca57c0691c7df03` |
| `source/real-product-reference-pack/instagram-DPjdseCDbDR/selected/02-front-to-edge-frame-180-t06.000.jpg` | 180 / 6.000 s | `7562c36447d3a4cecd2dce2b44beda2af728635f5d36c8caf5f164aef18cf19b` |
| `source/real-product-reference-pack/instagram-DPjdseCDbDR/selected/03-back-to-edge-frame-135-t04.500.jpg` | 135 / 4.500 s | `0efa9fb07149e428d7a7e4553a713cfcd2759115bc49ae1f43153514f7fe5c21` |
| `source/real-product-reference-pack/instagram-DPjdseCDbDR/selected/04-white-back-frame-060-t02.000.jpg` | 60 / 2.000 s | `b00ae16d857b02318b298bb1d627c9abf6a9cbd8fba0b4b142892bda467107e7` |
| `source/real-product-reference-pack/instagram-DPjdseCDbDR/product-only-crops/product-reference-pack.jpg` | Four-view face-free crop board | `84a1325a972ce2ae2f911d49af792c42062a46f0371babf4a821a9ee324a7ede` |

The sequence proves that the reverse is plain white, the physical edge is very
thin and pale/white, and the black perimeter is printed front-face artwork
rather than a black side wall. Product-only crops are the preferred model
references; the filmed person's face must not be used as an identity reference
or cloned. See `source/real-product-reference-pack/instagram-DPjdseCDbDR/REFERENCE_PACK.md`.

## Consented Max/workshop sources

Max explicitly consented to synthetic use of his likeness. No other person was
cloned.

| Local source | Pixels | SHA-256 |
| --- | ---: | --- |
| `source/max-workshop-back-reference.webp` | 1920 × 1920 | `4a61f1f4ea8a13f27b41ff212a0f6e034f030529b64e8239a6ec856029252f51` |
| `source/max-workshop-side-reference.webp` | 1920 × 1920 | `2f0551c5deda735bfc80f129fae37c4ae5a5b4f39f0cb72042a8991cbd85b37e` |
| `source/max-workshop-profile-reference.webp` | 1920 × 1920 | `5a7129c797ef58736ba0387e2a0f67f8bc1b1ee021f903d7d03875907c30c397` |

## Nano Banana 2 stills

Six malformed wrapper jobs were submitted first. Server records show each as
1:1, zero references and a 230-character truncated prompt. They cost 9 credits
and were rejected.

Six valid 9:16, three-reference Nano Banana 2 jobs then cost 9 credits:

`638bcec0-f347-42e2-9e5c-ff9499991121`,
`0f67694c-4b09-4a97-9bf5-2591208ffcb1`,
`28e294fe-942d-4246-874b-85a34136566a`,
`75610b5a-e9ed-4b6a-a368-8d00e4e6d260`,
`c256bc4b-3b2e-4065-b3d5-0d127fe2b93c`,
`48d7a48b-f7dd-4205-9345-bed2775b1d04`.

Selected take 08:

- generated still SHA-256:
  `1a8f5a1374fc9abc8e4a30d50921c3cc300c2bf6ac37a597a07fe268f1c16bbe`
- rejected composited exact-face still SHA-256:
  `16bab59954f0aaf0c5f558f28aa428c89b48bbeff170246a0b9db7741f501aaa`

The exact-face still was made by overlaying the canonical artwork and is not a
valid source image for future video generation.

## Native V03 still gate

After the real construction turn was recovered, four new Nano Banana 2 stills
were generated with six explicit references per job:

1. consented synthetic Max identity/composition;
2. exact Jannaway sign-face artwork;
3. real printed-front product crop;
4. real front-to-edge product crop;
5. real back-to-edge product crop;
6. real white-back product crop.

All jobs received the complete flattened prompt, 9:16 aspect ratio, 1K
resolution and all six media roles.

| Take | Job ID | Output SHA-256 | Agent QC |
| --- | --- | --- | --- |
| 01 | `76d6dd29-6a9a-4f89-b2ed-4913516fd7df` | `f02cb47e86e6f9d1a1b5e2b6bbe9fa6174a0e4864a635a2f69f3601bfe3216ab` | Rejected: black front band too thin |
| 02 | `c5f44c5f-55fe-4617-ad21-7dcb0f3b203a` | `7746386a40417a62a855afb44d422ded7ac3ffbc47ece1c43c5b4abc92162924` | Rejected: black front band too thin |
| 03 | `4f240f84-0622-488d-805f-191b6cd06763` | `f87bb500b9e94df5914d9e4fedd7afd9df9df8b427e55e50895cf3fb942b4aea` | Rejected: black front border missing |
| 04 | `01436c8d-b89a-414a-91db-9db1ccd35954` | `f33e3e169e2f98d288347af6f1a2fa7c8c5b2a1c62eb37a1411385df8c0d3570` | Rejected: black front band too thin |

The account ledger records four Nano Banana 2 spends of `-1.5` credits, 6
credits total, with 1488 credits remaining immediately afterward. The files
are untouched native outputs. No SVG, panel, border or lettering was
composited or corrected. All four are rejected; no V03 candidate is a valid
video source.

## Aborted V04 geometry correction

The four-take V04 border-correction prompt was cost-quoted at 1.5 credits per
take but aborted before generation. Actual cost was zero. Max identified that
it still split product truth across flat artwork, multiple construction views
and numeric geometry. That structure allowed the model to reinterpret a real
manufactured sign.

Evidence:
`working/batches/hero-still/v04-border-correction/`.

## Locked-real-sign product calibration V01

The replacement experiment used only:

1. the real printed-front product crop as the locked manufactured-object
   master; and
2. the exact Jannaway face as replacement printing only.

All four jobs received the same literal prompt, 16:9 aspect ratio, 1K
resolution and both references. No creative variant text was used.

| Take | Job ID | Output SHA-256 | Agent QC |
| --- | --- | --- | --- |
| 01 | `6b50a1b2-ac90-4621-a763-bb0ea72a1902` | `e29d79e4c0c2ce53c2b0beb02d30364df68fdc31030cd44a65c1e4653b32e962` | Reject exact art: heart simplified |
| 02 | `91c3e535-fe6f-400b-9abe-a5c263ffd681` | `1ae83cca1afb4dda263604ee7bb09a7883acc5a8a0ba9fb4070ea00e3572a40e` | Product-realism candidate |
| 03 | `4c0831d8-b5b2-4beb-960a-9848a5b76823` | `588121fe08ebd7db366119f057e4c50d31e5151c3e587657ebbe2333740c8b4c` | Recommended for Max's product approval |
| 04 | `8962bdd9-8bb4-4cc4-880a-2f1850d7d080` | `62039aaf5b53fb11c4625ddfa3ab82419712f4a9f679d0a7421e7f8638fe7d6b` | Product-realism candidate |

Supporting hashes:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| Locked real-front crop | 34,135 | `4de7858d22906267bfa0afa624693f92b89df798b427c948567f4a6152e8ab7b` |
| Exact submitted prompt | 1,686 | `cbfc7715231c47ba88d2dfd4e6e64a0a79659ccc6afd272d4e7449ef31b0cdc1` |
| Native CLI argument helper | 1,508 | `e6df4cf6c142199cd9f285c3c749217105b88561ab3a88be92a460fe591815ff` |
| Master/target/four-take contact sheet | 256,475 | `1adfd7e7d9c086f70a3c6c0fe841c2cbd8de0bcc9e3a5e117670581c72926cd6` |

The ledger records four additional `-1.5` Nano Banana 2 transactions, 6
credits total, leaving 1482 credits. All four native outputs solve the
different-white pasted-panel appearance and preserve a visually substantial
black front band. Max approved Take 03 as the validated product checkpoint on
23 July 2026. No image was composited or repaired.

Approval:
`approvals/PRODUCT_IMAGE_CHECKPOINT.md`.

## Approved-product-lock hero stills V05

Four identical Nano Banana 2 jobs used:

1. approved product Take 03 as the sole complete-sign authority; and
2. the consented synthetic-Max keyframe as identity, clothing, body-scale and
   workshop authority only.

The invalid marker plate in the identity keyframe was explicitly excluded.
Every job received the complete prompt, both references, 9:16 aspect ratio and
1K resolution.

| Take | Job ID | Output SHA-256 | Agent QC |
| --- | --- | --- | --- |
| 01 | `166349ab-b616-4213-b385-f5e028ce7fb1` | `0af3797d7fad5145a1b4a2a50ebe73f7596e51509b522202f0a77f301589d6f8` | Recommended for human hero approval |
| 02 | `a0a8180f-b1c2-4ba0-99fb-160cbea1860b` | `3bd7be7ee6b5a66bb8c90af09ff7c67a15bc29b3de8d45f2702894202152c294` | Pass, secondary |
| 03 | `6af1cfb7-6542-4690-aeb4-05ebddb997f3` | `c729feddfc36d8a19535124644a8eaf22b7c3638d0579664c992ec8101c1fe3d` | Pass, secondary |
| 04 | `7aea6341-a82b-47cd-ac72-a855025ee2fc` | `10316551143ef31bc65c2cd2f6d03530efa3ee094f95a03526f1efe8c3b9ec34` | Pass, secondary |

Contact sheet:

- path:
  `working/batches/hero-still/v05-approved-product-lock/contact-sheet-identity-product-takes.jpg`;
- bytes: 280,434;
- SHA-256:
  `3b7f84b3d1b94593a6d0aefd3435cc0fb3457485dcaf7426eac45243a1e5eab4`.

The ledger records four more `-1.5` transactions, 6 credits total, leaving
1476 credits. All four are untouched native outputs and pass agent review.
Max later approved Take 01. A separate four-image white-back batch cost 6
credits, and Max approved Start Take 01 before the validated native video was
submitted.

## Seedance motion

- Job: `7d7f3cb6-13ce-4721-bcc1-fc0d369de561`
- Model: Seedance 2.0 Standard
- Settings: 9:16, 1080p, High bitrate, 8 seconds, no audio, no multi-shot
- Start media: `d6675e0b-0224-4220-80b7-bd2692592e08`
- End media: `ed03186d-b8ea-4966-9a4d-a61dbe9b8e8f`
- Exact-art reference: `fec3fcac-f0db-4676-ba99-12a6d23b00f1`
- Cost: 72 credits
- Raw file: 35,954,202 bytes
- Raw SHA-256:
  `fd187238800f91e2159d37d674da64bbe2078da61719c8e7398893a6a344f77a`

The raw video is genuine generated movement, but it is rejected product
evidence: the sign becomes too thick and its reverse is black. Those faults
follow from the edge and white-back references being absent from that
generation request; the real reference pack was recovered later.

## Rejected finished outputs

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `exports/DM-C017-JANNAWAY-master-1080x1920.mp4` | 7,325,341 | `0303e15853373c78188140edfc6e1b988fe735f7d5c8bcd458acba0e6685a9c6` |
| `exports/DM-C017-JANNAWAY-phone-preview-720x1280.mp4` | 1,229,929 | `c5511c0e558f0287f78f8570b196b5d8ad9754f4d84d6bcc7c182089b487b6e4` |
| `exports/DM-C017-JANNAWAY-synthetic-sound.wav` | 1,536,044 | `735c2e2da6663c85c8f475feb9c737db7a52d299ddef0d6416e06f13c7c77d66` |

The master and preview additionally contain a forbidden tracked face
replacement. The panel is visibly whiter than the physical border and reads as
an overlay. The files are retained only as failure evidence.

## Rejected-method QC evidence

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| Full Reel filmstrip | 530,028 | `6b36607ccc6277822e5096505d2bdcc4205e64bc4c3b8ca8c63912bf8b1ee4a5` |
| Source-versus-video JPG | 906,488 | `af3d93cce16b9565357b526a392a5affdbda9f73231227fa269c7fbbd87f1e11` |
| 122-frame lettering QC PDF | 5,723,359 | `57417855409e46d0c9fdbfecdbd64d3160e88c6da8a662dc852168f91c6c255e` |
| Planar track JSON | 106,673 | `9cc2bdb2c692af9df43da7c05b630218ca2f37c684d41a43e085faab43735dcd` |
| QC report JSON | 5,044 | `dd9ac18637f73cdac5bb105b53e8b8c4c7366ee9f6fb8fb777a581db02e0de99` |

These checks prove format, continuity and source-pixel mapping only. They
failed to assess coherent material, border colour, thin profile and white
reverse, so they do not constitute an acceptance result.

## Claude/Fable consultation

The real authenticated Fable CLI was consulted successfully earlier in this
DM-C017 investigation. Its useful cautions were that edge-on homographies,
non-rigid planes and non-monotonic rotation were the core tracking risks.
Subsequent direct testing superseded its earlier browser-only assumption by
proving the native `hf.exe` route.

A fresh read-only Fable re-review was attempted on 23 July 2026, but the CLI
returned no output before a 244-second timeout. That second attempt is recorded
as failed and is not represented as a consultation result.

## Cost summary

- Malformed Nano Banana 2 wrapper jobs: 9 credits
- Earlier valid Nano Banana 2 stills: 9 credits
- Native V03 six-reference stills: 6 credits
- Locked-real-sign product-calibration stills: 6 credits
- Approved-product-lock synthetic-Max hero stills: 6 credits
- Matched plain-white reverse stills: 6 credits
- Rejected Seedance 2.0 v02: 72 credits
- Validated native Seedance 2.0 v03: 72 credits
- Validated method incremental cost: 90 credits
- Total known historical DM-C017 Higgsfield spend: 186 credits
- Verified balance after validated video: 1,398 credits
- Local OpenCV/FFmpeg processing: no incremental service charge surfaced
- Publishing: none

No unknown monetary conversion is represented as £0.

## Validated v03 artifacts

| Artifact | SHA-256 |
| --- | --- |
| Native video | `8239be73824ac44d5b89704e0fedc7b5ffc2744d62a0fb2f55f62125ce901c6e` |
| Finished 1080 × 1920 master | `7cfb52c26fa5727817e718e282a59bb5aa80377ee1730533629ad602d25a2a0b` |
| 720 × 1280 phone preview | `4730e21852a05367f4ac36a321e546ee3a9c3baea863befcb8432dd3fa82522f` |
| Exact delivered SVG | `e180b9e0a4a11825541d7c545fe01b534cf40bacc87c47383bc56fc2ea6b6184` |
| Exact delivered PDF | `1628f8a149312edca56216c0390cb7bdb52c5072804a48d5029407b57ce5456a` |

Validated native job:
`bf94cfac-e34f-4da7-8922-6cfc8322b1fc`.

Max's human approval record is `approvals/NATIVE_VIDEO_CHECKPOINT.md`.
