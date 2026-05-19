# v14-Only Solr Changes

Continues `typo3-solr` from [full guide](full-guide.md).

## v14-Only Solr Changes

> The following Solr-related changes are relevant when running EXT:solr on **TYPO3 v14**.

### EXT:solr v14 Compatibility **[v14 only]**

The published [Version Matrix](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Appendix/VersionMatrix.html) lists **EXT:solr 14.0** for **TYPO3 14.3**. Until that version is available as a stable Composer tag, upstream development tracks `main` (`dev-main` / `14.0.x-dev`). Re-check [Packagist](https://packagist.org/packages/apache-solr-for-typo3/solr) and [GitHub releases](https://github.com/TYPO3-Solr/ext-solr/releases) when you plan an upgrade.

### Fluid 5.0 in Search Templates **[v14 only]**

Search result templates and facet partials must comply with Fluid 5.0 strict typing:
- ViewHelper arguments are strictly typed.
- No underscore-prefixed template variables.
- Review custom result and facet templates for type mismatches.

### TypoScriptFrontendController Removal **[v14 only]**

Custom indexer or search plugins referencing `$GLOBALS['TSFE']` must migrate to request attributes. This affects:
- Custom `IndexQueueInitializer` implementations
- PSR-14 event listeners for `AfterSearchHasBeenExecutedEvent`
- Custom `ResultParser` classes

### TCA `searchFields` Migration **[v14 only]**

If your custom record TCA uses `ctrl.searchFields` for Solr indexing configuration, note that `searchFields` is removed from `ctrl` in v14. Use per-column `'searchable' => true` instead. This does not directly affect Solr Index Queue configuration (which uses its own field mapping), but may affect backend search behavior.
