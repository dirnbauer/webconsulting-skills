# References

Continues `typo3-solr` from [full guide](full-guide.md).

## References

### Official Documentation

- [EXT:solr Documentation](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/)
- [EXT:tika Documentation](https://docs.typo3.org/p/apache-solr-for-typo3/tika/main/en-us/)
- [Version Matrix](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Appendix/VersionMatrix.html)
- [Dynamic Fields Reference](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Appendix/DynamicFieldTypes.html)
- [tx_solr.search Reference](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Configuration/Reference/TxSolrSearch.html)
- [tx_solr.index Reference](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Configuration/Reference/TxSolrIndex.html)
- [tx_solr.suggest Reference](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Configuration/Reference/TxSolrSuggest.html)
- [Extension Settings](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Configuration/Reference/ExtensionSettings.html)
- [PSR-14 Events](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Development/Events.html)
- [Indexing (Development)](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Development/Indexing.html)
- [Index Queue](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Backend/IndexQueue.html)
- [Facets](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Frontend/Facets.html)
- [Autosuggest](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Frontend/Autosuggest.html)
- [AJAX Results](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Frontend/Ajax.html)
- [Customize Frontend](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Frontend/Customize.html)
- [Fluid Structure](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Frontend/Structure.html)
- [Scheduler Tasks](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Backend/Scheduler.html)
- [FAQ](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/FAQ/Index.html)

### GitHub Repositories

- [EXT:solr](https://github.com/TYPO3-Solr/ext-solr)
- [EXT:tika](https://github.com/TYPO3-Solr/ext-tika)
- [TYPO3-Solr Organization](https://github.com/TYPO3-Solr)
- [main branch (14.0.x-dev)](https://github.com/TYPO3-Solr/ext-solr/tree/main)
- [Docker Images](https://hub.docker.com/r/typo3solr/ext-solr/tags)

### Apache Solr Server

- [Reference Guide](https://solr.apache.org/guide/solr/latest/)
- [Dense Vector Search](https://solr.apache.org/guide/solr/latest/query-guide/dense-vector-search.html)
- [Text to Vector (LLM Module)](https://solr.apache.org/guide/solr/latest/query-guide/text-to-vector.html)
- [Solr Modules](https://solr.apache.org/guide/solr/latest/configuration-guide/solr-modules.html)
- [Solr 9.8 module Javadoc (historical `llm` path)](https://solr.apache.org/docs/9_8_0/modules/llm/index.html) — current Reference Guide uses the **`language-models` module** and `org.apache.solr.languagemodels.*` / `solr.languagemodels.*` class names; confirm against your Solr version's docs.
- [Tutorial: Vectors](https://solr.apache.org/guide/solr/latest/getting-started/tutorial-vectors.html)

### Commercial & Hosting

- [typo3-solr.com](https://www.typo3-solr.com/)
- [Changelog EXT:solr](https://typo3-solr.com/solr-for-typo3/versions/changelog-extsolr)
- [Changelog EXT:solrfal](https://typo3-solr.com/solr-for-typo3/versions/changelog-extsolrfal)
- [hosted-solr.com](https://hosted-solr.com/en/)
- [hosted-solr.com Pricing](https://hosted-solr.com/en/pricing/)
- [dkd Enterprise Support](https://www.dkd.de/en/products/solr-enterprise-search/)
- [dkd Workshops](https://www.dkd.de/en/services/workshops/)

### DDEV

- [ddev-typo3-solr Addon](https://github.com/ddev/ddev-typo3-solr)
- [DDEV Addons Directory](https://addons.ddev.com/addons/ddev/ddev-typo3-solr)

### Mittwald

- [Solr Documentation](https://developer.mittwald.de/docs/v2/platform/databases/solr/)

### Environment Config

- [helhum/dotenv-connector](https://github.com/helhum/dotenv-connector)
- [Packagist](https://packagist.org/packages/helhum/dotenv-connector)
- [TYPO3 Environment Configuration](https://docs.typo3.org/permalink/t3coreapi:environment-configuration)

### Community

- [TYPO3 Slack #ext-solr](https://typo3.slack.com/messages/ext-solr/)
- [GitHub Issues](https://github.com/TYPO3-Solr/ext-solr/issues)
- [TYPO3 Extensions (TER)](https://extensions.typo3.org/extension/solr)

### Blogs & Tutorials

- [Sease: Neural Search](https://sease.io/2022/01/apache-solr-neural-search.html)
- [Sease: KNN Benchmark](https://sease.io/2022/01/apache-solr-neural-search-knn-benchmark.html)
- [Sease: Semantic Search Text-to-Vector](https://sease.io/2025/07/semantic-search-text-to-vector-with-apache-solr.html)
- [Sease: SeededKnnVectorQuery (Solr 10)](https://sease.io/2026/02/lexically-accelerated-vector-search-seededknnvectorquery-support-in-apache-solr-10.html)
- [LangChain4j Embedding Models](https://docs.langchain4j.dev/category/embedding-models)
