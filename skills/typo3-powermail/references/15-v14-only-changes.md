# v14-Only Changes

Continues `typo3-powermail` from [full guide](full-guide.md).

## v14-Only Changes

> The following items apply when the **TYPO3 Core** in your project is **v14** (and Powermail itself supports that Core version per its `composer.json`). Until Packagist allows `typo3/cms-core:^14`, treat v14 notes as **forward-looking** for integrations and custom code audits.

### EXT:form Hooks Removed **[v14 only]**

If your **custom extension code** integrates with **Core EXT:form** (not only Powermail), note that **all EXT:form hooks are removed** in v14:
- `beforeRendering`, `afterSubmit`, `initializeFormElement`
- `beforeFormSave`, `beforeFormDelete`, `beforeFormDuplicate`, `beforeFormCreate`
- `afterBuildingFinished`, `beforeRemoveFromParentRenderable`

These are replaced by corresponding PSR-14 events (e.g., `BeforeFormIsSavedEvent`, `BeforeRenderableIsRenderedEvent`).

### AbstractFinisher Changes **[v14 only]**

`AbstractFinisher->getTypoScriptFrontendController()` is removed (#107507). Finishers needing request context must use the PSR-7 request from the form runtime instead of `$GLOBALS['TSFE']`.

### EXT:form Storage Adapters **[v14.1+ only]**

TYPO3 v14.1 introduces **Storage Adapters** for EXT:form, allowing pluggable storage backends for form definitions. This may affect how Powermail and EXT:form coexist in projects using both.

### Fluid 5.0 Template Compatibility **[v14 only]**

Powermail Fluid templates must comply with Fluid 5.0 strict typing:
- ViewHelper arguments are strictly typed (integers vs strings matter).
- No underscore-prefixed variables in Fluid templates.
- Verify custom Fluid partials and templates for type mismatches.


Source: https://github.com/dirnbauer/webconsulting-skills
