# 12. PSR-14 Events

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 12. PSR-14 Events

The extension dispatches a single PSR-14 event:

| Event | Purpose |
|-------|---------|
| `RegisterViewModesEvent` | Register, remove, or modify view types |

It also ships listeners for TYPO3 Core events:

| Listener | Core event listened to | Purpose |
|----------|------------------------|---------|
| `GridViewButtonBarListener` | `ModifyButtonBarEvent` | Injects view toggle buttons into DocHeader |
| `GridViewQueryListener` | `ModifyDatabaseQueryForRecordListingEvent` | Modifies database queries for record listings |
| `GridViewRecordActionsListener` | `ModifyRecordListRecordActionsEvent` | Collects record action buttons |
| `RecordFilterButtonBarListener` | `ModifyButtonBarEvent` | Adds filter controls to DocHeader |
| `RecordFilterQueryListener` | `ModifyDatabaseQueryForRecordListingEvent` | Applies active filters to record queries |
| `RecordFilterAdditionalContentListener` | `RenderAdditionalContentToRecordListEvent` | Renders the filter UI above the record list |

### Register a View Type via Event

```php
use TYPO3\CMS\Core\Attribute\AsEventListener;
use Webconsulting\RecordsListTypes\Event\RegisterViewModesEvent;

#[AsEventListener]
final class RegisterKanbanViewListener
{
    public function __invoke(RegisterViewModesEvent $event): void
    {
        $event->addViewMode('kanban', [
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:viewMode.kanban',
            'icon' => 'module-list',
            'description' => 'Kanban board view',
        ]);
    }
}
```

### Event API

```php
$event->addViewMode(string $id, array $config): void
$event->removeViewMode(string $id): void
$event->hasViewMode(string $id): bool
$event->modifyViewMode(string $id, array $config): void
$event->getViewModes(): array
```
