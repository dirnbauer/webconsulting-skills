# 6. Code Style Configuration

Continues `typo3-fractor` from [full guide](full-guide.md).

## 6. Code Style Configuration

### TypoScript Formatting

```php
<?php
use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\FractorTypoScript\Configuration\TypoScriptProcessorOption;
use Helmich\TypoScriptParser\Parser\Printer\PrettyPrinterConfiguration;
use Helmich\TypoScriptParser\Parser\Printer\PrettyPrinterConditionTermination;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/Configuration/'])
    ->withOptions([
        TypoScriptProcessorOption::INDENT_SIZE => 2,
        TypoScriptProcessorOption::INDENT_CHARACTER => PrettyPrinterConfiguration::INDENTATION_STYLE_SPACES,
        TypoScriptProcessorOption::ADD_CLOSING_GLOBAL => false,
        TypoScriptProcessorOption::INCLUDE_EMPTY_LINE_BREAKS => true,
        TypoScriptProcessorOption::INDENT_CONDITIONS => true,
        TypoScriptProcessorOption::CONDITION_TERMINATION => PrettyPrinterConditionTermination::Keep,
    ]);
```

**Indent character options:**
- `PrettyPrinterConfiguration::INDENTATION_STYLE_SPACES` -- use spaces
- `PrettyPrinterConfiguration::INDENTATION_STYLE_TABS` -- use tabs
- `'auto'` -- detect from file and keep existing

**Condition termination options:**
- `PrettyPrinterConditionTermination::Keep` -- keep existing
- `PrettyPrinterConditionTermination::EnforceGlobal` -- always `[global]`
- `PrettyPrinterConditionTermination::EnforceEnd` -- always `[end]`

### XML/FlexForm Formatting

```php
<?php
use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\FractorXml\Configuration\XmlProcessorOption;
use a9f\Fractor\ValueObject\Indent;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/Configuration/'])
    ->withOptions([
        XmlProcessorOption::INDENT_CHARACTER => Indent::STYLE_TAB,
        XmlProcessorOption::INDENT_SIZE => 1,
    ]);
```

### File Extension Filtering

Control which file extensions each processor handles:

```php
<?php
use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\FractorFluid\Configuration\FluidProcessorOption;
use a9f\FractorTypoScript\Configuration\TypoScriptProcessorOption;
use a9f\FractorXml\Configuration\XmlProcessorOption;
use a9f\FractorYaml\Configuration\YamlProcessorOption;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/packages/'])
    ->withOptions([
        FluidProcessorOption::ALLOWED_FILE_EXTENSIONS => ['html'],
        TypoScriptProcessorOption::ALLOWED_FILE_EXTENSIONS => ['typoscript', 'tsconfig'],
        XmlProcessorOption::ALLOWED_FILE_EXTENSIONS => ['xml', 'xlf'],
        YamlProcessorOption::ALLOWED_FILE_EXTENSIONS => ['yaml', 'yml'],
    ]);
```

**Default extensions:**
- Fluid: `html`, `xml`, `txt`
- TypoScript: `typoscript`, `tsconfig`, `ts`
- XML: `xml`
- YAML: `yaml`, `yml`
