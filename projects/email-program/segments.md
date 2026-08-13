# Segments & Flow Recipes

*Paste-ready. Segment queries go in Customers → Segments → Create segment.
Flow recipes go in Shopify Flow (included on our plan).*

## Base segments

**All email subscribers (campaign default)**
```
email_subscription_status = 'SUBSCRIBED'
```

**Engaged 90d (use for campaigns once list >5k to protect deliverability)**
```
email_subscription_status = 'SUBSCRIBED' AND last_order_date > -90d
```

**Lapsed buyers (win-back, 90 days)**
```
email_subscription_status = 'SUBSCRIBED' AND last_order_date <= -90d AND last_order_date > -365d
```

## Occasion tagging (powers email 06)

Shopify segments can't filter "bought a wedding product 11 months ago" directly,
so we tag at order time with Flow, then segment on the tag.

**Flow recipe — "Tag occasion buyers":**
- Trigger: Order created
- Condition: any line item title contains `Mr & Mrs` OR `Wedding` OR `Anniversary`
- Action: Add customer tag `occasion-wedding`, add customer tag `occasion-YYYY-MM`
  (use Flow's date formatting for order month)

**Segment — anniversary reminder (rebuilt monthly, send to the cohort from 11 months ago):**
```
customer_tags CONTAINS 'occasion-wedding' AND customer_tags CONTAINS 'occasion-2025-09'
```
*(Example: send in August 2026 to the `occasion-2025-09` cohort — 11 months on,
a month before their date.)*

**Companion Flow recipes worth turning on at the same time (from the checkout audit):**
- Order created with no shipping phone → tag `no-phone` (dispatch exception list)
- Order created where shipping postcode doesn't match `^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$` → tag `check-address` + internal notification (catches the `IV1 1ID` class of failed-delivery risk)
