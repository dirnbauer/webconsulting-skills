# 15. Database Structure

Continues `typo3-solr` from [full guide](full-guide.md).

## 15. Database Structure

| Table | Purpose |
|-------|---------|
| `tx_solr_indexqueue_item` | Items queued for indexing (type, uid, errors, timestamps) |
| `tx_solr_indexqueue_indexing_property` | Additional indexing properties per queue item |
| `tx_solr_last_searches` | Recently executed search terms |
| `tx_solr_statistics` | Search statistics (terms, result counts, timestamps) |
| `tx_solr_eventqueue_item` | Event queue for delayed monitoring mode |

Key columns in `tx_solr_indexqueue_item`:

| Column | Type | Purpose |
|--------|------|---------|
| `item_type` | varchar | Table name (e.g., `pages`, `tx_news_domain_model_news`) |
| `item_uid` | int | Record UID |
| `indexing_configuration` | varchar | TypoScript configuration name |
| `changed` | int | Timestamp when record was last changed |
| `indexed` | int | Timestamp when record was last indexed |
| `errors` | text | Error message from last indexing attempt |
