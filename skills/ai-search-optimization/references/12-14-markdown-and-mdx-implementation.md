# 14. Markdown & MDX Implementation

Continues `ai-search-optimization` from [full guide](full-guide.md).

## 14. Markdown & MDX Implementation

This section covers AI search optimization for static sites and documentation platforms using Markdown (MD) and MDX.

### 14.1 Frontmatter for AI Search

Use frontmatter to define structured metadata that frameworks can transform into meta tags and structured data:

```yaml
---
title: "How to Optimize Content for AI Search Engines"
description: "Complete guide to AEO and GEO strategies for ChatGPT, Perplexity, and Google AI Overviews visibility."
date: 2025-01-15
lastmod: 2025-01-15
author:
  name: "Jane Doe"
  title: "SEO Specialist"
  linkedin: "https://linkedin.com/in/janedoe"
  twitter: "https://twitter.com/janedoe"
tags: ["aeo", "geo", "ai-search", "seo"]
category: "SEO"
image: "/images/ai-search-guide.jpg"
schema:
  type: "Article"
  wordCount: 2500
draft: false
---
```

### 14.2 Content Structure Best Practices

```markdown
# Main Topic as H1 (Single, Contains Primary Question/Keyword)

Brief 2-3 sentence summary answering the main question directly.
This paragraph is what AI engines extract first.

## What is [Topic]?

Direct definition in 1-2 sentences. [Topic] is...

### Key Characteristics

- **Point 1:** Specific, factual information
- **Point 2:** Verifiable data with source
- **Point 3:** Actionable insight

## How Does [Topic] Work?

Clear process explanation.

1. First step with expected outcome
2. Second step with verification
3. Third step with result

## Why is [Topic] Important?

| Benefit | Impact | Evidence |
|---------|--------|----------|
| Benefit 1 | Measurable result | Source/study |
| Benefit 2 | Specific outcome | Data point |

## Frequently Asked Questions

<details>
<summary>Question 1?</summary>

Direct answer to question 1.

</details>

<details>
<summary>Question 2?</summary>

Direct answer to question 2.

</details>
```

### 14.3 JSON-LD in MDX (Next.js / Astro)

#### Next.js App Router

```tsx
// components/JsonLd.tsx
type JsonLdProps = {
  data: Record<string, unknown>;
};

export function JsonLd({ data }: JsonLdProps) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(data).replace(/</g, '\\u003c'),
      }}
    />
  );
}
```

```mdx
---
title: "AI Search Optimization Guide"
---

import { JsonLd } from '@/components/JsonLd';

<JsonLd data={{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "AI Search Optimization Guide",
  "author": {
    "@type": "Person",
    "name": "Jane Doe"
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-01-15"
}} />

# AI Search Optimization Guide

Content here...
```

#### Astro with astro-seo-schema

```bash
npm install schema-dts astro-seo-schema
```

```astro
---
// src/layouts/Article.astro
import { Schema } from 'astro-seo-schema';
const { frontmatter } = Astro.props;
---
<html>
<head>
  <Schema item={{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": frontmatter.title,
    "description": frontmatter.description,
    "author": {
      "@type": "Person",
      "name": frontmatter.author.name
    },
    "datePublished": frontmatter.date,
    "dateModified": frontmatter.lastmod
  }} />
</head>
<body>
  <slot />
</body>
</html>
```

### 14.4 FAQ Schema Component for MDX

```tsx
// components/FAQ.tsx
import { JsonLd } from './JsonLd';

type FAQItem = {
  question: string;
  answer: string;
};

type FAQProps = {
  items: FAQItem[];
};

export function FAQ({ items }: FAQProps) {
  const schemaData = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": items.map(item => ({
      "@type": "Question",
      "name": item.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": item.answer
      }
    }))
  };

  return (
    <>
      <JsonLd data={schemaData} />
      <section className="faq">
        {items.map((item, index) => (
          <details key={index}>
            <summary>{item.question}</summary>
            <p>{item.answer}</p>
          </details>
        ))}
      </section>
    </>
  );
}
```

```mdx
import { FAQ } from '@/components/FAQ';

## Frequently Asked Questions

<FAQ items={[
  {
    question: "What is AEO?",
    answer: "Answer Engine Optimization (AEO) is the practice of optimizing content to be cited directly in AI-generated answers."
  },
  {
    question: "How is GEO different from SEO?",
    answer: "GEO targets AI-generated search results, while traditional SEO focuses on ranking in link-based search results."
  }
]} />
```

### 14.5 Raw MDX View with URL Parameter

Enable viewing raw MDX source for transparency and AI training accessibility:

#### Next.js Implementation

```typescript
// next.config.js - Rewrite .md URLs to API
module.exports = {
  async rewrites() {
    return [
      {
        source: '/docs/:path*.md',
        destination: '/api/raw-mdx?path=:path*',
      },
    ];
  },
};
```

```typescript
// app/api/raw-mdx/route.ts
import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const filePath = searchParams.get('path');
  
  if (!filePath) {
    return NextResponse.json({ error: 'Path required' }, { status: 400 });
  }
  
  // Prevent directory traversal
  const safePath = filePath.replace(/\.\./g, '');
  const mdxPath = path.join(process.cwd(), 'content', `${safePath}.mdx`);
  
  try {
    const content = fs.readFileSync(mdxPath, 'utf8');
    return new NextResponse(content, {
      headers: { 'Content-Type': 'text/plain; charset=utf-8' },
    });
  } catch {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
}
```

**Usage:**
- `/docs/getting-started` → Rendered page
- `/docs/getting-started.md` → Raw MDX source

#### Query Parameter Alternative

```typescript
// app/docs/[...slug]/page.tsx
import { notFound } from 'next/navigation';
import fs from 'fs';
import path from 'path';

type Props = {
  params: { slug: string[] };
  searchParams: { raw?: string };
};

export default async function Page({ params, searchParams }: Props) {
  const slug = params.slug.join('/');
  const mdxPath = path.join(process.cwd(), 'content', `${slug}.mdx`);
  
  // Show raw MDX if ?raw=true
  if (searchParams.raw === 'true') {
    try {
      const rawContent = fs.readFileSync(mdxPath, 'utf8');
      return (
        <article>
          <header>
            <p className="text-sm text-gray-500">
              Raw MDX source • <a href={`/docs/${slug}`}>View rendered</a>
            </p>
          </header>
          <pre className="p-4 bg-gray-50 rounded overflow-auto">
            <code>{rawContent}</code>
          </pre>
        </article>
      );
    } catch {
      notFound();
    }
  }
  
  // Normal MDX rendering
  // ... your MDX processing
}
```

**Usage:**
- `/docs/getting-started` → Rendered page
- `/docs/getting-started?raw=true` → Raw MDX source

### 14.6 Automatic Schema Generation from Frontmatter

```typescript
// lib/generateSchema.ts
type Frontmatter = {
  title: string;
  description: string;
  date: string;
  lastmod?: string;
  author?: {
    name: string;
    title?: string;
    linkedin?: string;
    twitter?: string;
  };
  image?: string;
  schema?: {
    type?: 'Article' | 'HowTo' | 'FAQPage';
    wordCount?: number;
  };
};

export function generateSchema(frontmatter: Frontmatter, url: string) {
  const schemaType = frontmatter.schema?.type || 'Article';
  
  const baseSchema = {
    "@context": "https://schema.org",
    "@type": schemaType,
    "headline": frontmatter.title,
    "description": frontmatter.description,
    "url": url,
    "datePublished": frontmatter.date,
    "dateModified": frontmatter.lastmod || frontmatter.date,
  };
  
  if (frontmatter.author) {
    const sameAs = [
      frontmatter.author.linkedin,
      frontmatter.author.twitter,
    ].filter(Boolean);
    
    baseSchema["author"] = {
      "@type": "Person",
      "name": frontmatter.author.name,
      "jobTitle": frontmatter.author.title,
      ...(sameAs.length > 0 && { "sameAs": sameAs }),
    };
  }
  
  if (frontmatter.image) {
    baseSchema["image"] = frontmatter.image;
  }
  
  if (frontmatter.schema?.wordCount) {
    baseSchema["wordCount"] = frontmatter.schema.wordCount;
  }
  
  return baseSchema;
}
```

### 14.7 MD/MDX AI Search Checklist

- [ ] **Frontmatter:** Title, description, date, lastmod, author with credentials
- [ ] **Structure:** Single H1, logical heading hierarchy, direct answers first
- [ ] **Schema:** JSON-LD in layout or per-page (Article, FAQPage, HowTo)
- [ ] **FAQ sections:** Use `<details>/<summary>` with FAQPage schema
- [ ] **Tables:** For comparisons (AI extracts structured data)
- [ ] **Lists:** Bullet points and numbered steps
- [ ] **Last modified:** Visible and in frontmatter
- [ ] **Author bio:** Name, credentials, social links
- [ ] **Raw view:** Optional `.md` or `?raw=true` endpoint
- [ ] **Images:** Alt text, proper dimensions, WebP format
- [ ] **llms.txt:** LLM-friendly site index (see Section 15)

---
