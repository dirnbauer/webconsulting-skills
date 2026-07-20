---
name: "typo3-fractor"
description: "Automates non-PHP TYPO3 upgrade migrations with Fractor for FlexForms, TypoScript, Fluid, YAML, XLIFF translation files, Htaccess, and composer.json changes. Use when running or configuring Fractor, upgrading non-PHP TYPO3 files, migrating FlexForms or TypoScript, modernizing Fluid templates, or combining Rector and Fractor for v14 work."
compatibility: "TYPO3 14.x"
metadata:
  version: "1.2.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 Fractor Skill

> Source: https://github.com/dirnbauer/webconsulting-skills

Fractor is a generic file refactoring tool that automates non-PHP migrations for TYPO3 upgrades. It complements [Rector](https://github.com/sabbelasichon/typo3-rector) (which handles PHP) by migrating FlexForms, TypoScript, Fluid templates, YAML, XLIFF translation files, Htaccess files, and composer.json. Fractor is stable since v1.0 (July 2026); it is maintained by Simon Schaufelberger and Andreas Wolf and partly funded through TYPO3 community budgets.

**Target:** TYPO3 **v14.x** for this skill collection. Upstream Fractor sets may still be named `TYPO3_12`, `TYPO3_13`, etc. — those are historical bundle identifiers for rules you apply while moving code **toward** a v14 codebase.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

> **Safety:** Never run Fractor on production. Always run on a development environment with version control. Review and test changes before releasing.

## Fractor vs Rector

| Tool | Handles | Package |
|------|---------|---------|
| **Rector** | PHP code (classes, TCA PHP, ext_localconf, etc.) | `ssch/typo3-rector` |
| **Fractor** | Non-PHP files (FlexForms, TypoScript, Fluid, YAML, Htaccess, composer.json) | `a9f/typo3-fractor` |

Use both together for complete TYPO3 upgrades. See the `typo3-extension-upgrade` skill for the full workflow.

## 1. Installation

```bash
composer require --dev a9f/typo3-fractor
# or with DDEV:
ddev composer require --dev a9f/typo3-fractor
```

> **Important:** Like Rector, Fractor loads the project autoloader and requires a PHP version
> that can parse the installed TYPO3 packages. For TYPO3 v14 targets, run Fractor with
> PHP 8.2+. Use DDEV or a container if your local PHP is older.

> **Always run Fractor, never skip it.** Non-PHP files (FlexForms, TypoScript, Fluid) contain
> version-specific patterns that are easy to miss in manual review. Fractor rules are
> maintained by the TYPO3 community and cover edge cases.

This meta-package installs all TYPO3-specific file processors (set as of Fractor v1.0):
- `a9f/fractor` (core engine)
- `a9f/fractor-extension-installer` (automatic processor registration)
- `a9f/fractor-xml` (FlexForm/XML processing)
- `a9f/fractor-fluid` (Fluid template processing)
- `a9f/fractor-typoscript` (TypoScript/TSconfig processing)
- `a9f/fractor-yaml` (YAML processing)
- `a9f/fractor-htaccess` (Htaccess processing)
- `a9f/fractor-xliff` (XLIFF translation file processing — new in v1.0; pairs with the `typo3-translations` skill)
- `a9f/fractor-composer-json` (composer.json processing — **still not part of the meta-package**; add `composer require --dev a9f/fractor-composer-json` when you need it)

## 2. Configuration

### Quick Start

Generate a default config:

```bash
vendor/bin/typo3-fractor-init
```

### Manual Configuration

Create `fractor.php` in your project root:

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;

return FractorConfiguration::configure()
    ->withPaths([
        __DIR__ . '/packages/',
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ]);
```

### Configuration for v14

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;

return FractorConfiguration::configure()
    ->withPaths([
        __DIR__ . '/Configuration/',
        __DIR__ . '/Resources/',
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ]);
```

### Skip Rules or Files

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;
use a9f\Typo3Fractor\TYPO3v12\FlexForm\MigrateRequiredFlagFlexFormFractor;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/packages/'])
    ->withSkip([
        MigrateRequiredFlagFlexFormFractor::class,
        __DIR__ . '/packages/legacy_ext/',
        __DIR__ . '/packages/my_ext/Resources/Private/Templates/Old.html' => [
            \a9f\Typo3Fractor\TYPO3v14\Fluid\ChangeLogoutHandlingInFeLoginFractor::class,
        ],
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ]);
```

### Apply Single Rules

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\TYPO3v12\FlexForm\MigrateItemsIndexedKeysToAssociativeFractor;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/packages/'])
    ->withRules([
        MigrateItemsIndexedKeysToAssociativeFractor::class,
    ]);
```

## 3. Running Fractor

### Dry Run (Preview)

```bash
vendor/bin/fractor process --dry-run
```

### Apply Changes

```bash
vendor/bin/fractor process
```

### Useful CLI Options (since v1.0)

```bash
vendor/bin/fractor process --dry-run --no-diffs        # summary without diff output
vendor/bin/fractor process --dry-run --rules-summary   # which rules changed which files
vendor/bin/fractor process --memory-limit=2G           # raise the limit for large projects
```

> **Breaking in v1.0:** the `--quiet` CLI option was removed.

### Run Single Rule from Set

```bash
vendor/bin/fractor process --only="a9f\Typo3Fractor\TYPO3v14\TypoScript\RemoveExternalOptionFromTypoScriptFractor"
```

### With DDEV

```bash
ddev exec vendor/bin/fractor process --dry-run
ddev exec vendor/bin/fractor process
```

## 4. Available Set Lists

### Level Sets (Cumulative)

Apply all rules up to a target version:

| Set List | Includes |
|----------|----------|
| `Typo3LevelSetList::UP_TO_TYPO3_10` | Imports `UP_TO_TYPO3_9` plus `TYPO3_10` rules only (see package `config/level/up-to-typo3-10.php`) |
| `Typo3LevelSetList::UP_TO_TYPO3_11` | ... + v11 |
| `Typo3LevelSetList::UP_TO_TYPO3_12` | ... + v12 |
| `Typo3LevelSetList::UP_TO_TYPO3_13` | ... + v13 |
| `Typo3LevelSetList::UP_TO_TYPO3_14` | ... + v14 |

### Version-Specific Sets

Apply rules for a single version only:

| Set List | Description |
|----------|-------------|
| `Typo3SetList::TYPO3_12` | v12 rules only |
| `Typo3SetList::TYPO3_13` | v13 rules only |
| `Typo3SetList::TYPO3_14` | v14 rules only |

## 5. Rules by File Type and Version

### FlexForm Rules (v12)

| Rule | Migration |
|------|-----------|
| `MigrateEmailFlagToEmailTypeFlexFormFractor` | `eval=email` → `type=email` |
| `MigrateEvalIntAndDouble2ToTypeNumberFlexFormFractor` | `eval=int/double2` → `type=number` |
| `MigrateInternalTypeFolderToTypeFolderFlexFormFractor` | `internalType=folder` → `type=folder` |
| `MigrateItemsIndexedKeysToAssociativeFractor` | Indexed items → `label`/`value` keys |
| `MigrateNullFlagFlexFormFractor` | `eval=null` → `nullable=true` |
| `MigratePasswordAndSaltedPasswordToPasswordTypeFlexFormFractor` | Password eval → `type=password` |
| `MigrateRenderTypeColorpickerToTypeColorFlexFormFractor` | `renderType=colorPicker` → `type=color` |
| `MigrateRequiredFlagFlexFormFractor` | `eval=required` → `required=1` |
| `MigrateTypeNoneColsToSizeFlexFormFractor` | `cols` → `size` for type=none |
| `RemoveTceFormsDomElementFlexFormFractor` | Remove `<TCEforms>` wrapper |

### TypoScript Rules (v12)

| Rule | Migration |
|------|-----------|
| `MigrateTypoScriptLoginUserAndUsergroupConditionsFractor` | Legacy conditions → Symfony expressions |
| `MigrateDeprecatedTypoScriptConditionsFractor` | Deprecated TypoScript `[compatVersion]` / old condition syntax → supported forms |
| `RemoveConfigDisablePageExternalUrlFractor` | Remove `config.disablePageExternalUrl` |
| `RemoveConfigDoctypeSwitchFractor` | Remove `config.doctypeSwitch` |
| `RemoveConfigMetaCharsetFractor` | Remove `config.metaCharset` |
| `RemoveConfigSendCacheHeadersOnlyWhenLoginDeniedInBranchFractor` | Remove deprecated cache header config |
| `RemoveConfigSpamProtectEmailAddressesAsciiOptionFractor` | Remove `ascii` option |
| `RemoveNewContentElementWizardOptionsFractor` | Remove legacy CE wizard TSconfig |
| `RemoveWorkspaceModeOptionsFractor` | Remove workspace mode options |
| `RenameConfigXhtmlDoctypeToDoctypeFractor` | `xhtmlDoctype` → `doctype` |
| `RenameTcemainLinkHandlerMailKeyFractor` | Rename mail link handler key |
| `UseConfigArrayForTSFEPropertiesFractor` | TSFE properties → config array |

### Fluid Rules (bundle id `TYPO3_8`)

| Rule | Migration |
|------|-----------|
| `ReplaceCaseDefaultWithDefaultCaseFluidFractor` | `<f:case default="true">` → `<f:defaultCase>` (new in v1.0; applied through the cumulative level sets) |

### Fluid Rules (v12)

| Rule | Migration |
|------|-----------|
| `AbstractMessageGetSeverityFluidFractor` | Migrate severity constants in Fluid |

### TypoScript rules (bundle id `TYPO3_13`)

These rules are published under the historical set name **`Typo3SetList::TYPO3_13`** (v13-targeted rules). They still run when you apply the cumulative **`Typo3LevelSetList::UP_TO_TYPO3_14`** level set on a v14 codebase.

| Rule | Migration |
|------|-----------|
| `MigrateIncludeTypoScriptSyntaxFractor` | `<INCLUDE_TYPOSCRIPT:` → `@import` |
| `RemovePageDoktypeRecyclerFromUserTsConfigFractor` | Remove recycler doktype from TSconfig |

### TypoScript Rules (v14)

| Rule | Migration |
|------|-----------|
| `MigrateTypoScriptConditionGetTSFEFractor` | `getTSFE()` conditions → new API |
| `MigrateTypoScriptGetDataPathFractor` | getData path changes |
| `RemoveDuplicateDoktypeRestrictionConfigurationFractor` | Remove duplicate doktype restrictions |
| `RemoveExposeNonexistentUserInForgotPasswordDialogSettingInFeLoginFractor` | Remove deprecated fe_login setting |
| `RemoveExternalOptionFromTypoScriptFractor` | Remove `external` option |
| `RemoveFrontendAssetConcatenationAndCompressionFractor` | Remove asset concatenation/compression settings |
| `RemoveModWebLayoutDefLangBindingFractor` | Remove `mod.web_layout.defLangBinding` |
| `RemoveUserTSConfigAuthBeRedirectToURLFractor` | Remove `auth.BE.redirectToURL` |

### Fluid Rules (v14)

| Rule | Migration |
|------|-----------|
| `ChangeLogoutHandlingInFeLoginFractor` | Migrate fe_login logout handling |

### YAML Rules (v14)

| Rule | Migration |
|------|-----------|
| `MigrateLegacyFormTemplatesFractor` | Migrate legacy EXT:form templates |

### Htaccess Rules (v14)

| Rule | Migration |
|------|-----------|
| `RemoveUploadsFromDefaultHtaccessFractor` | Remove `/uploads/` from .htaccess |


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
