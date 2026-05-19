# 14. Best Practices

Continues `typo3-solr` from [full guide](full-guide.md).

## 14. Best Practices

### Production Checklist

- [ ] Correct configset version deployed (`ext_solr_14_0_0`)
- [ ] Solr JVM memory configured (`SOLR_JAVA_MEM=-Xms512m -Xmx1g`)
- [ ] Solr NOT publicly accessible (firewall, reverse proxy)
- [ ] Scheduler task "Index Queue Worker" running regularly
- [ ] Logging disabled in production
- [ ] Solr data volume backed up
- [ ] Solr / EXT:solr security + configset notes applied for your Solr minor (jar / `typo3lib` layout)
- [ ] Extension + **per-language** Solr connection reviewed against official EXT:solr docs for your major

### Security

- Solr must **never** be publicly accessible. Use firewall rules or bind to `127.0.0.1`
- Use a reverse proxy (nginx/Apache) with authentication if remote access is needed
- Monitor [Apache Solr security advisories](https://solr.apache.org/security.html)
- Keep Tika Server updated (EXT:tika 13.1 requires Apache Tika **3.2.3+** — verify current advisories on Apache Tika / Solr sites)

### Performance

- **Commit strategy:** Use `autoSoftCommit` (1-5 seconds) for near-real-time, `autoCommit` (15-60 seconds) for durability
- **Cache warming:** Configure `newSearcher` and `firstSearcher` events in `solrconfig.xml`
- **Segment merging:** Monitor segment count in Solr Admin, consider `optimize` during off-peak

### Multi-Site / Multi-Language

- One Solr core per language (e.g., `core_en`, `core_de`) with language-specific schema
- Each TYPO3 site configures its own Solr connection in site config YAML
- Use `siteHash` to isolate documents per site

### Environment Configuration

Use `helhum/dotenv-connector` to manage Solr credentials per environment:

- `.env` file per environment (local, staging, production) with `SOLR_HOST`, `SOLR_PORT`, etc.
- Never hardcode connection details in site config YAML committed to VCS
- Commit `.env.example` with placeholder values
