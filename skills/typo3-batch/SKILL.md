---
name: typo3-batch
description: >-
  Orchestrate large-scale TYPO3 code changes across multiple files in parallel. Migrations,
  bulk TCA modernization, Fluid template refactoring, hook-to-event conversions, namespace
  renames, and extension-wide upgrades. Decomposes work into independent units, executes
  them, and verifies with tests. Use when working with batch, migrate, bulk, mass refactor,
  convert all, upgrade all, rename across, find and replace, parallel, codemod, TYPO3 migration.
compatibility: TYPO3 14.x
metadata:
  version: "1.0.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 Batch Operations

> Adapted from Boris Cherny's (Anthropic) Claude Code `/batch` skill for TYPO3 contexts.
> **Target:** TYPO3 v14.x only.

Orchestrate large-scale, parallelizable changes across a TYPO3 codebase. Decompose work
into 5–30 independent units, present a plan, then execute each unit with verification.

## Process

1. **Research**: Scan codebase to find all affected files
2. **Decompose**: Split work into independent, non-conflicting units
3. **Plan**: Present numbered plan to user for approval
4. **Execute**: Apply each unit, run verification after each
5. **Report**: Summarize changes, list any failures

## Execution Rules

- Each unit must be independently verifiable
- Never modify the same file in two different units
- Run `composer normalize` / `php -l` / PHPStan after PHP changes
- Run tests if available (`vendor/bin/phpunit`)
- Commit each unit separately with descriptive message
- Stop and report if a unit breaks tests

## Common TYPO3 Batch Operations

### 1. Hook → PSR-14 Event Migration

**Research**: Find all entries in `$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']` and
`$GLOBALS['TYPO3_CONF_VARS']['EXTCONF']`.

**Decompose**: One unit per hook class.

**Per unit:**

```
1. Identify the hook interface/method
2. Find the corresponding PSR-14 event (see mapping below)
3. Create new event listener class with #[AsEventListener]
4. Move logic from hook method to __invoke()
5. Remove hook registration from ext_localconf.php
6. If **not** using `#[AsEventListener]`: register the listener in `Services.yaml`. With the attribute and `autoconfigure: true` (default), no extra `tags:` entry is required.
7. Run php -l on new file
```

**Hook → event mapping (verify in [Core event lists](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/Events/Index.html)):**

> **DataHandler (`t3lib/class.t3lib_tcemain.php`):** TYPO3 Core does **not** expose generic PSR-14 events named like `BeforeRecordOperationEvent` / `AfterRecordOperationEvent` under `TYPO3\CMS\Core\DataHandling\Event`. For datamap/cmdmap reactions, use **`SC_OPTIONS` hook classes** (see [typo3-datahandler](../typo3-datahandler/SKILL.md) §9). Do not “migrate” those hooks to non-existent events.

| Hook / legacy API | Typical direction |
|---|---|
| `processDatamap_afterDatabaseOperations` / related `SC_OPTIONS` | Keep **`processDatamapClass`** hook methods (no 1:1 Core event) |
| `processDatamap_preProcessFieldArray` | Keep hook or narrow Core events for your table/field if documented |
| `processCmdmap_postProcess` | Keep **`processCmdmapClass`** hook methods |
| `drawHeaderHook` | `ModifyButtonBarEvent` |
| `drawFooterHook` | `ModifyButtonBarEvent` |
| `checkFlexFormValue` | Still often a hook; **`AfterFlexFormDataStructureParsedEvent`** is for DS parsing, not a drop-in for validation — confirm in Core for your case |
| `pageRendererRender` | `\TYPO3\CMS\Core\Page\Event\BeforeJavaScriptsRenderingEvent` (asset rendering) — confirm vs. your hook usage |
| `tslib_fe->contentPostProc` (cached) | `AfterCacheableContentIsGeneratedEvent` |
| `tslib_fe->contentPostProc` (output) | `AfterCachedPageIsPersistedEvent` — verify name in Core for your TYPO3 version |
| `tslib_fe->contentPostProc` (all) | No single PSR-14 replacement — split by what the hook actually does |
| `BackendUtility->getPagesTSconfig` | `ModifyLoadedPageTsConfigEvent` |
| `generatePageTSconfig` | `ModifyLoadedPageTsConfigEvent` |

**Not 1:1 replacements (verify before batch-rewriting):**

- **`drawHeaderHook` / `drawFooterHook`** — Legacy backend doc-header integration points. `ModifyButtonBarEvent` covers the **button bar** only; full header/footer chrome may need a different Core event or a documented alternative for your module type.
- **`tslib_fe->contentPostProc`** — Sub-hooks (`all`, `cached`, `output`) run at different FE pipeline stages. Map **cached** → `AfterCacheableContentIsGeneratedEvent`, **output** → `AfterCachedPageIsPersistedEvent` where applicable; **`all`** has no drop-in event — re-check Core docs.

### 2. TCA modernization (cumulative toward v14 target)

**Research**: Scan all `Configuration/TCA/` and `Configuration/TCA/Overrides/` files.

**Decompose**: One unit per TCA file.

**Per unit:**

```
1. Replace 'eval' => 'required' → 'required' => true
2. Replace 'eval' => 'trim' → keep where trimming is desired (trim is NOT applied by default)
3. Replace 'eval' => 'null' → 'nullable' => true
4. Replace 'eval' => 'int' → 'type' => 'number'
5. Replace 'renderType' => 'inputDateTime' → 'type' => 'datetime'
6. Replace 'renderType' => 'inputLink' → 'type' => 'link'
7. Replace 'renderType' => 'colorPicker' → 'type' => 'color'
8. Replace 'type' => 'input', 'eval' => 'email' → 'type' => 'email'
9. Convert items arrays: [0] => label, [1] => value → ['label' => ..., 'value' => ...]
10. Remove boilerplate columns auto-created from `ctrl` on TYPO3 v14: hidden, starttime, endtime, fe_group, language fields
11. Use palettes for enablecolumns: visibility → hidden, access → starttime, endtime
12. Remove convention fields from ext_tables.sql (auto-added to database)
13. Run php -l to verify syntax
```

### 3. GeneralUtility::makeInstance → DI

**Research**: Find all `GeneralUtility::makeInstance()` calls in Classes/.

**Decompose**: One unit per class file.

**Per unit:**

```
1. Identify all makeInstance calls in the class
2. For each: add constructor parameter with type
3. Replace makeInstance calls with $this->propertyName
4. Add/update Services.yaml if needed
5. Use readonly promoted properties
6. Verify with php -l
```

### 4. Fluid Template Refactoring

**Research**: Scan `Resources/Private/Templates/`, `Partials/`, `Layouts/`.

**Decompose**: One unit per template directory or logical group.

**Per unit:**

```
1. Replace hardcoded strings with <f:translate> keys
2. Add missing XLIFF entries to locallang.xlf
3. Replace <a href="..."> with <f:link.page> or <f:link.typolink>
4. Replace <img> with <f:image>
5. Extract repeated blocks to Partials
6. Add accessibility attributes (alt, aria-label, role)
```

### 5. Namespace Rename / Extension Key Change

**Research**: Find all files containing old namespace/extension key.

**Decompose**: Group by file type (PHP, Fluid, YAML, TypoScript, SQL).

**Per unit:**

```
PHP files:
  1. Replace namespace declarations
  2. Replace use statements
  3. Replace class references in strings (DI, TCA)
  
Fluid files:
  1. Replace {namespace} declarations
  2. Replace ViewHelper references
  
Configuration files:
  1. Update composer.json autoload
  2. Update ext_emconf.php
  3. Update Services.yaml service names
  4. Update TCA table prefixes
  5. Update TypoScript paths (EXT:old → EXT:new)
  
Database:
  1. Generate SQL rename migration
  2. Update ext_tables.sql
```

### 6. ext_localconf / ext_tables Cleanup

**Research**: Scan `ext_localconf.php` and `ext_tables.php` for movable code.

**Decompose**: One unit per concern (TSconfig, TypoScript, icons, modules, plugins).

**Per unit:**

```
Page TSconfig:
  1. Extract addPageTSConfig() calls
  2. Create Configuration/page.tsconfig
  3. Remove from ext_localconf.php

User TSconfig:
  1. Extract addUserTSConfig() calls  
  2. Create Configuration/user.tsconfig
  3. Remove from ext_localconf.php

Icons:
  1. Extract icon registry calls
  2. Move to Configuration/Icons.php (v14)
  3. Remove from ext_localconf.php

Backend modules:
  1. Extract registerModule() calls
  2. Move to Configuration/Backend/Modules.php
  3. Remove from ext_tables.php
```

### 7. Test Infrastructure Setup

**Research**: Check if `Tests/` directory exists, find testable classes.

**Decompose**: One unit per test type.

**Per unit:**

```
Unit tests:
  1. Create Tests/Unit/ structure
  2. Generate test class per service/utility class
  3. Add phpunit.xml.dist configuration
  
Functional tests:
  1. Create Tests/Functional/ structure
  2. Add fixture files
  3. Generate test for repository/DataHandler usage

CI pipeline:
  1. Create .github/workflows/ci.yml
  2. Configure PHP matrix (8.2, 8.3, 8.4, 8.5)
  3. Configure CI matrix (TYPO3 v14, PHP 8.2+)
```

### 8. PHP 8.4 Migration

**Research**: Scan Classes/ for PHP 8.4 migration candidates.

**Decompose**: One unit per class file.

**Per unit:**

```
1. Add property hooks where getter/setter pattern exists
2. Use asymmetric visibility (public private(set)) on DTOs
3. Replace array_search + if with array_find() **only after checking semantics** — `array_search()` returns a **key** for a given value; `array_find()` takes a **callback** and returns the first matching **value** (or null). Not drop-in replacements.
4. Replace array_filter + reset with array_find() where a callback-based “first match” is what you need
5. Replace `foreach` + conditional checks with `array_any()` / `array_all()` for value-based logic. These do **not** replace `array_key_exists()` (key-based checks).
6. Add #[\Deprecated] attribute to legacy methods
7. Run php -l to verify syntax
```

### 9. Content Blocks Migration

**Research**: Scan TCA, ext_tables.sql, and Fluid templates for classic content elements.

**Decompose**: One unit per content element / record type.

**Per unit:**

```
1. Create ContentBlocks/ContentElements/<name>/config.yaml
2. Map TCA columns to YAML fields
3. Move Fluid template to `ContentBlocks/ContentElements/<name>/templates/` (not `Source/`)
4. Align field definitions in `config.yaml` with TCA columns (no separate `EditorInterface.yaml` in Content Blocks)
5. Remove old TCA override file
6. Remove SQL from ext_tables.sql (columns become automatic)
7. Test rendering in frontend
```

### 10. Localization / XLIFF Batch

**Research**: Find all hardcoded strings in Fluid, PHP flash messages, TCA labels.

**Decompose**: One unit per language file scope (frontend, backend, TCA).

**Per unit:**

```
1. Extract strings from templates/PHP
2. Generate XLIFF keys following convention
3. Add entries to Resources/Private/Language/locallang.xlf
4. Replace hardcoded strings with LLL: references
5. Create de.locallang.xlf with German translations (if applicable)
```

## Plan Template

Present to user before executing:

```
## Batch Plan: [Description]

Target: EXT:my_extension (TYPO3 v14)
Files affected: 23
Units: 8

| # | Unit | Files | Risk |
|---|------|-------|------|
| 1 | TCA/Overrides/tt_content.php | 1 | Low |
| 2 | TCA/Overrides/pages.php | 1 | Low |
| 3 | Classes/Controller/ListController.php | 1 | Medium |
| 4 | Classes/Service/ImportService.php | 1 | Medium |
| 5 | Resources/Private/Templates/ (6 files) | 6 | Low |
| 6 | ext_localconf.php → Configuration/ | 4 | Medium |
| 7 | Tests/Unit/ (new) | 5 | Low |
| 8 | locallang.xlf updates | 3 | Low |

Estimated: ~15 minutes

Proceed? [y/n]
```

## Verification Checklist (per unit)

- [ ] `php -l` passes on all modified PHP files
- [ ] `composer normalize` passes (if composer.json touched)
- [ ] PHPStan passes (if configured)
- [ ] Unit tests pass (if available)
- [ ] Functional tests pass (if available)
- [ ] Frontend rendering unchanged (manual spot check)
- [ ] Backend forms still work (manual spot check)

## Abort Conditions

Stop the batch and report if:
- A unit breaks existing tests
- PHP syntax error in generated code
- Two units unexpectedly need the same file
- User requests stop

## v14-Only Batch Migration Targets

> The following batch migration patterns are **v14-specific**.

### Common v14 Batch Operations **[v14 only]**

| Batch Operation | What to Migrate |
|----------------|-----------------|
| Remove `$GLOBALS['TSFE']` | All PHP files referencing TypoScriptFrontendController |
| Annotations → Attributes | All `@validate`, `@ignorevalidation` in Extbase controllers |
| `MailMessage->send()` removed (#108097) → inject `TYPO3\CMS\Core\Mail\MailerInterface` and call `$this->mailer->send($email)` | All email-sending code ([Breaking #108097](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-108097-MailMessage-sendRemoved.html)) |
| `ctrl.searchFields` removed (v14) → per-field `searchable` in field `config` | See [Breaking: #106972](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-106972-TCAControlOptionSearchFieldsRemoved.html) |
| TCA `interface` removal | All TCA files with `interface` key |
| Backend module parent IDs | All `Modules.php` with `web`, `file`, `tools` parents |
| Fluid 5.0 types | All Fluid templates with incorrect ViewHelper argument types |
| FlexForm pointer fields | All FlexForm XML with pointer configurations |
| Asset `external` property | All TypoScript with `external = 1` |
| Remove legacy `switchableControllerActions` / plugin subtypes | Removed in **v12** — not a v14-only migration |

---

## Credits & Attribution

Adapted from Boris Cherny's (Anthropic) Claude Code bundled `/batch` skill for TYPO3 contexts.

**Copyright (c) Anthropic** — Batch operation patterns (MIT License)

Thanks to Netresearch DTT GmbH for their contributions to the TYPO3 community.

Source: https://github.com/dirnbauer/webconsulting-skills
