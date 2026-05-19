# 9. PSR-14 Events Reference

Continues `typo3-solr` from [full guide](full-guide.md).

## 9. PSR-14 Events Reference

### Monitoring Events

| Event | Fired when |
|-------|-----------|
| `RecordInsertedEvent` | A monitored record is inserted |
| `RecordUpdatedEvent` | A monitored record is updated |
| `VersionSwappedEvent` | A version is swapped (workspace publish) |
| `RecordMovedEvent` | A record is moved |
| `RecordGarbageCheckEvent` | A garbage check is triggered |
| `RecordDeletedEvent` | A record is deleted |
| `PageMovedEvent` | A page is moved |
| `ContentElementDeletedEvent` | A content element is deleted |

### Data Update Processing Events

| Event | Fired when |
|-------|-----------|
| `ProcessingFinishedEvent` | Data update processing is complete |
| `DelayedProcessingQueuingFinishedEvent` | Update queued in event queue (delayed mode) |
| `DelayedProcessingFinishedEvent` | Delayed processing complete (scheduler) |

### Index Queue Events

| Event | Fired when |
|-------|-----------|
| `AfterIndexQueueHasBeenInitializedEvent` | Index queue initialization finished |
| `AfterIndexQueueItemHasBeenMarkedForReindexingEvent` | An index queue item was marked for reindexing |
| `AfterRecordsForIndexQueueItemsHaveBeenRetrievedEvent` | Records for index queue items were fetched |

### Indexing Events

The following classes exist in current EXT:solr releases; always confirm against your installed `vendor/apache-solr-for-typo3/solr/Classes/` tree.

| Event | Fired when |
|-------|-----------|
| `AfterFrontendPageUriForIndexingHasBeenGeneratedEvent` | Frontend page URI for indexing was generated |
| `AfterItemHasBeenIndexedEvent` | One item was indexed |
| `AfterItemsHaveBeenIndexedEvent` | A batch of items was indexed |
| `BeforePageDocumentIsProcessedForIndexingEvent` | Before page document is processed (add extra documents) |
| `AfterPageDocumentIsCreatedForIndexingEvent` | After page document created (replace/substitute) |
| `BeforeDocumentIsProcessedForIndexingEvent` | Before non-page record document is processed |
| `BeforeDocumentsAreIndexedEvent` | Before documents are sent to Solr (add custom fields) |
| `BeforeItemIsIndexedEvent` | Before one item is indexed |
| `BeforeItemsAreIndexedEvent` | Before a batch of items is indexed |

### Search Events

| Event | Fired when |
|-------|-----------|
| `AfterFrequentlySearchHasBeenExecutedEvent` | Frequently-searched query finished |
| `AfterInitialSearchResultSetHasBeenCreatedEvent` | Initial result set was created before later processing |
| `AfterSearchHasBeenExecutedEvent` | Search finished |
| `AfterSearchQueryHasBeenPreparedEvent` | Search query object prepared |
| `AfterSuggestQueryHasBeenPreparedEvent` | Suggest query object prepared |
| `BeforeSearchFormIsShownEvent` | Search form rendering starts |
| `BeforeSearchResultIsShownEvent` | Search result rendering starts |

### Routing Events

| Event | Fired when |
|-------|-----------|
| `BeforeVariableInCachedUrlAreReplacedEvent` | Cached URL variables are about to be substituted |
| `BeforeCachedVariablesAreProcessedEvent` | Cached URL variables are about to be processed |
| `AfterUriIsProcessedEvent` | Final search URI was processed |

### Other Events

| Event | Fired when |
|-------|-----------|
| `AfterFacetIsParsedEvent` | Facet component modification |
| `AfterSiteHashHasBeenDeterminedForSiteEvent` | Override calculated site hash |
| `AfterVariantIdWasBuiltEvent` | Variant id generation finished |

### Example: Add custom fields to documents (TYPO3 v14)

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExt\EventListener;

use ApacheSolrForTypo3\Solr\Event\Indexing\BeforeDocumentsAreIndexedEvent;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener(identifier: 'my-ext/enrich-solr-documents')]
final class EnrichSolrDocuments
{
    public function __invoke(BeforeDocumentsAreIndexedEvent $event): void
    {
        foreach ($event->getDocuments() as $document) {
            $document->addField('custom_score_floatS', $this->calculateScore($document));
        }
    }

    private function calculateScore(\ApacheSolrForTypo3\Solr\System\Solr\Document\Document $document): float
    {
        return match ($document->getField('type')['value'] ?? '') {
            'pages' => 1.0,
            'tx_news_domain_model_news' => 0.8,
            default => 0.5,
        };
    }
}
```

`#[AsEventListener]` is available in TYPO3 13+. If you prefer configuration-based registration, register the same listener in `Services.yaml`:

```yaml
MyVendor\MyExt\EventListener\EnrichSolrDocuments:
  tags:
    - name: event.listener
      identifier: 'my-ext/enrich-solr-documents'
```
