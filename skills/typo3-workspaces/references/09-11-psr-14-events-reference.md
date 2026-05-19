# 11. PSR-14 Events Reference

Continues `typo3-workspaces` from [full guide](full-guide.md).

## 11. PSR-14 Events Reference

### AfterRecordPublishedEvent

Fired after a record has been published from a workspace to live.

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Workspaces\Event\AfterRecordPublishedEvent;

#[AsEventListener]
final class AfterPublishListener
{
    public function __invoke(AfterRecordPublishedEvent $event): void
    {
        $table = $event->getTable();
        $liveId = $event->getRecordId();

        // Example: Clear external CDN cache after publishing
        if ($table === 'pages') {
            // Trigger CDN purge for the published page
        }

        // Example: Notify external system
        if ($table === 'tx_news_domain_model_news') {
            // Send webhook to newsletter system
        }
    }
}
```

### SortVersionedDataEvent

Fired after sorting data in the Workspaces backend module. Use to apply custom sorting.

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Workspaces\Event\SortVersionedDataEvent;

#[AsEventListener]
final class CustomWorkspaceSortListener
{
    public function __invoke(SortVersionedDataEvent $event): void
    {
        // Custom sorting logic for workspace module
        $data = $event->getData();
        // ... modify $data ...
        $event->setData($data);
    }
}
```

### Key Events

| Event | When Fired |
|-------|------------|
| `AfterCompiledCacheableDataForWorkspaceEvent` | After compiling cacheable workspace version data |
| `AfterDataGeneratedForWorkspaceEvent` | After generating all workspace version data |
| `AfterRecordPublishedEvent` | After a record is published to live |
| `GetVersionedDataEvent` | After preparing/cleaning workspace version data |
| `IsReferenceConsideredForDependencyEvent` | When evaluating whether a reference is considered a workspace dependency |
| `ModifyVersionDifferencesEvent` | When computing diffs between live and workspace version |
| `RetrievedPreviewUrlEvent` | When adjusting the preview URL for a workspace record |
| `SortVersionedDataEvent` | After sorting workspace version data in the module |

All events are in the `\TYPO3\CMS\Workspaces\Event\` namespace.
