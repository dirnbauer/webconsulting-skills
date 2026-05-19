# v14-Only Changes

Continues `typo3-workspaces` from [full guide](full-guide.md).

## v14-Only Changes

> The following workspace changes apply **exclusively to TYPO3 v14**.

### "Freeze Editing" Removed **[v14 only]**

Workspace "Freeze Editing" feature has been removed (#107323). Workspaces can no longer be frozen to prevent editing. Remove any code that references `freezeEditingWorkspace` or relies on frozen workspace state.

### Workspace-Aware Inline Child Tables **[v14 only]**

All inline (IRRE) child tables used in workspace-enabled parent tables **should** have `'versioningWS' => true` in their TCA ctrl (#106821). On TYPO3 v14, a missing flag triggers a **deprecation** and Core may **auto-add** it at TCA compile time — set the flag explicitly in extensions now; it becomes a **hard requirement in v15**.

### Workspace Selector Moved to Sidebar **[v14.2+ only]**

The workspace selector has been moved from the top bar to the **backend sidebar**. Workspaces now support **color** and **description** fields for visual distinction in the sidebar selector. Update any documentation or screenshots referencing the top bar workspace switcher.

### Editor Information in Publish Module **[v14 only]**

The workspace "Publish" module now shows **editor information** (#106074) — which backend user last modified each record. This helps reviewers identify who made changes.

### `swap` vs `publish` in cmdmaps **[v14]**

`DataHandlerHook` treats **`swap` and `publish` as aliases** — both call `version_swap()`. Prefer **`action => 'publish'`** in new code. The workspace version UID must always be passed as **`swapWith`** (Core reads `(int)$value['swapWith']`):

```php
// ✅ Always pass the offline/workspace version uid as swapWith (live record id is the cmdmap key)
$cmd['tt_content'][10]['version'] = [
    'action' => 'publish',
    'swapWith' => $workspaceVersionUid,
];

// 'swap' still works as an alias but publish is clearer
$cmd['tt_content'][10]['version'] = ['action' => 'swap', 'swapWith' => $workspaceVersionUid];
```

---
