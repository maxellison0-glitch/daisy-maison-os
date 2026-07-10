# Daisy Maison — Permanent Learnings

*Distilled from experiments and operating experience. These are settled facts, not hypotheses.*

---

## Mounting Strips — Pricing Architecture

- Mounting Strips launched April 2025. By June 2026: ~6,559 attach orders, ~£15,660 lifetime revenue, ~£1,100/month and rising.
- The product costs pennies. Margin is near-100%. Every pricing decision here flows almost entirely to profit.
- **Price test live 6 Jun 2026:** £1.95 → £2.25 (+15%). Success condition: revenue per day equal or higher than baseline (i.e. the 15% price rise is not cancelled by a >15% drop in attach rate).
- How pricing is stored: variant price only + product title (e.g. "(£2.25) Mounting Strips"). No hardcoded values in the theme. Globo and Candy Rack both read price live from Shopify — no app config needed when price changes.
- Rollback is two field changes in Shopify Admin. Takes under 2 minutes.
- Separate Mounting Strips variants exist at £3.90 and £4.95 — these are untouched by the £1.95/£2.25 test.

---

## Add-On Strategy

- **Attach rate is driven by product type, not season or occasion.** The key variable is wall-mounted vs freestanding:
  - Wall-mounted street signs → Mounting Strips attach rate 30–44% (Valentine's peak ~42–44%)
  - Freestanding items (pebble pictures, standing acrylic plates, number plates) → attach rate ~10–15%
  - Father's Day is a big volume season but low strip attach (~15%) because the hero products are freestanding
- The freestanding range currently attaches nothing — it is the untapped segment. New add-ons there are fully incremental, not cannibalising strips.
- **Microfiber cleaning cloth** identified as the cleanest first new add-on: cheap to source, easy to pack, near-100% margin, natural pair for pebble pictures at checkout.
- **Wooden easel** is next in line for pebble pictures — pending a packing/shipping-fit check before committing.
- Testing order: (1) price increase existing product → signal with zero new work; (2) cloth at checkout → prove freestanding-attach concept; (3) easel → once cloth validates the thesis.

---

## Business Operating Rules

- **Revenue metric:** always use `total_sales` (full revenue including shipping and tax). Never use `gross_sales` as the headline figure.
- **Daily floor:** £3,000 total_sales. Flag 🟢 if hit, 🔴 if missed. ROAS floor: 3x (Shopify total_sales ÷ total ad spend).
- **TEST OCT 2022** Facebook campaign is intentional. It runs by design, targets higher AOV products. Report its spend and clicks like any other campaign, nothing more.
- **Be decisive.** The owner prefers to be told what to do with brief reasoning and is not looking for a yes man, but rather a partner genuinely making the correct decisions for this real company. Don't offer choices unless the stakes are high and options are genuinely close.
- **Distorted days to note, not weight:** Shopify outage 3 Jun (Google Ads off, Facebook spent through it, ROAS 1.68x — not representative). Google Ads offline 2 Jun — also not representative.
- **Long-term objective:** owner capable of running ads in-house by ~Q4 2026. Daryl (~£1k/month) stays as long as he's worth it. The goal is removing dependence, not removing Daryl. Key unresolved dependency: the CSS partner behind [RDD] campaigns.
- **Daily digest tone:** honest mirror. Flag downward trends early. Never dress up bad days. The honesty is the asset.
