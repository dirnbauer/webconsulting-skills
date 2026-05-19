# 13. v14-Only Changes (Manual — Not Handled by Rector)

Continues `typo3-update` from [full guide](full-guide.md).

## 13. v14-Only Changes (Manual — Not Handled by Rector)

> The following changes apply **exclusively to TYPO3 v14** and require **manual migration**.
> They are NOT fully covered by `ssch/typo3-rector` (check your installed version; the TYPO3 14 rule set counts **tens** of rules and changes between releases).
> For automated migrations, run `Typo3LevelSetList::UP_TO_TYPO3_14` first, then address these manually.

### Fluid 5.0 Template Changes **[v14 only]**

Rector handles PHP-side ViewHelper declarations (`UseStrictTypesInFluidViewHelpersRector`), but Fluid **template** changes require manual review:

- ViewHelper arguments in `.html` templates must match strict types (e.g., `tabindex` must be int, not string).
- Fluid variable names with **underscore prefix** (`_myVar`) are disallowed — rename in all templates.
- CDATA sections in Fluid templates are **no longer removed** automatically.
- Use `{variable as type}` casting for ambiguous ViewHelper arguments.

### TypoScriptFrontendController Removed **[v14 only]**

Not covered by Rector — context-dependent migration requiring manual analysis:

- `$GLOBALS['TSFE']` and `TypoScriptFrontendController` are fully removed.
- Each usage needs different request attribute replacements:
  ```php
  // ❌ Removed in v14
  $tsfe = $GLOBALS['TSFE'];
  
  // ✅ TYPO3 v14 pattern
  $pageInformation = $request->getAttribute('frontend.page.information');
  $language = $request->getAttribute('language');
  $typoscript = $request->getAttribute('frontend.typoscript');
  ```

### Backend Module Renaming **[v14 only]**

Not a PHP migration — requires manual update to `Configuration/Backend/Modules.php`:

| Old Parent | New Parent |
|------------|------------|
| `web` | `content` |
| `file` | `media` |
| `tools` | `admin` **or** `system` (Core split tools into multiple parents — map each module to its new parent in `Configuration/Backend/Modules.php`) |

### Runtime TCA Modifications Forbidden **[v14 only]**

`$GLOBALS['TCA']` is **read-only after boot** in TYPO3 v14 — stricter than older majors. Static TCA under `Configuration/TCA/` has been the supported approach **since v12**; extensions still mutating TCA from `ext_tables.php`, middleware, or event listeners must be refactored (architectural change, not a one-line replace).

### Plugin Subtypes Removed **[v14 only]**

- **`switchableControllerActions`:** deprecated in **TYPO3 v10.3** ([#89463](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/10.3/Deprecation-89463-SwitchableControllerActions.html)) and removed later — not a v14-only topic, but legacy FlexForm/plugins may still reference it until you split plugins.
- **`list_type` subtypes / plugin list types:** further tightened in **v14** (#105538) — each variant needs its own `configurePlugin()` / registration and TypoScript/FlexForm split.

### EXT:form Hooks → PSR-14 Events **[v14 only]**

Hook-to-event migration requires manual rewrite of hook implementations:
- EXT:form hooks removed across multiple breaking changes (e.g., #107566 for `afterInitializeCurrentPage`, #107518, #107528, #107568, #107569, #107343, #107380, #107382, #107388, #98239): `beforeRendering`, `afterSubmit`, `initializeFormElement`, `beforeFormSave`, `beforeFormDelete`, `beforeFormDuplicate`, `beforeFormCreate`, `afterBuildingFinished`, `beforeRemoveFromParentRenderable`, `afterInitializeCurrentPage`.
- Replace with corresponding PSR-14 events (e.g., `BeforeFormIsSavedEvent`, `BeforeRenderableIsRenderedEvent`).

### Frontend Asset Pipeline **[v14 only]**

Rector removes PHP configuration (`RemoveConcatenateAndCompressHandlerRector`), but the **infrastructure replacement** is manual:
- CSS/JS concatenation and compression removed from TYPO3 Core entirely.
- Must configure web server compression (nginx gzip, Apache mod_deflate) or use build tools (Vite, webpack).
- TypoScript `config.concatenateCss`, `config.compressCss`, `config.concatenateJs`, `config.compressJs` must be removed (handled by Fractor, not Rector).

### New TCA Features **[v14 only]**

New features to adopt (not migrations):
- **New TCA type `country`** (#99911) for country selection fields.
- **New `itemsProcessors`** option (#107889) for dynamic item generation.
- **Type-specific `title` (and `previewRenderer`) in TCA `types`** — [Feature #108027](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108027-Type-SpecificCtrlPropertiesInTCATypes.html) (not “arbitrary ctrl copies” per type — see changelog).
- **Type-specific TCA defaults** (#107281).

### New Fluid ViewHelpers **[v14 only]**

- `<f:page.meta>` — set page meta tags from Fluid templates.
- `<f:page.title>` — set page title from Fluid templates.
- `<f:page.headerData>` / `<f:page.footerData>` — inject raw HTML into head/footer ([Feature #107056](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-107056-IntroduceHeaderDataAndFooterDataViewHelpers.html)).

### Localization System **[v14 only]**

Rector handles parser class replacement (`ReplaceLocalizationParsersWithLoaders`) and label syntax (`MigrateLabelReferenceToDomainSyntaxRector`), but these features are new:
- **XLIFF 2.x** translation files supported alongside XLIFF 1.2.
- **Translation domain mapping** (#93334) for flexible XLIFF file resolution.

### New DataHandler Features **[v14 only]**

- **`discard` command** (#107519) — discard workspace changes programmatically.
- **ISO8601 date handling improved** — qualified and unqualified ISO8601 dates supported.

### v14.1 Features **[v14.1+ only]**

Verify each item in the [official v14.1 changelog](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html) for your minor (entries change over time). Examples that have appeared in v14.1 discussions include **default theme “Camino”**, **per-column content restrictions**, **Fluid Components** tuning, and **PHP 8.5** support — confirm before documenting them for a specific project.

### v14.2 Features **[v14.2+ only]**

- **Backend search by frontend URL** — find pages by their frontend URL in page tree and live search.
- **Workspace selector moved to sidebar** with color and description.
- **Extbase identity map language-aware** — identity map now considers language when resolving objects.
- **XLIFF `xml:space` attribute** — whitespace handling respects the attribute.
- **QR Code for frontend preview** — downloadable QR codes (PNG/SVG) for frontend URLs.

### New v14 Deprecations (removed in v15) — Not Yet Handled by Rector

**v14.0 (examples):**

- `ExtensionManagementUtility::addPiFlexFormValue()` ([#107047](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Deprecation-107047-ExtensionManagementUtilityAddPiFlexFormValue.html)) — use direct FlexForm TCA.

**v14.2+ examples:**

- `ExtensionManagementUtility::addFieldsToUserSettings` (#108843) — use TCA for user settings.
- `PageRenderer->addInlineLanguageDomain()` (#108963).
- `FormEngine "additionalHiddenFields"` key (#109102).

---
