# 7. Writing Custom Rules

Continues `typo3-fractor` from [full guide](full-guide.md).

## 7. Writing Custom Rules

### Custom XML/FlexForm Rule

Extend `AbstractXmlFractor` (in package `a9f/fractor-xml`). `XmlFractor` in `a9f\FractorXml\Contract` is the interface; the abstract base provides the DOM visitor wiring.

```php
<?php
declare(strict_types=1);

namespace Vendor\MyExtension\Fractor;

use a9f\FractorXml\AbstractXmlFractor;
use DOMNode;
use Symplify\RuleDocGenerator\ValueObject\RuleDefinition;

final class MyCustomFlexFormFractor extends AbstractXmlFractor
{
    public function canHandle(\DOMNode $node): bool
    {
        return $node->nodeName === 'config'
            && $node->parentNode instanceof \DOMElement;
    }

    public function refactor(DOMNode $node): DOMNode|int|null
    {
        // Modify the DOM node
        return $node;
    }

    public function getRuleDefinition(): RuleDefinition
    {
        return new RuleDefinition('Migrate custom FlexForm configuration', []);
    }
}
```

### Register Custom Rule

```php
<?php
// fractor.php
use a9f\Fractor\Configuration\FractorConfiguration;
use Vendor\MyExtension\Fractor\MyCustomFlexFormFractor;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/packages/'])
    ->withRules([
        MyCustomFlexFormFractor::class,
    ]);
```
