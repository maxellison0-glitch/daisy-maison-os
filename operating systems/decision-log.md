# Daisy Maison — Decision Log

*Important decisions and why they were made.*
*Log here when a decision is significant enough that future-you might wonder why it was made.*

---

## Format

Each entry:
- **Date** — when decided
- **Decision** — what was decided
- **Reason** — why
- **Expected outcome** — what success looks like
- **Risk** — what could go wrong
- **Rollback** — how to undo it if needed
- **Result** — fill in when known

---

## Log

---

### 2026-06-06 — Raise Mounting Strips price £1.95 → £2.25

**Decision:** Increase Mounting Strips variant price by 15% (£1.95 → £2.25). Also update product title to reflect new price.

**Reason:** Strips are near-100% margin. Attach rate on wall-mounted signs is 30–44%. Someone spending £30 on a sign is unlikely to balk at 30p more. Demand expected to be near-inelastic. Upside is pure profit; downside is small and fully reversible.

**Expected outcome:** Revenue per day from Mounting Strips equal or higher than pre-change baseline (units × £2.25 ≥ units × £1.95 at prior attach rate).

**Risk:** Attach rate drops >15%, cancelling the price increase benefit. Unlikely but possible.

**Rollback:** Two field changes in Shopify Admin (variant price + product title). Under 2 minutes.

**Result:** Pending — monitoring over 2–3 weeks. See `mounting-strips-price-test.md`.

---

### 2026-06-06 — Consolidate Daisy Maison OS into AA Daisy Maison OS\operating systems\

**Decision:** Move `context.md`, `Add-On_Products_Plan.md`, `mounting-strips-price-test.md` from `C:\Users\maxel\context.md\` to `C:\Users\maxel\AA Daisy Maison OS\operating systems\`. Update morning digest SKILL.md to point to new paths.

**Reason:** Knowledge was scattered across multiple locations with no single source of truth. The `context.md` folder was a working directory, not a permanent OS. The `AA Daisy Maison OS` folder was created as the intended permanent home.

**Expected outcome:** All Daisy Maison knowledge in one organised location. Digest reads and writes from the correct path.

**Risk:** If any other automations reference old paths, they break silently. Mitigated by auditing all scheduled tasks before moving.

**Rollback:** Files still exist at original locations (copies, not moves). Re-point SKILL.md paths.

**Result:** Complete. Digest paths updated. Files verified at new location.

---

### 2026-09-23 — Rebuild the mobile homepage as a shop floor (on a theme copy)

**Decision:** Rebuild the mobile homepage from sections Ella already has. The new order is:
1. Promise bar
2. Hero carousel of the two biggest sellers (Mr & Mrs sign first, then the family sign), with "Shop Christmas gifts" as the small link
3. Shop by occasion (3 across)
4. Real best sellers from a new automated "Best sellers" collection
5. Proof strip with numbers
6. The Christmas edit
7. How it works (with a screenshot of the live sign preview)
8. Real reviews
9. Shop by recipient
10. Made in Lancashire
11. Instagram, then an inline 10% sign-up

Sale badges and the tealight holder come off the homepage. Built on the unpublished copy "In construction 🚧" (207623029075). Max publishes. Details: `projects/homepage-rebuild/README.md`.

**Reason:** 7% of sessions land on the homepage. Direct homepage landers convert at 0.99% (1,413 sessions, 14 checkouts, last 30 days) against 9.97% for search (per the brief, 7% of all sessions land on the homepage). The old page gave them nowhere obvious to go: a generic hero with a wedding button, a hand-picked row led by a £10.99 tealight holder, a text-only promise slider and one tile per screen.

**Expected outcome:** Direct homepage-landing conversion rises from 0.99% towards the search figure. Anything above 2.5% over the 28 days after publishing pays for the work. Measure with the ShopifyQL query in the README, split by `referrer_source`.

**Risk:**
- The hero goes stale after Christmas. It needs an owner and a calendar date (see "Swapping the seasonal hero").
- Best sellers is all-time, so the Valentine's sign ranks #2 in the Christmas run-up.
- Claims to confirm before publishing. The owner declared the first two established; the site data doesn't back them yet:
  - "10,000+ five-star reviews": no source found, and Feefo is closed. Max changed it to "Thousands of 5-star reviews" on 23 Sep.
  - The welcome 10% covers 54 collections, not the whole order. Nothing confirms that a welcome email flow sends the code to people who sign up with the homepage form.
  - Dispatch times disagree: the proof strip and FAQ say 5–7 working days; the FAQ says up to 7–14 at Christmas; the free-delivery rate says 3–5.
- Publishing the copy would undo any live-theme edits made after 10:43 on 23 Sep.

**Rollback:** Re-publish the previous live theme, which stays in the theme library. Or restore `index.before.json` and `header-group.before.json` from `projects/homepage-rebuild/`. The Best sellers collection can be unpublished or deleted separately.

**Max's review, 23 Sep:** He liked the reviews, Shop by occasion, Best sellers and the Christmas button. Changed on the copy the same day:
- "Lytham St Annes" is now "Lancashire" everywhere.
- The hero is a three-slide carousel, not one still photo, with its own photo per slide on desktop too.
- The low-resolution workshop video is removed. The "Personalised by you" words stay as a plain panel.
- The announcement bar is one soft line, "Free UK delivery over £50". The "[date]" line is gone until the Christmas cut-off is set.

He asked for the Christmas heart. The Christmas slide first used the Family Festive star instead: it sold 128 units in Oct–Dec 2025, against 16 for the "Our 1st Christmas Together" heart.

Second pass, same day: he asked for the wedding street sign first and called the star and blossom-tree photos "chopped". Framed and hand-held products lose their edges in the 5:4 phone crop. The hero is now two street-sign slides: the Mr & Mrs sign, then the family sign. In Oct–Dec 2025 those were the #1 and #2 products, with 690 and 652 sold, about five times the star. "Shop Christmas gifts" is the small link on both slides.

**Result:** Published by Max on 24 Sep 2026: the copy "In construction 🚧" is now the live theme. Measure 28 days after publishing, around 22 Oct, with the README query.

---

### 2026-09-24 — Move Merry & Bright and Family Festive star onto the native builder; Mr & Mrs one-line signs

**Decision:**
- The last two Christmas decorations still on Globo (Merry & Bright, Family Festive star) move onto the native heart builder that the other Christmas decorations use. They get the Christmas gift wrap kit through `dm-wrap-kits`.
- On the Mr & Mrs page, a customer who fills in line 1 and leaves line 2 empty now sees a one-line sign, not the sample date.

Built and tested on a throwaway copy, then applied to Max's working draft "Copy of In construction 🚧" (207727198547), which goes live when he publishes it. Details: `projects/theme-changes-2026-09/README.md`.

**Reason:** Max asked for both. The Globo pages were the odd ones out in the Christmas range. The Mr & Mrs preview showed a line 2 the customer hadn't asked for, next to a caption saying "Your sign".

**Risk:**
- Property keys must match what fulfilment reads. They are copied verbatim from each product's own Globo form, and the star's from its real orders. The star keeps its own quirks: `Size` not `Size 1`, `(Large heart)` without a price, and Teen/Baby pebbles.
- Merry & Bright's year question moves from `Add 2025?` to `Add 2026?`, matching Wonderland.
- No gift boxes on the star until its size is confirmed (its description says 12 × 12 / 20 × 20 cm).
- Anything changed on the live theme after the draft was made (16:46, 24 Sep) must be copied into the draft before publishing.

**Rollback:** Republish the previous theme, or revert the three files using the diff in the project folder.

**Result:** Pending publish.
