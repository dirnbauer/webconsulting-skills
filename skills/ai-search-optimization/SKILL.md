---
name: "ai-search-optimization"
description: "Optimizes content for Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO), including schema, llms.txt, AI crawler rules, conversational query targeting, and visibility measurement. Use when the user asks about AI search visibility, ChatGPT Search, Perplexity, Google AI Overviews, AI crawlers, AEO, GEO, llms.txt, or making a site easier for answer engines to cite."
metadata:
  version: "1.0.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# AI Search Optimization (AEO & GEO)

> Source: https://github.com/dirnbauer/webconsulting-skills

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


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
