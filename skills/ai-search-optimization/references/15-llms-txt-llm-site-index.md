# 15. llms.txt - LLM Site Index

Continues `ai-search-optimization` from [full guide](full-guide.md).

## 15. llms.txt - LLM Site Index

The `llms.txt` standard provides a structured, machine-readable file to help LLMs understand and navigate your website content efficiently.

> **Note:** As of late 2025, adoption by major AI companies is still limited, but implementing
> llms.txt is low-effort and future-proofs your site for AI discovery.

### 15.1 What is llms.txt?

Similar to `robots.txt` for crawlers, `llms.txt` is a Markdown file at your site root that:

- Provides a **concise index** of key documentation/pages
- Includes **descriptions** to help LLMs understand content purpose
- Enables AI tools to **find relevant content** without parsing your entire site
- Supports an optional **llms-full.txt** with complete documentation

### 15.2 Basic llms.txt Format

```markdown
# Your Company Name

> Brief one-sentence description of your site/product.

Additional context about the site, target audience, and how to use this index.

## Documentation

- [Getting Started](/docs/getting-started): Quick introduction for new users
- [API Reference](/docs/api): Complete API documentation with examples
- [Configuration Guide](/docs/configuration): Setup and configuration options

## Tutorials

- [Building Your First App](/tutorials/first-app): Step-by-step beginner guide
- [Advanced Patterns](/tutorials/advanced): In-depth exploration of features

## Optional

- [About Us](/about): Company background and team
- [Blog](/blog): Latest news and articles
- [Changelog](/changelog): Version history and updates
```

**Key rules:**
- Single H1 (`#`) with site/project name
- Blockquote (`>`) with brief description
- H2 sections (`##`) for content groups
- Links formatted as `[Title](URL): Description`
- `## Optional` section for content LLMs can skip

### 15.3 llms-full.txt - Complete Documentation

For sites with extensive documentation, provide a `llms-full.txt` containing your entire documentation in a single Markdown file:

```markdown
# Your Company Documentation

> Complete documentation for Your Company's platform.

---

## Getting Started

[Full content of getting started page...]

---

## API Reference

### Authentication

[Full API auth documentation...]

### Endpoints

[Full API endpoints documentation...]

---

## Configuration

[Full configuration documentation...]
```

**Use cases:**
- AI coding assistants need full API context
- Complex integrations require complete documentation
- Technical support AI needs comprehensive knowledge base

### 15.4 TYPO3 Implementation

TYPO3 has a dedicated extension for llms.txt generation:

```bash
# Install the extension (TYPO3 v14 — verify Packagist)
ddev composer require web-vision/ai-llms-txt
```

#### Site Configuration

```yaml
# config/sites/main/config.yaml
imports:
  - resource: 'EXT:ai_llms_txt/Configuration/Routes/RouterEnhancer.yaml'
```

#### TypoScript Configuration

```typoscript
# Include extension TypoScript
@import 'EXT:ai_llms_txt/Configuration/TypoScript/setup.typoscript'

# Custom configuration
plugin.tx_aillmstxt {
    settings {
        # Pages to include (comma-separated UIDs or "auto")
        includePages = auto
        
        # Exclude specific pages
        excludePages = 1,2,3
        
        # Include page types
        includeDoktypes = 1,4
        
        # Maximum depth
        maxDepth = 3
    }
}
```

#### Manual llms.txt via Static Route

For full control, create a static route:

```yaml
# config/sites/main/config.yaml
routes:
  - route: llms.txt
    type: staticText
    content: |
      # Your TYPO3 Site
      
      > Enterprise content management and digital experience platform.
      
      ## Main Sections
      
      - [Home](https://example.com/): Main landing page
      - [Products](https://example.com/products): Our product catalog
      - [Documentation](https://example.com/docs): Technical documentation
      - [Blog](https://example.com/blog): Latest articles and news
      
      ## Optional
      
      - [About Us](https://example.com/about): Company information
      - [Contact](https://example.com/contact): Get in touch
```

### 15.5 Next.js Implementation

#### Static File (Simple)

```markdown
<!-- public/llms.txt -->
# Your Next.js App

> Modern web application built with Next.js.

## Pages

- [Home](/): Main landing page
- [Documentation](/docs): Technical docs
- [Blog](/blog): Latest articles
```

#### Dynamic Generation (App Router)

```typescript
// app/llms.txt/route.ts
import { getDocPages, getBlogPosts } from '@/lib/content';

export async function GET() {
  const docs = await getDocPages();
  const posts = await getBlogPosts();
  
  const content = `# Your Site Name

> Brief description of your site.

## Documentation

${docs.map(doc => `- [${doc.title}](/docs/${doc.slug}): ${doc.description}`).join('\n')}

## Blog

${posts.slice(0, 10).map(post => `- [${post.title}](/blog/${post.slug}): ${post.excerpt}`).join('\n')}

## Optional

- [About](/about): About us
- [Contact](/contact): Get in touch
`;

  return new Response(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, must-revalidate',
    },
  });
}
```

#### llms-full.txt Generation

```typescript
// app/llms-full.txt/route.ts
import { getDocPages } from '@/lib/content';
import fs from 'fs';
import path from 'path';

export async function GET() {
  const docs = await getDocPages();
  
  let fullContent = `# Complete Documentation

> Full documentation for Your Site.

`;

  for (const doc of docs) {
    const mdxPath = path.join(process.cwd(), 'content/docs', `${doc.slug}.mdx`);
    try {
      const content = fs.readFileSync(mdxPath, 'utf8');
      // Remove frontmatter
      const cleanContent = content.replace(/^---[\s\S]*?---\n/, '');
      fullContent += `---\n\n## ${doc.title}\n\n${cleanContent}\n\n`;
    } catch {
      // Skip if file not found
    }
  }

  return new Response(fullContent, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, must-revalidate',
    },
  });
}
```

### 15.6 Astro Implementation

#### Using Integration

```bash
npm install @waldheimdev/astro-ai-llms-txt
```

```javascript
// astro.config.mjs
import llmsTxt from '@waldheimdev/astro-ai-llms-txt';

export default {
  integrations: [
    llmsTxt({
      projectName: 'Your Project',
      description: 'Your project description.',
      site: 'https://your-domain.com',
    }),
  ],
};
```

#### Manual API Route

```typescript
// src/pages/llms.txt.ts
import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  const docs = await getCollection('docs');
  const blog = await getCollection('blog');
  
  const content = `# Your Astro Site

> Static site built with Astro.

## Documentation

${docs.map(doc => `- [${doc.data.title}](/docs/${doc.slug}): ${doc.data.description}`).join('\n')}

## Blog

${blog.slice(0, 10).map(post => `- [${post.data.title}](/blog/${post.slug}): ${post.data.excerpt}`).join('\n')}
`;

  return new Response(content, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
```

### 15.7 llms.txt Best Practices

| Aspect | Recommendation |
|--------|----------------|
| **File size** | Keep under 50KB for efficient parsing |
| **Descriptions** | Brief, informative (not marketing copy) |
| **Links** | Use absolute URLs for external consumption |
| **Updates** | Regenerate on content changes |
| **Sections** | Group logically (Docs, API, Tutorials, Optional) |
| **Optional section** | Mark non-essential content LLMs can skip |

### 15.8 llms.txt Checklist

- [ ] **llms.txt** at site root with structured index
- [ ] **H1 heading** with site/project name
- [ ] **Blockquote summary** describing the site
- [ ] **Organized sections** (Docs, API, Blog, Optional)
- [ ] **Link descriptions** for each URL
- [ ] **llms-full.txt** for documentation-heavy sites (optional)
- [ ] **Cache headers** set appropriately (1 hour recommended)
- [ ] **UTF-8 encoding** with text/plain content type

---
