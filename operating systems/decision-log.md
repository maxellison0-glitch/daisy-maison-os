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
