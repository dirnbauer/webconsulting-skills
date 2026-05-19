# 4. DataHandler Setup Script

Continues `typo3-workspaces` from [full guide](full-guide.md).

## 4. DataHandler Setup Script

### CLI Command: Create Workspace with DataHandler

```php
<?php

declare(strict_types=1);

namespace MyVendor\MySitepackage\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

/**
 * CLI command to create a workspace with base configuration.
 *
 * With `autoconfigure: true` in `Services.yaml`, `#[AsCommand]` is enough — no `console.command` tag needed.
 */
#[AsCommand(
    name: 'workspace:setup',
    description: 'Create a workspace with backend group and base configuration',
)]
final class SetupWorkspaceCommand extends Command
{

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);

        // Step 1: Create backend user group for workspace editors
        $data = [];
        $data['be_groups']['NEW_ws_group'] = [
            'pid' => 0,
            'title' => 'Workspace Editors',
            'description' => 'Backend group for workspace editing access',
            // Grant access to common tables
            'tables_modify' => 'pages,tt_content,sys_file_reference',
            'tables_select' => 'pages,tt_content,sys_file_reference,sys_file',
            // Grant LIVE workspace access
            'workspace_perms' => 1,
            // Page types allowed
            'pagetypes_select' => '1,3,4,6,7,199,254',
            // Explicitly allow content types
            'explicit_allowdeny' => '',
        ];

        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        if (!empty($dataHandler->errorLog)) {
            $io->error('Failed to create backend group: ' . implode(', ', $dataHandler->errorLog));
            return Command::FAILURE;
        }

        $groupUid = $dataHandler->substNEWwithIDs['NEW_ws_group'] ?? 0;
        $io->success('Created backend group "Workspace Editors" (uid=' . $groupUid . ')');

        // Step 2: Create the custom workspace
        $data = [];
        $data['sys_workspace']['NEW_workspace'] = [
            'pid' => 0,
            'title' => 'Staging Workspace',
            'description' => 'Content staging workspace for preview and review before publishing',
            'adminusers' => 'be_groups_' . $groupUid,
            'members' => 'be_groups_' . $groupUid,
            // Stages: default stages (Editing, Ready to publish) are always available
            // Publish access: 0 = no restriction, 1 = only publish-stage content, 2 = only owners can publish
            'publish_access' => 0,
            // Allow editing of non-versionable records (live edit)
            // Field name matches Core TCA / DB column (historical spelling "notificaton")
            'edit_allow_notificaton_settings' => 0,
        ];

        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        $dataHandler->start($data, []);
        $dataHandler->process_datamap();

        if (!empty($dataHandler->errorLog)) {
            $io->error('Failed to create workspace: ' . implode(', ', $dataHandler->errorLog));
            return Command::FAILURE;
        }

        $wsUid = $dataHandler->substNEWwithIDs['NEW_workspace'] ?? 0;
        $io->success('Created workspace "Staging Workspace" (uid=' . $wsUid . ')');

        $io->section('Next Steps');
        $io->listing([
            'Assign backend users to the "Workspace Editors" group',
            'Configure DB mounts and file mounts on the group',
            'Set up Scheduler tasks: "Workspaces auto-publication" + "Workspaces cleanup preview links"',
            'Configure TSconfig: options.workspaces.previewLinkTTLHours = 48',
            'Test: switch to the workspace in the backend sidebar and edit a page',
        ]);

        return Command::SUCCESS;
    }
}
```

**Run:**

```bash
# DDEV
ddev exec bin/typo3 workspace:setup

# Non-DDEV
bin/typo3 workspace:setup
```

### SQL Setup (LOCAL DDEV ONLY)

> **WARNING: These SQL queries are for LOCAL DDEV development environments ONLY.**
> **NEVER run raw SQL on production.** Use the DataHandler CLI command above instead.
> Raw SQL bypasses DataHandler, reference index, history, and cache clearing.

```sql
-- ============================================================
-- LOCAL DDEV ONLY - Workspace base configuration
-- Save this block as setup-workspace.sql, then run: ddev mysql < setup-workspace.sql
-- ============================================================

-- 1. Create backend user group for workspace editors
INSERT INTO be_groups (pid, title, description, workspace_perms, tables_modify, tables_select, pagetypes_select, tstamp, crdate)
VALUES (
    0,
    'Workspace Editors',
    'Backend group for workspace editing access',
    1,  -- 1 = access to LIVE workspace
    'pages,tt_content,sys_file_reference',
    'pages,tt_content,sys_file_reference,sys_file',
    '1,3,4,6,7,199,254',
    UNIX_TIMESTAMP(),
    UNIX_TIMESTAMP()
);

SET @group_uid = LAST_INSERT_ID();

-- 2. Create custom workspace
INSERT INTO sys_workspace (pid, title, description, adminusers, members, publish_access, tstamp, crdate)
VALUES (
    0,
    'Staging Workspace',
    'Content staging workspace for preview and review before publishing',
    CONCAT('be_groups_', @group_uid),
    CONCAT('be_groups_', @group_uid),
    0,  -- 0 = no publish restriction
    UNIX_TIMESTAMP(),
    UNIX_TIMESTAMP()
);

SET @ws_uid = LAST_INSERT_ID();

-- 3. Verify
SELECT 'Backend Group' AS type, @group_uid AS uid, 'Workspace Editors' AS title
UNION ALL
SELECT 'Workspace' AS type, @ws_uid AS uid, 'Staging Workspace' AS title;

-- 4. Check existing workspace-enabled tables
SELECT TABLE_NAME
FROM information_schema.COLUMNS
WHERE COLUMN_NAME = 't3ver_oid'
  AND TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME;
```

```bash
# Run in DDEV:
ddev mysql < setup-workspace.sql
```
