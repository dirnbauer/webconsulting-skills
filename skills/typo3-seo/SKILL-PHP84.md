---
name: typo3-seo-php84
description: PHP 8.4 patterns for TYPO3 SEO services. Modern code patterns for meta tag handling and sitemap generation.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-seo
  - php-modernization
triggers:
  - seo php 8.4
  - meta tags php84
---

# TYPO3 SEO with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-seo](./SKILL.md) - Main SEO guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. Modern SEO Service Pattern

### Meta Tag Service with Property Hooks

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Seo;

final class MetaTagService
{
    public string $title {
        set (string $value) {
            // Auto-truncate to SEO-friendly length
            $this->title = mb_substr($value, 0, 60);
        }
    }

    public string $description {
        set (string $value) {
            // Truncate and clean description
            $clean = strip_tags($value);
            $this->description = mb_substr($clean, 0, 160);
        }
    }

    public array $keywords {
        get => $this->keywords;
        set (array $value) {
            // Limit keywords and lowercase
            $this->keywords = array_slice(
                array_map('strtolower', $value),
                0,
                10
            );
        }
    }
}
```

---

## 2. Sitemap Generator with Modern Patterns

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Seo;

final readonly class SitemapEntry
{
    public function __construct(
        public string $url,
        public \DateTimeImmutable $lastModified,
        public float $priority = 0.5,
        public string $changeFrequency = 'weekly',
    ) {}
}

final class SitemapGenerator
{
    /**
     * @param SitemapEntry[] $entries
     */
    public function hasHighPriorityPages(array $entries): bool
    {
        return array_any($entries, fn(SitemapEntry $e) => $e->priority > 0.8);
    }

    /**
     * @param SitemapEntry[] $entries
     */
    public function findByUrl(array $entries, string $urlPattern): ?SitemapEntry
    {
        return array_find(
            $entries,
            fn(SitemapEntry $e) => str_contains($e->url, $urlPattern)
        );
    }
}
```

---

## 3. Structured Data with Type Safety

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Seo;

final readonly class SchemaArticle
{
    public function __construct(
        public string $headline,
        public string $description,
        public \DateTimeImmutable $datePublished,
        public ?\DateTimeImmutable $dateModified = null,
        public ?string $author = null,
        public ?string $image = null,
    ) {}

    public function toJsonLd(): array
    {
        return array_filter([
            '@context' => 'https://schema.org',
            '@type' => 'Article',
            'headline' => $this->headline,
            'description' => $this->description,
            'datePublished' => $this->datePublished->format('c'),
            'dateModified' => $this->dateModified?->format('c'),
            'author' => $this->author ? ['@type' => 'Person', 'name' => $this->author] : null,
            'image' => $this->image,
        ]);
    }
}
```

---

## References

- [typo3-seo SKILL.md](./SKILL.md)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
