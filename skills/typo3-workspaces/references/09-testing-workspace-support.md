# 9. Testing Workspace Support

Continues `typo3-workspaces` from [full guide](full-guide.md).

## 9. Testing Workspace Support

### Prerequisites: Install Testing Framework

**Step 1: Require dev dependencies**

```bash
# DDEV
ddev composer require --dev typo3/testing-framework:"^9.0" phpunit/phpunit:"^11.0"

# Non-DDEV
composer require --dev typo3/testing-framework:"^9.0" phpunit/phpunit:"^11.0"
```

> For TYPO3 v14 use `typo3/testing-framework:"^9.0"` (see `typo3-testing` skill for details).

**Step 2: Create PHPUnit configuration for functional tests**

Create `Build/phpunit-functional.xml` in your extension root:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/FunctionalTestsBootstrap.php"
         colors="true"
         cacheResult="false">
    <testsuites>
        <testsuite name="Functional">
            <directory>Tests/Functional</directory>
        </testsuite>
    </testsuites>
    <php>
        <!-- Functional tests need a database. DDEV provides one automatically. -->
        <!-- For non-DDEV: set typo3DatabaseHost, typo3DatabaseUsername, etc. -->
        <!-- Example for DDEV (auto-detected, usually no env vars needed): -->
        <!-- <env name="typo3DatabaseHost" value="db"/> -->
        <!-- <env name="typo3DatabaseUsername" value="db"/> -->
        <!-- <env name="typo3DatabasePassword" value="db"/> -->
        <!-- <env name="typo3DatabaseName" value="db"/> -->
    </php>
</phpunit>
```

**Step 3: Create directory structure**

```bash
mkdir -p Tests/Functional/Fixtures
```

```
your-extension/
├── Build/
│   └── phpunit-functional.xml       ← PHPUnit config
├── Classes/
│   └── ...
├── Configuration/
│   └── TCA/
├── Tests/
│   └── Functional/
│       ├── Fixtures/
│       │   └── WorkspaceTestData.csv ← Test data
│       └── WorkspaceAwareTest.php    ← Test class
├── composer.json
└── ext_emconf.php
```

**Step 4: Ensure composer.json has autoload-dev**

```json
{
    "autoload-dev": {
        "psr-4": {
            "MyVendor\\MyExtension\\Tests\\": "Tests/"
        }
    }
}
```

Then run:

```bash
# DDEV
ddev composer dump-autoload

# Non-DDEV
composer dump-autoload
```

### Functional Test Setup

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\Tests\Functional;

use TYPO3\CMS\Core\Authentication\BackendUserAuthentication;
use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\Context\WorkspaceAspect;
use TYPO3\CMS\Core\Core\Bootstrap;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;

final class WorkspaceAwareTest extends FunctionalTestCase
{
    /**
     * Load the workspaces extension for all tests in this class.
     */
    protected array $coreExtensionsToLoad = [
        'workspaces',
    ];

    /**
     * Load your own extension.
     */
    protected array $testExtensionsToLoad = [
        'typo3conf/ext/my_extension',
    ];

    protected function setUp(): void
    {
        parent::setUp();

        // Import base data: pages, content, workspace record, backend user
        $this->importCSVDataSet(__DIR__ . '/Fixtures/WorkspaceTestData.csv');

        // Initialize backend user (uid=1 from fixture, must be admin for DataHandler)
        $this->setUpBackendUser(1);
        Bootstrap::initializeLanguageObject();
    }

    /**
     * Helper: set the current workspace context.
     */
    private function setWorkspaceId(int $workspaceId): void
    {
        $context = GeneralUtility::makeInstance(Context::class);
        $context->setAspect('workspace', new WorkspaceAspect($workspaceId));
        $GLOBALS['BE_USER']->setWorkspace($workspaceId);
    }

    /**
     * Test: Record created in workspace is NOT visible in live.
     */
    public function testRecordCreatedInWorkspaceNotVisibleInLive(): void
    {
        // Switch to workspace 1
        $this->setWorkspaceId(1);

        // Create a record in the workspace via DataHandler
        $data = [
            'tt_content' => [
                'NEW_1' => [
                    'pid' => 1,
                    'CType' => 'text',
                    'header' => 'Workspace Only Content',
                    'bodytext' => '<p>This should not be live</p>',
                ],
            ],
        ];

        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        self::assertEmpty($dataHandler->errorLog, 'DataHandler errors: ' . implode(', ', $dataHandler->errorLog));

        // Switch back to LIVE
        $this->setWorkspaceId(0);

        // Query live records -- the workspace record should NOT appear
        $queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getQueryBuilderForTable('tt_content');

        $liveRecords = $queryBuilder
            ->select('uid', 'header')
            ->from('tt_content')
            ->where(
                $queryBuilder->expr()->eq('pid', 1),
                $queryBuilder->expr()->eq('t3ver_wsid', 0),
                $queryBuilder->expr()->neq('t3ver_state', 1) // exclude new placeholders
            )
            ->executeQuery()
            ->fetchAllAssociative();

        $headers = array_column($liveRecords, 'header');
        self::assertNotContains('Workspace Only Content', $headers);
    }

    /**
     * Test: Workspace overlay returns modified content.
     */
    public function testWorkspaceOverlayReturnsModifiedContent(): void
    {
        // Record uid=10 exists in fixture with header "Original Header"
        // Workspace version exists with header "Modified In Workspace"
        $this->setWorkspaceId(1);

        $row = \TYPO3\CMS\Backend\Utility\BackendUtility::getRecordWSOL('tt_content', 10);

        self::assertIsArray($row);
        self::assertSame('Modified In Workspace', $row['header']);
    }

    /**
     * Test: Workspace publish command makes staged content live for a record pair.
     *
     * Publish live tt_content uid=10 using the workspace version row (swapWith = offline version uid).
     */
    public function testPublishWorkspaceRecordPairMakesContentLive(): void
    {
        $this->setWorkspaceId(1);

        // Publish workspace record for tt_content uid=10
        $cmd = [
            'tt_content' => [
                10 => [
                    'version' => [
                        'action' => 'publish',
                        'swapWith' => $this->getWorkspaceVersionUid('tt_content', 10, 1),
                    ],
                ],
            ],
        ];

        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start([], $cmd);
        $dataHandler->process_cmdmap();

        self::assertEmpty($dataHandler->errorLog);

        // Switch to LIVE and verify
        $this->setWorkspaceId(0);
        $row = \TYPO3\CMS\Backend\Utility\BackendUtility::getRecord('tt_content', 10);

        self::assertSame('Modified In Workspace', $row['header']);
    }

    /**
     * Helper: Get the uid of the workspace version of a record.
     */
    private function getWorkspaceVersionUid(string $table, int $liveUid, int $workspaceId): int
    {
        $queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getQueryBuilderForTable($table);
        $queryBuilder->getRestrictions()->removeAll();

        $row = $queryBuilder
            ->select('uid')
            ->from($table)
            ->where(
                $queryBuilder->expr()->eq('t3ver_oid', $liveUid),
                $queryBuilder->expr()->eq('t3ver_wsid', $workspaceId),
                $queryBuilder->expr()->eq('deleted', 0)
            )
            ->executeQuery()
            ->fetchAssociative();

        return (int)($row['uid'] ?? 0);
    }
}
```

### CSV Fixture File

Create `Tests/Functional/Fixtures/WorkspaceTestData.csv`:

```csv
"be_users"
,"uid","pid","username","password","admin","workspace_perms"
,1,0,"admin","$2y$12$placeholder",1,1

"sys_workspace"
,"uid","pid","title","adminusers","members","deleted"
,1,0,"Test Workspace","1","1",0

"pages"
,"uid","pid","title","slug","deleted","t3ver_oid","t3ver_wsid","t3ver_state"
,1,0,"Test Page","/test-page",0,0,0,0

"tt_content"
,"uid","pid","header","CType","bodytext","deleted","t3ver_oid","t3ver_wsid","t3ver_state"
,10,1,"Original Header","text","<p>Original</p>",0,0,0,0
,11,1,"Modified In Workspace","text","<p>Modified</p>",0,10,1,0
```

### Run Tests

**DDEV (recommended):**

```bash
# Run all workspace functional tests
ddev exec bin/phpunit -c Build/phpunit-functional.xml \
  Tests/Functional/WorkspaceAwareTest.php

# Run a single test method
ddev exec bin/phpunit -c Build/phpunit-functional.xml \
  --filter testWorkspaceOverlayReturnsModifiedContent \
  Tests/Functional/WorkspaceAwareTest.php

# Verbose output (shows each test name)
ddev exec bin/phpunit -c Build/phpunit-functional.xml \
  -v Tests/Functional/WorkspaceAwareTest.php
```

DDEV auto-provides the test database. No extra env vars needed.

**Non-DDEV (manual database config):**

```bash
# Set database credentials for the test runner
export typo3DatabaseHost="127.0.0.1"
export typo3DatabasePort="3306"
export typo3DatabaseUsername="root"
export typo3DatabasePassword="root"
export typo3DatabaseName="typo3_test"

bin/phpunit -c Build/phpunit-functional.xml \
  Tests/Functional/WorkspaceAwareTest.php
```

> The testing framework creates a **temporary database** per test case. Your env vars point to the DB server -- the framework handles the rest.

**Troubleshooting test failures:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Table 'sys_workspace' doesn't exist` | `workspaces` not in `$coreExtensionsToLoad` | Add `'workspaces'` to array |
| `Table 'be_users' has no column 'workspace_perms'` | Schema not created for test DB | Ensure `workspaces` is loaded before `setUp()` |
| `Access denied for user` | Wrong DB credentials | Check env vars or DDEV status (`ddev describe`) |
| `Call to undefined method setUpBackendUser` | Wrong testing-framework version | Use `typo3/testing-framework ^9.0` on TYPO3 v14 |
| `Record not found after DataHandler` | CSV fixture malformed | Verify CSV: first row is table name, second row is column headers, data rows start with comma |
