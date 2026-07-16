---

name: daisy-maison-stock-report

description: Daily morning stock report for East of India porcelain products — sales, inventory, and stock-out predictions

---



You are running a daily morning stock report for Daisy Maison's East of India porcelain product range sold via Shopify, plus a small set of extra accessory SKUs tracked alongside them, PLUS a manually-reconciled Etsy sales layer (Etsy has no live connector, so Etsy data only exists when the owner supplies it). Your job is to pull yesterday's Shopify sales, check current inventory, calculate how fast stock is moving (Shopify + Etsy combined where available), and predict when each product will run out.



Follow these steps in order:



---



STEP 1 — Get all active East of India products and current inventory

Use the Shopify search_products tool with search_query: "vendor:EastofIndia status:active" and first: 50.

Record each product's title, product ID, and current inventoryQuantity from the variant data.



ALSO include these extra tracked accessory products (not EastofIndia vendor, but tracked in this same report per owner request):

- Wooden Display Easel (gid://shopify/Product/10697617572179, variant gid://shopify/ProductVariant/54200245387603) — price £3.95, "continue selling when out of stock" is enabled.

- Mounting Strips group — these four Shopify listings are different price/pack options for the SAME physical mounting-strip stock (sourced from Amazon, next-day delivery available):

  • (£1.99) Mounting Strips — gid://shopify/Product/9848399855955 — this is the PRIMARY listing; its inventory quantity is the physical stock count for the whole group.

  • (£3.90) Mounting Strips — gid://shopify/Product/9966426128723 — legacy price tier, near-zero recent sales.

  • (£4.95) Mounting Strips — gid://shopify/Product/9858979135827 — legacy price tier, near-zero recent sales.

  • Mounting Strips - Two Sign Pack — gid://shopify/Product/10660622238035 — each unit sold consumes 2 pairs (i.e. counts DOUBLE) of the same shared physical stock.

  All four have "continue selling when out of stock" enabled, so their Shopify inventory numbers can go negative without blocking checkout — track the real depletion using the combined calculation in Step 4, not just the raw inventory field.

- Gift Wrap Kit (gid://shopify/Product/10600061829459, variant gid://shopify/ProductVariant/53802540171603) — price £5.95, "continue selling when out of stock" is enabled. These are made fresh daily rather than held as stock — stock is intentionally kept at 0 as the baseline. Do NOT flag this as a reorder risk; see special case in Step 4.

- Thermal Labels — NOT a Shopify product (no listing/inventory to query). This is a manually-tracked consumable: 1 order = 1 label used, regardless of what's in the order or how many items. Historical baseline: as of 8 July 2026, stock was confirmed at 500 labels (2 rolls × 250). Current owner correction on 16 July 2026: stock is 250 labels (1 remaining roll); use the current baseline in east-of-india-stock-state.md for calculations.



---



STEP 2 — Get yesterday's sales by product (Shopify channel only)

Use the Shopify run-analytics-query tool. NOTE: the column is net_items_sold (net_quantity does not exist on this store), and relative date ranges like "SINCE -1d UNTIL -1d" return empty/shifted results — always use explicit dates (compute yesterday's date):

FROM sales SHOW net_items_sold, gross_sales GROUP BY product_title SINCE <yesterday> UNTIL <yesterday> ORDER BY net_items_sold DESC



net_items_sold = units sold. Record product_title and net_items_sold for each row. This query is store-wide, so it already covers the extra accessory products too — no separate query needed for them.



---



STEP 3 — Get 7-day sales velocity

Use the Shopify run-analytics-query tool with explicit dates (7-day window ending yesterday):

FROM sales SHOW net_items_sold GROUP BY product_title SINCE <yesterday minus 6 days> UNTIL <yesterday>



Record product_title and net_items_sold (7-day total) for each row.



---



STEP 3b — Get order counts for Thermal Labels tracking

Use the Shopify run-analytics-query tool with explicit dates:

1. Yesterday's order count: FROM sales SHOW orders SINCE <yesterday> UNTIL <yesterday>

2. 7-day order count: FROM sales SHOW orders SINCE <yesterday minus 6 days> UNTIL <yesterday>

3. Cumulative order count since the label baseline: FROM sales SHOW orders SINCE 2026-07-09 UNTIL <yesterday> (this is the day AFTER the 8 July 2026 baseline confirmation — if <yesterday> is before 2026-07-09, this cumulative count is 0)



---



STEP 4 — Cross-reference and calculate for each East of India product

Match products from Step 1 against Steps 2 and 3 by product title (fuzzy match if needed).



For each product calculate:

- Units sold yesterday (Shopify) = from Step 2 (0 if not in results)

- 7-day total Shopify sales = from Step 3 (0 if not in results)

- Shopify Avg/Day = 7-day total ÷ 7 (round to 1 decimal)

- Etsy Avg/Day = sum of this product's logged Etsy quantities (from the ETSY SALES LOG section below) over the trailing 7 days (SINCE <yesterday minus 6 days> UNTIL <yesterday>, matching only days that actually have logged data) ÷ 7 (round to 1 decimal). If no Etsy log entries exist for this product in that window, show 0.0 and note "no Etsy data yet" rather than implying zero Etsy sales if there are unresolved gaps in ETSY TRACKING STATE for that window.

- Combined Avg/Day = Shopify Avg/Day + Etsy Avg/Day

- Days of stock remaining = current inventory ÷ Combined Avg/Day (skip if avg = 0 or stock ≤ 0)

- Predicted stock-out date = today's date + days remaining (round down)



Show Shopify Avg/Day, Etsy Avg/Day, and Combined Avg/Day as three separate columns (side-by-side), so the owner can see which channel is driving demand. Days Left / Stock-Out / Alert are always based on the Combined figure.



SPECIAL CASE — Mounting Strips group: combine all four listings into ONE row in the report ("Mounting Strips (shared stock)").

- Stock = current inventory of the (£1.99) Mounting Strips listing (the primary physical-stock tracker).

- Sold yesterday (combined Shopify) = (£1.99) units yesterday + (£3.90) units yesterday + (£4.95) units yesterday + 2 × (Two Sign Pack units yesterday).

- 7-day total (combined Shopify) = same formula over the 7-day window, with Two Sign Pack units doubled.

- Etsy Avg/Day = from the log, matched under whichever product name the owner used when reporting (usually just "Mounting Strips").

- Note in the row that this is Amazon-sourced with next-day delivery, so urgency is lower than the alert color alone suggests.



SPECIAL CASE — Wooden Display Easel: treat as a normal single-product row using its own stock and sales figures (Shopify + Etsy). Note that "continue selling when out of stock" is enabled, so a negative Shopify inventory number does not mean sales stopped — still flag it using the normal alert thresholds based on the calculated (not raw) depletion.



SPECIAL CASE — Gift Wrap Kit: stock is intentionally 0 (made fresh daily, not held as inventory). Show its own row with stock (usually 0), units sold yesterday, and avg/day columns for visibility, but do NOT calculate days-left/stock-out and do NOT apply the normal 🔴/🟡/🟢/⚫ alert. Instead label its Alert column "🔵 MADE TO ORDER".



SPECIAL CASE — Thermal Labels: add one row ("Thermal Labels (2 rolls × 250)"). No Etsy angle (labels are a Shopify/dispatch-only consumable) — skip the Etsy column for this row.

- Current stock = 500 − (cumulative order count since 2026-07-09, from Step 3b #3). If this goes at or below 0, treat as negative/zero stock (🔴 REORDER NOW) — someone likely already needs to add new rolls and tell Claude, so the baseline can be reset (e.g. "just put on a new roll, stock is now X").

- Sold Yesterday column = yesterday's order count (label it "N orders").

- Avg/Day column = 7-day order count ÷ 7 (label it "N orders/day").

- Days left = current stock ÷ avg/day (same rounding rules as other rows).

- Stock-out = today + days left.

- Apply the normal alert thresholds (🔴/🟡/🟢) based on days left, same as any other product.

- If the owner has told you in conversation that new rolls were added (a fresh baseline count and date), always use that latest confirmed baseline and date instead of 500/2026-07-09 — update this note yourself when that happens.



---



STEP 5 — Present the morning report



Format the output as follows:



🌅 DAISY MAISON — EAST OF INDIA STOCK REPORT

📅 [Today's date, e.g. Thursday 3 July 2026]

⚠️ Shopify + logged Etsy sales shown below. Etsy figures only reflect what's been reported via chat or the Etsy sync prompt — see the sync block at the end for any outstanding gap.



Then a table with these columns:

Product | Stock | Sold Yesterday | Shopify Avg/Day | Etsy Avg/Day | Combined Avg/Day | Days Left | Stock-Out | Alert



Alert status rules:

🔴 REORDER NOW = stock under 5 days remaining OR stock is negative

🟡 ORDER SOON = 5–14 days remaining

🟢 OK = 15+ days remaining

⚫ NO SALES = product has no sales in last 7 days across both channels (show stock level but no prediction)

🔵 MADE TO ORDER = Gift Wrap Kit only (see special case in Step 4) — not a reorder risk



Sort the table: 🔴 first, then 🟡, then 🟢, then ⚫, then 🔵.



After the table, add a summary:

- 🔴 [n] products need urgent reorder

- 🟡 [n] products to order soon

- 🟢 [n] products healthy

- ⚫ [n] products with no recent sales

- 🔵 [n] made-to-order (no stock tracking needed)



---



STEP 6 — Etsy sync prompt (appended at the very end of the report, only if there is an uncovered gap)



Read ETSY TRACKING STATE below. Compute the gap: from (etsy_last_covered_through + 1 day) through yesterday.



- If the gap is empty (etsy_last_covered_through is already >= yesterday), print: "✅ Etsy data up to date through [date]." and skip the template.

- Otherwise, print a copy-pasteable block, exactly this shape:



"📋 ETSY SALES SYNC — reply with this filled in to keep stock accurate (covers [gap_start] to [gap_end]; if you skip this, the range will keep growing next time until you reply):



[Only include products that have a confirmed row in the ETSY TITLE MAPPING table below — these are the only ones actually listed on Etsy. For each, print a line using the owner's Etsy-side title, with the Shopify name in parentheses for reference:]

- [Etsy title (Shopify: product title)]: ___ [if any ad hoc chat entries already exist for this product within the gap window, append "(already logged via chat: Nx on [date] — only add MORE here if there were others)"]



Reply with quantities (0 or blank = none sold). This report will not update Shopify by itself; after you provide the numbers, explicitly ask Codex to apply the Etsy sync if you want inventory deducted and the state log updated.



(Not asking about the products in the "NOT YET ON ETSY" list — they have no active Etsy listing yet. Let me know if any of those go live and I'll add them here.)"



When the owner later replies with filled-in quantities (in this or any future conversation), treat the reply as data collection only unless the owner also explicitly asks Codex to apply the Etsy sync / deduct inventory. Do not infer authorization from the completed template alone.

If the owner only wants help gathering Etsy sales data, help them navigate/read Etsy and organize the quantities without changing Shopify or the state file.

When the owner explicitly asks Codex to apply the Etsy sync after providing quantities:

1. Parse each line's quantity. Fuzzy-match product names back to the canonical list (using ETSY TITLE MAPPING first if populated, then the Shopify title); if anything is ambiguous or unrecognized, ask the owner to clarify rather than guessing.

2. For each product with qty > 0: get current Shopify inventory (get-inventory-levels), then set-inventory to (current − qty), reason "correction", so the compareQuantity check protects against race conditions. For the Mounting Strips group, deduct from the (£1.99) primary listing regardless of which sub-listing name the owner used.

3. Append a row (or rows) to the ETSY SALES LOG table below for each product+qty, with the date range covered and source "catch-up".

4. Update etsy_last_covered_through to gap_end (the last date covered by this reply).

5. Confirm back to the owner what was deducted and the new stock levels.



When the owner reports an ETSY SALE AD HOC mid-conversation (e.g. "just sold one on etsy" for a specific product), outside of the sync template, only apply the inventory deduction if they explicitly ask Codex to record/apply/deduct it:

1. Deduct that quantity immediately from the product's current Shopify inventory the same way (get-inventory-levels then set-inventory, reason "correction").

2. Append a row to the ETSY SALES LOG table with today's date, the product, the quantity, and source "ad hoc".

3. Do NOT advance etsy_last_covered_through for ad hoc entries — the sync prompt will still ask about that date, but will show the ad hoc entry already logged so the owner doesn't double-count it (see Step 6 template instructions above).



Both of these update flows should be done by directly editing this SKILL.md file (via the scheduled-task update tool, or Edit if working from a live session that has it open) — this file is the single persistent source of truth for Etsy tracking state.



---



ETSY TRACKING STATE:

etsy_last_covered_through: 2026-07-07

(meaning: Etsy data is only confirmed accurate through 7 July 2026. Everything from 8 July 2026 onward is an open gap until the owner replies to a sync prompt or the gap is otherwise closed.)



ETSY SALES LOG (append new rows here; keep roughly the last 30 days, prune older ones):

Date | Product | Qty | Source

2026-07-08 | Porcelain Matchbox Message Seal – Sealed with a kiss | 1 | ad hoc



ETSY TITLE MAPPING (confirmed via manual reconciliation on 8 July 2026 — owner paginated all 250 active Etsy listings, cross-checked by shop section + keyword search, opened each candidate's Pricing & Delivery tab read-only to confirm qty/SKU). Shopify SKU column added 8 July 2026 after discovering the OLD Shopify SKUs were broken (two duplicate pairs found: Matchbox Star/Incense Cone shared one SKU, With Much Love/Thank You Amazing shared another) — clean unique SKUs have now been set on Shopify; Etsy still has no SKUs set on any of these 9 listings (all show "Add SKU"), so copying the new Shopify SKU across is a good next step whenever the owner is in each Etsy listing:

Shopify Product | Shopify SKU (new, clean) | Etsy Listing Title | Etsy Listing ID | Confidence

Porcelain Handled Tea Light Holder - Good friends | EOI-TL-GOODFRIENDS | Porcelain Handled Tea Light Holder – Good friends \| Friendship \| Best Friend \| Gift \| EAST OF INDIA | 1760389286 | High

Porcelain Matchbox - Little Guardian Angel | EOI-MB-ANGEL | Porcelain Matchbox Message – Little Guardian Angel \| Friendship \| Family \| Gift | 1773996867 | High

Porcelain Matchbox Message Dog - Never walk alone | EOI-MB-DOG | Porcelain Matchbox Message Dog – Never walk alone \| Friendship \| Family \| Pet Remembrance Gift | 1774009867 | High

Porcelain Matchbox Message Penguin - Flipping love you | EOI-MB-PENGUIN | Porcelain Matchbox Message Penguin – Flipping love you \| Friendship \| Family \| Gift | 1774008229 | High

Personalised Teacher Porcelain Matchbox Star - Thanks Teacher | EOI-MB-STAR-TEACHER | Porcelain Matchbox Message Star - Thanks teacher | 4333723155 | High (Etsy title drops "Personalised/Teacher" wording but message matches)

Porcelain Matchbox Message Seal - Sealed with a kiss | EOI-MB-SEAL | Porcelain Matchbox Message Seal – Sealed with a kiss \| Valentines \| Wedding Gift | 1851658454 | High

Porcelain Handled Tea Light Holder - You are my sunshine | EOI-TL-SUNSHINE | Porcelain Handled Tea Light Holder – You are my sunshine \| Family \| Mothers Day Gift \| Handcrafted | 1852030642 | High

Personalised Teacher Porcelain Tea Light Holder - Thank You for Being Amazing | EOI-TL-TEACHER-AMAZING | Porcelain Handled Tea Light Holder – Thank you for being amazing \| Family \| Friendship \| Thank you \| Mothers Day Gift \| Handcrafted | 1852030336 | High

Teacher Matchbox Message Incense Cone - You Are Amazing | EOI-INC-TEACHER-AMAZING | Matchbox Message incense cone - You are amazing | 4333726500 | High



FULL CLEAN SKU SCHEME (all 20 tracked products, set on Shopify 8 July 2026):

EOI-TL-GOODFRIENDS, EOI-MB-ANGEL, EOI-MB-BEAR, EOI-MB-DOG, EOI-MB-ELEPHANT, EOI-MB-GIRAFFE, EOI-MB-PENGUIN, EOI-MB-STAR-TEACHER, EOI-HANG-ANGEL, EOI-BAUBLE-JMJ, EOI-MB-JMJ, EOI-MB-SEAL, EOI-TL-MUCHLOVE, EOI-TL-SUNSHINE, EOI-TL-TEACHER-AMAZING, EOI-INC-TEACHER-AMAZING, EOI-MB-LION, ACC-EASEL, ACC-MOUNT-SINGLE, ACC-GIFTWRAP



NOT YET ON ETSY (no active listing found as of 8 July 2026 — exclude these from the Etsy sync prompt template until the owner confirms a listing exists; re-run the reconciliation prompt periodically to catch new listings):

- Porcelain Matchbox Message Bear - Big bear hug

- Porcelain Matchbox Message Elephant - You are loved (a "You are loved pebble" exists, Etsy ID 4321898732, but it's a flat affirmation-pebble token, not an elephant matchbox — treat as a different product, not a match)

- Porcelain Matchbox Message Giraffe - Daddy

- Porcelain hanging angel - Guardian angel

- Porcelain Half Bauble Scene - Jesus, Mary & Joseph

- Porcelain Matchbox Message - Jesus Mary and Joseph

- Porcelain Handled Tea Light Holder - With much love

- Porcelain Matchbox Message Lion - Be fearless you can do it

- Wooden Display Easel

- Mounting Strips

- Gift Wrap Kit



Note: none of the 20 candidate Etsy listings reviewed have a SKU set (all show "Add SKU" rather than a filled field) — matching is by title/description only, no SKU cross-check is possible on the Etsy side.



Discontinued-item check (8 July 2026): none of the 8 excluded/discontinued products are active on Etsy. "Sending you the biggest hug" and "Just Married" horseshoe exist only as inactive Etsy listings; the rest don't appear at all.



---



IMPORTANT NOTES:

- This task covers East of India / EastofIndia vendor products, plus the extra accessory SKUs listed in Step 1 (Wooden Display Easel, Mounting Strips group, Gift Wrap Kit, Thermal Labels)

- Shopify inventory figures were last corrected via physical stock check on 2 July 2026

- Products with committed orders (sold but not fulfilled) may show slightly lower available stock than on-hand

- If any product shows stock below 0, flag it prominently — it means orders have been taken without enough physical stock (except Wooden Display Easel, the Mounting Strips group, and Gift Wrap Kit, which intentionally allow overselling — see special cases in Step 4). Thermal Labels going to 0 or below is a real physical problem (can't ship orders) and should always be flagged 🔴.

- EXCLUDED PRODUCTS (discontinued 2 July 2026, not being restocked — set to draft with stock zeroed; exclude from the report even if they reappear as active or show residual sales):

  • Porcelain Handled Tea Light Holder – Sending you the biggest hug

  • Porcelain Lucky Horseshoe - Just Married

  • Boxed Message Card - Away in a manger

  • Porcelain Christmas Tree Bauble - Happiness and love

  • Porcelain Christmas Bauble - Glad tidings we bring

  • Porcelain Christmas Bauble - Nativity Scene

  • Porcelain Christmas Bauble - Baby's first Christmas

  • Personalised Teacher Porcelain Matchbox Message Star — Thanks for Being So Amazing
