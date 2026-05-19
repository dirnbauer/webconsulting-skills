# 13. Testing

Continues `typo3-solr` from [full guide](full-guide.md).

## 13. Testing

### Functional Test Setup

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExt\Tests\Functional;

use ApacheSolrForTypo3\Solr\Tests\Integration\IntegrationTestBase;

/**
 * EXT:solr ships IntegrationTestBase (see vendor path Tests/Integration/). Method names
 * differ by version — copy patterns from EXT:solr's own Tests/Integration tree.
 */
final class CustomIndexingTest extends IntegrationTestBase
{
    protected array $testExtensionsToLoad = [
        'apache-solr-for-typo3/solr',
        'my-vendor/my-ext',
    ];

    protected function setUp(): void
    {
        parent::setUp();
        $this->writeDefaultSolrTestSiteConfiguration();
    }

    public function testFollowExtSolrIntegrationPatterns(): void
    {
        $this->importCSVDataSet(__DIR__ . '/Fixtures/news_records.csv');
        // Queue + indexing: mirror EXT:solr Tests/Integration (e.g. IndexServiceTest). Helpers such as
        // assertSolrContainsDocumentCount() exist on IntegrationTestBase once documents are indexed.
        $this->assertSolrIsEmpty();
    }
}
```

### Testing Custom Event Listeners

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExt\Tests\Unit\EventListener;

use ApacheSolrForTypo3\Solr\Event\Indexing\BeforeDocumentsAreIndexedEvent;
use ApacheSolrForTypo3\Solr\System\Solr\Document\Document;
use MyVendor\MyExt\EventListener\EnrichSolrDocuments;
use PHPUnit\Framework\TestCase;

final class EnrichSolrDocumentsTest extends TestCase
{
    public function testCustomScoreIsAdded(): void
    {
        $document = new Document();
        $document->setField('type', 'pages');

        $event = $this->createMock(BeforeDocumentsAreIndexedEvent::class);
        $event->method('getDocuments')->willReturn([$document]);

        $listener = new EnrichSolrDocuments();
        $listener($event);

        self::assertNotNull($document->getField('custom_score_floatS'));
    }
}
```
