# FAQ / Common Recipes

Continues `typo3-solr` from [full guide](full-guide.md).

## FAQ / Common Recipes

### One Table, Two Index Configs (e.g. News + Events from EXT:news)

A common pattern: EXT:news is installed once but serves two purposes -- classic news articles and an event calendar (or product announcements, press releases, etc.). You want them as **separate facet values** in search.

**Step 1: Two Index Queue configurations for the same table**

Use `additionalWhereClause` to split records by category, type field, or sysfolder PID:

```typoscript
plugin.tx_solr.index.queue {

    # Config 1: Classic news articles
    news = 1
    news {
        type = tx_news_domain_model_news
        additionalWhereClause = categories.uid IN (1,2,3)

        fields {
            title = title
            content = SOLR_CONTENT
            content.cObject = COA
            content.cObject {
                10 = TEXT
                10.field = bodytext
            }
            category_stringM = SOLR_RELATION
            category_stringM {
                localField = categories
                multiValue = 1
            }
            url = TEXT
            url {
                typolink.parameter = {$plugin.tx_news.settings.detailPid}
                typolink.additionalParams = &tx_news_pi1[controller]=News&tx_news_pi1[action]=detail&tx_news_pi1[news]={field:uid}
                typolink.additionalParams.insertData = 1
                typolink.returnLast = url
            }
            # Custom field to distinguish in facets
            newstype_stringS = TEXT
            newstype_stringS.value = News
        }
    }

    # Config 2: Events (same table, different records)
    events = 1
    events {
        type = tx_news_domain_model_news
        additionalWhereClause = categories.uid IN (4,5,6)

        fields {
            title = title
            content = SOLR_CONTENT
            content.cObject = COA
            content.cObject {
                10 = TEXT
                10.field = bodytext
            }
            category_stringM = SOLR_RELATION
            category_stringM {
                localField = categories
                multiValue = 1
            }
            # Event-specific fields
            eventdate_dateS = datetime
            eventlocation_stringS = TEXT
            eventlocation_stringS {
                field = teaser
            }
            url = TEXT
            url {
                typolink.parameter = {$plugin.tx_news.settings.detailPid}
                typolink.additionalParams = &tx_news_pi1[controller]=News&tx_news_pi1[action]=detail&tx_news_pi1[news]={field:uid}
                typolink.additionalParams.insertData = 1
                typolink.returnLast = url
            }
            newstype_stringS = TEXT
            newstype_stringS.value = Event
        }
    }
}
```

**Alternative split strategies** (use only one):

| Strategy | `additionalWhereClause` | When to use |
|----------|------------------------|-------------|
| By category | `categories.uid IN (4,5,6)` | Different category trees for news vs events |
| By sysfolder | `pid IN (50,51)` | News and events stored in separate sysfolders |
| By type field | `tx_news_domain_model_news.type = 1` | EXT:news type field distinguishes record types |
| By tag | `tags.uid = 10` | Tagged with a specific tag |

**Step 2: Facet on the custom field**

```typoscript
plugin.tx_solr.search.faceting {
    facets {
        newstype {
            label = Content Type
            field = newstype_stringS
        }
    }
}
```

This shows "News (42)" and "Event (15)" as facet options.

**Step 3: Initialize both queue configs**

In the EXT:solr backend module -> Index Queue tab, both "news" and "events" appear as separate indexing configurations. Select both and click "Queue selected content".

**How it works internally:** Each config creates its own `tx_solr_indexqueue_item` entries with `indexing_configuration = 'news'` or `indexing_configuration = 'events'`. The Scheduler worker processes both. In Solr, the documents have `type = tx_news_domain_model_news` (the table name) but differ in the `newstype_stringS` field.

> **Tip:** If you want the Solr `type` field itself to differ (e.g., `type = news` vs `type = events`), you can override it in the fields config: `type = TEXT` / `type.value = events`. Be aware this affects other type-based filtering.

### Different Detail Page URLs per Config

When news and events have separate detail pages:

```typoscript
plugin.tx_solr.index.queue.news.fields.url {
    typolink.parameter = 42
    # ...
}

plugin.tx_solr.index.queue.events.fields.url {
    typolink.parameter = 55
    # ...
}
```

### Three or More Configs from One Table

The pattern scales -- you can create as many Index Queue configs as needed for the same table. Each gets its own name, `additionalWhereClause`, field mappings, and detail page URL.
