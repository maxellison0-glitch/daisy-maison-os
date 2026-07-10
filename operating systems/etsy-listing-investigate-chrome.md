# Etsy Listing Investigator — Claude in Chrome prompt (Daisy Maison)

**Purpose:** read-only. Maps the full structure of one Etsy listing (starting with the wedding/Mr & Mrs street sign) so we can plan where to add an upsell variation. Changes nothing.

**Recommended model:** Claude Sonnet (fast, strong at structured DOM extraction). Use Opus for the strategy/edit-planning step afterwards.

**How to use:** open Etsy logged in, paste the prompt below into Claude in Chrome, let it run, copy the `=== ETSY LISTING MAP ===` block, paste it back into the Daisy Maison chat.

---

## PROMPT (copy everything below this line)

You are investigating ONE Etsy listing for my shop, Daisy Maison UK, to document its full current structure. **This is read-only. Do not edit, save, publish, deactivate, or change any field, setting, or price. Do not click "Save", "Publish", or "Update". Read and report only.** If any action would change the listing, skip it and note it. Currency is GBP (£); report prices exactly as shown.

**Step 1 — find the listing.** Go to https://www.etsy.com/your/shops/me/tools/listings (Shop Manager → Listings). Find the main **Mr & Mrs / wedding personalised street sign** listing (title contains "Mr & Mrs" and "Wedding" / "Street Sign"). If more than one matches, pick the one with the most sales/reviews and note that others exist. Open its **Edit** page. Also open the public-facing listing page in a second tab so you can cross-check what a buyer actually sees.

**Step 2 — document every element below.** Read the full editor, scrolling through all sections. Capture:

- **Title** — the complete title, exactly.
- **Photos & video** — number of photos, one-line description of what each shows, whether there's a video.
- **Category / listing type** — the taxonomy/category shown, and whether it's a physical/made-to-order listing.
- **Price** — base price, and whether a sale/discount is currently applied (show both the original and sale price if shown).
- **Quantity** and **SKU** if visible.
- **Personalisation** — is it enabled? Is it required? The exact instruction text shown to buyers, and the character limit.
- **Variations** — this is the priority. For EACH variation set: the set name (e.g. "Size", "Colour", "Frame"), every option within it, whether each option changes the price (and by how much / to what price), whether it links to quantities/SKUs, and whether it's visible to buyers. Note if there are zero variations.
- **Item options / attributes** — any "About this listing" attributes (made by, occasion, style, etc.).
- **Mounting strips / add-ons** — how (if at all) mounting strips or any other add-on is currently offered on THIS listing: is it a variation, a separate linked listing, a personalisation option, or not present? Describe the exact mechanism.
- **Tags** — list all tags (up to 13).
- **Materials** — list them.
- **Shipping** — the shipping/delivery profile name, the delivery price shown to buyers, and the processing/dispatch time.
- **Returns & exchanges** — what the policy shows.
- **Section** — which shop section it's filed under.

**Step 3 — output.** Print ONE fenced code block in exactly this structure, filling every field (use "not shown" or "none" where nothing applies). No commentary outside the block.

```
=== ETSY LISTING MAP — Daisy Maison ===
Investigated: <date>
Listing URL (public): <url>
Listing ID: <id if visible>
Other matching listings: <yes+names / none>

TITLE: <full title>

PHOTOS: <count> | video: <yes/no>
  <1-line note per photo>

CATEGORY / TYPE: <taxonomy> | <physical/made-to-order>
PRICE: base £<n> | sale price £<n or none> | discount <detail or none>
QUANTITY: <n> | SKU: <value or not shown>

PERSONALISATION: enabled <yes/no> | required <yes/no> | char limit <n>
  Instruction text: "<exact text>"

VARIATIONS:
  Set 1 — "<name>": visible <yes/no> | affects price <yes/no>
    - <option> | price <£n or +£n or none> | qty/SKU <detail>
    - ...
  Set 2 — "<name>": ...
  (or: "No variations")

ITEM OPTIONS / ATTRIBUTES:
  <attribute>: <value>
  ...

MOUNTING STRIPS / ADD-ONS: <mechanism — variation / separate listing / personalisation / not present + detail>

TAGS: <tag1, tag2, ... up to 13>
MATERIALS: <list>

SHIPPING: profile "<name>" | delivery price £<n> | processing time <detail>
RETURNS: <policy summary>
SECTION: <section name>

NOTES: <anything unclear, multiple matches, or a field that couldn't be read>
=== END ===
```
