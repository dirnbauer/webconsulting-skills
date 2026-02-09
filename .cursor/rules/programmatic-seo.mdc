---
name: programmatic-seo
description: >-
  Build SEO-optimized pages at scale using templates and data. Use for directory pages,
  location pages, comparison pages, integration pages, or any pattern-based content
  strategy. Triggers on "programmatic SEO", "template pages", "pages at scale", or
  "[keyword] + [city] pages".
license: MIT
metadata:
  version: "1.0.0"
---

# Programmatic SEO

> **Source:** This skill is adapted from **[AgentKits Marketing](https://github.com/aitytech/agentkits-marketing)** 
> by AITYTech. Enterprise-grade AI marketing automation (MIT License).

Build SEO-optimized pages at scale using templates and data. Create pages that rank, provide value, and avoid thin content penalties.

---

## Core Principles

### 1. Unique Value Per Page
Every page must provide value specific to that page:
- Unique data, insights, or combinations
- Not just swapped variables in a template
- Avoid "thin content" penalties

### 2. Proprietary Data Wins
Hierarchy of data defensibility:
1. **Proprietary** (you created it)
2. **Product-derived** (from your users)
3. **User-generated** (your community)
4. **Licensed** (exclusive access)
5. **Public** (anyone can use—weakest)

### 3. Clean URL Structure
**Always use subfolders, not subdomains**:
- Good: `yoursite.com/templates/resume/`
- Bad: `templates.yoursite.com/resume/`

Subfolders pass authority to your main domain.

---

## The 12 Programmatic SEO Playbooks

### 1. Templates
**Pattern**: "[Type] template" or "free [type] template"
**Example**: "resume template", "invoice template"

**URL**: `/templates/[type]/`

### 2. Curation
**Pattern**: "best [category]" or "top [number] [things]"
**Example**: "best website builders", "top 10 crm software"

**URL**: `/best/[category]/`

### 3. Conversions
**Pattern**: "[X] to [Y]" or "[amount] [unit] in [unit]"
**Example**: "$10 USD to GBP", "100 kg to lbs"

**URL**: `/convert/[from]-to-[to]/`

### 4. Comparisons
**Pattern**: "[X] vs [Y]" or "[X] alternative"
**Example**: "webflow vs wordpress", "notion alternatives"

**URL**: `/compare/[x]-vs-[y]/`

### 5. Examples
**Pattern**: "[type] examples" or "[category] inspiration"
**Example**: "saas landing page examples"

**URL**: `/examples/[type]/`

### 6. Locations
**Pattern**: "[service/thing] in [location]"
**Example**: "coworking spaces in san diego"

**URL**: `/[service]/[city]/`

### 7. Personas
**Pattern**: "[product] for [audience]"
**Example**: "payroll software for agencies"

**URL**: `/for/[persona]/`

### 8. Integrations
**Pattern**: "[your product] [other product] integration"
**Example**: "slack asana integration"

**URL**: `/integrations/[product]/`

### 9. Glossary
**Pattern**: "what is [term]" or "[term] definition"
**Example**: "what is pSEO", "api definition"

**URL**: `/glossary/[term]/`

### 10. Translations
Same content in multiple languages.

**URL**: `/[lang]/[page]/`

### 11. Directory
**Pattern**: "[category] tools" or "[type] software"
**Example**: "ai copywriting tools"

**URL**: `/directory/[category]/`

### 12. Profiles
**Pattern**: "[person/company name]"
**Example**: "stripe ceo", "airbnb founding story"

**URL**: `/companies/[name]/`

---

## Choosing Your Playbook

| If you have... | Consider... |
|----------------|-------------|
| Proprietary data | Stats, Directories, Profiles |
| Product with integrations | Integrations |
| Design/creative product | Templates, Examples |
| Multi-segment audience | Personas |
| Local presence | Locations |
| Tool or utility product | Conversions |
| Content/expertise | Glossary, Curation |
| Competitor landscape | Comparisons |

You can combine playbooks:
- **Locations + Personas**: "Marketing agencies for startups in Austin"
- **Curation + Locations**: "Best coworking spaces in San Diego"

---

## Implementation Framework

### 1. Keyword Pattern Research

- Identify the repeating structure
- Validate demand (aggregate search volume)
- Assess competition (can you realistically compete?)

### 2. Data Schema Design

```
For "[Service] in [City]" pages:

city:
  - name
  - population
  - relevant_stats

service:
  - name
  - description
  - typical_pricing

local_providers:
  - name
  - rating
  - reviews_count
```

### 3. Template Design

```
H1: [Service] in [City]: [Year] Guide

Intro: [Dynamic paragraph using city stats]

Section 1: Why [City] for [Service]
[City-specific data and insights]

Section 2: Top [Service] Providers in [City]
[Data-driven list]

Section 3: Pricing for [Service] in [City]
[Local pricing data]

Related: [Service] in [Nearby Cities]
```

### 4. Internal Linking Architecture

**Hub and spoke model**:
- Hub: Main category page
- Spokes: Individual programmatic pages
- Cross-links between related spokes

**Avoid orphan pages**:
- Every page reachable from main site
- XML sitemap for all pages
- Breadcrumbs for hierarchy

---

## Quality Checks

### Pre-Launch

- [ ] Each page provides unique value
- [ ] Not just variable substitution
- [ ] Unique titles and meta descriptions
- [ ] Schema markup implemented
- [ ] Connected to site architecture
- [ ] In XML sitemap

### Post-Launch Monitoring

- Indexation rate in Search Console
- Rankings by page pattern
- Engagement metrics
- Watch for thin content warnings

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Just swapping city names | Add unique local data |
| Multiple pages targeting same keyword | Clear hierarchy, no cannibalization |
| Too many low-quality pages | Quality over quantity |
| Pages exist for Google, not users | Focus on genuine utility |

---

## Credits & Attribution

This skill is adapted from **[AgentKits Marketing](https://github.com/aitytech/agentkits-marketing)** by AITYTech.

**Copyright (c) AITYTech** - MIT License  
Adapted by webconsulting.at for this skill collection
