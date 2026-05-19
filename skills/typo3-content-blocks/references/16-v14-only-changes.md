# v14-Only Changes

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## v14-Only Changes

> The following changes affect Content Blocks development on **TYPO3 v14 only**.

### New TCA Type `country` **[v14 only]**

TYPO3 v14 introduces a native `country` TCA type (#99911). Content Blocks can use this for country selection fields. Check Content Blocks YAML documentation for support of this field type.

### TCA `itemsProcessors` **[v14 only]**

New `itemsProcessors` option (#107889) enables dynamic item generation for select fields. Content Blocks may expose this via YAML configuration for advanced select field customization.

### Type-Specific TCA Properties **[v14 only]**

- **Type-specific `ctrl` properties** (#108027) — `title`, `label`, and other ctrl properties can now be overridden per record type in the `types` section.
- **Type-specific TCA defaults** (#107281) — default values can differ per record type.

### Fluid 5.x / 5.3 Strict Types **[v14 only]**

Content Block Fluid templates must comply with Fluid 5.x strict typing:
- ViewHelper arguments are strictly typed. Ensure correct types (int vs string).
- Reusable components and partials should define their public API with root-level `<f:argument>` declarations.
- Union types are available for component arguments, but use them sparingly because each branch must be handled explicitly.
- No underscore-prefixed variable names (`_myVar`).
- CDATA sections are preserved (not stripped).

### Content Element Restrictions per Column **[v14.1+ only]**

TYPO3 v14.1 integrates `content_defender` functionality into Core. Backend layouts can now restrict which Content Elements (including Content Blocks) are allowed per `colPos` without third-party extensions.

---
