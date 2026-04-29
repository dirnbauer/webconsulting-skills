---
name: typo3-translations
description: TYPO3 localization and translation-file guidance. Use this skill whenever the user asks to create, edit, audit, migrate, or validate TYPO3 labels, locallang.xlf, labels.xlf, XLIFF 1.2 or XLIFF 2.0 files, LLL references, Content Blocks labels, backend labels, English/German localizations, ICU MessageFormat strings, missing translation keys, duplicate labels, or translation cleanup.
compatibility: TYPO3 14.x
metadata:
  version: "1.1.0"
  related_skills:
    - typo3-content-blocks
    - typo3-shadcn-content-elements
    - typo3-conformance
license: MIT / CC-BY-SA-4.0
---

# TYPO3 Translations

> Source: https://github.com/dirnbauer/webconsulting-skills

Use this skill for TYPO3 translation files, localization keys, XLIFF format
choices, `LLL:` references, and editor-facing labels. Other TYPO3 skills own
their domain logic; this skill owns how strings are named, localized, validated,
and stored.

## Use Cases

- Create or update extension labels in `Resources/Private/Language/*.xlf`.
- Create or update Content Blocks labels in `ContentBlocks/**/language/*.xlf`.
- Add German or other locale files beside English source files.
- Convert generated v14-only labels to XLIFF 2.0.
- Keep TYPO3 v13-compatible projects on XLIFF 1.2.
- Localize TCA labels, backend module labels, Content Blocks wizard labels,
  field descriptions, and frontend UI labels.
- Add pluralized runtime messages with native ICU MessageFormat.
- Audit missing, duplicate, unused, or unresolved translation keys.
- Adopt TYPO3 v14 translation domains without breaking existing `LLL:EXT:`
  references.
- Debug labels that render as raw keys, English fallback, or empty strings.

## Default Workflow

1. **Inventory the translation surface.**
   - Find source files such as `Resources/Private/Language/*.xlf` and
     `ContentBlocks/**/language/*.xlf`.
   - Find consumers in PHP, TCA, YAML, TypoScript, Fluid, TSconfig, and
     Content Blocks configuration.
   - Identify the source language and target locales before editing.

2. **Choose the XLIFF format intentionally.**
   - Follow the existing project format for small edits unless the user asks for
     a migration.
   - For newly generated TYPO3 v14 Content Blocks labels, prefer XLIFF 2.0.
   - Avoid mixing XLIFF versions inside one generated label family without a
     project reason.

3. **Name keys for the editor or runtime intent.**
   - Use stable semantic keys such as `title`, `description`,
     `field.cta_text.label`, or `wizard.group.hero.label`.
   - Do not key translations by temporary copy or by visual implementation
     details.
   - Keep shared generic labels in shared language files and element-specific
     labels beside the element when the shared label would be vague.

4. **Localize, do not just mirror.**
   - Translate labels into natural product language for the target locale.
   - Preserve product names, placeholders, HTML-safe markup, and ICU placeholder
     names exactly when they are not meant to change.
   - Make titles concise and descriptions self-explanatory.

5. **Validate before finishing.**
   - Parse every changed `.xlf` as XML.
   - Check duplicate unit IDs within each file.
   - Check every `LLL:` reference resolves to a real key.
   - Check target files contain the same units as their source file unless the
     omission is intentional.

## TYPO3 API First

Use TYPO3's localization APIs instead of custom XML parsers or hand-rolled
label resolution.

### PHP

Use `LanguageServiceFactory` when you need a context-aware language service.
Do not rely on `$GLOBALS['LANG']` in frontend or CLI code; it is not reliably
available there.

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Controller;

use Psr\Http\Message\ServerRequestInterface;
use TYPO3\CMS\Core\Localization\LanguageServiceFactory;

final readonly class ExampleController
{
    public function __construct(
        private LanguageServiceFactory $languageServiceFactory,
    ) {}

    public function label(ServerRequestInterface $request): string
    {
        $languageService = $this->languageServiceFactory->createFromSiteLanguage(
            $request->getAttribute('language'),
        );

        return $languageService->sL(
            'LLL:EXT:my_extension/Resources/Private/Language/locallang.xlf:button.save',
        );
    }
}
```

For backend-only code, `$GLOBALS['LANG']` is often already initialized by the
backend bootstrap. Prefer a helper so the dependency is obvious:

```php
private function getLanguageService(): \TYPO3\CMS\Core\Localization\LanguageService
{
    return $GLOBALS['LANG'];
}
```

`sL()` returns the plain translated string. Escape it yourself before output in
a web context.

### ICU MessageFormat in PHP

Use `LanguageService::translate()` with named arguments for ICU messages. Named
arguments trigger ICU handling; positional arguments continue to behave like
classic `sprintf` placeholders.

```php
$label = $languageService->translate(
    'file_count',
    'my_extension.messages',
    ['count' => 5],
);
```

In Extbase-only code, `LocalizationUtility::translate()` is acceptable for
convenience:

```php
$label = \TYPO3\CMS\Extbase\Utility\LocalizationUtility::translate(
    'file_count',
    'MyExtension',
    ['count' => 1],
);
```

### Fluid

Use `<f:translate>` and pass named arguments for ICU strings:

```html
<f:translate key="file_count" arguments="{count: numberOfFiles}" />
<f:translate key="greeting" arguments="{name: userName, count: messageCount}" />
```

Outside an Extbase template context, use the full `LLL:EXT:` reference:

```html
<f:translate key="LLL:EXT:my_extension/Resources/Private/Language/locallang.xlf:key1" />
```

### TCA and Backend Configuration

Use complete `LLL:EXT:` paths for TCA labels and descriptions:

```php
'ctrl' => [
    'title' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_my_table',
],
'columns' => [
    'title' => [
        'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_my_table.title',
    ],
],
```

### Translation Domains

TYPO3 v14 can resolve translation domains such as `my_extension.messages:key`
in addition to traditional file references. Domain references are shorter and
can be adopted incrementally.

```php
$label = $languageService->sL('my_extension.messages:button.save');
```

Use the development commands from `EXT:lowlevel` to inspect domains:

```bash
php bin/typo3 language:domain:list
php bin/typo3 language:domain:list --extension=my_extension
php bin/typo3 language:domain:search save
```

Avoid filename conflicts such as `locallang.xlf` and `messages.xlf` containing
different labels for the same generated `messages` domain.

## XLIFF 2.0 Pattern

Use this shape for new generated TYPO3 v14 source labels:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="2.0" xmlns="urn:oasis:names:tc:xliff:document:2.0" srcLang="en">
  <file id="messages">
    <unit id="title">
      <segment>
        <source>Text &amp; Media</source>
      </segment>
    </unit>
    <unit id="description">
      <segment>
        <source>Combine editorial copy, media, and calls to action in one balanced content section.</source>
      </segment>
    </unit>
  </file>
</xliff>
```

Use this shape for approved German targets:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="2.0" xmlns="urn:oasis:names:tc:xliff:document:2.0" srcLang="en" trgLang="de">
  <file id="messages">
    <unit id="title">
      <segment state="final">
        <source>Text &amp; Media</source>
        <target>Text &amp; Media</target>
      </segment>
    </unit>
    <unit id="description">
      <segment state="final">
        <source>Combine editorial copy, media, and calls to action in one balanced content section.</source>
        <target>Kombiniert redaktionelle Texte, Medien und Handlungsaufrufe in einem ausgewogenen Inhaltsbereich.</target>
      </segment>
    </unit>
  </file>
</xliff>
```

## ICU MessageFormat

- Store ICU MessageFormat strings as normal XLIFF `source` and `target` text.
- Prefer named placeholders over positional placeholders.
- Do not translate placeholder names.
- Keep plural/select branches complete in every locale.
- Escape XML-significant characters such as `&`, `<`, and `>`.
- Use TYPO3's `translate()` API or Fluid named arguments for ICU runtime
  interpolation. `sL()` only resolves the label string.

Example:

```xml
<unit id="items.count">
  <segment>
    <source>{count, plural, one {# item} other {# items}}</source>
  </segment>
</unit>
```

German target:

```xml
<unit id="items.count">
  <segment state="final">
    <source>{count, plural, one {# item} other {# items}}</source>
    <target>{count, plural, one {# Eintrag} other {# Eintraege}}</target>
  </segment>
</unit>
```

## TYPO3 References

- Use `LLL:EXT:extension_key/Resources/Private/Language/labels.xlf:key` for
  shared labels.
- Use the Content Blocks local language file for element-specific labels.
- Register custom backend groups, field labels, and module labels with localized
  `LLL:` references. Do not expose raw machine IDs such as `hero`, `data`, or
  `team` as editor-facing labels.
- When using `ExtensionManagementUtility::addTcaSelectItemGroup()`, pass the
  visible label as an `LLL:` reference and keep the group identifier stable.

## Content Blocks Workflow

Content Blocks keeps labels beside the block, commonly in
`ContentBlocks/<Type>/<name>/language/labels.xlf`. The English `labels.xlf` is
the source file, and translations use locale prefixes such as
`de.labels.xlf`.

1. Put editor-facing `title` and `description` in the block language file.
2. Use Content Blocks key conventions for fields:
   - `title`
   - `description`
   - `<field>.label`
   - `<field>.description`
   - `<collection>.<child>.label`
3. Run the generator to see what Content Blocks expects:

   ```bash
   vendor/bin/typo3 content-blocks:language:generate vendor/block --print
   vendor/bin/typo3 content-blocks:language:generate vendor/block --extension=my_extension
   ```

4. Remember that `labels.xlf` entries take precedence over inline labels in
   `config.yaml`. If an inline YAML label appears ignored, check the XLIFF file.
5. For generated TYPO3 v14-only catalogs, convert or emit the generated labels
   as XLIFF 2.0 after the Content Blocks key list is known.

## Pitfalls And First Steps

| Problem | Common Cause | First Steps |
|---------|--------------|-------------|
| German target is ignored | XLIFF 2 segment has `state="translated"` while approved-only loading is active | Change reviewed translations to `state="reviewed"` or `state="final"`. Only relax `requireApprovedLocalizations` for a deliberate preview/debugging workflow. |
| English fallback appears | Target file is missing, has the wrong prefix, or is not next to the source file | Verify `de.locallang.xlf` or `de.labels.xlf` sits beside `locallang.xlf` or `labels.xlf` and has `trgLang="de"` for XLIFF 2.0. |
| `en.locallang.xlf` is not loaded | TYPO3 expects the unprefixed source file to be English | Rename the source to `locallang.xlf` or `labels.xlf`; do not create an `en.*.xlf` source file. |
| XLIFF 2.0 breaks an older project | TYPO3 v13 does not support XLIFF 2.x | Keep XLIFF 1.2 until the extension is v14-only and translation tools support 2.x. |
| Raw `LLL:EXT:...` appears | Wrong path, extension key, filename, or unit ID | Copy the exact path, parse the file, verify the unit ID, clear caches, and check domain/list commands if domains are used. |
| Label shows unescaped HTML | `sL()` returns raw text | Escape in the output context or keep markup out of labels unless the renderer intentionally handles it. |
| ICU plural does not interpolate | Label was fetched with `sL()` or positional arguments | Use `LanguageService::translate()` or `<f:translate arguments="{count: value}">` with named arguments. |
| Translation domain resolves the wrong file | Conflicting `locallang.xlf` and `messages.xlf` or stale `cache.l10n` | Avoid conflicting files, flush caches, then run `language:domain:list`. |
| Content Blocks label differs from YAML | `labels.xlf` has precedence over inline `config.yaml` labels | Regenerate or print labels with `content-blocks:language:generate`, then edit the XLIFF source. |
| Target file has missing labels | Source and target unit IDs drifted | Diff unit IDs from source and target, add missing units, and keep source text in target files for translator context. |
| Multiple languages in one file | XLIFF file tries to contain more than one target language | Split into one target file per language prefix, for example `de.locallang.xlf` and `fr.locallang.xlf`. |
| Multiple `<file>` elements are used | External tooling exported a multi-file XLIFF document | Split into one TYPO3 label file with exactly one `<file>` element. |

## Problem-Solving Playbooks

### A label displays as a raw key or `LLL:` string

1. Confirm the reference syntax:
   `LLL:EXT:my_extension/Resources/Private/Language/locallang.xlf:key`.
2. Confirm the extension key matches `composer.json` / TYPO3 extension key.
3. Confirm the source file exists and is readable from the installed extension.
4. Confirm the unit ID exists exactly once in the source file.
5. Parse the source and target XLIFF files as XML.
6. Flush TYPO3 caches. For domains, inspect `language:domain:list`.

### German labels are still English

1. Verify the English source is unprefixed.
2. Verify the German file is named with the same base filename and `de.` prefix.
3. Verify `trgLang="de"` for XLIFF 2.0 or `target-language="de"` for XLIFF 1.2.
4. Verify every German unit contains a `target`.
5. For XLIFF 2.0, mark reviewed translations as `state="reviewed"` or
   `state="final"`.
6. Clear caches and test in a backend/frontend language context that really is
   German.

### Add a new Content Blocks label set

1. Run `content-blocks:language:generate ... --print`.
2. Copy the generated unit IDs into the block source `labels.xlf`.
3. Rewrite raw field identifiers into editor-facing source text.
4. Add `de.labels.xlf` with matching unit IDs and German targets.
5. Keep custom labels that are not generated by Content Blocks, but place them
   after generated keys or in a clearly named shared file.
6. Parse XML and run the project's Content Blocks or unit checks.

### Add ICU pluralization

1. Write the ICU message in the source XLIFF as a normal `source` string.
2. Add all plural/select branches needed by the target language.
3. Translate the target string without changing placeholder names.
4. Fetch it with `LanguageService::translate()` and named arguments, or with
   Fluid `<f:translate arguments="{count: value}">`.
5. Test at least `0`, `1`, and multiple values.

### Migrate generated v14 labels to XLIFF 2.0

1. Confirm the extension no longer supports TYPO3 v13.
2. Confirm translation tooling can read and write XLIFF 2.x.
3. Convert source attributes to `version="2.0"`, XLIFF 2 namespace, and
   `srcLang="en"`.
4. Convert `trans-unit` entries to `unit` plus `segment`.
5. Convert target files to `trgLang="<locale>"` and approved
   `segment state="reviewed"` or `state="final"`.
6. Validate XML, compare unit IDs, then run a backend smoke test.

## Verification Commands

```bash
# XML well-formedness
find Resources ContentBlocks -name '*.xlf' -print0 2>/dev/null | xargs -0 -n1 xmllint --noout

# Find unresolved labels or raw machine-looking wizard labels
rg -n "LLL:|group:|label:|description:" Configuration ContentBlocks Resources -S

# Check XLIFF versions in a project
rg -n '<xliff version=' Resources ContentBlocks -S

# Inspect TYPO3 v14 translation domains, when EXT:lowlevel is installed
php bin/typo3 language:domain:list
```

If `xmllint` is unavailable, use the project's PHP runtime with `DOMDocument` to
parse each changed file.

## Quality Bar

- Translation files are valid XML and use one deliberate XLIFF structure per
  generated label family.
- Source and target files stay structurally aligned.
- German labels read like German editor UI, not literal English word order.
- Descriptions help editors choose the correct content element or setting.
- ICU placeholders, HTML tags, and TYPO3 `LLL:` targets remain intact.
- Runtime code uses TYPO3 APIs (`LanguageService`, `LocalizationUtility`,
  `<f:translate>`, TCA `LLL:` references), not custom label loaders.

## FAQ

**Should I use XLIFF 2.0 or 1.2?**

Use XLIFF 2.0 for new TYPO3 v14-only work. Keep XLIFF 1.2 when the extension
still supports TYPO3 v13 or when the team's translation tools cannot handle
XLIFF 2.x yet.

**Should I create `en.locallang.xlf`?**

No. The unprefixed source file is English. Add target files with locale
prefixes, for example `de.locallang.xlf`.

**Can one XLIFF file contain multiple target languages?**

No. Keep one source file and one additional file per target locale.

**Why is `state="translated"` not visible?**

TYPO3 normally loads approved translations. In XLIFF 2.x, use
`state="reviewed"` or `state="final"` for approved targets.

**When do I use `sL()` versus `translate()`?**

Use `sL()` to resolve a plain `LLL:` or domain label. Use `translate()` when
you need arguments, especially named ICU MessageFormat arguments.

**Can I use ICU MessageFormat in TYPO3 labels?**

Yes in TYPO3 14.2 and newer. Store ICU strings as regular XLIFF text and pass
named arguments through `LanguageService::translate()`, `LocalizationUtility`,
or Fluid `<f:translate>`.

**Are translation domains required?**

No. Existing `LLL:EXT:` references continue to work. Domains are a TYPO3 v14
option for shorter references and can be adopted gradually.

**Why did my Content Blocks inline label stop showing?**

Content Blocks gives `labels.xlf` precedence over inline YAML labels. Check the
block language file first.

**Are XLIFF labels for editorial content?**

No. XLIFF files are for labels and short UI messages. Editorial content is
localized through TYPO3 content and record localization.

## Official Sources

- TYPO3 Explained: Localization and XLIFF format
  https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Localization/XliffFormat.html
- TYPO3 Explained: LanguageService API
  https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Localization/LocalizationApi/LanguageService.html
- TYPO3 Explained: XLIFF API and Fluid translation usage
  https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Localization/XliffApi.html
- TYPO3 Core changelog: ICU MessageFormat support
  https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-104546-SupportICUMessageFormatForPluralForms.html
- TYPO3 Core changelog: Translation domain mapping
  https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-93334-TranslationDomainMapping.html
- TYPO3 Content Blocks: language folder and `labels.xlf`
  https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/Definition/Language/Index.html
- TYPO3 Content Blocks: language generation command
  https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/Commands/LanguageGenerate/Index.html
