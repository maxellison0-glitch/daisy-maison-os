# Family beach sunset pebble picture (2 Oct 2026)

**Product:** "Personalised Family Pebble Picture Gift — Beach Sunset | Unique Family Home Gift UK"
- Handle `family-beach-sunset-personalised-pebble-picture`, id `10904193761619`.
- Made from Max's three photos of the real picture:
  - white frame;
  - "FAMILY / TOGETHER IS OUR FAVOURITE PLACE TO BE";
  - a beach sunset with three pebble people holding hands;
  - "DADDY ♥ MUMMY ♥ RUBY" beneath.

**Status:** not finished.
- The product exists, with its gallery.
- The builder config is on the unpublished copy **"Claude – family beach pebble picture (2 Oct)"** (theme `208280125779`). That copy is a duplicate of live "Claude – pet preview colours (2 Oct)" (`208260268371`).
- **On the copy, the personalisation builder does not switch on for this product yet** (see "Blocked" below).
- Not published. Max publishes.

## Product (modelled on Family Walk In The Park, its closest family sibling)

| | Value | Source |
|---|---|---|
| Price | £29.95, compare-at £34.95 (shows SAVE £5.00) | Same as Walk In The Park and the Mum picture in Max's screenshot |
| Variant | Default Title, untracked, 1.1 kg, taxable | Same as siblings |
| Tags | `Pebble People` | Same as siblings |
| Collections | Framed Pebble Art, My Home, Occasions, Pebble People | Walk In The Park's manual collections |
| Status | **Unlisted**, published to Online Store only | Reachable by direct link for the preview, but kept out of search, collections and recommendations until Max publishes |
| Description | Walk In The Park's, with the scene, wording and "up to 8 family members" changed | Spec and delivery text copied as-is |
| SEO | Sibling pattern for the title. The sibling's "FAST FREE DELIVERY" claim was left out, because free delivery only applies over £50 | |

**For Max to check:**
- **Frame size.** The description copies the sibling spec (21x30cm, white or grey). The photos show the same landscape frame, but please confirm.
- **SKU.** Left blank, because siblings use mixed formats (`86607`, `PP-002-WED`).

**When Max publishes the theme:** switch the product from Unlisted to Active so it appears in the collections.

## Builder config (on the copy)

- `snippets/dm-pebble-picture-builder.liquid` (md5 `8aed4ba9…`):
  - The handle uses the existing Walk In The Park builder type (`walkpark`): frame colour, 1–8 pebble characters, each with a name, and keep-or-change wording.
  - INCREDIBLE OFFER second picture £20 (`20-incredible-offer`).
  - Wooden Display Easel and Gift Wrap Kit add-ons.
  - Inside the walkpark block, this handle gets its own:
    - heading, "Create your family beach pebble picture";
    - default wording, "Family – Together is our favourite place to be";
    - frame list, using the standard `dm_frame_values`, White first.
  - Walk In The Park itself is unchanged.
- `snippets/dm-proof.liquid` (md5 `f9dc79d9…`): reuses the verbatim family-pebble-picture review already used on the Family Blossom Tree, "Delighted with my lovely family pebble picture. Even better than I'd dared to hope.", with the line "Loved by families across the UK".
- No matching heart is offered, because there is no beach-family heart product.
- Full change: `family-beach-0210.diff`.

## Blocked: the builder stays hidden for this product

Phone tests on the copy (390px, gated loads):
- **New product:** the gallery, title, price and proof line all render. The builder root renders with valid config JSON, its scripts load, and there are no script errors. But the root keeps its `hidden` attribute, so the page falls back to the plain Add to Cart.
- **Same result** with a builder type of its own (`beachfamily`) and with the existing `walkpark` type.
- **Control:** Walk In The Park on the same copy shows the full builder (frame, pebble characters with names, wording, second picture £20, easel, wrap kit).
- **Admin data:** identical apart from status (Unlisted vs Active) and handle. `/products/<handle>.js` and `.json` both return 200.
- **Not the cause:** `layout/theme.liquid` does not gate pebble pictures by handle.
- **Likely cause:** `assets/daisy-pebble-picture.js` only switches on for known handles. My permission check blocked reading that script, so this is untested. It needs Max's OK to read and, if so, a one-line addition on the copy.

## Images (Higgsfield)

The reference inputs were Max's photos:
- the close-up;
- the front-on shot, cropped to the frame so that the workshop background (and a person in it) was not sent.

No faces went into the generator. Every image's wording was checked at full size: FAMILY / TOGETHER IS OUR FAVOURITE PLACE TO BE / DADDY ♥ MUMMY ♥ RUBY, correct on all nine.

| Input | SHA-256 |
|---|---|
| `ref-front.jpg` (cropped) | `e48037c538b991c2f5a7fac62ae269cdae08287f40f1428845fd04bbdae5d491` |
| `ref-close.jpg` | `d5e00566789db53c64314dc0d9086ff07aacbccd9c830bd644975bc7f06522ed` |

**Set 1: GPT Image 2.5, high, 2k, 2.75 credits each, 11 credits**

| Job | Shot | On product |
|---|---|---|
| `31e3da52-b99f-49f9-847d-46aaec516f2f` | Hands holding it among pink roses (mirrors the wedding hero) | yes |
| `a7a9fd77-59d6-41de-b2e6-8246fa806d4f` | Christmas kraft-gift flat lay (mirrors the Mum hero) | yes |
| `dd9d1f55-8353-4cec-8d0e-6a0302d14de9` | Oak sideboard, coastal living room | yes |
| `287a0e98-37ff-4618-903c-d52521f0205e` | Lifted out of a kraft gift box | yes |

**Set 2: Nano Banana 2, 2k, 2 credits each, 10 credits.** Max asked for "less twee, more modern".

| Job | Shot | On product |
|---|---|---|
| `521c5577-9677-4f6e-8307-1580baf55439` | Floating oak shelf, window shadows | yes (gallery image 1) |
| `d717c970-70ef-46b8-9c14-0770d37926dc` | Black hallway console, mushroom lamp | yes |
| `f2e8c1ca-b85e-4d95-b62a-7690ac2b219c` | Studio terracotta plinth with two pebbles | yes (gallery image 2) |
| `3b2fb44a-85d4-4e46-bd2a-0f5da230c6f3` | Picture ledge over a sofa | **no**: the frame is shown roughly sofa-width, which misleads on the 21x30cm size |
| `606c2430-31f2-41b9-819d-05e0a7e801f1` | Hand placing it on a walnut sideboard | yes. Note: a book spine in the background has AI lettering |

**Total spend:** 21 credits (balance before: 1,736).

**Verdicts.** Every image is `agent-pass` only. None is `max-approved`.

**Gallery order:**
1. Shelf.
2. Plinth.
3. Real close-up photo.
4. Christmas flat lay.
5. Hallway.
6. Hand.
7. Gift box.
8. Sideboard.
9. Roses.
10. The existing Christmas-wrapped picture.
11. The existing wrap-kit contents image.
