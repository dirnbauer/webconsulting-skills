# 7. Search Configuration

Continues `typo3-solr` from [full guide](full-guide.md).

## 7. Search Configuration

### Essential Settings

```typoscript
plugin.tx_solr {
    enabled = 1
    search {
        targetPage = 42
        initializeWithEmptyQuery = 1
        showResultsOfInitialEmptyQuery = 0
        trustedFields = url
        keepExistingParametersForNewSearches = 1
    }
}
```

### Faceting

```typoscript
plugin.tx_solr.search {
    faceting = 1
    faceting {
        facets {
            contentType {
                label = Content Type
                field = type
            }
            category {
                label = Category
                field = category_stringM
            }
            year {
                label = Year
                field = year_intS
                type = queryGroup
                queryGroup {
                    2026 {
                        query = [2026-01-01T00:00:00Z TO 2026-12-31T23:59:59Z]
                    }
                    2025 {
                        query = [2025-01-01T00:00:00Z TO 2025-12-31T23:59:59Z]
                    }
                    2024 {
                        query = [2024-01-01T00:00:00Z TO 2024-12-31T23:59:59Z]
                    }
                }
            }
        }
    }
}
```

**Facet / rendering modes:** `options` (default), `optionsFiltered`, `optionsPrefixGrouped`, `optionsSinglemode`, `optionsToggle`, `queryGroup`, `hierarchy`, `dateRange`, `numericRange`, `rootline`.

### Suggest / Autocomplete

```typoscript
plugin.tx_solr {
    suggest = 1
    suggest {
        numberOfSuggestions = 10
        suggestField = spell
        showTopResults = 1
        numberOfTopResults = 5
        additionalTopResultsFields = url,type
    }
}
```

The built-in suggest uses the devbridge/jQuery-Autocomplete library. For a jQuery-free approach, see [SKILL-FRONTEND.md](../SKILL-FRONTEND.md).

### Sorting, Highlighting, Spellcheck

```typoscript
plugin.tx_solr.search {
    sorting = 1
    sorting {
        defaultOrder = asc
        options {
            relevance {
                field = relevance
                label = Relevance
            }
            title {
                field = sortTitle
                label = Title
            }
            created {
                field = created
                label = Date
            }
        }
    }

    results {
        resultsHighlighting = 1
        resultsHighlighting {
            fragmentSize = 200
            wrap = <mark>|</mark>
        }
    }

    spellchecking = 1
}
```

### Route Enhancers

SEO-friendly search URLs:

```yaml
routeEnhancers:
  SolrSearch:
    type: SolrFacetMaskAndCombineEnhancer
    extensionKey: solr
    solr:
      type: Extbase
      extension: Solr
      plugin: pi_results
      routes:
        - routePath: '/search/{q}'
          _controller: 'Search::results'
          _arguments:
            q: q
```

<!-- SCREENSHOT: frontend-search-facets.png - Search results with facets -->
