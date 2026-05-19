# 6. Structured Data (JSON-LD)

Continues `typo3-seo` from [full guide](full-guide.md).

## 6. Structured Data (JSON-LD)

### Organization Schema

```typoscript
page.headerData.200 = TEXT
page.headerData.200.value (
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "webconsulting",
    "url": "https://webconsulting.at",
    "logo": "https://webconsulting.at/logo.png",
    "sameAs": [
        "https://www.linkedin.com/company/webconsulting",
        "https://github.com/webconsulting"
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+43-1-234567",
        "contactType": "customer service"
    }
}
</script>
)
```

### Breadcrumb Schema (Dynamic)

Generate JSON-LD in PHP (or a dedicated ViewHelper / data processor) with `json_encode()`, then output the finished JSON string in Fluid. Building JSON-LD via TypoScript string concatenation is error-prone and commonly breaks quoting, commas, or escaping.

```html
<f:if condition="{breadcrumbJsonLd}">
    <script type="application/ld+json">{breadcrumbJsonLd -> f:format.raw()}</script>
</f:if>
```

`breadcrumbJsonLd` should come from PHP using `json_encode($data, JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR)`. Avoid `JSON_UNESCAPED_SLASHES` when embedding in `<script>` elements — without it, `/` is escaped as `\/`, which prevents user content containing `</script>` from prematurely closing the tag.

### Advanced Structured Data with EXT:schema

```bash
# Install schema extension for advanced structured data
ddev composer require brotkrueml/schema
```

Always verify that the chosen `brotkrueml/schema` release explicitly supports your TYPO3 core version on Packagist before documenting or installing it.

```php
<?php
// In a PSR-14 event listener
use Brotkrueml\Schema\Type\TypeFactory;
use Brotkrueml\Schema\Manager\SchemaManager;

#[AsEventListener]
final class AddSchemaListener
{
    public function __construct(
        private readonly TypeFactory $typeFactory,
        private readonly SchemaManager $schemaManager,
    ) {}

    public function __invoke(SomeEvent $event): void
    {
        $organization = $this->typeFactory->create('Organization')
            ->setProperty('name', 'My Company')
            ->setProperty('url', 'https://example.com');
        
        $this->schemaManager->addType($organization);
    }
}
```
