# Family beach sunset pebble picture (2 Oct 2026)

**Product:** "Personalised Family Pebble Picture Gift — Beach Sunset | Unique Family Home Gift UK"
- Handle `family-beach-sunset-personalised-pebble-picture`, id `10904193761619`.
- Made from Max's three photos of the real picture:
  - white frame;
  - "FAMILY / TOGETHER IS OUR FAVOURITE PLACE TO BE";
  - a beach sunset with three pebble people holding hands;
  - "DADDY ♥ MUMMY ♥ RUBY" beneath.

**Status:** built and tested on the unpublished copy **"Claude – family beach pebble picture (2 Oct)"** (theme `208280125779`), a duplicate of live "Claude – pet preview colours (2 Oct)" (`208260268371`). Not published. Max publishes, then switches the product from Unlisted to Active.

Preview: https://daisymaison.co.uk/products/family-beach-sunset-personalised-pebble-picture?preview_theme_id=208280125779

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

## Fixed: the builder stayed hidden at first

Phone tests on the copy (390px, gated loads):
- **New product:** the gallery, title, price and proof line all render. The builder root renders with valid config JSON, its scripts load, and there are no script errors. But the root keeps its `hidden` attribute, so the page falls back to the plain Add to Cart.
- **Same result** with a builder type of its own (`beachfamily`) and with the existing `walkpark` type.
- **Control:** Walk In The Park on the same copy shows the full builder (frame, pebble characters with names, wording, second picture £20, easel, wrap kit).
- **Admin data:** identical apart from status (Unlisted vs Active) and handle. `/products/<handle>.js` and `.json` both return 200.
- **Not the cause:** `layout/theme.liquid` does not gate pebble pictures by handle.
- **Cause:** `assets/daisy-pebble-picture.js` has its own list of allowed handles (`var handles = [...]`) and stops if the page's handle isn't on it. Reading the script was blocked by the permission check until Max asked for the landing page to be finished.
- **Fix:** the handle was added to that list on the copy (md5 `562e86cd…`).
- **Lesson:** a new pebble picture needs its handle in **both** `dm-pebble-picture-builder.liquid` (config) **and** `daisy-pebble-picture.js` (allowlist).

**Tested after the fix** (390px phone, copy):
- The builder shows "Create your family beach pebble picture" and £34.95 / £29.95 / SAVE £5.00.
- Fields: Frame Colour (White first), 1–8 pebble characters with names, and keep-or-change wording ("Family – Together Is Our Favourite Place To Be").
- Offers: second picture £20, easel £5.95, gift wrap kit £5.95.
- Proof line: "Loved by families across the UK".
- Basket: 1× £29.95, with `Frame Colour: White`, `Change Text?: NO Keep Family – Together is our favourite place to be`, `No. of pebbles: 3 (Inc dog/cat)`, Pebble 1 Adult / Name 1 Daddy, Pebble 2 Adult / Name 2 Mummy, Pebble 3 Child / Name 3 Ruby, and `*SECOND FRAME*: NO Thanks`.
- No script errors.

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

**Set 3: Nano Banana 2, 2k, 2 credits each, 10 credits.** Max asked for "less boring backgrounds, no wooden tables, modern, different angles". He also said "Nano Banana 2 only @ 2k" and "no GPT image", so the four GPT images were taken off the product.

| Job | Shot | On product |
|---|---|---|
| `cc4aaa79-2ee1-4819-a97a-47318f22cfe2` | Terracotta plinth and wall, low three-quarter angle | yes |
| `846a32be-ff43-4abf-940f-8c6c8bf3a2bb` | Overhead flat lay on sage linen | yes |
| `7289a465-ad0b-4901-8a12-74451a5de6fc` | Macro side angle on the pebbles | yes (near the end) |
| `056ac205-480a-45c3-8486-c19d8ff8ad5b` | Minimal Christmas mantel | yes |
| `193dcbee-e0b6-40be-99c9-f3fe04a9def7` | Stone windowsill, sea at sunset | yes |

**Total spend:** 31 credits (balance before: 1,736).

**Verdicts.** Every image is `agent-pass` only. None is `max-approved`.

**Gallery order:** Max asked for set 2's #4 and #2 first, then #3. Set 2's #4 is the sofa-ledge shot I had first left off over scale; Max chose to use it.
1. Sofa ledge.
2. Hallway.
3. Plinth.
4. Terracotta.
5. Sea window.
6. Real close-up photo.
7. Christmas mantel.
8. Shelf.
9. Sage flat lay.
10. Hand.
11. Pebble macro.
12. The existing Christmas-wrapped picture.
13. The existing wrap-kit contents image.

## Names box, 2 Oct (Max)

Max asked to rename the personalisation to "names to appear underneath" and put it below the first line box.
- The separate "Name" box under each pebble is gone.
- In its place is one **"Names to appear underneath"** box, placed below the wording box (the picture's first line). It is optional, with placeholder "e.g. Daddy, Mummy, Ruby".
- The second picture gets the same box, prefilled from the first.
- The basket property is `Names to appear underneath`.
- Intro copy: "Choose your frame colour, pebble characters, wording and the names to appear underneath."
- Builder snippet md5 `335c2cf2…`.
- Max asked for no more testing, so this was not tested on the storefront. Only the saved checksum was verified.

## Surcharge from 6 pebbles, 2 Oct (Max)

Max asked for a surcharge on more than 5 pebbles.
- **Product:** the store's existing pebble surcharge, `3-7-8-pebbles-1` "(+£3) 7/8 Pebbles", at £3.00. Max did not give a price, so £3 is assumed.
- **When:** on this picture only, it is now added for 6, 7 or 8 pebbles (threshold 5).
- **Second picture:** the surcharge applies per frame, the second picture included.
- **Basket:** the surcharge line carries `Add-on: Extra pebble people (6-8)`.
- **Page total:** includes the surcharge, through the cart model's `calculateTotal`.
- **Selector:** the count options now show the surcharge, "6 (Inc dog/cat) (+£3.00)" and so on. This is a new `showPrice` flag in `daisy-pebble-picture.js`.
- **Other pebble pictures:** unchanged, because none of them sets the `showPrice` flag. They still add £3 at 7–8 without showing it on the selector.
- **Checks:** JS md5 `7b8f7f06…` (syntax checked with `node --check`), builder md5 `f6714d98…`. Not storefront-tested, per Max.

## Hero image plan, 2 Oct (team didn't like sets 1–3)

**Why sets 1–3 missed.** They broke the house hero format. Hero images of the 6 best sellers in Framed Pebble Art (sorted by best-selling):

| Best seller | Hero |
|---|---|
| Wedding flower arch | Hands hold the frame, wedding roses blurred behind |
| Mum flutterby | Christmas kraft flat lay |
| Family blossom tree | Hands, blurred garden |
| Engagement love tree | Hands, golden garden bokeh |
| Christening | Hands, white flowers / garden |
| Family flutterby | Hands, bright white room |

**The format:**
- Two hands, with no face, hold the white frame up front-on.
- The frame fills about 70% of the square, so the wording and names read on a phone. 95% of traffic is mobile.
- A soft, warm, blurred occasion background behind it.
- Sets 2–3 went to interiors, plinths and flat lays. The frame was small, the props led, and the result looked off-brand in the collection grid.

**Brief for the new hero (Nano Banana 2, 2k):**
- References:
  - The real photos (product).
  - The Family Blossom Tree hero (composition only; its artwork is not to be copied).
  - The Mum Christmas hero (layout for the Christmas flat lay).
- Options:
  1. Hands, blurred British beach at golden hour (dunes, sea, low sun), which ties to the print.
  2. Hands, blurred cottage garden, no pink roses.
  3. Hands, bright white room.
  4. Christmas kraft flat lay in the Mum-hero layout, for gallery image 2 in gifting season.

**Sign-off in one round:**
1. Show the team the best-seller sheet next to options 1–3.
2. Each person picks one, and the most votes becomes the hero.
3. Objections must be specific ("pebbles look fake", "too dark"), so the next round fixes the actual problem.

**Gallery after the vote:**
1. The winning hero.
2. The Christmas flat lay.
3. The real close-up photo.
4. One or two modern shots.
5. The wrap-kit images.
