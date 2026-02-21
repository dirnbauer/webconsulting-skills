# Screenshots for typo3-solr Skill

All screenshots should be taken from TYPO3 13.4 LTS with EXT:solr 13.1 and Apache Solr 9.10.1.

## Required Screenshots

| Filename | Description | Where to capture |
|----------|-------------|------------------|
| `backend-module-overview.png` | EXT:solr backend module main view showing connection status | TYPO3 Backend > Search module > Overview tab |
| `index-queue-tab.png` | Index Queue tab showing queued items with type, count, and error status | TYPO3 Backend > Search module > Index Queue tab |
| `solr-admin-query.png` | Solr Admin UI query panel with a sample query and JSON results | Solr Admin > Core > Query (run `q=*:*&rows=5`) |
| `solr-analysis-screen.png` | Solr Analysis screen showing how text is tokenized and stemmed | Solr Admin > Core > Analysis |
| `reports-module-solr.png` | TYPO3 Reports module showing all Solr status checks (green) | TYPO3 Backend > Admin Tools > Reports > Status Report |
| `ddev-solr-admin.png` | DDEV Solr Admin UI at port 8984 showing core list | Browser: `https://<project>.ddev.site:8984/solr/` |
| `frontend-search-facets.png` | Frontend search results page with active facets and result list | Frontend: search page with facet sidebar |
| `tika-extension-settings.png` | EXT:tika extension settings showing Tika Server configuration | TYPO3 Backend > Admin Tools > Settings > Extension Configuration > tika |

## Screenshot Guidelines

- Resolution: at least 1200px wide
- Format: PNG
- Dark mode: capture in light mode for better readability
- Sensitive data: blur or replace any real credentials, domains, or personal data
- Browser chrome: crop to content area only (no browser UI)
