---
name: typo3-solr
description: >-
  Expert guidance on Apache Solr search integration for TYPO3: installation,
  Index Queue, faceting, suggest, PSR-14 events, custom indexers, LLM/vector
  search (Solr native), DDEV/Docker/production setup, deep debugging &
  troubleshooting, and file indexing via solrfal. Use when working with solr,
  search, indexing, facets, suggest, autocomplete, vector search, solrfal, tika.
compatibility: TYPO3 13.4 - 14.x
metadata:
  version: "1.0.0"
  related_skills:
    - typo3-content-blocks
    - typo3-datahandler
    - typo3-seo
    - ai-search-optimization
---

# Apache Solr for TYPO3

> **Compatibility:** TYPO3 v13.4 LTS (current) and v14.x (when EXT:solr 14.0 releases).
> EXT:solr 13.1 targets TYPO3 13.4. A `task/14LTS_compatibility` dev branch is actively being developed.
> All custom PHP code in this skill uses TYPO3 v14 conventions (PHP 8.2+, `#[AsEventListener]`, constructor promotion).

> **TYPO3 API First:** Always use TYPO3's built-in APIs and EXT:solr's TypoScript/PSR-14 events before creating custom implementations. Do not reinvent what EXT:solr already provides.

## Sources

This skill is based on the following authoritative sources:

1. [EXT:solr Documentation](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/)
2. [EXT:tika Documentation](https://docs.typo3.org/p/apache-solr-for-typo3/tika/main/en-us/)
3. [Version Matrix](https://docs.typo3.org/p/apache-solr-for-typo3/solr/main/en-us/Appendix/VersionMatrix.html)
4. [GitHub: TYPO3-Solr/ext-solr](https://github.com/TYPO3-Solr/ext-solr)
5. [GitHub: v14 dev branch](https://github.com/TYPO3-Solr/ext-solr/tree/task/14LTS_compatibility)
6. [Apache Solr Reference Guide](https://solr.apache.org/guide/solr/latest/)
7. [Solr Dense Vector Search](https://solr.apache.org/guide/solr/latest/query-guide/dense-vector-search.html)
8. [Solr Text to Vector (LLM)](https://solr.apache.org/guide/solr/latest/query-guide/text-to-vector.html)
9. [typo3-solr.com](https://www.typo3-solr.com/)
10. [hosted-solr.com](https://hosted-solr.com/en/)
11. [ddev-typo3-solr](https://github.com/ddev/ddev-typo3-solr)
12. [Mittwald Solr Docs](https://developer.mittwald.de/docs/v2/platform/databases/solr/)
13. [helhum/dotenv-connector](https://github.com/helhum/dotenv-connector)

## 1. Architecture Overview

EXT:solr connects TYPO3 CMS to an Apache Solr search server, providing full-text search, faceted navigation, autocomplete, and (since Solr 9.8) vector/semantic search.

```mermaid
graph LR
    subgraph typo3 [TYPO3 CMS]
        Editor[Editor creates/edits content]
        Monitor[Monitoring detects changes]
        Queue[Index Queue]
        Scheduler[Scheduler Worker]
        Plugin[Search Plugin]
    end
    subgraph solr [Apache Solr Server]
        Core[Solr Core]
        Schema[Schema / Configset]
    end
    Editor --> Monitor
    Monitor --> Queue
    Queue --> Scheduler
    Scheduler -->|HTTP POST documents| Core
    Plugin -->|HTTP GET query| Core
    Core --> Plugin
```

### Document Lifecycle

```mermaid
sequenceDiagram
    participant E as Editor
    participant T as TYPO3
    participant M as Monitor
    participant Q as Index Queue
    participant S as Scheduler
    participant Solr as Solr Server

    E->>T: Create/edit record
    T->>M: DataHandler triggers PSR-14 event
    M->>Q: Add/update queue item
    Note over Q: tx_solr_indexqueue_item
    S->>Q: Poll for pending items
    Q->>S: Return items to index
    S->>Solr: POST document (JSON)
    Solr-->>S: 200 OK
    S->>Q: Mark item as indexed
```

### Component Overview

| Component | Package | Purpose | Required? |
|-----------|---------|---------|-----------|
| **EXT:solr** | `apache-solr-for-typo3/solr` | Core search integration | Yes |
| **EXT:tika** | `apache-solr-for-typo3/tika` | Text/metadata extraction from files | Only for file indexing |
| **EXT:solrfal** | Funding extension | FAL file indexing into Solr | Only for file indexing |
| **EXT:solrconsole** | Funding extension | Backend management console | Optional |
| **EXT:solrdebugtools** | Funding extension | Query debugging, score analysis | Optional (recommended for dev) |

<!-- SCREENSHOT: backend-module-overview.png - EXT:solr backend module main view -->

## 2. Version Compatibility Matrix

| EXT:solr | TYPO3 | Apache Solr | Configset | PHP | EXT:tika | EXT:solrfal |
|----------|-------|-------------|-----------|-----|----------|-------------|
| **13.1** | **13.4** | **9.10.1** | `ext_solr_13_1_0` | 8.2 - 8.4 | 13.1 | 13.0 |
| 12.1 | 12.4 | 9.10.1 | `ext_solr_12_1_0` | 8.1 - 8.3 | 12.1 | 12.0 |

### TYPO3 v14 Readiness

EXT:solr does **not** yet have a stable v14 release. Active development happens on the [`task/14LTS_compatibility`](https://github.com/TYPO3-Solr/ext-solr/tree/task/14LTS_compatibility) branch (last updated Feb 17, 2026).

**Key v14 changes in the dev branch:**
- Fluid v5 ViewHelper compatibility
- TSFE removal: `FrontendEnvironment/Tsfe` refactored to `FrontendSimulation/FrontendAwareEnvironment`
- `ext_emconf.php` removed (Composer-only)
- TCA `searchFields` deprecation handled
- FlexForm registration via `registerPlugin()` instead of `addPiFlexFormValue()`
- New configset: `ext_solr_14_0_0`

**Testing with the dev branch:**

```bash
composer require apache-solr-for-typo3/solr:dev-task/14LTS_compatibility
```

> **Warning:** This branch is WIP. Do not use in production.

### CVE-2025-24814 Migration

Apache Solr 9.8.0+ disables loading `jar` files via `lib` directive in configsets. The `solr-typo3-plugin` must be moved from `/configsets/ext_solr_*/typo3lib/` to `/typo3lib/` at the Solr server root. Docker users: pull image v13.0.1+ -- the migration runs automatically.

## 3. Installation & Setup

### Composer

```bash
composer require apache-solr-for-typo3/solr
```

### DDEV Setup

The recommended local development setup uses the [ddev-typo3-solr](https://github.com/ddev/ddev-typo3-solr) addon:

```bash
ddev add-on get ddev/ddev-typo3-solr
ddev restart
```

Configure `.ddev/typo3-solr/config.yaml`:

```yaml
config: 'vendor/apache-solr-for-typo3/solr/Resources/Private/Solr/solr.xml'
typo3lib: 'vendor/apache-solr-for-typo3/solr/Resources/Private/Solr/typo3lib'
configsets:
  - name: 'ext_solr_13_1_0'
    path: 'vendor/apache-solr-for-typo3/solr/Resources/Private/Solr/configsets/ext_solr_13_1_0'
cores:
  - name: 'core_en'
    schema: 'english/schema.xml'
  - name: 'core_de'
    schema: 'german/schema.xml'
```

Auto-initialize cores on boot in `.ddev/config.yaml`:

```yaml
hooks:
  post-start:
    - exec-host: ddev solrctl apply
```

**Useful DDEV commands:**

| Command | Description |
|---------|-------------|
| `ddev solrctl apply` | Create cores from config |
| `ddev solrctl wipe` | Delete all cores |
| `ddev solr version` | Check Solr version |
| `ddev launch :8984` | Open Solr Admin UI |
| `ddev logs -s typo3-solr` | View Solr logs |

<!-- SCREENSHOT: ddev-solr-admin.png - DDEV Solr Admin at :8984 -->

### Docker (Production)

```yaml
services:
  solr:
    image: typo3solr/ext-solr:13.1
    ports:
      - "8983:8983"
    volumes:
      - solr-data:/var/solr
    restart: unless-stopped

volumes:
  solr-data:
    driver: local
```

The image ships default cores for all languages. Persistent data is stored at `/var/solr` (owned by UID 8983).

### Standalone Solr

Deploy the configset from EXT:solr into your Solr installation:

```bash
cp -r vendor/apache-solr-for-typo3/solr/Resources/Private/Solr/* $SOLR_INSTALL_DIR/server/solr/
```

Create cores via `core.properties` files or REST API:

```bash
curl -X POST http://localhost:8983/api/cores -H 'Content-Type: application/json' -d '{
  "create": {
    "name": "core_en",
    "configSet": "ext_solr_13_1_0",
    "schema": "english/schema.xml",
    "instanceDir": "cores/core_en",
    "dataDir": "/var/solr/data/core_en"
  }
}'
```

### Managed Hosting: Mittwald

Mittwald provides a managed Solr service via their container platform. Use the Terraform module:

```hcl
module "solr" {
  source         = "mittwald/solr/mittwald"
  solr_version   = "9"
  solr_core_name = "typo3"
  solr_heap      = "2g"
}
```

Access Solr at `http://solr:8983` inside the container. For local debugging:

```bash
mw container port-forward --port 8983
```

### Managed Hosting: hosted-solr.com

[hosted-solr.com](https://hosted-solr.com/en/) by dkd provides pre-configured Solr cores optimized for EXT:solr. Plans start at EUR 10/month (2 indexes, 4000 documents). After creating a core, configure it in your TYPO3 site config using the provided host, port, and path.

### TYPO3 Site Configuration

In `config/sites/<identifier>/config.yaml`:

```yaml
solr_enabled_read: true
solr_host_read: solr
solr_port_read: '8983'
solr_scheme_read: http
solr_path_read: /
solr_core_read: core_en
```

For DDEV, use the DDEV hostname and HTTPS port:

```yaml
solr_host_read: <project>.ddev.site
solr_port_read: '8984'
solr_scheme_read: https
```

<!-- SCREENSHOT: reports-module-solr.png - TYPO3 Reports module Solr status -->

### Environment Configuration (helhum/dotenv-connector)

Never hardcode Solr connection details. Use [helhum/dotenv-connector](https://github.com/helhum/dotenv-connector) for per-environment configuration:

```bash
composer require helhum/dotenv-connector
```

`.env` (gitignored):

```env
SOLR_HOST=solr
SOLR_PORT=8983
SOLR_SCHEME=http
SOLR_PATH=/
SOLR_CORE_EN=core_en
SOLR_CORE_DE=core_de
```

`.env.example` (committed to VCS):

```env
SOLR_HOST=solr
SOLR_PORT=8983
SOLR_SCHEME=http
SOLR_PATH=/
SOLR_CORE_EN=core_en
SOLR_CORE_DE=core_de
```

In `config/system/additional.php`, override site config values programmatically or use a post-processing approach. For simple setups, keep `.env` values and reference them in deployment scripts that generate site config YAML per environment.

## 4. EXT:tika -- When You Need It (and When Not)

EXT:tika integrates Apache Tika for metadata extraction, language detection, and text extraction from ~1200 file formats.

```mermaid
graph TD
    Question{"Do you index files?<br/>(PDF, DOCX, XLSX)"}
    Question -->|Yes| NeedTika[Install EXT:tika + EXT:solrfal]
    Question -->|No| SkipTika[Skip -- EXT:solr handles<br/>pages and records natively]
    NeedTika --> TikaServer["Run Tika Server 3.2.2+<br/>(Docker recommended)"]
```

**Three backends (choose one):**

| Backend | Recommended? | Setup |
|---------|-------------|-------|
| **Tika Server** | Yes | Standalone Docker container, newest Tika version |
| **Solr Cell** | Acceptable | Uses Tika built into Solr, no extra service needed |
| **Tika App** | Deprecated | Requires Java on webserver, do not use |

**When you NEED EXT:tika:**
- File indexing via EXT:solrfal (search inside PDFs, Word documents, etc.)
- Automatic FAL metadata enrichment (EXIF, XMP, document properties)
- Language detection on uploaded files

**When you DON'T need it:**
- Only indexing pages and structured records (news, events, products) via Index Queue
- EXT:solr handles page content and record fields natively without Tika

**Version:** EXT:tika 13.1. Requires Tika Server **3.2.2+** (CVE-2025-54988 fix).

See [SKILL-SOLRFAL.md](SKILL-SOLRFAL.md) for complete file indexing setup.

## 5. Configset & Schema

The configset defines how Solr processes and indexes text. EXT:solr ships configsets at `Resources/Private/Solr/configsets/ext_solr_13_1_0/`.

### Structure

```
ext_solr_13_1_0/
├── conf/
│   ├── solrconfig.xml
│   ├── english/
│   │   └── schema.xml
│   ├── german/
│   │   └── schema.xml
│   └── ... (other languages)
└── typo3lib/             # moved to server root since Solr 9.8
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

### Site Hash Strategy

Since EXT:solr 13.0, the default site hash strategy changed from **domain-based** (deprecated) to **site-identifier-based**. Configure in Extension Settings:

- `siteHashStrategy = 1` (site-identifier, **default and recommended**)
- `siteHashStrategy = 0` (domain, deprecated, removed in 13.1.x+)

If upgrading from 12.x, you must re-index after switching strategies.

## 6. Index Queue Configuration

The Index Queue is the central mechanism for getting TYPO3 records into Solr.

```mermaid
graph LR
    subgraph monitoring [Record Monitoring]
        Edit[Record created/edited]
        Event[PSR-14 DataUpdate Event]
    end
    subgraph queue [Index Queue]
        Item["tx_solr_indexqueue_item"]
    end
    subgraph processing [Processing]
        Worker[Scheduler: Index Queue Worker]
        Solr[Solr Server]
    end
    Edit --> Event
    Event --> Item
    Worker -->|polls| Item
    Worker -->|POST document| Solr
```

### Pages

Pages are indexed out of the box. No additional configuration needed. The page indexer sends the rendered page content to Solr.

### Custom Records

Index any TYPO3 record table via TypoScript. Full example for EXT:news:

```typoscript
plugin.tx_solr.index.queue {
    news = 1
    news {
        type = tx_news_domain_model_news

        fields {
            abstract = teaser
            author = author
            authorEmail_stringS = author_email
            title = title

            content = SOLR_CONTENT
            content {
                cObject = COA
                cObject {
                    10 = TEXT
                    10 {
                        field = bodytext
                        noTrimWrap = || |
                    }
                }
            }

            category_stringM = SOLR_RELATION
            category_stringM {
                localField = categories
                multiValue = 1
            }

            keywords = SOLR_MULTIVALUE
            keywords {
                field = keywords
            }

            tags_stringM = SOLR_RELATION
            tags_stringM {
                localField = tags
                multiValue = 1
            }

            url = TEXT
            url {
                typolink.parameter = {$plugin.tx_news.settings.detailPid}
                typolink.additionalParams = &tx_news_pi1[controller]=News&tx_news_pi1[action]=detail&tx_news_pi1[news]={field:uid}
                typolink.additionalParams.insertData = 1
                typolink.returnLast = url
            }
        }

        attachments {
            fields = related_files
        }
    }
}
```

### Content Objects

| Object | Purpose |
|--------|---------|
| `SOLR_CONTENT` | Strips HTML/RTE from field content |
| `SOLR_RELATION` | Resolves relations (categories, tags, etc.), supports `multiValue = 1` |
| `SOLR_MULTIVALUE` | Splits a comma-separated field into multiple values |

### Records Outside Siteroot

To index records stored in sysfolders outside the site tree:

```typoscript
plugin.tx_solr.index.queue.news {
    additionalPageIds = 45,48
}
```

Enable monitoring in Extension Settings: "Enable tracking of records outside siteroot".

### Monitoring

EXT:solr detects record changes via PSR-14 events. Two modes:

- **Immediate** (default): changes are processed directly during the DataHandler operation
- **Delayed**: changes are queued in `tx_solr_eventqueue_item` and processed by a scheduler task ("Event Queue Worker")

Configure via Extension Settings: `monitoringType`.

<!-- SCREENSHOT: index-queue-tab.png - Backend module Index Queue tab -->

## 7. Search Configuration

### Essential Settings

```typoscript
plugin.tx_solr {
    enabled = 1
    search {
        targetPage = 42
        initializeWithEmptyQuery = 1
        showResultsOfInitialEmptyQuery = 0
        trustedFields = url
        keepExistingParametersForNewSearches = 1
    }
}
```

### Faceting

```typoscript
plugin.tx_solr.search {
    faceting = 1
    faceting {
        facets {
            contentType {
                label = Content Type
                field = type
            }
            category {
                label = Category
                field = category_stringM
            }
            year {
                label = Year
                field = year_intS
                type = queryGroup
                queryGroup {
                    2025 {
                        query = [2025-01-01T00:00:00Z TO 2025-12-31T23:59:59Z]
                    }
                    2024 {
                        query = [2024-01-01T00:00:00Z TO 2024-12-31T23:59:59Z]
                    }
                }
            }
        }
    }
}
```

**Facet types:** `options` (default), `queryGroup`, `hierarchy`, `dateRange`, `numericRange`.

### Suggest / Autocomplete

```typoscript
plugin.tx_solr {
    suggest = 1
    suggest {
        numberOfSuggestions = 10
        suggestField = spell
        showTopResults = 1
        numberOfTopResults = 5
        additionalTopResultsFields = url,type
    }
}
```

The built-in suggest uses the devbridge/jQuery-Autocomplete library. For a jQuery-free approach, see [SKILL-FRONTEND.md](SKILL-FRONTEND.md).

### Sorting, Highlighting, Spellcheck

```typoscript
plugin.tx_solr.search {
    sorting = 1
    sorting {
        defaultOrder = asc
        options {
            relevance {
                field = relevance
                label = Relevance
            }
            title {
                field = sortTitle
                label = Title
            }
            created {
                field = created
                label = Date
            }
        }
    }

    results {
        resultsHighlighting = 1
        resultsHighlighting {
            fragmentSize = 200
            wrap = <mark>|</mark>
        }
    }

    spellchecking = 1
}
```

### Route Enhancers

SEO-friendly search URLs:

```yaml
routeEnhancers:
  SolrSearch:
    type: SolrFacetMaskAndCombineEnhancer
    extensionKey: solr
    solr:
      type: Extbase
      extension: Solr
      plugin: pi_results
      routes:
        - routePath: '/search/{q}'
          _controller: 'Search::results'
          _arguments:
            q: q
```

<!-- SCREENSHOT: frontend-search-facets.png - Search results with facets -->

## 8. Fluid Templates & Frontend

### Template Paths

```typoscript
plugin.tx_solr {
    view {
        templateRootPaths.10 = EXT:my_ext/Resources/Private/Templates/Solr/
        partialRootPaths.10 = EXT:my_ext/Resources/Private/Partials/Solr/
        layoutRootPaths.10 = EXT:my_ext/Resources/Private/Layouts/Solr/
    }
}
```

### Key Templates

| Template | Purpose |
|----------|---------|
| `Templates/Search/Results.html` | Main search results page |
| `Templates/Search/Form.html` | Search form |
| `Partials/Result/Document.html` | Single result item |
| `Partials/Facets/OptionsFacet.html` | Options facet rendering |
| `Partials/Facets/QueryGroupFacet.html` | Query group facet |

Copy default templates from EXT:solr to your extension path and modify them.

## 9. PSR-14 Events Reference

### Monitoring Events

| Event | Fired when |
|-------|-----------|
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

### Indexing Events

| Event | Fired when |
|-------|-----------|
| `BeforePageDocumentIsProcessedForIndexingEvent` | Before page document is processed (add extra documents) |
| `AfterPageDocumentIsCreatedForIndexingEvent` | After page document created (replace/substitute) |
| `BeforeDocumentIsProcessedForIndexingEvent` | Before non-page record document is processed |
| `BeforeDocumentsAreIndexedEvent` | Before documents are sent to Solr (add custom fields) |

### Other Events

| Event | Fired when |
|-------|-----------|
| `AfterFacetIsParsedEvent` | Facet component modification |
| `AfterUriIsProcessedEvent` | URI building in search context |
| `AfterSiteHashHasBeenDeterminedForSiteEvent` | Override calculated site hash |

### Example: Add Custom Fields to Documents (v14 Style)

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

**v13 fallback** (if `#[AsEventListener]` is not available): register in `Services.yaml`:

```yaml
MyVendor\MyExt\EventListener\EnrichSolrDocuments:
  tags:
    - name: event.listener
      identifier: 'my-ext/enrich-solr-documents'
```

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

## 11. LLM & Vector Search (Solr Server Native)

Apache Solr 9.8+ includes a native LLM module for semantic/vector search. This runs on the **Solr server side** -- EXT:solr queries the results.

```mermaid
graph LR
    subgraph indexing [Index Time]
        Text[Document text]
        URP["TextToVectorUpdateProcessor"]
        API1["Embedding API<br/>(OpenAI, Mistral, etc.)"]
        Vector1[Dense Vector]
        SolrIdx["Solr Index<br/>(DenseVectorField)"]
    end
    subgraph querying [Query Time]
        Query[User query text]
        QP["knn_text_to_vector parser"]
        API2["Embedding API"]
        Vector2[Query Vector]
        KNN["KNN Search"]
        Results[Ranked Results]
    end
    Text --> URP --> API1 --> Vector1 --> SolrIdx
    Query --> QP --> API2 --> Vector2 --> KNN --> Results
    SolrIdx -.->|similarity| KNN
```

### Prerequisites

- Apache Solr **9.8+** with the `llm` module enabled
- An external embedding API account (OpenAI, Mistral AI, Cohere, or HuggingFace)

### Schema: DenseVectorField

Add to your schema (or use a custom configset):

```xml
<fieldType name="knn_vector" class="solr.DenseVectorField"
           vectorDimension="1536"
           similarityFunction="cosine"
           knnAlgorithm="hnsw"/>

<field name="vector" type="knn_vector" indexed="true" stored="true"/>
```

`vectorDimension` must match your embedding model (e.g., OpenAI `text-embedding-3-small` = 1536 dimensions).

### Model Configuration

Register the query parser in `solrconfig.xml`:

```xml
<queryParser name="knn_text_to_vector"
             class="org.apache.solr.llm.textvectorisation.search.TextToVectorQParserPlugin"/>
```

Upload a model definition:

```bash
curl -XPUT 'http://localhost:8983/solr/core_en/schema/text-to-vector-model-store' \
  --data-binary @model.json -H 'Content-type:application/json'
```

`model.json` (OpenAI example):

```json
{
  "class": "dev.langchain4j.model.openai.OpenAiEmbeddingModel",
  "name": "openai-embed",
  "params": {
    "baseUrl": "https://api.openai.com/v1",
    "apiKey": "sk-...",
    "modelName": "text-embedding-3-small",
    "timeout": 60,
    "maxRetries": 3
  }
}
```

Supported providers: OpenAI, Mistral AI, Cohere, HuggingFace. See [LangChain4j Embedding Models](https://docs.langchain4j.dev/category/embedding-models) for all parameters.

### Indexing with Vectors

Add an update processor chain in `solrconfig.xml`:

```xml
<updateRequestProcessorChain name="vectorisation">
  <processor class="solr.llm.textvectorisation.update.processor.TextToVectorUpdateProcessorFactory">
    <str name="inputField">_text_</str>
    <str name="outputField">vector</str>
    <str name="model">openai-embed</str>
  </processor>
  <processor class="solr.RunUpdateProcessorFactory"/>
</updateRequestProcessorChain>
```

**Two-pass strategy** (recommended for production): index documents normally first, then enrich with vectors in a second pass to avoid blocking the indexing pipeline with slow API calls.

### Querying

**Semantic search** (text in, vector out):

```
?q={!knn_text_to_vector model=openai-embed f=vector topK=10}customer complaints handling
```

**Raw vector search:**

```
?q={!knn f=vector topK=10}[0.1, 0.2, 0.3, ...]
```

**Threshold search** (all documents above similarity):

```
?q={!vectorSimilarity f=vector minReturn=0.7}[0.1, 0.2, 0.3, ...]
```

**Hybrid search** (BM25 + vector re-ranking):

```
?q=customer complaints
&rq={!rerank reRankQuery=$rqq reRankDocs=50 reRankWeight=2}
&rqq={!knn_text_to_vector model=openai-embed f=vector topK=50}customer complaints
```

### Pre-Filtering

Combine vector search with traditional filters:

```
?q={!knn_text_to_vector model=openai-embed f=vector topK=10 preFilter=type:pages}search query
```

### EXT:solr Integration

EXT:solr 13.1 has initial vector search support. For custom integration, use a PSR-14 event listener on `BeforeDocumentsAreIndexedEvent` to add vector data to documents via your own embedding service call.

> **Note:** Full native vector search support in EXT:solr (Index Queue -> vector fields, Fluid templates for vector results) is still evolving. Monitor the [GitHub repository](https://github.com/TYPO3-Solr/ext-solr) for updates.

### Use Cases

| Use Case | Approach |
|----------|----------|
| **Smart site search** | `knn_text_to_vector` finds semantically similar content |
| **Similar content** | Given a document's vector, find K nearest neighbors |
| **Multilingual bridge** | Embeddings can match across languages |
| **FAQ matching** | Match user questions to FAQ answers despite different wording |
| **RAG preparation** | Use Solr as retrieval layer for LLM-powered Q&A |
| **File discovery** | Combined with solrfal + Tika: semantic search over documents |

## 12. Debugging & Troubleshooting

This section is the core reference for diagnosing and fixing EXT:solr issues.

### 12.1 Where to Start: Diagnostic Flowchart

```mermaid
graph TD
    Start["Problem with Solr?"]
    Start --> A{"Reports module:<br/>all green?"}
    A -->|No| Fix1["Fix connection config<br/>(see 12.2)"]
    A -->|Yes| B{"Index Queue:<br/>items present?"}
    B -->|No| Fix2["Initialize queue<br/>(see 12.3)"]
    B -->|Yes| C{"Items have<br/>errors?"}
    C -->|Yes| Fix3["Check error messages<br/>(see 12.3)"]
    C -->|No| D{"Solr Admin:<br/>documents exist?"}
    D -->|No| Fix4["Run scheduler worker<br/>(see 12.3)"]
    D -->|Yes| E{"Frontend shows<br/>results?"}
    E -->|No| Fix5["Check TypoScript,<br/>site hash (see 12.4)"]
    E -->|Yes| Done["Working!"]
```

**Step 1:** Check TYPO3 Reports module (Admin Tools -> Reports -> Status Report). All Solr-related checks must be green.

**Step 2:** Open Solr Admin UI. DDEV: `ddev launch :8984`. Production: `https://your-host:8983/solr/`.

**Step 3:** EXT:solr backend module -> "Index Queue" tab. Are items queued? Any errors?

<!-- SCREENSHOT: reports-module-solr.png - TYPO3 Reports module Solr status -->

### 12.2 Connection Problems

**"Search is currently not available"** -- full checklist:

1. Verify site config values: `solr_host_read`, `solr_port_read`, `solr_scheme_read`, `solr_path_read`
2. Click "Initialize connection" in the EXT:solr backend module after ANY config change
3. Test from CLI:
   ```bash
   # Inside DDEV container
   ddev exec curl -s http://solr:8983/solr/core_en/admin/ping
   # From host
   curl -sk https://<project>.ddev.site:8984/solr/core_en/admin/ping
   ```
4. **DDEV networking:** Inside the container, Solr is reachable at hostname `solr` on port `8983`. From the host, use `<project>.ddev.site:8984` with HTTPS.
5. **Firewall:** Ensure port 8983 (or 8984 for DDEV) is open
6. **HTTPS:** DDEV uses self-signed certificates. Use `solr_scheme_read: https` with DDEV.

### 12.3 Indexing Problems

#### Nothing in Index Queue

- **TypoScript not loaded:** Check the Template module on the root page. EXT:solr static templates must be included.
- **Queue not initialized:** Backend module -> "Index Queue" tab -> select record types -> click "Queue selected content"
- **Missing config:** `plugin.tx_solr.index.queue.[table] = 1` must exist for each table
- **Records outside siteroot:** Set `additionalPageIds` and enable "tracking of records outside siteroot" in Extension Settings

#### Items in Queue but Not Indexed

- **Scheduler not running:** A "Index Queue Worker" scheduler task must be configured and executing
- **Check errors:** Inspect the `errors` column:
  ```sql
  SELECT item_type, errors, COUNT(*) as cnt
  FROM tx_solr_indexqueue_item
  WHERE errors != ''
  GROUP BY item_type, errors;
  ```
- **Forced webroot:** If TYPO3 cannot auto-detect the web root (CLI context), configure "Forced webroot" in the scheduler task settings
- **Memory:** Large content can exceed PHP `memory_limit`. Increase for the scheduler process.

#### Items Indexed but Wrong/Missing Content

- **Check the actual document** in Solr Admin UI:
  ```
  q=*:*&fq=type:tx_news_domain_model_news&rows=5&fl=uid,title,content,url,siteHash
  ```
- **Field mapping:** Verify `plugin.tx_solr.index.queue.[table].fields` TypoScript matches your Solr schema fields
- **HTML in content:** Use `SOLR_CONTENT` to strip HTML from RTE fields
- **Relations empty:** Use `SOLR_RELATION` with `multiValue = 1` for category/tag fields

#### Re-indexing

1. **Soft re-index:** Backend module -> clear queue -> re-queue -> run scheduler task
2. **Force re-index:** Scheduler task "Force Re-Indexing of a site" for specific configurations
3. **Nuclear option** (DDEV only): `TRUNCATE tx_solr_indexqueue_item;` then re-initialize via backend module

### 12.4 Search / Query Problems

#### No Results in Frontend

```mermaid
graph LR
    Plugin["Search Plugin<br/>(Fluid)"] --> TS["TypoScript Config"]
    TS --> SolrQ["Solr Query<br/>(HTTP GET)"]
    SolrQ --> Response["Solr Response<br/>(JSON)"]
    Response --> Render["Fluid Rendering"]
```

- **targetPage:** `plugin.tx_solr.search.targetPage` must point to the page containing the search plugin
- **Disabled:** Check `plugin.tx_solr.enabled` is not set to `0`
- **Site hash mismatch:** Documents indexed with wrong site hash won't appear. Test in Solr Admin:
  ```
  q=YOUR_TERM&fq=siteHash:YOUR_EXPECTED_HASH
  ```
- **Access restrictions:** Documents have an `access` field. Ensure frontend user group matches.

#### Wrong Results / Bad Relevance

- **debugQuery:** In Solr Admin, run `q=YOUR_TERM&debugQuery=true` to see score breakdowns
- **EXT:solrdebugtools:** Install for Debug\Query ViewHelper, Explain functionality, and score pie charts
- **Boosting:** Configure field weights:
  ```typoscript
  plugin.tx_solr.search.query {
      boostFunction = recip(ms(NOW,created),3.16e-11,1,1)
      boostQuery = type:pages^2.0
  }
  ```

#### Facets Not Showing

- `plugin.tx_solr.search.faceting = 1` missing
- Field not indexed (check dynamic field suffix matches schema)
- `initializeWithEmptyQuery = 1` needed to show facets before any search
- Facet field has zero values in indexed documents

### 12.5 Logging Deep Dive

Enable logging to analyze indexing and search operations:

```typoscript
plugin.tx_solr.logging {
    debugOutput = 1
    exceptions = 1
    indexing = 1
    indexing.indexQueueInitialization = 1
    indexing.pageIndexed = 1
    indexing.queue.news = 1
    query.rawGet = 1
    query.rawPost = 1
    query.queryString = 1
    query.searchWords = 1
}
```

Configure a dedicated log file in `config/system/additional.php`:

```php
$GLOBALS['TYPO3_CONF_VARS']['LOG']['ApacheSolrForTypo3']['Solr']['writerConfiguration'] = [
    \Psr\Log\LogLevel::DEBUG => [
        \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
            'logFile' => \TYPO3\CMS\Core\Core\Environment::getVarPath() . '/log/solr.log',
        ],
    ],
];
```

**Where to find output:** `var/log/solr.log`, Admin Tools -> Log module.

> **Warning:** Disable logging on production. Log data grows quickly and impacts performance.

### 12.6 Solr Admin UI as Debugging Tool

<!-- SCREENSHOT: solr-admin-query.png - Solr Admin query panel -->

Key diagnostic queries:

| Query | Purpose |
|-------|---------|
| `q=*:*&rows=0` | Total document count |
| `q=*:*&fq=type:pages&rows=5&fl=uid,title,url,siteHash` | Check indexed pages |
| `q=*:*&fq=type:tx_news_domain_model_news&fl=uid,title,content` | Check custom records |
| `q=YOUR_TERM&debugQuery=true` | Score explanation |
| `q=*:*&facet=true&facet.field=type&rows=0` | Document type distribution |
| `q=*:*&fq=siteHash:YOUR_HASH&rows=0` | Documents per site hash |

**Core Admin:** Reload a core after schema changes (Analysis tab -> Reload Core).

**Analysis screen:** Test how text is tokenized and stemmed. Paste text into the field analysis tool to see how Solr processes it.

<!-- SCREENSHOT: solr-analysis-screen.png - Solr Analysis screen -->

### 12.7 Database-Level Debugging (DDEV Only)

```sql
-- Queue fill state per type
SELECT item_type, indexing_configuration,
       COUNT(*) as total,
       SUM(CASE WHEN errors != '' THEN 1 ELSE 0 END) as errors
FROM tx_solr_indexqueue_item
GROUP BY item_type, indexing_configuration;

-- Failed items with error messages
SELECT uid, item_type, item_uid, errors, changed, indexed
FROM tx_solr_indexqueue_item
WHERE errors != ''
LIMIT 20;

-- Event queue (delayed monitoring)
SELECT * FROM tx_solr_eventqueue_item
ORDER BY tstamp DESC LIMIT 20;

-- Stale items (changed but not re-indexed)
SELECT uid, item_type, item_uid, changed, indexed
FROM tx_solr_indexqueue_item
WHERE changed > indexed
LIMIT 20;

-- Clear all errors (to retry indexing)
UPDATE tx_solr_indexqueue_item SET errors = '' WHERE errors != '';
```

### 12.8 Common Issues Quick Reference

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "Search is currently not available" | Solr connection misconfigured | Check site config, initialize connection |
| No results for any query | Site hash mismatch | Check `siteHashStrategy`, re-index |
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
| Configset version mismatch | Wrong configset deployed | Redeploy matching `ext_solr_13_1_0` |
| Jar loading error (Solr 9.8+) | CVE-2025-24814 migration needed | Move `typo3lib/` to server root, or pull Docker 13.0.1+ |
| Tika: connection timeout | Tika Server not running or wrong port | Check Docker container, test connection in extension settings |
| Language core missing | No core for language | Create core with matching language schema |

## 13. Testing

### Functional Test Setup

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExt\Tests\Functional;

use ApacheSolrForTypo3\Solr\Tests\Integration\IntegrationTestCase;

final class CustomIndexingTest extends IntegrationTestCase
{
    protected array $testExtensionsToLoad = [
        'apache-solr-for-typo3/solr',
        'my-vendor/my-ext',
    ];

    public function testNewsRecordIsIndexed(): void
    {
        $this->importCSVDataSet(__DIR__ . '/Fixtures/news_records.csv');
        $this->indexQueue('news');

        $searchResult = $this->searchInSolr('test news title');
        self::assertGreaterThan(0, $searchResult->getResultCount());
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

## 14. Best Practices

### Production Checklist

- [ ] Correct configset version deployed (`ext_solr_13_1_0`)
- [ ] Solr JVM memory configured (`SOLR_JAVA_MEM=-Xms512m -Xmx1g`)
- [ ] Solr NOT publicly accessible (firewall, reverse proxy)
- [ ] Scheduler task "Index Queue Worker" running regularly
- [ ] Logging disabled in production
- [ ] Solr data volume backed up
- [ ] CVE patches applied (Solr 9.8.0+ jar migration)
- [ ] `siteHashStrategy = 1` (site-identifier)

### Security

- Solr must **never** be publicly accessible. Use firewall rules or bind to `127.0.0.1`
- Use a reverse proxy (nginx/Apache) with authentication if remote access is needed
- Monitor [Apache Solr security advisories](https://solr.apache.org/security.html)
- Keep Tika Server updated (CVE-2025-54988: requires 3.2.2+)

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

## Related Skills

- **typo3-datahandler**: Database operations that trigger Solr indexing
- **typo3-seo**: SEO configuration that complements Solr search
- **ai-search-optimization**: AEO/GEO for AI search visibility
- **typo3-content-blocks**: Content Elements that can be indexed
- **typo3-testing**: Testing patterns for TYPO3 extensions

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
- [v14 Development Branch](https://github.com/TYPO3-Solr/ext-solr/tree/task/14LTS_compatibility)
- [Docker Images](https://hub.docker.com/r/typo3solr/ext-solr/tags)

### Apache Solr Server

- [Reference Guide](https://solr.apache.org/guide/solr/latest/)
- [Dense Vector Search](https://solr.apache.org/guide/solr/latest/query-guide/dense-vector-search.html)
- [Text to Vector (LLM Module)](https://solr.apache.org/guide/solr/latest/query-guide/text-to-vector.html)
- [Solr Modules](https://solr.apache.org/guide/solr/latest/configuration-guide/solr-modules.html)
- [LLM API Javadoc](https://solr.apache.org/docs/9_8_0/modules/llm/index.html)
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

## Credits & Attribution

- **dkd Internet Service GmbH** for developing and maintaining EXT:solr, EXT:tika, and the TYPO3-Solr ecosystem
- **Apache Software Foundation** for Apache Solr and Apache Tika
- **b13** for maintaining the ddev-typo3-solr addon
- **Helmut Hummel (helhum)** for dotenv-connector
- **Mittwald** for managed Solr hosting documentation
