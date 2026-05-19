# 13. Extending

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 13. Extending

### Override Templates via TypoScript

TypoScript goes under the **plugin namespace** `module.tx_recordsgridview` (historical key from the extension’s early name). The extension key remains `records_list_types`.

```typoscript
module.tx_recordsgridview {
    view {
        templateRootPaths.100 = EXT:your_extension/Resources/Private/Templates/RecordsListTypes/
        partialRootPaths.100 = EXT:your_extension/Resources/Private/Partials/RecordsListTypes/
        layoutRootPaths.100 = EXT:your_extension/Resources/Private/Layouts/RecordsListTypes/
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

```php
class CustomThumbnailService extends ThumbnailService
{
    public function getThumbnailForRecord(string $table, array $record, string $imageField): ?FileInterface
    {
        if ($table === 'tx_yourext_domain_model_item') {
            return $this->getFromExternalSource($record);
        }
        return parent::getThumbnailForRecord($table, $record, $imageField);
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

```javascript
// Event prefix `recordsGridview:` matches the historical extension codename (same story as TypoScript `module.tx_recordsgridview`).
document.addEventListener('recordsGridview:viewModeChanged', (event) => {
    console.log('View mode changed to:', event.detail.mode);
});
```
