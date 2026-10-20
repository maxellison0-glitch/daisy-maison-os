# Daisy Maison Weekly Review + Email Sheets (Mondays 08:25 UK)

Set up 20 Oct 2026 by Max. Source of truth for the "Daisy Weekly Review"
scheduled task. Runs after the Monday morning digest. The review feeds the
email plan in the same run, and both land in GitHub.

```text
You are running the Daisy Maison weekly review, unattended, on Monday
morning Europe/London. Work in the daisy-maison-os checkout (clone
maxellison0-glitch/daisy-maison-os if it isn't there). Keep it efficient:
read only the files named here.

Read: digests/ (last 7 files), checks/ (last 7 files), operating
systems/approvals.md, operating systems/email-sends.md, operating
systems/email-playbook.md (calendar + results log), the newest 2 files in
operating systems/email-builds/, .claude/skills/daisy-email/SKILL.md.

PART A — WEEKLY REVIEW (last Mon–Sun)
1. Shopify: FROM sales SHOW gross_sales, total_sales, orders SINCE -7d UNTIL
   yesterday, and SINCE -14d UNTIL -7d (check both are 7 days).
   FROM sales SHOW orders, total_sales GROUP BY order_utm_campaign WHERE
   order_utm_medium = 'email' SINCE -7d UNTIL yesterday.
   FROM sales SHOW gross_sales, orders GROUP BY product_title SINCE -7d
   UNTIL yesterday ORDER BY orders DESC LIMIT 10.
2. Windsor: weekly spend, clicks, conversions per campaign (google_ads
   880-835-8049, facebook 1574764016252349 incl. purchases + value).
3. Write reviews/review_YYYY-MM-DD.md (Monday's date), max 40 lines:
   - Week vs last week: sales, orders, AOV, ad spend, ROAS (green 2.7x, goal 3x).
   - Campaigns: one line each, earned its money or not (cost per purchase vs
     the 7-day average; Google by its own conversions value, marked as such).
   - Emails: one line per send (email-tagged sales, sales per 1,000 sent,
     send-day lift vs same weekday a week earlier). Add one row per send to
     the Results log in email-playbook.md.
   - Changes made last week (from approvals.md Decided) and whether each
     was right, by the test stated when it was made.
   - Reels: posted, candidates, built as ads (from checks/).
   - THE ONE RECOMMENDATION for this week, with the number behind it.

PART B — THIS WEEK'S EMAIL BUILD SHEETS
4. Using the review, the Christmas calendar in email-playbook.md and the
   send cap (up to 3 campaign sends a week through Christmas: two to Engaged
   + Customers, the third to a narrower group), write one build sheet per
   send in operating systems/email-builds/YYYY-MM-DD-<slug>.md, in the exact
   build-sheet format of the daisy-email skill (fenced block: Template,
   Segment(s) with size, Send, Subject, Preview text, Blocks).
   - Check every price and product URL live in Shopify (search_products)
     the same morning. Never invent reviews, numbers or deadlines; use
     [CONFIRM ...] for anything Max must supply.
   - If last week's review shows a template/subject/segment clearly won,
     reuse it; change ONE thing per week (playbook rule).
   - Add a planned row per send to operating systems/email-sends.md.
   - New offers or discounts are NOT allowed without Max's yes: write the
     sheet without the offer and add the offer as a proposal in approvals.md.

5. Commit everything: "Weekly review + email sheets YYYY-MM-DD"; push. THE
   COMMIT MUST END UP ON MAIN: if you're on a claude/... branch, open a PR
   and merge it into main yourself.

6. FINAL REPLY (Max's notification), max 6 lines:
   - "Week: £<sales> (<±%> vs last week), ROAS <x.xx>x <GREEN/RED>"
   - "Best: <campaign/product>. Worst: <campaign>."
   - "This week: <the one recommendation>"
   - "Emails ready: <Day> <subject> → paste prompt with <file>" (one line each)
   Max builds each email by pasting the prompt in
   operating systems/email-builds/AGENT-PROMPT-shopify-email.md into Claude
   in Chrome with the file name.
```
