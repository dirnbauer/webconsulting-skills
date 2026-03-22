# TYPO3 Fractor Appendix

## Resources

- **Fractor Repository**: https://github.com/andreaswolf/fractor
- **TYPO3 Fractor Package**: https://github.com/andreaswolf/fractor/tree/main/packages/typo3-fractor
- **Packagist**: https://packagist.org/packages/a9f/typo3-fractor
- **TYPO3 Rector** (PHP companion): https://github.com/sabbelasichon/typo3-rector
- **Related Skills**: `typo3-extension-upgrade` (full upgrade workflow), `typo3-rector` (PHP migrations)

## v14-Only Fractor Targets

> The following non-PHP migration targets are **v14-specific** and handled by Fractor `Typo3SetList::TYPO3_14` rules.

### What Fractor does **not** cover

- **TCA migrations in PHP files** such as `ctrl.searchFields`, `ctrl.is_static`, or `interface` cleanup belong to **Rector** / manual PHP edits, not Fractor.
- **PHP API migrations** such as `FlexFormService` -> `FlexFormTools` also belong to **Rector** / manual PHP refactoring.

### TypoScript Migrations **[v14 only]**

- **`config.concatenateCss` / `config.concatenateJs` removed** — remove these settings; delegate to web server or build tools.
- **`config.compressCss` / `config.compressJs` removed** — same as above.
- **`external` property removed** for asset inclusion — remove `external = 1` from TypoScript.
- **TypoScript condition `getTSFE()` removed** — use request-based conditions.

### Htaccess Migrations **[v14 only]**

- **Updated default `.htaccess` template** (#105244) — Fractor can apply the updated template.

### FlexForm / XML Migrations **[v14 only]**

- Use Fractor for **non-PHP FlexForm XML** cleanups that are backed by actual Fractor rules in the installed package.
- If the change is a **PHP class rename** or a **TCA migration**, switch to the `typo3-rector` skill instead.
