# Sat 17 Oct 2026: Free delivery weekend (spec for the agent prompt)

This replaces the Saturday "bestsellers" email in `2026-10-17_and_20-claude.md`.
It reuses that email's three bestsellers and adds the offer. It doesn't add an
extra send.

**Why this hook (not a % sitewide discount):**
- **Email is tiring the list.** There were 7 campaign emails in 14 days
  (2, 5 ×2, 7, 9, 13, 15 Oct), to the same ~19k–51k people. Email-tagged sales by
  send: £38, £0, £0, **£283**, £96, £43, £67. One focused new range with a strong
  photo (the pebble glow-up, 7 Oct) did 3–7× the rest. Everything since is lower.
  That's frequency and sameness, not a dead list.
- **Free delivery over £25 is the shipping-threshold test we already wanted.**
  Shipping averages £5.40 an order and is the likeliest reason people back out at
  checkout. A £25 minimum also pushes order value up: a Large Mr & Mrs sign
  (£20.24) plus strips and a gift box gets there.
- **A % discount now teaches the list to wait for Black Friday, 5 weeks out,**
  and comes straight off margin with the store already near the 2.3x floor.
- It's a code, so it only applies to people who use it, and the digest can count it.

**Max to approve before pasting:** the code and the £25 minimum.

Paste everything below into Claude in Chrome, after the master prompt in
`AGENT-PROMPT-shopify-email.md`.

```text
CAMPAIGN NAME: Free delivery weekend - 17 Oct
DUPLICATE FROM: 🎄 A little piece of your family on the tree 🎄
TEST TO: maxellison0@gmail.com

DISCOUNT
  Type: Free shipping
  Method: Discount code
  Code: FREEDELIVERY25
  Countries: United Kingdom
  Exclude shipping rates over: leave off
  Minimum purchase requirement: Minimum purchase amount £25.00
  Customer eligibility: All customers
  Maximum uses: Limit to one use per customer
  Combinations: none ticked
  Active dates: start 17 Oct 2026 00:00, end 19 Oct 2026 23:59 (UK time)

SUBJECT: Free delivery this weekend 🚚
PREVIEW TEXT: On orders over £25 with code FREEDELIVERY25, until Sunday midnight

SEGMENTS
  DM Email – Engaged (opened 30d)
  DM Email – Customers (ordered 12m)

BLOCKS (in this order)
 1. Header image: keep the one from the duplicated email.
 2. Text block, background #F3F2EE, centred:
    Heading (Georgia, #2F3B2E): Free delivery this weekend
    Line (code in #8E3B33, bold): Use code FREEDELIVERY25 on orders over £25.
    Small line: Ends Sunday 19 October at midnight.
 3. Text: Our three most-ordered gifts this week, each one personalised by hand.
 4. Product: Personalised Mr & Mrs Street Sign Gift — Wedding Anniversary or Couple Present UK
    Caption under it: Our most-ordered gift this week. Small £11.25, Medium £17.24, Large £20.24.
    Button: PERSONALISE YOURS → https://daisymaison.co.uk/products/mr-mrs-personalised-street-sign-gift
 5. Product: Personalised Engagement Pebble Picture Gift — Love Tree | Engagement or Proposal Present UK
    Caption: For the couple who just said yes. £24.95.
    Button: PERSONALISE YOURS → https://daisymaison.co.uk/products/engagement-proposal-love-tree-personalised-pebble-picture-copy
 6. Product: Personalised Family Street Sign Gift — Custom Family Name Sign | Personalised Home Gift UK
    Caption: Your family name, made for the front door. From £14.95.
    Button: PERSONALISE YOURS → https://daisymaison.co.uk/products/family-personalised-street-sign
 7. Text (small): Tip: a Large sign with mounting strips and a gift box takes you over £25.
 8. Button: SHOP NOW → https://daisymaison.co.uk/collections/christmas-gifts-top-picks
 9. Footer: keep from the duplicated email.

SEND (Max does this after approving the draft): Sat 17 Oct, 10:00 UK time.
```

## Judge it (Tue 20 Oct)

- FREEDELIVERY25 uses and those orders' average value (Shopify → Discounts).
- Email-tagged sales vs the last four sends (£96 / £43 / £67 / £38 averages about £61).
- Checkout abandonment for 17–19 Oct vs the 7-day average (31.5%).
- Unsubscribes (Shopify Email report). If they jump, the cadence is too high.
