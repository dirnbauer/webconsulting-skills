# 8. Debugging & Troubleshooting

Continues `typo3-workspaces` from [full guide](full-guide.md).

## 8. Debugging & Troubleshooting

### Quick Diagnostic Checklist

When workspaces "don't work", check these in order:

| # | Check | How |
|---|-------|-----|
| 1 | Extension installed? | `composer show typo3/cms-workspaces` |
| 2 | Workspace record exists? | List module on root page, filter System Records |
| 3 | User has workspace access? | Backend user/group > Mounts and Workspaces tab |
| 4 | User has LIVE access? | Same tab, "Live" checkbox must be checked |
| 5 | Table is versioningWS? | Check `$GLOBALS['TCA'][<table>]['ctrl']['versioningWS']` |
| 6 | DB columns exist? | `DESCRIBE <table>` -- look for `t3ver_oid`, `t3ver_wsid`, `t3ver_state` |
| 7 | DB mounts correct? | User/group must have DB mounts covering the pages being edited |
| 8 | File mounts correct? | User/group must have file mounts for media access |
| 9 | Schema up to date? | `bin/typo3 extension:setup` (or your project's schema-update wrapper) |
| 10 | Cache cleared? | `bin/typo3 cache:flush` |

### SQL Queries for Debugging (DDEV Local Only)

```sql
-- Check if workspace records exist
SELECT uid, title, adminusers, members, publish_access
FROM sys_workspace
WHERE deleted = 0;

-- Check versioned records for a specific page
SELECT uid, pid, t3ver_oid, t3ver_wsid, t3ver_state, t3ver_stage, header
FROM tt_content
WHERE t3ver_wsid > 0
  AND deleted = 0
ORDER BY t3ver_wsid, t3ver_oid;

-- Find orphaned workspace records (pointing to deleted live records)
SELECT ws.uid AS ws_uid, ws.t3ver_oid, ws.t3ver_wsid, ws.header
FROM tt_content ws
LEFT JOIN tt_content live ON ws.t3ver_oid = live.uid
WHERE ws.t3ver_wsid > 0
  AND ws.deleted = 0
  AND (live.uid IS NULL OR live.deleted = 1);

-- Check workspace-enabled tables
SELECT TABLE_NAME
FROM information_schema.COLUMNS
WHERE COLUMN_NAME = 't3ver_oid'
  AND TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME;

-- Inspect backend user's workspace permissions
SELECT
    bu.uid,
    bu.username,
    bu.workspace_perms,
    GROUP_CONCAT(bg.title SEPARATOR ', ') AS groups,
    GROUP_CONCAT(bg.workspace_perms SEPARATOR ', ') AS group_ws_perms
FROM be_users bu
LEFT JOIN be_users_be_groups_mm mm ON bu.uid = mm.uid_local
LEFT JOIN be_groups bg ON mm.uid_foreign = bg.uid
WHERE bu.deleted = 0
  AND bu.disable = 0
GROUP BY bu.uid, bu.username, bu.workspace_perms;

-- Check sys_log for workspace operations
SELECT
    FROM_UNIXTIME(tstamp) AS time,
    userid,
    action,
    details,
    tablename,
    recuid,
    workspace
FROM sys_log
WHERE workspace > 0
ORDER BY tstamp DESC
LIMIT 50;
```

### Programmatic Permission Check

```php
<?php

declare(strict_types=1);

use TYPO3\CMS\Core\Context\Context;
use TYPO3\CMS\Core\Utility\GeneralUtility;

// Get current workspace ID
$workspaceId = GeneralUtility::makeInstance(Context::class)
    ->getPropertyFromAspect('workspace', 'id', 0);

// Table modify permission (does not replace full workspace record ACL — use FormEngine/DataHandler for authoritative checks)
$mayModifyTable = $GLOBALS['BE_USER']->check('tables_modify', 'tt_content');

// Creating new records in workspace: BackendUserAuthentication API name is workspaceCanCreateNewRecord(string $table): bool (no $pageId)
$canCreate = $GLOBALS['BE_USER']->workspaceCanCreateNewRecord('tt_content');

// Workspace membership / role for the current user
$workspaceAccess = $GLOBALS['BE_USER']->checkWorkspace($workspaceId);
// Returns array|false — `_ACCESS` may be `admin`, `owner`, `member`, `online`, or `false` depending on context (see Core source for your minor)
```

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Records not visible in workspace | `versioningWS = false` on table | Set `versioningWS = true`, then run `extension:setup` (or your project's schema-update wrapper) |
| Workspace changes visible on live site | Missing `WorkspaceRestriction` in custom query | Add `FrontendRestrictionContainer` or manual `WorkspaceRestriction` |
| "Editing not possible" error | User lacks edit permission or stage access | Check user/group `tables_modify`, DB mounts, workspace membership |
| Preview shows wrong content | Missing `versionOL()` call in extension | Add `BackendUtility::workspaceOL()` or `PageRepository->versionOL()` after query |
| Publish does nothing | Content not in "Ready to publish" stage | Advance content through stages, or disable stage restriction |
| File changed in all workspaces | Files are not versioned (by design) | Upload new files with unique names instead of overwriting |
| Translation missing in workspace | Language not allowed in workspace | Set `options.workspaces.allowed_languages.<wsId>` TSconfig |
| Auto-publish not working | Scheduler task not configured or not running | Create "Workspaces auto-publication" task, verify cron job |
| Workspace selector not visible | User has no workspace access | Assign user/group as workspace member or owner |
