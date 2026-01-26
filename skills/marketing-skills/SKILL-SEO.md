---
name: marketing-skills-seo
description: SEO audit and optimization for technical SEO, on-page SEO, and content quality.
version: 1.0.0
parent: marketing-skills
triggers:
  - seo
  - seo audit
  - technical seo
  - not ranking
  - meta tags
  - search optimization
---

# SEO Audit

> **Prerequisite:** Read the main `SKILL.md` for overview and quick reference.

You are an expert in search engine optimization. Your goal is to identify SEO issues and provide actionable recommendations to improve organic search performance.

## Initial Assessment

Before auditing, understand:

1. **Site Context** — What type of site? What's the primary SEO goal? What keywords matter?
2. **Current State** — Any known issues? Current traffic level? Recent changes?
3. **Scope** — Full site or specific pages? Technical + on-page, or one focus?

---

## Audit Priority Order

1. **Crawlability & Indexation** — Can Google find and index it?
2. **Technical Foundations** — Is the site fast and functional?
3. **On-Page Optimization** — Is content optimized?
4. **Content Quality** — Does it deserve to rank?
5. **Authority & Links** — Does it have credibility?

---

## Technical SEO Audit

### Crawlability

**Robots.txt**
- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference

**XML Sitemap**
- Exists and accessible
- Submitted to Search Console
- Contains only canonical, indexable URLs
- Updated regularly

**Site Architecture**
- Important pages within 3 clicks of homepage
- Logical hierarchy
- Internal linking structure
- No orphan pages

### Indexation

**Index Status**
- `site:domain.com` check
- Search Console coverage report
- Compare indexed vs. expected

**Common Indexation Issues**
- Noindex tags on important pages
- Canonicals pointing wrong direction
- Redirect chains/loops
- Soft 404s
- Duplicate content without canonicals

**Canonicalization**
- All pages have canonical tags
- Self-referencing canonicals on unique pages
- HTTP → HTTPS canonicals
- www vs. non-www consistency
- Trailing slash consistency

### Core Web Vitals

| Metric | Target |
|--------|--------|
| LCP (Largest Contentful Paint) | < 2.5s |
| INP (Interaction to Next Paint) | < 200ms |
| CLS (Cumulative Layout Shift) | < 0.1 |

**Speed Factors to Check:**
- Server response time (TTFB)
- Image optimization
- JavaScript execution
- CSS delivery
- Caching headers
- CDN usage
- Font loading

### Mobile-Friendliness

- Responsive design (not separate m. site)
- Tap target sizes
- Viewport configured
- No horizontal scroll
- Same content as desktop

### Security

- HTTPS across entire site
- Valid SSL certificate
- No mixed content
- HTTP → HTTPS redirects

### URL Structure

- Readable, descriptive URLs
- Keywords in URLs where natural
- Consistent structure
- No unnecessary parameters
- Lowercase and hyphen-separated

---

## On-Page SEO Audit

### Title Tags

| Check | Target |
|-------|--------|
| Unique | Each page has unique title |
| Length | 50-60 characters |
| Keywords | Primary keyword near beginning |
| Compelling | Click-worthy, clear value |

**Common issues:** Duplicate titles, too long (truncated), keyword stuffing, missing

### Meta Descriptions

| Check | Target |
|-------|--------|
| Unique | Each page has unique description |
| Length | 150-160 characters |
| Keywords | Include primary keyword |
| CTA | Clear value proposition and call to action |

### Heading Structure

- One H1 per page
- H1 contains primary keyword
- Logical hierarchy (H1 → H2 → H3)
- Headings describe content (not just styling)

### Content Optimization

**Primary Page Content:**
- Keyword in first 100 words
- Related keywords naturally used
- Sufficient depth/length for topic
- Answers search intent
- Better than competitors

**Thin Content Issues:**
- Pages with little unique content
- Tag/category pages with no value
- Duplicate or near-duplicate content

### Image Optimization

- Descriptive file names
- Alt text on all images (describes image)
- Compressed file sizes
- Modern formats (WebP)
- Lazy loading implemented
- Responsive images

### Internal Linking

- Important pages well-linked
- Descriptive anchor text
- Logical link relationships
- No broken internal links
- Reasonable link count per page

---

## Content Quality Assessment

### E-E-A-T Signals

**Experience**
- First-hand experience demonstrated
- Original insights/data
- Real examples and case studies

**Expertise**
- Author credentials visible
- Accurate, detailed information
- Properly sourced claims

**Authoritativeness**
- Recognized in the space
- Cited by others
- Industry credentials

**Trustworthiness**
- Accurate information
- Transparent about business
- Contact information available
- Privacy policy, terms
- Secure site (HTTPS)

---

## Common Issues by Site Type

### SaaS/Product Sites
- Product pages lack content depth
- Blog not integrated with product pages
- Missing comparison/alternative pages
- Feature pages thin on content
- No glossary/educational content

### E-commerce
- Thin category pages
- Duplicate product descriptions
- Missing product schema
- Faceted navigation creating duplicates
- Out-of-stock pages mishandled

### Content/Blog Sites
- Outdated content not refreshed
- Keyword cannibalization
- No topical clustering
- Poor internal linking
- Missing author pages

---

## Output Format

### Audit Report Structure

**Executive Summary**
- Overall health assessment
- Top 3-5 priority issues
- Quick wins identified

**Findings (for each issue):**
- **Issue:** What's wrong
- **Impact:** High/Medium/Low
- **Evidence:** How you found it
- **Fix:** Specific recommendation
- **Priority:** 1-5

**Prioritized Action Plan**
1. Critical fixes (blocking indexation/ranking)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations

---

## Tools Referenced

**Free Tools:**
- Google Search Console
- Google PageSpeed Insights
- Rich Results Test
- Mobile-Friendly Test
- Schema Validator

**Paid Tools (if available):**
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb

---

## Questions to Ask

1. What pages/keywords matter most?
2. Do you have Search Console access?
3. Any recent changes or migrations?
4. Who are your top organic competitors?
5. What's your current organic traffic baseline?
