# 8. Workspace-Aware Operations

Continues `typo3-datahandler` from [full guide](full-guide.md).

## 8. Workspace-Aware Operations

When working with workspaces:

```php
<?php
declare(strict_types=1);

// Check if we're in a workspace
$workspaceId = $GLOBALS['BE_USER']->workspace;

if ($workspaceId > 0) {
    // In workspace - DataHandler will create versioned records
    // Use the wsol (workspace overlay) for reading
}

// Force live workspace for specific operations
$previousWorkspace = $GLOBALS['BE_USER']->workspace;
$GLOBALS['BE_USER']->setWorkspace(0);

// ... perform operations ...

$GLOBALS['BE_USER']->setWorkspace($previousWorkspace);
```
