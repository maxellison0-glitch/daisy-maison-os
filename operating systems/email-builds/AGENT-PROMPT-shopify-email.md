# Shopify Email build: agent prompt (reusable)

**Agent: Claude in Chrome** (chosen 16 Oct 2026). It works inside Max's own
logged-in Chrome, so there's no login hand-off or Shopify 2FA prompt, and Max can
watch and stop it. ChatGPT/Codex also built one well on ~9 Oct. Claude in Chrome
is preferred because the Shopify Email editor is a fiddly drag-and-drop canvas,
and a session that is already logged in and visible is the safer place for it.

**How to use (updated 20 Oct 2026):** paste the fenced block below into Claude
in Chrome with Shopify admin open, and replace BUILD SHEET FILE at the bottom
with the file name Claude gives you (e.g. `2026-10-22-christmas-pebble-pictures.md`).
The agent reads the spec straight from GitHub in Max's logged-in browser, so
nothing needs copying by hand. Claude (in the repo) writes one build sheet per
send in `operating systems/email-builds/`.

**Template reuse:** the agent builds by DUPLICATING a previous campaign, so the
header, fonts, colours and footer carry over. When one comes out right, note its
name under "Proven templates" at the bottom. The next spec duplicates that one.

```text
You are building ONE marketing email in Shopify Email for Daisy Maison
(daisymaisonuk.myshopify.com, a UK personalised-gift shop). Work in this Chrome
tab, which is already logged in to Shopify admin. Follow the steps exactly. Do
not improvise copy, prices, products, dates or reviews. If anything in the spec
doesn't match what you see in Shopify (a price, a product, a page), STOP and
tell me instead of guessing.

HARD RULES
- Never click Send or Schedule until I type "go" in this chat after your report.
  When I do, schedule it for the send time in the spec (UK time), not now.
- Never change products, prices, themes or settings outside the steps below.
- Never write a customer review or a number that isn't in the spec.
- Brand: white email background. Headings Georgia, colour #2F3B2E. Body
  Helvetica/Arial, #232323. Buttons solid #2F3B2E with white UPPERCASE text.
  Offer/highlight block background #F3F2EE. The colour #8E3B33 is used ONCE,
  only on the offer words. At most one emoji, and only in the subject line.

STEP 0: read the spec
  Open https://github.com/maxellison0-glitch/daisy-maison-os/blob/main/operating%20systems/email-builds/
  followed by the BUILD SHEET FILE named at the bottom of this prompt. The spec
  is the fenced block in that file (Template, Segment(s), Send, Subject,
  Preview text, Blocks). Lines in [SQUARE BRACKETS] are checks for you to do
  or gaps to ask me about, never text to paste into the email.
  If the file says DUPLICATE FROM, use that; otherwise duplicate the newest
  campaign listed under "Proven templates" at the bottom of
  operating systems/email-builds/AGENT-PROMPT-shopify-email.md.

STEP 1 (only if the spec has a DISCOUNT section): create the discount
  Shopify admin → Discounts → Create discount → choose the type in the spec.
  Enter every setting exactly as listed. Save. Then reopen it and confirm the
  code, the minimum, the dates and that it says Active / Scheduled.

STEP 2: start the email from the proven template
  Shopify admin → Marketing → Campaigns. Find the campaign named in
  "DUPLICATE FROM". Open its ⋯ menu → Duplicate. Rename the copy to the
  "CAMPAIGN NAME" in the spec. If Duplicate isn't available, create a new
  Shopify Email and tell me, then continue with the blank template.

STEP 3: content
  Set Subject and Preview text exactly as in the spec.
  Rebuild the body block by block in the order listed in BLOCKS. Delete any
  leftover blocks from the duplicated email that aren't in the list. Keep the
  header image and footer from the duplicate unless the spec says otherwise.
  For product blocks, use the product picker and choose the exact products
  named. Check that the price shown matches the spec.
  For every button and link, paste the exact URL from the spec.

STEP 4: recipients
  Set "To" to the segments listed under SEGMENTS (exact names). Read back the
  recipient count Shopify shows and include it in your report.

STEP 5: check and test
  Use desktop and mobile preview. Check: no leftover text from the old email;
  every link points where the spec says; the prices match; the discount code
  is spelled exactly as in the spec; images load.
  Send a test email to the address in TEST TO.
  Save the draft.

STEP 6: report back in this format
  - Draft name:
  - Subject / Preview:
  - Recipients count shown:
  - Discount created? code / min / dates / status:
  - Blocks in order (one line each):
  - Anything that didn't match the spec or that you couldn't do:
  - Test email sent to:
Then stop and wait for me.

STEP 7 (after I type "go" and you've scheduled it): log it
  On GitHub open operating systems/email-sends.md → pencil (Edit). Find the
  row for this send (or add one at the bottom of the table, same columns):
  Send date "YYYY-MM-DD HH:MM", Campaign = subject line, Recipients =
  "<count Shopify showed> (Shopify, at scheduling)" plus the segment names.
  Leave Cost as it is. Commit directly to main with the message
  "Log email send <date>". Tell me when done.

BUILD SHEET FILE: <paste file name here>
```

## Proven templates

| Campaign (in Shopify) | Template | Built by | Verdict (Max) |
|---|---|---|---|
| 🎄 A little piece of your family on the tree 🎄 (13 Oct) | A, festive header | Codex | use as the base until one built by this prompt is approved |
