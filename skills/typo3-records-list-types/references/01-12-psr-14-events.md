# 12. PSR-14 Events

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 12. PSR-14 Events

| Event | Purpose |
|-------|---------|
| `RegisterViewModesEvent` | Register, remove, or modify view types |
| `GridViewButtonBarListener` | Injects toggle buttons into DocHeader |
| `GridViewQueryListener` | Modifies database queries |
| `GridViewRecordActionsListener` | Collects record action buttons |

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
