# 12.7 Database-Level Debugging

Continues `typo3-solr` from [full guide](full-guide.md).

### 12.7 Database-Level Debugging

> See **12.0 Layer 6** for the complete SQL query cookbook.

Quick reference:

```sql
-- Overview: what's in the queue?
SELECT item_type, indexing_configuration,
       COUNT(*) as total,
       SUM(CASE WHEN errors != '' THEN 1 ELSE 0 END) as errors
FROM tx_solr_indexqueue_item
GROUP BY item_type, indexing_configuration;

-- What went wrong?
SELECT uid, item_type, item_uid, errors, changed, indexed
FROM tx_solr_indexqueue_item
WHERE errors != ''
LIMIT 20;

-- Event queue (delayed monitoring mode)
SELECT * FROM tx_solr_eventqueue_item
ORDER BY tstamp DESC LIMIT 20;

-- Items that need re-indexing
SELECT uid, item_type, item_uid, changed, indexed
FROM tx_solr_indexqueue_item
WHERE changed > indexed
LIMIT 20;

-- Reset errors to retry indexing
UPDATE tx_solr_indexqueue_item SET errors = '' WHERE errors != '';
```

### 12.8 Common Issues Quick Reference

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "Search is currently not available" | Solr connection misconfigured | Check site config, initialize connection |
| No results for any query | Site hash mismatch | Verify site / language Solr config vs indexed `site` field, then re-index |
| Empty Index Queue | TypoScript not loaded on root page | Include EXT:solr static templates |
| Queue items never indexed | Scheduler task not running | Create "Index Queue Worker" task |
| Items in queue with errors | Indexing failure (memory, URL) | Check `errors` column in DB |
| Facets not visible | `faceting = 0` or empty field | Enable faceting, check field has values |
| Suggest not working | `suggest = 0` or jQuery missing | Enable suggest, check JS includes |
| Wrong content in results | Field mapping incorrect | Fix TypoScript `fields` config |
| Access-restricted pages missing | `linkAccessRestrictedPages` not set | Add `config.typolinkLinkAccessRestrictedPages = 1` |
| URL generation fails for records | `detailPid` not configured | Set the correct detail page ID |
| Docker: permission denied on `/var/solr` | Volume ownership wrong | Ensure UID 8983 owns the volume |
| DDEV: port 8984 not reachable | Addon not installed or Solr down | `ddev add-on get ddev/ddev-typo3-solr && ddev restart` |
| Configset version mismatch | Wrong configset deployed | Redeploy matching `ext_solr_14_0_0` |
| Jar loading error (Solr 9.8+ config) | Solr hardened `<lib>` / configset loading (**CVE-2025-24814** class of issue) | Follow EXT:solr / Solr release notes: relocate `typo3lib/`, update Docker image (**13.0.1+** image tag), align configset with supported layout |
| Tika: connection timeout | Tika Server not running or wrong port | Check Docker container, test connection in extension settings |
| Language core missing | No core for language | Create core with matching language schema |
