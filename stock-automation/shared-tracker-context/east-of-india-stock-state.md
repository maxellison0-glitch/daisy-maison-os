# East of India Stock State

Created from Claude automation prompt on 2026-07-09.

This file is the Codex persistent state for the East of India stock report. It replaces the Claude instruction to edit `SKILL.md`.

## Etsy Tracking State

etsy_last_covered_through: 2026-07-07

Meaning: Etsy data is confirmed accurate through 7 July 2026. Everything from 8 July 2026 onward is an open gap until the owner replies to a sync prompt or the gap is otherwise closed.

## Etsy Sync Authorization Policy

Completed Etsy sync quantities are data collection only. Do not update Shopify inventory or this state file from a filled-in template unless the owner explicitly asks Codex to apply the Etsy sync, deduct inventory, or record the sale. If the owner only asks for help finding Etsy sales data, help collect and organize the quantities without changing Shopify or persistent state.

## Etsy Sales Log

Keep roughly the last 30 days.

| Date | Product | Qty | Source |
| --- | --- | ---: | --- |
| 2026-07-08 | Porcelain Matchbox Message Seal - Sealed with a kiss | 1 | ad hoc |

## Etsy Title Mapping

| Shopify Product | Shopify SKU | Etsy Listing Title | Etsy Listing ID | Confidence |
| --- | --- | --- | --- | --- |
| Porcelain Handled Tea Light Holder - Good friends | EOI-TL-GOODFRIENDS | Porcelain Handled Tea Light Holder - Good friends \| Friendship \| Best Friend \| Gift \| EAST OF INDIA | 1760389286 | High |
| Porcelain Matchbox - Little Guardian Angel | EOI-MB-ANGEL | Porcelain Matchbox Message - Little Guardian Angel \| Friendship \| Family \| Gift | 1773996867 | High |
| Porcelain Matchbox Message Dog - Never walk alone | EOI-MB-DOG | Porcelain Matchbox Message Dog - Never walk alone \| Friendship \| Family \| Pet Remembrance Gift | 1774009867 | High |
| Porcelain Matchbox Message Penguin - Flipping love you | EOI-MB-PENGUIN | Porcelain Matchbox Message Penguin - Flipping love you \| Friendship \| Family \| Gift | 1774008229 | High |
| Personalised Teacher Porcelain Matchbox Star - Thanks Teacher | EOI-MB-STAR-TEACHER | Porcelain Matchbox Message Star - Thanks teacher | 4333723155 | High |
| Porcelain Matchbox Message Seal - Sealed with a kiss | EOI-MB-SEAL | Porcelain Matchbox Message Seal - Sealed with a kiss \| Valentines \| Wedding Gift | 1851658454 | High |
| Porcelain Handled Tea Light Holder - You are my sunshine | EOI-TL-SUNSHINE | Porcelain Handled Tea Light Holder - You are my sunshine \| Family \| Mothers Day Gift \| Handcrafted | 1852030642 | High |
| Personalised Teacher Porcelain Tea Light Holder - Thank You for Being Amazing | EOI-TL-TEACHER-AMAZING | Porcelain Handled Tea Light Holder - Thank you for being amazing \| Family \| Friendship \| Thank you \| Mothers Day Gift \| Handcrafted | 1852030336 | High |
| Teacher Matchbox Message Incense Cone - You Are Amazing | EOI-INC-TEACHER-AMAZING | Matchbox Message incense cone - You are amazing | 4333726500 | High |

## Full Clean SKU Scheme

Set on Shopify 2026-07-08:

EOI-TL-GOODFRIENDS, EOI-MB-ANGEL, EOI-MB-BEAR, EOI-MB-DOG, EOI-MB-ELEPHANT, EOI-MB-GIRAFFE, EOI-MB-PENGUIN, EOI-MB-STAR-TEACHER, EOI-HANG-ANGEL, EOI-BAUBLE-JMJ, EOI-MB-JMJ, EOI-MB-SEAL, EOI-TL-MUCHLOVE, EOI-TL-SUNSHINE, EOI-TL-TEACHER-AMAZING, EOI-INC-TEACHER-AMAZING, EOI-MB-LION, ACC-EASEL, ACC-MOUNT-SINGLE, ACC-GIFTWRAP

## Extra Tracked Accessories

### Wooden Display Easel

- Product GID: `gid://shopify/Product/10697617572179`
- Variant GID: `gid://shopify/ProductVariant/54200245387603`
- Price: GBP 3.95
- Continue selling when out of stock: enabled.
- Treat as normal single-product row using Shopify + Etsy where available.

### Mounting Strips Group

These four Shopify listings are different price/pack options for the same physical mounting-strip stock. Source: Amazon, next-day delivery available.

- Primary physical-stock listing: `(GBP 1.99) Mounting Strips`
  - Product GID: `gid://shopify/Product/9848399855955`
  - SKU: `ACC-MOUNT-SINGLE`
- Legacy price tier: `(GBP 3.90) Mounting Strips`
  - Product GID: `gid://shopify/Product/9966426128723`
- Legacy price tier: `(GBP 4.95) Mounting Strips`
  - Product GID: `gid://shopify/Product/9858979135827`
- Two Sign Pack:
  - Product GID: `gid://shopify/Product/10660622238035`
  - Each unit sold consumes 2 pairs of the shared physical stock.

All four have continue selling when out of stock enabled. Report them as one row: `Mounting Strips (shared stock)`.

### Gift Wrap Kit

- Product GID: `gid://shopify/Product/10600061829459`
- Variant GID: `gid://shopify/ProductVariant/53802540171603`
- SKU: `ACC-GIFTWRAP`
- Price: GBP 5.95
- Continue selling when out of stock: enabled.
- Made fresh daily rather than held as stock.
- Baseline stock is intentionally 0.
- Do not flag reorder risk. Alert: BLUE MADE TO ORDER.

### Thermal Labels

- Not a Shopify product.
- Manually tracked consumable.
- One Shopify order uses one label.
- Baseline as of 2026-07-08: 500 labels, 2 rolls x 250.
- Current calculation starts from 2026-07-09, the day after baseline confirmation.

Current baseline:

- Baseline date: 2026-07-16
- Baseline quantity: 250 labels (one remaining roll)

If new rolls are added, update this baseline date and quantity.

Max correction recorded 2026-07-16: the previous estimated 30 labels was wrong;
physical stock is one roll of 250 labels. Thermal-label usage tracking restarts
from 2026-07-17 against this corrected baseline.

## Supplier Purchase Evidence

Invoice photo supplied by Max and recorded 2026-07-16. This is purchase/receipt
evidence only; it does not directly update Shopify inventory.

| Invoice date | Invoice number | Product code | Supplier description | Qty | Unit price |
| --- | --- | ---: | --- | ---: | ---: |
| 2026-07-14 | 14044-82 | 34 | Matchbox-Seal | 5 | GBP 2.50 |
| 2026-07-14 | 14044-82 | 1568 | Suspension-Oil new borrowed blue | 20 | GBP 1.95 |
| 2026-07-14 | 14044-82 | 5663 | Matchbox-Thanks teacher | 25 | GBP 2.50 |
| 2026-07-14 | 14044-82 | 5706 | Handled tea light holder-Thank you | 70 | GBP 3.95 |

Invoice totals shown: goods GBP 390.50, discount GBP 39.05, VAT GBP 70.29,
invoice total GBP 421.74. Product-code/SKU mapping for the supplier lines still
needs confirmation before allocating these quantities to Shopify stock rows.

## Invoice Application Log

On 2026-07-16 Max explicitly asked to apply the invoice to the Shopify
inventory counters. The following compare-and-set updates were completed at
the Shopify `Shop location`, using reason `received`:

| Shopify item | Previous available | Invoice qty added | New available |
| --- | ---: | ---: | ---: |
| Porcelain Matchbox Message Seal - Sealed with a kiss | 1 | 5 | 6 |
| Lucky Sixpence (Boxed) - Old, New, Borrowed, Blue | 36 | 20 | 56 |
| Personalised Teacher Porcelain Matchbox Star - Thanks Teacher | 4 | 25 | 29 |
| Personalised Teacher Porcelain Tea Light Holder - Thank You for Being Amazing | -3 | 70 | 67 |

The supplier-code-1568 line was mapped to Lucky Sixpence after searching the
live Shopify catalog. No other inventory counters were changed.

Standing receipt rule: a clear physical invoice or delivery note in a photo is
treated as delivered just now. Apply legible quantities automatically, record
the document reference and Europe/London processing timestamp, and keep any
unmatched line separate until its SKU mapping is confirmed.

## Not Yet On Etsy

Exclude these from Etsy sync prompt until the owner confirms an active Etsy listing exists:

- Porcelain Matchbox Message Bear - Big bear hug
- Porcelain Matchbox Message Elephant - You are loved
- Porcelain Matchbox Message Giraffe - Daddy
- Porcelain hanging angel - Guardian angel
- Porcelain Half Bauble Scene - Jesus, Mary & Joseph
- Porcelain Matchbox Message - Jesus Mary and Joseph
- Porcelain Handled Tea Light Holder - With much love
- Porcelain Matchbox Message Lion - Be fearless you can do it
- Wooden Display Easel
- Mounting Strips
- Gift Wrap Kit

## Discontinued / Excluded Products

Discontinued 2026-07-02, not being restocked. Exclude from the report even if active or residual sales appear:

- Porcelain Handled Tea Light Holder - Sending you the biggest hug
- Porcelain Lucky Horseshoe - Just Married
- Boxed Message Card - Away in a manger
- Porcelain Christmas Tree Bauble - Happiness and love
- Porcelain Christmas Bauble - Glad tidings we bring
- Porcelain Christmas Bauble - Nativity Scene
- Porcelain Christmas Bauble - Baby's first Christmas
- Personalised Teacher Porcelain Matchbox Message Star - Thanks for Being So Amazing

## Notes

- Shopify inventory figures were last corrected via physical stock check on 2026-07-02.
- Products with committed orders may show lower available stock than on-hand.
- Negative stock is urgent except for Wooden Display Easel, Mounting Strips group, and Gift Wrap Kit where overselling is intentionally enabled.
- Thermal Labels at or below 0 is a real physical dispatch problem and must be flagged urgent.
