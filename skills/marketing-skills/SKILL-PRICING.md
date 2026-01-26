---
name: marketing-skills-pricing
description: Pricing strategy, packaging, value metrics, and monetization for SaaS and digital products.
version: 1.0.0
parent: marketing-skills
triggers:
  - pricing
  - pricing tiers
  - freemium
  - free trial
  - price increase
  - monetization
  - packaging
---

# Pricing Strategy

> **Prerequisite:** Read the main `SKILL.md` for overview and quick reference.

You are an expert in SaaS pricing and monetization strategy. Your goal is to help design pricing that captures value, drives growth, and aligns with customer willingness to pay.

## Before Starting

Gather this context:

### 1. Business Context
- What type of product? (SaaS, marketplace, e-commerce, service)
- What's your current pricing (if any)?
- What's your target market? (SMB, mid-market, enterprise)
- What's your go-to-market motion? (self-serve, sales-led, hybrid)

### 2. Value & Competition
- What's the primary value you deliver?
- What alternatives do customers consider?
- How do competitors price?

### 3. Current Performance
- Current conversion rate?
- Average revenue per user (ARPU)?
- Churn rate?

---

## Pricing Fundamentals

### The Three Pricing Axes

1. **Packaging** — What's included at each tier?
2. **Pricing Metric** — What do you charge for? (per user, usage, flat)
3. **Price Point** — How much do you charge?

### Value-Based Pricing

Price between the next best alternative and perceived value. Cost is a floor, not a basis.

```
Customer's perceived value     ───────── $1000
       ↑ Your opportunity
Your price                     ───────── $500
       ↑ Consumer surplus
Next best alternative          ───────── $300
       ↑ Differentiation value
Your cost to serve             ───────── $50
```

---

## Value Metrics

### What is a Value Metric?

The value metric is what you charge for—it should scale with the value customers receive.

### Common Value Metrics

| Metric | Best For | Example |
|--------|----------|---------|
| Per user/seat | Collaboration tools | Slack, Notion |
| Per usage | Variable consumption | AWS, Twilio |
| Per feature | Modular products | HubSpot add-ons |
| Per contact/record | CRM, email tools | Mailchimp |
| Per transaction | Payments, marketplaces | Stripe, Shopify |
| Flat fee | Simple products | Basecamp |
| Revenue share | High-value outcomes | Affiliate platforms |

### Choosing Your Value Metric

**Step 1:** Identify how customers get value
- What outcome do they care about?
- What would they pay more for?

**Step 2:** Map usage to value
- As customers use more of [metric], do they get more value?
- If yes → good value metric

**Step 3:** Validate with data
- Which usage patterns predict retention?
- Which customers pay the most, and why?

---

## Tier Structure

### How Many Tiers?

| Tiers | When to Use |
|-------|-------------|
| 2 tiers | Clear SMB vs. Enterprise split |
| 3 tiers | Industry standard (Good-Better-Best) |
| 4+ tiers | Wide range of customer sizes |

### Good-Better-Best Framework

| Tier | Purpose | Target |
|------|---------|--------|
| **Good** (Entry) | Remove barriers to entry | Small teams, try before buy |
| **Better** (Recommended) | Where most customers land | Growing teams, serious users |
| **Best** (Premium) | Capture high-value customers | Larger teams, power users |

### Tier Differentiation Strategies

**Feature gating:** Basic features in all, advanced in higher tiers
**Usage limits:** Same features, different limits (users, storage, API calls)
**Support level:** Email → Priority → Dedicated success
**Access:** API access, SSO, custom branding at higher tiers

### Example Tier Structure

```
                Starter      Pro          Business
                $29/mo       $79/mo       $199/mo
─────────────────────────────────────────────────────
Users           Up to 5      Up to 20     Unlimited
Projects        10           Unlimited    Unlimited
Storage         5 GB         50 GB        500 GB
Integrations    3            10           Unlimited
Analytics       Basic        Advanced     Custom
Support         Email        Priority     Dedicated
API Access      ✗            ✓            ✓
SSO             ✗            ✗            ✓
```

---

## Freemium vs Free Trial

### When to Use Freemium

**Freemium works when:**
- Product has viral/network effects
- Free users provide value (content, data, referrals)
- Large market where % conversion drives volume
- Low marginal cost to serve free users
- Clear feature/usage limits for upgrade trigger

**Freemium risks:**
- Free users may never convert
- Devalues product perception
- Support costs for non-paying users

### When to Use Free Trial

**Free trial works when:**
- Product needs time to demonstrate value
- Onboarding/setup investment required
- B2B with buying committees
- Higher price points
- Product is "sticky" once configured

**Trial length:**
- 7-14 days for simple products
- 14-30 days for complex products

**Credit card upfront:**
- Higher trial-to-paid conversion (40-50% vs. 15-25%)
- Lower trial volume, better qualified leads

### Hybrid Approaches

- **Freemium + Trial:** Free tier with limited features, trial of premium
- **Reverse trial:** Start with full access, downgrade to free after trial

---

## Pricing Research

### Van Westendorp Price Sensitivity

Ask respondents four questions:
1. At what price is it too expensive?
2. At what price is it too cheap (quality concern)?
3. At what price is it getting expensive but still considerable?
4. At what price is it a bargain?

**Analysis produces:**
- Acceptable price range
- Optimal price point
- Price sensitivity by segment

### MaxDiff Analysis

Show sets of 4-5 features, ask "most important" and "least important."
Results rank features by utility score for packaging decisions.

| Utility Score | Packaging Decision |
|---------------|-------------------|
| Top 20% | Include in all tiers (table stakes) |
| 20-50% | Use to differentiate tiers |
| 50-80% | Higher tiers only |
| Bottom 20% | Consider cutting or premium add-on |

---

## When to Raise Prices

### Signs It's Time

**Market signals:**
- Competitors have raised prices
- You're significantly cheaper than alternatives
- Prospects don't flinch at price

**Business signals:**
- Very high conversion rates (>40%)
- Very low churn (<3% monthly)
- Unit economics are strong

**Product signals:**
- Significant value added since last pricing
- Product more mature/stable

### Price Increase Strategies

1. **Grandfather existing** — New price for new only, existing keep old
2. **Delayed increase** — Announce 3-6 months out, time to lock in
3. **Increase tied to value** — Raise price but add features
4. **Plan restructure** — Change plans entirely, map existing customers

---

## Pricing Page Best Practices

### Above the Fold
- Clear tier comparison table
- Recommended tier highlighted
- Monthly/annual toggle
- Primary CTA for each tier

### Common Elements
- [ ] Feature comparison table
- [ ] Who each tier is for
- [ ] FAQ section
- [ ] Contact sales option
- [ ] Annual discount callout
- [ ] Money-back guarantee
- [ ] Customer logos/trust signals

### Pricing Psychology

- **Anchoring:** Show higher-priced option first
- **Decoy effect:** Middle tier obviously best value
- **Charm pricing:** $49 vs. $50 (for value-focused)
- **Round pricing:** $50 vs. $49 (for premium)
- **Annual savings:** 17-20% discount for annual

---

## Enterprise Pricing

### When to Add Custom Pricing

Add "Contact Sales" when:
- Deal sizes exceed $10k+ ARR
- Customers need custom contracts
- Implementation/onboarding required
- Security/compliance requirements

### Enterprise Tier Elements

**Table stakes:** SSO/SAML, audit logs, admin controls, uptime SLA
**Value-adds:** Dedicated support, custom onboarding, training, priority roadmap

---

## Pricing Checklist

### Before Setting Prices
- [ ] Defined target customer personas
- [ ] Researched competitor pricing
- [ ] Identified your value metric
- [ ] Conducted willingness-to-pay research

### Pricing Structure
- [ ] Chosen number of tiers
- [ ] Differentiated tiers clearly
- [ ] Set price points based on research
- [ ] Created annual discount strategy
- [ ] Planned enterprise tier

### Validation
- [ ] Tested with target customers
- [ ] Reviewed with sales team
- [ ] Validated unit economics
- [ ] Set up tracking for pricing metrics

---

## Questions to Ask

1. What pricing research have you done?
2. What's your current ARPU and conversion rate?
3. What's your primary value metric?
4. Who are your main pricing personas?
5. Are you self-serve, sales-led, or hybrid?
