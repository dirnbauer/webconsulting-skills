# 5. Configset & Schema

Continues `typo3-solr` from [full guide](full-guide.md).

## 5. Configset & Schema

The configset defines how Solr processes and indexes text. EXT:solr ships configsets at `Resources/Private/Solr/configsets/ext_solr_14_0_0/`.

### Structure

```
Resources/Private/Solr/
├── configsets/
│   └── ext_solr_14_0_0/
│       └── conf/
│           ├── solrconfig.xml
│           ├── english/
│           │   └── schema.xml
│           ├── german/
│           │   └── schema.xml
│           └── ... (other languages)
└── typo3lib/                 # at Solr root level, not inside the configset
```

Each language has its own `schema.xml` with language-specific analyzers (stemmer, stop words).

### Dynamic Field Types

Use dynamic field suffixes to add custom fields without modifying the schema:

| Suffix | Type | Multi | Example |
|--------|------|-------|---------|
| `_stringS` | string (not analyzed) | No | `category_stringS` |
| `_stringM` | string (not analyzed) | Yes | `tags_stringM` |
| `_textS` | text (analyzed) | No | `description_textS` |
| `_textM` | text (analyzed) | Yes | `keywords_textM` |
| `_intS` | integer | No | `year_intS` |
| `_floatS` | float | No | `price_floatS` |
| `_dateS` | date | No | `published_dateS` |
| `_boolS` | boolean | No | `active_boolS` |

Full reference: [Dynamic Fields Appendix](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Appendix/DynamicFieldTypes.html)

### Site hash / multi-site indexing

**EXT:solr** builds a per-request **site hash** so separate TYPO3 sites do not leak each other’s Solr documents. The exact **setting names and storage** (global extension config vs site / **site-language** config) **changed across majors** — do **not** hard-code a fake `siteHashStrategy` key here. Use the [official EXT:solr documentation](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/) and your installed version’s `Configuration/SiteConfiguration` + Extension Settings UI.

If searches return no hits after a migration, compare **domain**, **site identifier**, and **language-specific Solr connection** fields against the Solr core naming your indexer uses, then **re-index**.
