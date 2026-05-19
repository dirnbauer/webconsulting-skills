# 10. Independent Indexer (Custom Data)

Continues `typo3-solr` from [full guide](full-guide.md).

## 10. Independent Indexer (Custom Data)

For external data or when the RecordIndexer is not sufficient:

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExt\Indexer;

use ApacheSolrForTypo3\Solr\ConnectionManager;
use ApacheSolrForTypo3\Solr\Domain\Site\SiteRepository;
use ApacheSolrForTypo3\Solr\System\Solr\Document\Document;

final class ExternalDataIndexer
{
    public function __construct(
        private readonly ConnectionManager $connectionManager,
        private readonly SiteRepository $siteRepository,
    ) {}

    public function index(array $rows, int $rootPageId = 1, int $language = 0): void
    {
        $site = $this->siteRepository->getSiteByRootPageId($rootPageId);
        $connection = $this->connectionManager->getConnectionByPageId($rootPageId, $language);
        $documents = [];

        foreach ($rows as $row) {
            $document = new Document();
            $document->setField('id', 'external_' . $row['uid']);
            $document->setField('variantId', 'external_' . $row['uid']);
            $document->setField('type', 'external_record');
            $document->setField('appKey', 'EXT:solr');
            $document->setField('access', ['r:0']);
            $document->setField('site', $site->getDomain());
            $document->setField('siteHash', $site->getSiteHash());
            $document->setField('uid', $row['uid']);
            $document->setField('pid', $rootPageId);
            $document->setField('title', $row['title']);
            $document->setField('content', $row['content']);
            $document->setField('url', $row['url']);

            $documents[] = $document;
        }

        $connection->getWriteService()->addDocuments($documents);
    }

    public function clearIndex(string $type = 'external_record'): void
    {
        $connections = $this->connectionManager->getAllConnections();
        foreach ($connections as $connection) {
            $connection->getWriteService()->deleteByType($type);
        }
    }
}
```

### CLI Command Wrapper

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExt\Command;

use MyVendor\MyExt\Indexer\ExternalDataIndexer;
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;

#[AsCommand(name: 'myext:index-external', description: 'Index external data into Solr')]
final class IndexExternalCommand extends Command
{
    public function __construct(
        private readonly ExternalDataIndexer $indexer,
    ) {
        parent::__construct();
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        $rows = $this->fetchExternalData();

        $io->info(sprintf('Indexing %d records...', count($rows)));
        $this->indexer->index($rows);
        $io->success('Done.');

        return Command::SUCCESS;
    }

    private function fetchExternalData(): array
    {
        // Implement your data fetching logic
        return [];
    }
}
```
