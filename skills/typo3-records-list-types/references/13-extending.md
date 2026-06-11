# 13. Extending

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 13. Extending

### Override Templates via TSconfig

Template, partial, and layout overrides are configured per view type in page TSconfig via `templateRootPath` / `partialRootPath` / `layoutRootPath` (resolved by `ViewTypeRegistry::getTemplatePaths()`; custom paths are prepended before the extension's own `Resources/Private/` defaults).

```tsconfig
mod.web_list.viewMode.types {
    grid {
        templateRootPath = EXT:your_extension/Resources/Private/Templates/
        partialRootPath = EXT:your_extension/Resources/Private/Partials/
        layoutRootPath = EXT:your_extension/Resources/Private/Layouts/
    }
}
```

### Custom Record Actions

Listen to `ModifyRecordListRecordActionsEvent` (TYPO3 Core event):

```php
use TYPO3\CMS\Backend\RecordList\Event\ModifyRecordListRecordActionsEvent;
use TYPO3\CMS\Backend\Template\Components\ActionGroup;
use TYPO3\CMS\Backend\Template\Components\ComponentFactory;
use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Imaging\IconFactory;
use TYPO3\CMS\Core\Imaging\IconSize;

#[AsEventListener]
final class CustomRecordActionListener
{
    public function __construct(
        private readonly ComponentFactory $componentFactory,
        private readonly IconFactory $iconFactory,
    ) {}

    public function __invoke(ModifyRecordListRecordActionsEvent $event): void
    {
        $record = $event->getRecord();
        if ($record->getMainType() === 'tx_yourext_domain_model_item') {
            $event->setAction(
                action: $this->componentFactory
                    ->createLinkButton()
                    ->setHref('/my/custom/action?uid=' . $record->getUid())
                    ->setTitle('My Action')
                    ->setIcon($this->iconFactory->getIcon('actions-open', IconSize::SMALL)),
                actionName: 'myCustomAction',
                group: ActionGroup::secondary,
                after: 'edit'
            );
        }
    }
}
```

### Custom Thumbnail Logic

`ThumbnailService` exposes this public API:

```php
public function getFirstImage(string $table, int $uid, string $fieldName): ?FileInterface
public function getAllImages(string $table, int $uid, string $fieldName): array
public function getThumbnailUrl(FileInterface $file, int $width = self::DEFAULT_WIDTH, int $height = self::DEFAULT_HEIGHT): ?string
public function getThumbnailData(string $table, int $uid, string $fieldName): array  // {file, url, exists}
public function getFirstFileReference(string $table, int $uid, string $fieldName): ?FileReference
```

Override an entry point, e.g.:

```php
class CustomThumbnailService extends ThumbnailService
{
    public function getFirstImage(string $table, int $uid, string $fieldName): ?FileInterface
    {
        if ($table === 'tx_yourext_domain_model_item') {
            return $this->getFromExternalSource($table, $uid);
        }
        return parent::getFirstImage($table, $uid, $fieldName);
    }
}
```

Register override in `Services.yaml`:

```yaml
services:
  Webconsulting\RecordsListTypes\Service\ThumbnailService:
    class: YourVendor\YourExtension\Service\CustomThumbnailService
```

### JavaScript Hooks

The extension does not dispatch custom namespaced events. The shipped modules (`GridViewActions.js`, `HistoryOverlay.js`, `RecordFilters.js`) dispatch standard TYPO3/DOM events you can listen to:

```javascript
// Fired on the top document after drag-drop moves a page record
top.document.addEventListener('typo3:pagetree:refresh', () => {
    console.log('Page tree refreshed after record move');
});

// Fired on the clipboard panel after clipboard actions
document.querySelector('typo3-backend-clipboard-panel')
    ?.addEventListener('typo3:clipboard:update', () => {
        console.log('Clipboard contents changed');
    });
```
