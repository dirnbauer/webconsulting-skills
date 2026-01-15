---
name: ai-search-optimization
description: Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) strategies for AI-powered search visibility in ChatGPT, Perplexity, Google AI Overviews, and other AI search platforms.
version: 1.0.0
triggers:
  - aeo
  - geo
  - ai search
  - chatgpt search
  - perplexity
  - ai overviews
  - generative search
  - llm visibility
  - answer engine
---

# AI Search Optimization (AEO & GEO)

> **Scope:** Optimizing content for AI-powered search engines and answer engines
> This skill covers strategies for visibility in ChatGPT, Perplexity, Google AI Overviews, Microsoft Copilot, and other generative AI platforms.

## 1. Understanding AEO & GEO

### What is AEO (Answer Engine Optimization)?

Answer Engine Optimization focuses on structuring content to provide **direct, concise answers** to user queries through AI-powered platforms. Unlike traditional SEO which aims for link clicks, AEO optimizes for being **cited as the answer source**.

**Target platforms:**
- Google AI Overviews (formerly SGE)
- Perplexity AI
- ChatGPT Search
- Microsoft Copilot Search
- Voice assistants (Siri, Alexa, Google Assistant)

### What is GEO (Generative Engine Optimization)?

Generative Engine Optimization is the broader discipline of enhancing content visibility within **AI-generated search results**. It targets generative engines that synthesize answers from multiple sources rather than presenting traditional link lists.

**Key differences from traditional SEO:**

| Aspect | Traditional SEO | AEO/GEO |
|--------|----------------|---------|
| Goal | Rank in SERPs | Be cited in AI answers |
| User behavior | Click through to site | Get answer directly |
| Content format | Keyword-optimized pages | Structured, citable content |
| Success metric | Click-through rate | Citation frequency |
| Query type | Short keywords | Conversational, long-tail |

### The AI Search Landscape (2025-2026)

- **Google AI Overviews:** 2B+ monthly users across 200 countries ([TechCrunch](https://techcrunch.com/2025/07/23/googles-ai-overviews-have-2b-monthly-users-ai-mode-100m-in-the-us-and-india/))
- **Google AI Mode:** 100M+ monthly users in US and India
- **ChatGPT Search:** Real-time web search with citations
- **Perplexity AI:** Real-time citation engine, emphasis on freshness
- **Microsoft Copilot Search:** Bing integration with generative AI
- **Zero-click searches:** About 60% of global searches end without a click ([neotype.ai](https://neotype.ai/zeroclick-searches/))

## 2. Content Structure for AI Readability

### Semantic HTML Structure

AI systems extract information more effectively from well-structured content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Descriptive, Question-Answering Title</title>
</head>
<body>
    <article>
        <header>
            <h1>Primary Topic as Question or Clear Statement</h1>
            <p class="summary">Direct 2-3 sentence answer to the main question.</p>
        </header>
        
        <main>
            <section>
                <h2>Subtopic Heading</h2>
                <p>Detailed explanation with facts and data.</p>
                
                <ul>
                    <li>Key point 1 with specific information</li>
                    <li>Key point 2 with verifiable data</li>
                    <li>Key point 3 with actionable insight</li>
                </ul>
            </section>
        </main>
        
        <aside>
            <h3>Quick Facts</h3>
            <dl>
                <dt>Term</dt>
                <dd>Definition</dd>
            </dl>
        </aside>
    </article>
</body>
</html>
```

### Heading Hierarchy Best Practices

```markdown
# H1: Main Topic (contains primary question/keyword)
   └── ## H2: Major subtopic
          └── ### H3: Specific aspect
                 └── #### H4: Details (use sparingly)
```

**Rules:**
- Single H1 per page
- H1 should answer "What is this page about?"
- Use question-format headings when appropriate
- Include target keywords naturally

### The Inverted Pyramid Pattern

Structure content for AI extraction:

```
┌─────────────────────────────────────┐
│     DIRECT ANSWER (First 1-2       │ ← AI extracts this
│     sentences answer the query)     │
├─────────────────────────────────────┤
│     KEY FACTS & CONTEXT            │ ← Supporting evidence
│     (Bullet points, data, quotes)   │
├─────────────────────────────────────┤
│     DETAILED EXPLANATION           │ ← Comprehensive coverage
│     (Background, methodology,       │
│      examples, case studies)        │
├─────────────────────────────────────┤
│     RELATED TOPICS                 │ ← Topic authority signals
│     (Links to related content)      │
└─────────────────────────────────────┘
```

### Lists and Tables for Extraction

AI engines prefer structured data formats:

```html
<!-- Comparison Table -->
<table>
    <caption>Feature Comparison: Product A vs Product B</caption>
    <thead>
        <tr>
            <th>Feature</th>
            <th>Product A</th>
            <th>Product B</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Price</td>
            <td>$99/month</td>
            <td>$149/month</td>
        </tr>
        <!-- More rows -->
    </tbody>
</table>

<!-- Definition List for Terms -->
<dl>
    <dt>AEO</dt>
    <dd>Answer Engine Optimization - optimizing content for direct answers</dd>
    
    <dt>GEO</dt>
    <dd>Generative Engine Optimization - visibility in AI-generated results</dd>
</dl>

<!-- Step-by-Step Process -->
<ol>
    <li>Step one with clear action</li>
    <li>Step two with measurable outcome</li>
    <li>Step three with verification method</li>
</ol>
```

## 3. Schema Markup for AI Understanding

### Essential Schema Types

Research shows structured data significantly improves AI search visibility:

- Pages with schema are **up to 40% more likely** to appear in Google AI Overviews ([zarkx.com](https://www.zarkx.com/insights/ai-first-schema-implementation-rich-results))
- **Organization schema**: 2.8x increase in citation frequency
- **FAQPage schema**: 2.5x rise in answer inclusion
- **Article schema**: 2.2x boost in content citations
- Sites with 15+ schema types see **2.4x higher citation rates** ([surgeboom.com](https://surgeboom.com/research/structured-data-ai-citation-impact-study.html))

#### FAQPage Schema

```json
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "What is Answer Engine Optimization?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Answer Engine Optimization (AEO) is a strategic approach to structuring content so AI platforms like ChatGPT, Perplexity, and Google AI Overviews can easily extract and cite it as direct answers to user queries."
            }
        },
        {
            "@type": "Question",
            "name": "How is AEO different from SEO?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "While SEO focuses on ranking in traditional search results for clicks, AEO optimizes content to be cited directly in AI-generated answers, often resulting in zero-click interactions where users get information without visiting the source."
            }
        }
    ]
}
```

#### HowTo Schema

```json
{
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "How to Optimize Content for AI Search",
    "description": "Step-by-step guide to improving visibility in AI-powered search engines",
    "totalTime": "PT30M",
    "step": [
        {
            "@type": "HowToStep",
            "name": "Structure Content Semantically",
            "text": "Use proper HTML5 semantic elements like article, section, and aside",
            "position": 1
        },
        {
            "@type": "HowToStep",
            "name": "Implement Schema Markup",
            "text": "Add FAQPage, HowTo, and Article schema to your pages",
            "position": 2
        },
        {
            "@type": "HowToStep",
            "name": "Optimize for Conversational Queries",
            "text": "Write content that answers natural language questions",
            "position": 3
        }
    ]
}
```

#### Article Schema with Author

```json
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Complete Guide to AI Search Optimization",
    "description": "Learn how to optimize content for ChatGPT, Perplexity, and Google AI Overviews",
    "datePublished": "2025-01-15",
    "dateModified": "2025-01-15",
    "author": {
        "@type": "Person",
        "name": "Expert Name",
        "url": "https://example.com/about/expert-name",
        "jobTitle": "SEO Specialist",
        "sameAs": [
            "https://linkedin.com/in/expertname",
            "https://twitter.com/expertname"
        ]
    },
    "publisher": {
        "@type": "Organization",
        "name": "Company Name",
        "logo": {
            "@type": "ImageObject",
            "url": "https://example.com/logo.png"
        }
    }
}
```

#### Organization Schema

```json
{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Company Name",
    "url": "https://example.com",
    "logo": "https://example.com/logo.png",
    "description": "Brief description of what the organization does",
    "foundingDate": "2010",
    "sameAs": [
        "https://www.linkedin.com/company/companyname",
        "https://twitter.com/companyname",
        "https://github.com/companyname"
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+1-555-123-4567",
        "contactType": "customer service",
        "availableLanguage": ["English", "German"]
    }
}
```

## 4. E-E-A-T Signals for AI Trust

### Experience, Expertise, Authoritativeness, Trustworthiness

AI systems prioritize content from credible sources. Implement these signals:

### Author Bios

```html
<article>
    <!-- Content -->
    
    <footer class="author-bio">
        <img src="/authors/jane-doe.jpg" alt="Jane Doe" />
        <div class="author-info">
            <h4>About the Author</h4>
            <p class="author-name">Jane Doe, PhD</p>
            <p class="author-credentials">
                15 years of experience in digital marketing. 
                Former Head of SEO at Fortune 500 company.
                Published in Search Engine Journal, Moz, and Ahrefs Blog.
            </p>
            <ul class="author-links">
                <li><a href="https://linkedin.com/in/janedoe" rel="author">LinkedIn</a></li>
                <li><a href="https://twitter.com/janedoe" rel="author">Twitter</a></li>
            </ul>
        </div>
    </footer>
</article>
```

### Trust Signals Checklist

- [ ] **Author expertise:** Detailed bios with credentials and experience
- [ ] **Citations:** Link to reputable sources (studies, official docs, experts)
- [ ] **Contact information:** Clear "About Us" and "Contact" pages
- [ ] **HTTPS:** Secure connection required
- [ ] **Privacy policy:** Transparent data handling
- [ ] **Update dates:** Visible "Last updated" timestamps
- [ ] **Original research:** Proprietary data, case studies, expert quotes
- [ ] **Reviews/testimonials:** Third-party validation where applicable

### Building Domain Authority

1. **Earn quality backlinks** from reputable industry sites
2. **Get mentioned** in authoritative publications
3. **Contribute guest posts** to established platforms
4. **Participate in industry forums** and communities
5. **Create original research** that others cite

## 5. Content Freshness Strategy

### Update Frequency by Platform

| Platform | Freshness Preference | Recommended Update Cycle |
|----------|---------------------|--------------------------|
| Perplexity AI | Very high | Every 2-3 days for trending topics |
| ChatGPT Search | High | Weekly updates |
| Google AI Overviews | Moderate | Monthly refresh |
| Bing Copilot | Moderate | Monthly refresh |

### Content Refresh Protocol

```markdown
## Content Freshness Checklist

### Weekly Tasks
- [ ] Update statistics with latest data
- [ ] Refresh screenshots and examples
- [ ] Add new developments or news
- [ ] Update "Last modified" timestamp

### Monthly Tasks
- [ ] Review and update all factual claims
- [ ] Add new sections for emerging topics
- [ ] Update broken links
- [ ] Refresh expert quotes

### Quarterly Tasks
- [ ] Comprehensive content audit
- [ ] Competitive analysis
- [ ] Restructure based on query trends
- [ ] Update all schema markup
```

### Visible Timestamps

```html
<article>
    <header>
        <h1>Article Title</h1>
        <div class="article-meta">
            <time datetime="2025-01-15" itemprop="datePublished">
                Published: January 15, 2025
            </time>
            <time datetime="2025-01-15" itemprop="dateModified">
                Last Updated: January 15, 2025
            </time>
        </div>
    </header>
    <!-- Content -->
</article>
```

## 6. Robots.txt for AI Crawlers

### Allowing AI Bots

To be indexed by AI search engines, explicitly allow their crawlers:

```text
# robots.txt - AI Search Optimization

# Standard search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# OpenAI (ChatGPT)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

# Perplexity AI
User-agent: PerplexityBot
Allow: /

# Anthropic (Claude)
User-agent: ClaudeBot
Allow: /
User-agent: anthropic-ai
Allow: /

# Google AI (Gemini)
User-agent: Google-Extended
Allow: /

# Meta AI
User-agent: FacebookBot
Allow: /

# Common Crawl (used by many AI systems)
User-agent: CCBot
Allow: /

# Microsoft/Bing AI
User-agent: Applebot
Allow: /

# Default rule
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

# Sitemap
Sitemap: https://example.com/sitemap.xml
```

### Blocking AI Training While Allowing AI Search (Optional)

Some organizations want to be **cited in AI search results** but don't want their content **used to train AI models**. Here's how:

**Understanding the difference:**

| Bot | What it does | Block = |
|-----|--------------|---------|
| `GPTBot` | Crawls for **training** OpenAI models | Your content won't train future GPT versions |
| `ChatGPT-User` | **Live browsing** when users search | ChatGPT can't cite you in real-time answers |
| `Google-Extended` | Crawls for **training** Gemini AI | Your content won't train Gemini |
| `PerplexityBot` | **Live search** for Perplexity answers | Perplexity can't cite you |
| `CCBot` | Common Crawl - open **training datasets** | Your content won't be in public AI training data |

**Example: Block training, allow live search citations:**

```text
# BLOCK: AI model training (your content won't train future AI)
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

# ALLOW: Real-time AI search (AI can cite you in answers)
User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /
```

> **Note:** Most businesses focused on AI search visibility should **allow all bots** (Section 6 above).
> Only use this approach if you have specific concerns about AI training on your content.

### AI Bot Reference

| Bot Name | Company | Purpose |
|----------|---------|---------|
| GPTBot | OpenAI | Training data & ChatGPT browsing |
| ChatGPT-User | OpenAI | ChatGPT web browsing |
| PerplexityBot | Perplexity | Real-time search & citations |
| ClaudeBot | Anthropic | Training & retrieval |
| anthropic-ai | Anthropic | Claude AI training |
| Google-Extended | Google | Gemini AI training |
| FacebookBot | Meta | Meta AI training |
| CCBot | Common Crawl | Open dataset for AI training |

## 7. Conversational Query Optimization

### Target Long-Tail, Question-Based Queries

AI search favors natural language:

**Traditional keyword:** `"best project management software"`

**Conversational queries:**
- "What is the best project management software for small teams?"
- "How do I choose project management software for remote work?"
- "Which project management tool has the best free plan?"

### Question-Answer Content Pattern

```markdown
## What is [Topic]?

[Topic] is [direct definition in 1-2 sentences].

### Key characteristics:
- Characteristic 1
- Characteristic 2
- Characteristic 3

## How does [Topic] work?

[Clear explanation of process]

### Step-by-step breakdown:
1. First step
2. Second step
3. Third step

## Why is [Topic] important?

[2-3 sentences on significance]

### Benefits include:
- Benefit 1 with specific outcome
- Benefit 2 with measurable result
- Benefit 3 with real-world application
```

### FAQ Section Template

```html
<section class="faq">
    <h2>Frequently Asked Questions</h2>
    
    <details>
        <summary>What is Answer Engine Optimization?</summary>
        <p>Answer Engine Optimization (AEO) is the practice of...</p>
    </details>
    
    <details>
        <summary>How is GEO different from traditional SEO?</summary>
        <p>While traditional SEO focuses on...</p>
    </details>
    
    <details>
        <summary>Which AI search platforms should I optimize for?</summary>
        <p>The main platforms to consider are...</p>
    </details>
</section>
```

## 8. Multimedia Optimization

### Image Requirements

Perplexity and other AI engines prefer visual content:

```html
<figure>
    <img 
        src="/images/ai-search-diagram.webp" 
        alt="Diagram showing how AI search engines process and cite content"
        width="800"
        height="450"
        loading="lazy"
    />
    <figcaption>
        How AI search engines extract and cite content sources
    </figcaption>
</figure>
```

**Best practices:**
- Minimum 2 unique, relevant images per article
- Descriptive alt text (not keyword stuffing)
- WebP format for performance
- Include diagrams, infographics, process flows
- Add captions with context

### Video Integration

```html
<figure class="video-embed">
    <iframe 
        src="https://www.youtube.com/embed/VIDEO_ID"
        title="Detailed explanation of AI Search Optimization"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media"
        allowfullscreen
    ></iframe>
    <figcaption>
        Video: Complete guide to optimizing for AI search engines
    </figcaption>
</figure>
```

### Video Schema

```json
{
    "@context": "https://schema.org",
    "@type": "VideoObject",
    "name": "AI Search Optimization Tutorial",
    "description": "Learn how to optimize content for ChatGPT, Perplexity, and Google AI",
    "thumbnailUrl": "https://example.com/video-thumbnail.jpg",
    "uploadDate": "2025-01-15",
    "duration": "PT10M30S",
    "contentUrl": "https://example.com/videos/ai-search-tutorial.mp4"
}
```

## 9. Monitoring AI Search Visibility

### AI Brand Monitoring Tools

| Tool | Platforms Monitored | Key Features |
|------|---------------------|--------------|
| **Semrush AI Visibility** | ChatGPT, Gemini, Perplexity | Free tier, mention tracking |
| **Brand24** | ChatGPT, Perplexity, Claude, Gemini | Multi-platform analysis |
| **SE Ranking** | Google AI Overviews, ChatGPT, Gemini | Share of voice tracking |
| **Keyword.com** | Google AI Overviews, ChatGPT, Perplexity | Optimization suggestions |
| **BrandBeacon.ai** | ChatGPT, Perplexity | Competitor benchmarking |
| **Sight AI** | ChatGPT, Claude, Perplexity | Sentiment analysis |

### Key Metrics to Track

1. **Citation frequency:** How often your content is cited
2. **Brand mentions:** Unprompted mentions in AI responses
3. **Referral traffic:** Visits from AI search click-throughs
4. **Share of voice:** Your visibility vs competitors
5. **Sentiment:** Positive/negative context of mentions

### Manual Testing Protocol

```markdown
## Monthly AI Visibility Audit

### Test Queries (adapt to your niche)
1. "What is [your product/service]?"
2. "Best [your category] in [year]"
3. "[Your brand] vs [competitor]"
4. "How to [task your product solves]"
5. "[Your expertise area] best practices"

### Platforms to Test
- [ ] ChatGPT (chat.openai.com)
- [ ] Perplexity (perplexity.ai)
- [ ] Google (check for AI Overviews)
- [ ] Microsoft Copilot (copilot.microsoft.com)
- [ ] Claude (claude.ai)

### Record for Each Query
- Were you cited? (Yes/No)
- Citation context (positive/neutral/negative)
- Competitors mentioned
- Information accuracy
- Suggested improvements
```

## 10. AI Search Optimization Checklist

### Content Structure
- [ ] Clear H1 with primary topic/question
- [ ] Logical heading hierarchy (H1 > H2 > H3)
- [ ] Direct answer in first 1-2 sentences
- [ ] Bullet points and numbered lists
- [ ] Comparison tables where applicable
- [ ] Definition lists for terminology

### Technical Implementation
- [ ] Semantic HTML5 elements (article, section, aside)
- [ ] FAQPage schema on Q&A content
- [ ] HowTo schema on instructional content
- [ ] Article schema with author info
- [ ] Organization schema on about pages
- [ ] robots.txt allows AI crawlers
- [ ] XML sitemap updated and submitted

### Authority Signals
- [ ] Detailed author bios with credentials
- [ ] Links to author social profiles
- [ ] Citations to authoritative sources
- [ ] Visible publication and update dates
- [ ] HTTPS enabled
- [ ] Contact information accessible
- [ ] Privacy policy present

### Content Quality
- [ ] Original, expert-level content
- [ ] Factual claims supported by sources
- [ ] Regular updates (at least monthly)
- [ ] Addresses conversational queries
- [ ] Includes relevant images with alt text
- [ ] Mobile-responsive design

### Monitoring
- [ ] AI visibility monitoring tool configured
- [ ] Monthly manual query testing
- [ ] Competitor citation tracking
- [ ] Referral traffic analysis
- [ ] Content refresh schedule maintained

## 11. Platform-Specific Optimization

### Google AI Overviews

- Pages with schema are up to 40% more likely to appear in AI Overviews
- Focus on featured snippet optimization (still relevant)
- Emphasize E-E-A-T signals
- Target informational and comparison queries

### Perplexity AI

- **Freshness is critical** - update content every 2-3 days for trending topics
- Real-time citations from current sources
- Prefer authoritative domains
- Include unique images and data

### ChatGPT Search

- Web browsing uses GPTBot and ChatGPT-User
- Emphasizes recent, authoritative content
- Good at following citations and references
- Benefits from clear, structured content

### Microsoft Copilot

- Built on Bing index
- Strong integration with Microsoft ecosystem
- Emphasizes factual, well-sourced content
- Benefits from Bing Webmaster Tools optimization

## 12. Future-Proofing Your AI Search Strategy

### Emerging Trends

1. **Multimodal search:** AI understanding images, video, audio
2. **Conversational commerce:** AI-driven purchase decisions
3. **Personalized AI responses:** Context-aware answer customization
4. **Agent-based search:** AI agents completing tasks autonomously
5. **Real-time fact-checking:** AI validating claims before citation

### Adaptation Strategy

```markdown
## Quarterly Review Checklist

### AI Platform Updates
- [ ] Review new AI search features from major platforms
- [ ] Update robots.txt for new AI bot user agents
- [ ] Test visibility on new/emerging AI platforms

### Content Strategy
- [ ] Analyze which content types get most citations
- [ ] Identify gaps in AI coverage vs competitors
- [ ] Plan new content for underserved queries

### Technical Updates
- [ ] Review schema.org for new relevant types
- [ ] Update structured data implementation
- [ ] Test page speed and Core Web Vitals
```

---

## 13. TYPO3 Implementation Guide

> **Compatibility:** TYPO3 v13.x and v14.x (v14 preferred)
> All configurations in this section work on both v13 and v14.

This section covers TYPO3-specific implementation of AEO/GEO strategies using TYPO3 extensions, configuration, and best practices.

### Installation Mode: Composer vs Classic

> **⚠️ Composer Mode Highly Recommended**
>
> For AI search optimization, **Composer-based TYPO3 installations are strongly recommended**.
> All extensions in this guide are available via both Composer (Packagist) and TER (Classic Mode).

#### Why Composer Mode is Essential for Modern TYPO3

| Aspect | Composer Mode | Classic Mode |
|--------|---------------|--------------|
| **Dependency Resolution** | Automatic with version constraints | Manual, no transitive dependencies |
| **Autoloading** | PSR-4 optimized, production-ready | TYPO3 internal, less optimized |
| **Security** | Separate web root (`/public`) | All files in web root |
| **Updates** | Single command: `composer update` | Manual download/upload per extension |
| **Reproducibility** | `composer.lock` ensures identical installs | No version locking mechanism |
| **TYPO3 v14 Future** | Fully supported | Requires `composer.json` in all extensions |

#### Technical Explanation

**Composer Mode** uses PHP's standard dependency manager to:

1. **Resolve Dependencies Automatically**: Extensions like `brotkrueml/schema` depend on `psr/http-message` and other packages. Composer resolves the entire dependency tree, ensuring compatible versions are installed.

2. **Generate Optimized Autoloaders**: Composer creates a PSR-4 compliant autoloader that loads classes on-demand, improving performance compared to TYPO3's legacy class loading.

3. **Enforce Version Constraints**: The `composer.json` constraint `"typo3/cms-core": "^13.4 || ^14.0"` guarantees only compatible versions are installed.

4. **Enable Security Isolation**: The recommended structure places `vendor/`, `config/`, and other sensitive directories outside the web-accessible `/public` folder.

5. **Support Modern Workflows**: CI/CD pipelines, automated testing, and deployment tools expect Composer-based projects.

**TYPO3 v14 Breaking Change**: In TYPO3 v14, even Classic Mode requires every extension to have a valid `composer.json` with proper `type` and `extension-key` definitions. Extensions without this file will not be detected.

```json
// Required composer.json structure for all extensions (v14+)
{
    "name": "vendor/extension-key",
    "type": "typo3-cms-extension",
    "extra": {
        "typo3/cms": {
            "extension-key": "extension_key"
        }
    }
}
```

### Extension Compatibility Matrix

| Extension | TYPO3 v13 | TYPO3 v14 | PHP | Composer | TER | Purpose |
|-----------|-----------|-----------|-----|----------|-----|---------|
| `typo3/cms-seo` | ✓ | ✓ | 8.2+ | ✓ | ✓ | Core SEO (meta tags, sitemaps, canonicals) |
| `brotkrueml/schema` | ✓ (v4.x) | ✓ (v4.x) | 8.2+ | ✓ | ✓ | Schema.org structured data (JSON-LD) |
| `yoast-seo-for-typo3/yoast_seo` | ✓ | ✗ | 8.1+ | ✓ | ✓ | Content analysis, readability (v13 only) |
| `clickstorm/cs_seo` | ✓ (v9.3+) | ✓ (v9.3+) | 8.2+ | ✓ | ✓ | Extended SEO features, evaluations |

### 13.1 Required Extensions Installation

#### Composer Mode (Recommended)

```bash
# Core SEO extension (meta tags, sitemaps, canonicals)
ddev composer require typo3/cms-seo

# Schema.org structured data (essential for AI search)
# Version constraint ensures v13/v14 compatibility
ddev composer require brotkrueml/schema:"^4.2"

# Optional: Extended SEO features (v13/v14 compatible)
ddev composer require clickstorm/cs_seo:"^9.3"

# In Composer mode, extensions are auto-activated
# Verify installation:
ddev typo3 extension:list | grep -E "seo|schema"
```

**Version Constraints Explained:**

```json
{
    "require": {
        "typo3/cms-seo": "^13.4 || ^14.0",
        "brotkrueml/schema": "^4.2"
    }
}
```

- `^4.2` = Any version ≥4.2.0 and <5.0.0 (allows minor/patch updates)
- `^13.4 || ^14.0` = Supports both TYPO3 v13.4+ and v14.0+

#### Classic Mode (TER)

> **Note:** Classic Mode is supported but not recommended. TYPO3 v14 requires
> all extensions to have a valid `composer.json` even in Classic Mode.

1. **Download from TER:**
   - https://extensions.typo3.org/extension/seo
   - https://extensions.typo3.org/extension/schema

2. **Install via Extension Manager:**
   - Backend → Admin Tools → Extensions
   - Click "Upload Extension" or use "Get Extensions" to search TER
   - Activate each extension after upload

3. **Verify Installation:**
   - Check Admin Tools → Extensions for active status
   - Clear all caches after activation

### 13.2 Robots.txt Configuration for AI Bots

Configure robots.txt via TYPO3's static routes to allow AI crawlers:

```yaml
# config/sites/main/config.yaml
routes:
  - route: robots.txt
    type: staticText
    content: |
      # Standard search engines
      User-agent: Googlebot
      Allow: /
      
      User-agent: Bingbot
      Allow: /
      
      # OpenAI (ChatGPT)
      User-agent: GPTBot
      Allow: /
      
      User-agent: ChatGPT-User
      Allow: /
      
      # Perplexity AI
      User-agent: PerplexityBot
      Allow: /
      
      # Anthropic (Claude)
      User-agent: ClaudeBot
      Allow: /
      
      User-agent: anthropic-ai
      Allow: /
      
      # Google AI (Gemini)
      User-agent: Google-Extended
      Allow: /
      
      # Meta AI
      User-agent: FacebookBot
      Allow: /
      
      # Common Crawl (used by many AI systems)
      User-agent: CCBot
      Allow: /
      
      # Default
      User-agent: *
      Allow: /
      Disallow: /typo3/
      Disallow: /typo3conf/
      Disallow: /typo3temp/
      
      Sitemap: https://example.com/sitemap.xml
```

### 13.3 Schema.org Implementation with EXT:schema

#### Installation and Setup

```bash
ddev composer require brotkrueml/schema:"^4.2"
ddev typo3 extension:activate schema
```

Include the static TypoScript template in your site package.

#### FAQPage Schema via Fluid ViewHelper

```html
{namespace schema=Brotkrueml\Schema\ViewHelpers}

<schema:type.fAQPage>
    <f:for each="{faqItems}" as="faq">
        <schema:type.question -as="mainEntity" name="{faq.question}">
            <schema:type.answer -as="acceptedAnswer" text="{faq.answer}" />
        </schema:type.question>
    </f:for>
</schema:type.fAQPage>
```

#### Article Schema via Fluid ViewHelper

```html
{namespace schema=Brotkrueml\Schema\ViewHelpers}

<schema:type.article
    -id="https://example.com/article/{article.uid}"
    headline="{article.title}"
    description="{article.teaser}"
    datePublished="{article.crdate -> f:format.date(format: 'c')}"
    dateModified="{article.tstamp -> f:format.date(format: 'c')}"
>
    <schema:type.person -as="author"
        name="{article.author.name}"
        url="{article.author.profileUrl}"
    >
        <schema:property -as="sameAs" value="{article.author.linkedIn}" />
        <schema:property -as="sameAs" value="{article.author.twitter}" />
    </schema:type.person>
    
    <schema:type.organization -as="publisher"
        name="{settings.siteName}"
        url="{settings.siteUrl}"
    >
        <schema:type.imageObject -as="logo" url="{settings.logoUrl}" />
    </schema:type.organization>
</schema:type.article>
```

#### HowTo Schema via Fluid ViewHelper

```html
{namespace schema=Brotkrueml\Schema\ViewHelpers}

<schema:type.howTo
    name="How to Optimize Content for AI Search"
    description="Step-by-step guide to improving visibility in AI-powered search engines"
>
    <f:for each="{steps}" as="step" iteration="iter">
        <schema:type.howToStep -as="step"
            name="{step.title}"
            text="{step.description}"
            position="{iter.cycle}"
        />
    </f:for>
</schema:type.howTo>
```

#### Organization Schema via PHP API (PSR-14 Event)

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\EventListener;

use Brotkrueml\Schema\Event\RenderAdditionalTypesEvent;
use Brotkrueml\Schema\Type\TypeFactory;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener(identifier: 'site-package/add-organization-schema')]
final readonly class AddOrganizationSchema
{
    public function __construct(
        private TypeFactory $typeFactory,
    ) {}

    public function __invoke(RenderAdditionalTypesEvent $event): void
    {
        $organization = $this->typeFactory->create('Organization')
            ->setProperty('name', 'Your Company Name')
            ->setProperty('url', 'https://example.com')
            ->setProperty('logo', 'https://example.com/logo.png')
            ->setProperty('description', 'Brief company description for AI understanding')
            ->setProperty('sameAs', [
                'https://www.linkedin.com/company/yourcompany',
                'https://twitter.com/yourcompany',
                'https://github.com/yourcompany',
            ]);

        $contactPoint = $this->typeFactory->create('ContactPoint')
            ->setProperty('telephone', '+43-1-234567')
            ->setProperty('contactType', 'customer service')
            ->setProperty('availableLanguage', ['German', 'English']);

        $organization->setProperty('contactPoint', $contactPoint);

        $event->addType($organization);
    }
}
```

#### Dynamic Article Schema via PSR-14 Event

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\EventListener;

use Brotkrueml\Schema\Event\RenderAdditionalTypesEvent;
use Brotkrueml\Schema\Type\TypeFactory;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener(identifier: 'site-package/add-article-schema')]
final readonly class AddArticleSchema
{
    public function __construct(
        private TypeFactory $typeFactory,
    ) {}

    public function __invoke(RenderAdditionalTypesEvent $event): void
    {
        $request = $event->getRequest();
        $pageInformation = $request->getAttribute('frontend.page.information');
        $page = $pageInformation->getPageRecord();

        // Only add Article schema for specific doktypes (e.g., 1 = standard page)
        if ((int)$page['doktype'] !== 1) {
            return;
        }

        $article = $this->typeFactory->create('Article')
            ->setProperty('headline', $page['title'])
            ->setProperty('description', $page['description'] ?: $page['abstract'])
            ->setProperty('datePublished', date('c', $page['crdate']))
            ->setProperty('dateModified', date('c', $page['tstamp']));

        // Add author if available
        if (!empty($page['author'])) {
            $author = $this->typeFactory->create('Person')
                ->setProperty('name', $page['author']);
            $article->setProperty('author', $author);
        }

        $event->addType($article);
    }
}
```

### 13.4 Content Freshness with Last Modified Headers

#### TypoScript Configuration

```typoscript
# Expose last modified date in HTTP headers
config {
    sendCacheHeaders = 1
    additionalHeaders {
        10 {
            header = X-Content-Last-Modified
            value = TEXT
            value.data = page:SYS_LASTCHANGED
            value.strftime = %Y-%m-%dT%H:%M:%S%z
        }
    }
}

# Display last updated date in content
lib.lastModified = TEXT
lib.lastModified {
    data = page:SYS_LASTCHANGED
    strftime = %B %d, %Y
    wrap = <time datetime="|" itemprop="dateModified">Last updated: |</time>
}
```

#### Fluid Template for Visible Timestamps

```html
<article itemscope itemtype="https://schema.org/Article">
    <header>
        <h1 itemprop="headline">{page.title}</h1>
        <div class="article-meta">
            <time datetime="{page.crdate -> f:format.date(format: 'c')}" itemprop="datePublished">
                Published: <f:format.date format="F j, Y">{page.crdate}</f:format.date>
            </time>
            <time datetime="{page.SYS_LASTCHANGED -> f:format.date(format: 'c')}" itemprop="dateModified">
                Last Updated: <f:format.date format="F j, Y">{page.SYS_LASTCHANGED}</f:format.date>
            </time>
        </div>
    </header>
    
    <!-- Content -->
</article>
```

### 13.5 Author Bio Schema for E-E-A-T

#### TCA Extension for Author Fields

```php
<?php
// Configuration/TCA/Overrides/pages.php

use TYPO3\CMS\Core\Utility\ExtensionManagementUtility;

$additionalColumns = [
    'tx_sitepackage_author_name' => [
        'label' => 'Author Name',
        'config' => [
            'type' => 'input',
            'size' => 50,
            'max' => 255,
        ],
    ],
    'tx_sitepackage_author_title' => [
        'label' => 'Author Title/Credentials',
        'config' => [
            'type' => 'input',
            'size' => 50,
            'max' => 255,
        ],
    ],
    'tx_sitepackage_author_bio' => [
        'label' => 'Author Bio',
        'config' => [
            'type' => 'text',
            'rows' => 5,
        ],
    ],
    'tx_sitepackage_author_linkedin' => [
        'label' => 'Author LinkedIn URL',
        'config' => [
            'type' => 'link',
            'allowedTypes' => ['url'],
        ],
    ],
];

ExtensionManagementUtility::addTCAcolumns('pages', $additionalColumns);
ExtensionManagementUtility::addToAllTCAtypes(
    'pages',
    '--div--;Author,tx_sitepackage_author_name,tx_sitepackage_author_title,tx_sitepackage_author_bio,tx_sitepackage_author_linkedin'
);
```

#### Author Schema PSR-14 Event Listener

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\EventListener;

use Brotkrueml\Schema\Event\RenderAdditionalTypesEvent;
use Brotkrueml\Schema\Type\TypeFactory;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener(identifier: 'site-package/add-author-schema')]
final readonly class AddAuthorSchema
{
    public function __construct(
        private TypeFactory $typeFactory,
    ) {}

    public function __invoke(RenderAdditionalTypesEvent $event): void
    {
        $request = $event->getRequest();
        $pageInformation = $request->getAttribute('frontend.page.information');
        $page = $pageInformation->getPageRecord();

        if (empty($page['tx_sitepackage_author_name'])) {
            return;
        }

        $author = $this->typeFactory->create('Person')
            ->setProperty('name', $page['tx_sitepackage_author_name'])
            ->setProperty('jobTitle', $page['tx_sitepackage_author_title'] ?? '')
            ->setProperty('description', $page['tx_sitepackage_author_bio'] ?? '');

        if (!empty($page['tx_sitepackage_author_linkedin'])) {
            $author->setProperty('sameAs', [$page['tx_sitepackage_author_linkedin']]);
        }

        $event->addType($author);
    }
}
```

### 13.6 FAQ Content Element with Schema

#### Content Block Definition (EXT:content_blocks)

```yaml
# ContentBlocks/ContentElements/faq-accordion/config.yaml
name: vendor/faq-accordion
typeName: faq_accordion
title: FAQ Accordion
description: FAQ with structured data for AI search
group: common

fields:
  - identifier: faq_items
    type: Collection
    labelField: question
    fields:
      - identifier: question
        type: Text
        required: true
      - identifier: answer
        type: Textarea
        enableRichtext: true
        required: true
```

#### Fluid Template with Schema

```html
<!-- ContentBlocks/ContentElements/faq-accordion/Resources/Private/Frontend.html -->
{namespace schema=Brotkrueml\Schema\ViewHelpers}

<section class="faq-accordion">
    <schema:type.fAQPage>
        <f:for each="{data.faq_items}" as="item">
            <schema:type.question -as="mainEntity" name="{item.question}">
                <schema:type.answer -as="acceptedAnswer">
                    <schema:property -as="text" value="{item.answer -> f:format.stripTags()}" />
                </schema:type.answer>
            </schema:type.question>
            
            <details class="faq-item">
                <summary class="faq-question">{item.question}</summary>
                <div class="faq-answer">
                    <f:format.html>{item.answer}</f:format.html>
                </div>
            </details>
        </f:for>
    </schema:type.fAQPage>
</section>
```

### 13.7 Breadcrumb Schema

#### Fluid ViewHelper Implementation

```html
{namespace schema=Brotkrueml\Schema\ViewHelpers}

<nav aria-label="Breadcrumb">
    <schema:type.breadcrumbList>
        <f:for each="{breadcrumbs}" as="crumb" iteration="iter">
            <schema:type.listItem -as="itemListElement" position="{iter.cycle}">
                <schema:property -as="name" value="{crumb.title}" />
                <schema:property -as="item" value="{crumb.url}" />
            </schema:type.listItem>
        </f:for>
    </schema:type.breadcrumbList>
    
    <ol class="breadcrumb">
        <f:for each="{breadcrumbs}" as="crumb" iteration="iter">
            <li class="breadcrumb-item{f:if(condition: iter.isLast, then: ' active')}">
                <f:if condition="{iter.isLast}">
                    <f:then>{crumb.title}</f:then>
                    <f:else>
                        <a href="{crumb.url}">{crumb.title}</a>
                    </f:else>
                </f:if>
            </li>
        </f:for>
    </ol>
</nav>
```

### 13.8 Semantic HTML via Fluid Layouts

```html
<!-- Resources/Private/Layouts/Default.html -->
<!DOCTYPE html>
<html lang="{siteLanguage.locale.languageCode}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <f:render section="HeaderAssets" optional="true" />
</head>
<body>
    <header role="banner">
        <f:render partial="Header" />
    </header>
    
    <nav role="navigation" aria-label="Main navigation">
        <f:render partial="Navigation/Main" />
    </nav>
    
    <main role="main">
        <article>
            <header>
                <h1>{page.title}</h1>
                <f:if condition="{page.subtitle}">
                    <p class="lead">{page.subtitle}</p>
                </f:if>
            </header>
            
            <section>
                <f:render section="Content" />
            </section>
        </article>
    </main>
    
    <aside role="complementary">
        <f:render partial="Sidebar" optional="true" />
    </aside>
    
    <footer role="contentinfo">
        <f:render partial="Footer" />
    </footer>
</body>
</html>
```

### 13.9 TYPO3 AI Search Optimization Checklist

#### Extensions & Configuration
- [ ] EXT:seo installed and configured
- [ ] EXT:schema (brotkrueml/schema ^4.2) installed
- [ ] Static TypoScript templates included
- [ ] robots.txt configured via site config with AI bot rules

#### Schema Implementation
- [ ] Organization schema on all pages
- [ ] Article schema on content pages
- [ ] FAQPage schema on FAQ content
- [ ] HowTo schema on tutorial content
- [ ] BreadcrumbList on all pages
- [ ] Author/Person schema with credentials

#### Content Structure
- [ ] Semantic HTML5 elements in Fluid templates
- [ ] Proper heading hierarchy (single H1)
- [ ] Visible publication and update dates
- [ ] Author bios with credentials
- [ ] Alt text on all images via FAL

#### Technical
- [ ] SYS_LASTCHANGED used for content freshness
- [ ] Cache headers configured
- [ ] XML sitemap via EXT:seo
- [ ] Canonical URLs configured
- [ ] hreflang for multi-language sites

### 13.10 Debugging Schema Output

#### Admin Panel Integration

EXT:schema integrates with TYPO3's Admin Panel. Enable it to see generated JSON-LD:

```typoscript
# config/system/settings.php
$GLOBALS['TYPO3_CONF_VARS']['BE']['adminPanel'] = true;
```

#### Validation Tools

After implementing structured data, validate using:

1. **Schema Markup Validator**: https://validator.schema.org/
2. **Google Rich Results Test**: https://search.google.com/test/rich-results
3. **Google Search Console**: Submit and monitor structured data

#### View Generated JSON-LD

```bash
# Fetch page and extract JSON-LD
curl -s https://example.com/page | grep -o '<script type="application/ld+json">.*</script>'
```

---

## Resources & References

### Official Documentation
- [Google AI Overviews Guidelines](https://developers.google.com/search/docs/appearance/ai-overviews)
- [Schema.org Full Hierarchy](https://schema.org/docs/full.html)
- [OpenAI GPTBot Documentation](https://platform.openai.com/docs/gptbot)

### Industry Resources
- [Semrush AI Search Study](https://www.semrush.com/blog/content-optimization-ai-search-study/)
- [Ahrefs AI Impact on SEO](https://ahrefs.com/blog/ai-impact-on-seo/)

### Monitoring Tools
- [Semrush AI Visibility Checker](https://www.semrush.com/free-tools/ai-search-visibility-checker/)
- [Brand24 AI Brand Visibility](https://brand24.com/ai-brand-visibility-tool/)
- [SE Ranking AI Visibility Tracker](https://seranking.com/ai-visibility-tracker.html)

---

## Credits & Attribution

This skill synthesizes best practices from industry research by Microsoft Advertising,
Semrush, Ahrefs, and the broader SEO community's work on generative engine optimization.

**Key sources:**
- Microsoft Advertising: "From Discovery to Influence: A Guide to AEO and GEO"
- Semrush research on AI search content optimization
- Ahrefs analysis of AI impact on SEO

Created by webconsulting.at for the Claude Cursor Skills collection.
