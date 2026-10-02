# Pet sign landing page: audit and rebuild (2 Oct 2026)

**Page:** `/products/kitchen-personalised-street-sign?view=pets-edition`. This is the "Pet sign [shelley]" Meta ad's landing page. It renders the product `personalised-pet-street-sign-no-need-to-knock` (Small £16.95, was £24.95; Medium £24.94; Large £27.94) through Codex's own section, `sections/dm-pet-sign.liquid`. That section has its own script and styles, and its wording is under `pet_sign.*` in `locales/en.default.json`.

**Status:** built and tested on the unpublished copy **"Claude – pet landing page (2 Oct)"** (theme `208250732883`). It is a duplicate of the live theme "Soul Soap — gift notes & pet collection — 1 Oct" (`208196239699`), taken at 07:4x on 2 Oct. **Not published. Max publishes.**

Publishing replaces the whole live theme with this copy. Any edits made to the live theme after the copy was taken would be lost, including Codex's. Publish before more live edits, or re-apply them.

Preview: https://daisymaison.co.uk/products/kitchen-personalised-street-sign?view=pets-edition&preview_theme_id=208250732883

## Data (pulled 2 Oct)

- **Meta, "Pet sign [shelley]"** (started 1 Oct):
  - 1 Oct: £9.35 spend, 1,935 impressions, 14 link clicks, 2 landing page views.
  - 2 Oct (to 07:40): £2.23 spend, 6 link clicks, 1 landing page view.
  - No add-to-carts or purchases yet. Far too early to judge on ROAS; the house rule is 7 days and 100 clicks.
- **Shopify:** 8 sessions from social landed on this path on 1 Oct, with 0 add-to-carts. Meta counted only 2 landing page views for the same day. Most visitors left before the Meta pixel registered. The likely causes are the slow first load (all 23 images were loaded eagerly) and the cookie banner.
- **Reviews:**
  - Feefo's public API reports the `daisy-maison` account as **"Closed"**. That matters, because the site's trust badges still say "5/5 Feefo Rated · Gold Trusted Service 2026 · 3,326+ Verified Reviews". Max to check.
  - Trustpilot: 1,692 reviews, 1,439 of them five-star, TrustScore 4.1. A search for pet words found 20 reviews. **None is about a dog sign.** Most are dogs on pebble pictures, several of them complaints.

## Audit: what the page was missing compared with Mr & Mrs

| Mr & Mrs has | Pet page had |
|---|---|
| A live sign preview from the first second, with a worked example | A preview that was hidden until the customer typed |
| Personalisation in the advert's own words | Two blank boxes ("Type your main wording"), even though the ad sells one exact sign |
| Trust badges and a five-star review card | No reviews, ratings or social proof anywhere |
| Was/now price with a SAVE badge | £16.95 only, although Small has a £24.95 compare-at |
| Sticky Add to Cart bar with a live total | None. The button sat at about 1,630px down a phone |
| Dispatch time stated | "Delivery calculated at checkout" |
| Second-sign offer ("INCREDIBLE OFFER", £9.95) | None. **Needs Max's pricing decision** |
| Many lifestyle photos | 4 photos: one dog, one generic sign, a colour swatch and a sizes shot |
| FAQ, delivery, how it's made | 4 FAQs, then the footer |

## Built on the copy

1. **Headline matches the advert.**
   - Eyebrow: "Personalised pet sign".
   - Headline: "No Need to Knock Pet Sign".
   - Intro: "Add your dog's name and see your sign straight away…"
   - Rating line: "★★★★★ 1,400+ five-star reviews on Trustpilot". This is true: 1,439 of 1,692 reviews are five-star.
2. **One "Your dog's name" box.** The sign is written for the customer:
   - Line 1 is "No Need to Knock".
   - Line 2 is "{name} already knows you're here". "Buddy & Bella", "Rolo and Pip" or "Max, Ted" switch it to "know".
   - "Write your own wording instead" reveals the original two free-text lines, and the customer can switch back.
   - The basket gets the same `Line 1` / `Line 2` / `Colour border` / `Size` properties as before, so fulfilment sees no change.
3. **Preview always visible.** It shows the advert's sign ("NO NEED TO KNOCK / BUDDY ALREADY KNOWS YOU'RE HERE", dashed frame) as an example until the customer types.
4. **Was/now price.** £24.95 struck through, £16.95, SAVE £8.00. The badge shows only on sizes that have a compare-at price.
5. **Sticky add-to-basket bar** on phones once the main button scrolls away, with a live total. Tapping it with no name says "Add your dog's name." and jumps to the box.
6. **Dispatch line:** "Personalised and dispatched within 5–7 working days, with express options at checkout. Free UK delivery over £50." This is the store's own delivery policy.
7. **Store-wide proof line** under the button: "Loved by over 8,300 customers across the UK". This is the existing `dm-proof` aggregate line.
8. **Below the button:**
   - How it works (3 steps).
   - "What our customers say": three verbatim 5-star reviews, each labelled with its product.
     - Trustpilot · personalised sign: "I was really happy with my personalised Mancave sign… looks good on his shed… Quick delivery and good quality, and bigger than i thought."
     - Trustpilot · pebble picture: "First class service. I forgot to add a wee dog on to picture…"
     - Verified review · street sign: "I ordered a street sign for my kitchen…"
   - Codex's unused "Their house. Their sign." story, plus a gift line: new puppy, birthday, Christmas, dog walker.
   - Three new FAQs: can it go outside, can I add two dogs, how long will it take.
9. **Speed.** Only the first photo loads up front; the other gallery images and thumbnails now load lazily. The thumbnail strip is hidden on phones, as on Mr & Mrs.
10. **Bold button.** The main button is weight 800, matching the rest of the site since 29 Sep.

### Bug found and fixed in testing

Shopify's `t` filter HTML-escapes translations. On the first test, "you're" reached the basket as **"Rolo already knows you&#39;re here"**, which would have been printed on the sign.
- **Fix:** the two templates with apostrophes now use `_html` translation keys (`design_line_two_html`, `design_line_two_many_html`), which Shopify does not escape.
- **Backstop:** the script also decodes entities in its own sign templates. It never touches the customer's typing.

The re-test confirmed the basket gets "Rolo already knows you're here".

### Files changed (on the copy only)

The full change is in `pet-landing-0210.diff`.

| File | md5 after |
|---|---|
| `sections/dm-pet-sign.liquid` | `42dcffcc…` |
| `assets/dm-pet-sign.js` | `5e52dc95…` |
| `assets/dm-pet-sign.css` | `1acf534a…` |
| `locales/en.default.json` (only `pet_sign.*` changed) | `05d58a58…` |

## Tested on the copy (390px phone, gated loads)

- **On load:**
  - Headline, rating line, £24.95 / £16.95 / SAVE £8.00.
  - Sample preview "NO NEED TO KNOCK | BUDDY ALREADY KNOWS YOU'RE HERE".
  - Name box shown and own-wording lines hidden.
  - Sticky bar hidden at the top.
- **Scrolled down:** sticky bar shows "£16.95 Add my sign". Tapped with no name, it gives "Add your dog's name." and focuses the name box.
- **Typing "Rolo":** preview reads "NO NEED TO KNOCK | ROLO ALREADY KNOWS YOU'RE HERE". "Rolo & Pip" reads "already know you're here".
- **Medium:** £24.94, sale badge hidden.
- **Own wording:** the lines are prefilled from the design, and editing them updates the preview. Switching back returns to the name design.
- **Basket:** 1× Personalised Pet Street Sign — Small, £16.95, with `Line 1: No Need to Knock`, `Line 2: Rolo already knows you're here`, `Colour border: black`, `Size: Small`.
- No script errors.

## For Max to decide or supply

1. **Second-sign offer.** Mr & Mrs offers a second sign for £9.95. A "second sign for a friend's dog" offer would suit this niche, but it needs your price.
2. **Photos.** The gallery has one dog photo. Shot list for ChatGPT, all of the same black-bordered "No Need to Knock" sign:
   1. A cockapoo at a front door.
   2. A spaniel on a doormat looking up at the sign.
   3. A two-dog version, "Bella & Rolo already know you're here".
   4. A hand holding the Small sign, for scale.
   5. The sign gift-wrapped with a dog sniffing the present.
   6. The sign on a garden gate in the rain, for "indoor & outdoor".
3. **Feefo badges.** The Feefo account reads as closed, so the site-wide "Feefo Rated / Gold Trusted Service 2026" badges may no longer be backed up. Check before an ASA complaint does.
4. **Christmas order-by date.** It's worth adding to this page once the real cut-off dates are set.
5. **Pet-sign reviews.** There are none yet. Ask the first buyers for a photo of their dog with the sign; that is the strongest proof this page could have.

## Revised 2 Oct, 08:15: back to Line 1 / Line 2

Max rejected the dog's-name box. Our street-sign pages take Line 1 / Line 2 directly, so this page does too.
- The name box and the "write your own" toggle are removed.
- "Main Sign Text" / "Smaller Sign Text (Optional)" are the inputs again, with placeholders "e.g. No Need to Knock" / "e.g. Buddy already knows you're here".
- The preview still shows the advert's sign as the example until the customer types.

Re-tested on the copy: the preview updated to "ROLO ALREADY KNOWS YOU'RE HERE", and the basket got `Line 1: No Need to Knock`, `Line 2: Rolo already knows you're here`, Small, £16.95. Section md5 `05e2c06f…`, language file `ad399684…`.

## Published 2 Oct 2026, ~08:18

Max published "Claude – pet landing page (2 Oct)" (208250732883). The four pet files on live match the tested versions. Live check on the ad link: sample preview shown, typing updated the sign, and the basket got Line 1 "No Need to Knock" / Line 2 "Rolo already knows you're here", Small £16.95.

## Price change, 2 Oct 2026

At Max's request, the pet sign Small went from £16.95 to **£14.95**. The compare-at stays at £24.95, so the page now shows SAVE £10.00. Medium (£24.94) and Large (£27.94) are unchanged.

## Preview wording colour, 2 Oct 2026

The pet preview wording was hard-coded black. On every other street-sign preview the wording takes the border colour (`--dm-preview-colour`). It now does here too: in `dm-pet-sign.js`, `render()` sets both text lines' fill to the chosen colour (md5 `7c639577…`). Built on a fresh copy of live, **"Claude – pet preview colours (2 Oct)"** (208260268371), for Max to publish.

## No outlines on coloured signs, 2 Oct 2026

The theme's base CSS was outlining the preview's border and both lines in its dark text colour (#232323). On coloured signs that drew a black outline, and it swamped the small Line 2 so it looked black. `render()` now forces `stroke: none !important` on the plate, panel and both lines. Checked on all five colours, using computed styles and pixels: Sage/Grass/Blue/Grey come out pure colour with 0 dark pixels in Line 2, and Black stays black. dm-pet-sign.js md5 `da191154…`, on "Claude – pet preview colours (2 Oct)" (208260268371).
