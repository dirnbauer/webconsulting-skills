# 13. TYPO3 Implementation Guide

Continues `ai-search-optimization` from [full guide](full-guide.md).

## 13. TYPO3 Implementation Guide

> **Compatibility:** TYPO3 v14.x
> All configurations in this section work on TYPO3 v14.

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

3. **Enforce Version Constraints**: The `composer.json` constraint `"typo3/cms-core": "^14.0"` guarantees only compatible versions are installed.

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

### Extension compatibility (TYPO3 v14)

| Extension | TYPO3 v14 | PHP | Composer | TER | Purpose |
|-----------|-----------|-----|----------|-----|---------|
| `typo3/cms-seo` | ✓ | 8.2+ | ✓ | ✓ | Core SEO (meta tags, sitemaps, canonicals) |
| `brotkrueml/schema` | ✓ (verify v4.x on Packagist) | 8.2+ | ✓ | ✓ | Schema.org structured data (JSON-LD) |
| `clickstorm/cs_seo` | ✓ (verify v9.3+ on Packagist) | 8.2+ | ✓ | ✓ | Extended SEO features, evaluations |

> Other SEO extensions (e.g. Yoast) may lag Core — always check `require.typo3/cms-core` before installing.

### 13.1 Required Extensions Installation

#### Composer Mode (Recommended)

```bash
# Core SEO extension (meta tags, sitemaps, canonicals)
ddev composer require typo3/cms-seo

# Schema.org structured data (essential for AI search)
# Version constraint ensures TYPO3 v14 compatibility
ddev composer require brotkrueml/schema:"^4.2"

# Optional: Extended SEO features (TYPO3 v14)
ddev composer require clickstorm/cs_seo:"^9.3"

# In Composer mode, extensions are auto-activated
# Verify installation:
ddev typo3 extension:list | grep -E "seo|schema"
```

**Version Constraints Explained:**

```json
{
    "require": {
        "typo3/cms-seo": "^14.0",
        "brotkrueml/schema": "^4.2"
    }
}
```

- `^4.2` = Any version ≥4.2.0 and <5.0.0 (allows minor/patch updates)
- `^14.0` for `typo3/cms-seo` = TYPO3 v14 line only (this collection’s target)

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
      
      # OpenAI - model training
      User-agent: GPTBot
      Allow: /
      
      # OpenAI - ChatGPT Search index
      User-agent: OAI-SearchBot
      Allow: /
      
      # Perplexity AI - search index
      User-agent: PerplexityBot
      Allow: /
      
      # Anthropic (Claude) - model training
      User-agent: ClaudeBot
      Allow: /
      
      # Anthropic (Claude) - search indexing
      User-agent: Claude-SearchBot
      Allow: /
      
      # Google AI (Gemini training/grounding)
      User-agent: Google-Extended
      Allow: /
      
      # Meta AI training
      User-agent: Meta-ExternalAgent
      Allow: /
      
      # Apple (Siri, Spotlight, Apple Intelligence)
      User-agent: Applebot
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
ddev typo3 extension:setup -e schema
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
