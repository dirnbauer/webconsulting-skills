# 8. Fluid Templates & Frontend

Continues `typo3-solr` from [full guide](full-guide.md).

## 8. Fluid Templates & Frontend

### Template Paths

```typoscript
plugin.tx_solr {
    view {
        templateRootPaths.10 = EXT:my_ext/Resources/Private/Templates/Solr/
        partialRootPaths.10 = EXT:my_ext/Resources/Private/Partials/Solr/
        layoutRootPaths.10 = EXT:my_ext/Resources/Private/Layouts/Solr/
    }
}
```

### Key Templates

| Template | Purpose |
|----------|---------|
| `Templates/Search/Results.html` | Main search results page |
| `Templates/Search/Form.html` | Search form |
| `Partials/Result/Document.html` | Single result item |
| `Partials/Facets/Options.html` | Standard options facet rendering |
| `Partials/Facets/OptionsFiltered.html` | Options facet with active filtering state |
| `Partials/Facets/OptionsPrefixGrouped.html` | Prefix-grouped options rendering |
| `Partials/Facets/OptionsSinglemode.html` | Single-select options rendering |
| `Partials/Facets/OptionsToggle.html` | Toggle-style options rendering |
| `Partials/Facets/Hierarchy.html` | Hierarchy facet |
| `Partials/Facets/RangeDate.html` | Date range facet |
| `Partials/Facets/RangeNumeric.html` | Numeric range facet |
| `Partials/Facets/Rootline.html` | Rootline facet |
| `Partials/Facets/Default.html` | Default / fallback rendering (including queryGroup fallback) |

Copy default templates from EXT:solr to your extension path and modify them.
