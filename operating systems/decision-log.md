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
2. Hero carousel of three proven sellers (Christmas star, Mr & Mrs sign, Family Blossom Tree), one button each
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
  - "10,000+ five-star reviews": no source found, and Feefo is closed.
  - The welcome 10% covers 54 collections, not the whole order. Nothing confirms that a welcome email flow sends the code to people who sign up with the homepage form.
  - Dispatch times disagree: the proof strip and FAQ say 5–7 working days; the FAQ says up to 7–14 at Christmas; the free-delivery rate says 3–5.
- Publishing the copy would undo any live-theme edits made after 10:43 on 23 Sep.

**Rollback:** Re-publish the previous live theme, which stays in the theme library. Or restore `index.before.json` and `header-group.before.json` from `projects/homepage-rebuild/`. The Best sellers collection can be unpublished or deleted separately.

**Max's review, 23 Sep:** He liked the reviews, Shop by occasion, Best sellers and the Christmas button. Changed on the copy the same day:
- "Lytham St Annes" is now "Lancashire" everywhere.
- The hero is a three-slide carousel, not one still photo, with its own photo per slide on desktop too.
- The low-resolution workshop video is removed. The "Personalised by you" words stay as a plain panel.
- The announcement bar is one soft line, "Free UK delivery over £50". The "[date]" line is gone until the Christmas cut-off is set.

He asked for the Christmas heart. The Christmas slide uses the Family Festive star instead: it sold 128 units in Oct–Dec 2025, against 16 for the "Our 1st Christmas Together" heart. That is one image to swap back if he prefers the heart.

**Result:** Pending. The build is on the preview, waiting for Max to publish. Measure 28 days after publish.
