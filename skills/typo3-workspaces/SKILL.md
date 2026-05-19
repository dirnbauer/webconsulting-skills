---
name: "typo3-workspaces"
description: "Guides TYPO3 Workspaces versioning, staging, publishing, overlays, workspace-aware queries, file limitations, permissions, frontend preview, diagnostics, repair, and tests. Use when the user works with TYPO3 workspaces, draft content, staged publishing, versioning, workspace overlays, review workflows, file collections, or workspace-specific bugs."
compatibility: "TYPO3 14.x"
metadata:
  version: "2.0.0"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---
# TYPO3 Workspaces

> Source: https://github.com/dirnbauer/webconsulting-skills

> **Compatibility:** TYPO3 v14.x
> All code examples in this skill are designed to work on TYPO3 v14.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## Sources

This skill is based on 17 authoritative sources:

1. [TYPO3 Workspaces Extension Docs](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Index.html)
2. [Versioning (Workspaces Extension)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Administration/Versioning/Index.html)
3. [Creating a Custom Workspace](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Administration/CustomWorkspace/Index.html)
4. [Configuration Options (Workspaces)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Administration/Configuration/Index.html)
5. [PSR-14 Events (Workspaces)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Events/Index.html)
6. [Versioning & Workspaces (TYPO3 Explained / Core API)](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Workspaces/Index.html)
7. [TCA versioningWS Reference](https://docs.typo3.org/m/typo3/reference-tca/main/en-us/Ctrl/Index.html#confval-ctrl-versioningws)
8. [Restriction Builder (TYPO3 Explained / Doctrine DBAL)](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/DoctrineDbal/RestrictionBuilder/Index.html)
9. [b13 Blog: The Elegant Efficiency of TYPO3 Overlays (Benni Mack)](https://b13.com/blog/mastering-localization-and-content-staging)
10. [Scheduler Tasks (Workspaces)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/Administration/Scheduler/Index.html)
11. [Users Guide (Workspaces)](https://docs.typo3.org/c/typo3/cms-workspaces/main/en-us/UsersGuide/Index.html)
12. [TYPO3-CORE-SA-2025-022: Information Disclosure in Workspaces Module](https://typo3.org/security/advisory/typo3-core-sa-2025-022)
13. [Localized Content Guide](https://docs.typo3.org/m/typo3/guide-frontendlocalization/main/en-us/LocalizedContent/Index.html)
14. [File Collections (TYPO3 Explained)](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fal/Collections/Index.html)
15. [FAL Database Architecture](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fal/Architecture/Database.html)
16. [Forge Bug #60343: sys_file_metadata does not recognize workspace](https://forge.typo3.org/issues/60343)
17. [Forge Feature #97923: Combined folder_identifier field for sys_file_collection](https://forge.typo3.org/issues/97923)

## 1. Core Concepts

### What Are Workspaces?

Workspaces allow editors to prepare content changes **without affecting the live website**. Changes go through a configurable review process before publication.

There are two types:

- **LIVE workspace** (ID=0): The default state. Every change is immediately visible. Access must be **explicitly granted** to backend users/groups.
- **Custom workspaces** (ID>0): Safe editing environments. Changes are versioned, previewable, and go through stages before going live.

### How Versioning Works (Database Level)

Offline (workspace) versions live in the **same database table** as live records. They are identified by:

| Field | Purpose |
|-------|---------|
| `t3ver_oid` | Points to the live record's `uid` (0 for live records and workspace-new records) |
| `t3ver_wsid` | Workspace ID this version belongs to (0 for live) |
| `t3ver_state` | Special state flags (see below) |
| `t3ver_stage` | Workflow stage (0=editing, -10=ready to publish) |
| `pid` | Real page ID (same as the live record's pid) |

> **Note:** Before TYPO3 v11, offline versions had `pid = -1`. Since v11 (Breaking #92497), workspace records store their **real pid**. If you encounter `pid = -1` in legacy code or documentation, it is outdated.

**t3ver_state values (TYPO3 v14):**

| Value | Meaning |
|-------|---------|
| `0` | Default: workspace modification of existing live record |
| `1` | New record created exclusively in workspace (no live counterpart) |
| `2` | Delete placeholder (record marked for deletion upon publish) |
| `4` | Move pointer (record to be moved upon publish, stores new pid/sorting) |

> **Removed in v11:** `t3ver_state = -1` (old "new version" pendant), `t3ver_state = 3` (old "move placeholder"), and the `t3ver_move_id` field. If you see these values in legacy code, they are not used on TYPO3 v14.

### The Overlay Mechanism

TYPO3 **always fetches live records first**, then overlays workspace versions on top. For translations with workspaces, the chain is:

1. Fetch default language, live record (language=0, workspace=0)
2. Overlay workspace version (search for `t3ver_oid=<uid>` AND `t3ver_wsid=<current_ws>`)
3. Overlay language translation (search for `l10n_parent=<uid>` in target language)
4. Overlay workspace version of translation

The `uid` of the live record is **always preserved** during overlay -- this keeps all references and links intact.

### Publishing Workflow

- **Publish**: Draft content replaces live content through the workspace publish process.
- TYPO3 v14 still accepts DataHandler `version` commands with **`action => 'publish'`** (preferred) or **`action => 'swap'`** (alias handled the same as publish in `DataHandlerHook`). The parameter key for the workspace version UID remains **`swapWith`**, not `uid`.
- Do not rely on historic **bidirectional workspace “swap modes”** on `sys_workspace` (removed in v11, #92206) — that is separate from the `swap` **keyword** in cmdmaps.

## 2. CRITICAL: File/FAL Limitation

> **Files (FAL) are NOT versioned.** This is the single most important limitation of TYPO3 Workspaces.
> See also Section 2a below for the additional **file collection** limitation (folder-based collections).

### What This Means

- Files in `fileadmin/` live exclusively in the **LIVE workspace**
- If you **overwrite** a file, the change affects **ALL workspaces immediately**
- `sys_file_reference` records are workspace-versioned; physical files and `sys_file` records are not versioned like content overlays
- Replacing files inside existing references can still have edge cases in workspace previews; test on your exact TYPO3 minor and prefer new filenames over in-place replacement when possible.

### The Predictable Filename Security Problem

**Scenario:** An editor creates a workspace version of a page replacing `geschaeftsbericht2024.pdf` with `geschaeftsbericht2025.pdf`. The workspace is NOT published yet. However:

1. The new PDF is uploaded to `fileadmin/` immediately (files are live!)
2. An external person guesses the URL by incrementing the year
3. `geschaeftsbericht2025.pdf` is accessible before the content element referencing it is published

This is a **real security/confidentiality risk**.

### Workarounds

**1. Use non-guessable filenames:**

```
# Instead of:
fileadmin/reports/geschaeftsbericht2025.pdf

# Use hashed/random names:
fileadmin/reports/gb-a8f3e2b1c9d4.pdf
```

**2. Store confidential files outside the web root:**

```php
// config/system/settings.php
// Use a private storage that is NOT publicly accessible
// Deliver files programmatically via a controller
```

**3. Use EXT:secure_downloads (leuchtfeuer/secure-downloads):**

Files are delivered through a PHP script that checks access permissions. No direct file URL access.

**4. Server-level protection for sensitive directories:**

```apache
# Apache (.htaccess in a subdirectory)
<IfModule mod_authz_core.c>
    Require all denied
</IfModule>
```

```nginx
# NGINX
location /fileadmin/confidential/ {
    deny all;
    return 403;
}
```

**5. Use separate file references per workspace version:**

Upload the new file with a different name. Do NOT overwrite the existing file. The workspace version of the content element references the new file, the live version keeps the old one. Upon publishing, both files exist but only the new one is referenced.

### Rules for Workspace-Safe File Handling

- **NEVER** overwrite files that are used in content elements across workspaces
- **ALWAYS** upload new files with unique names when preparing workspace content
- **NEVER** rely on "the page is not published yet" to protect file confidentiality
- **CONSIDER** EXT:secure_downloads for any confidential documents
- **AUDIT** `fileadmin/` for files with predictable naming patterns

## 2a. File Collections and Workspaces

> **File collections (`sys_file_collection`) are workspace-versioned at the record level, but folder-based collections resolve files from the live filesystem at runtime -- there is no database relation to overlay.**

### How File Collections Work

`sys_file_collection` stores three collection types, distinguished by the `type` field:

| `type` value | Resolution mechanism | Database relations involved |
|---|---|---|
| `static` (0) | `sys_file_reference` rows (`tablenames='sys_file_collection'`, `fieldname='files'`) | One `sys_file_reference` row per file |
| `folder` (1) | `folder_identifier` string (e.g. `1:/user_upload/gallery/`) | **None** -- no join table, no reference rows |
| `category` (2) | `category` uid resolved via `sys_category_record_mm` | MM table (handled via parent record overlay) |

The TCA for `sys_file_collection` has `versioningWS => true`. This means the **collection record itself** gets workspace versions with `t3ver_*` fields. However, the record-level versioning only versions the fields stored in `sys_file_collection` -- it does **not** version the files that the collection resolves.

### Workspace Safety per Collection Type

| Collection Type | Record versioned? | File binding versioned? | Physical files versioned? | Workspace-safe? |
|---|---|---|---|---|
| **Static** | Yes | Yes (`sys_file_reference` has `versioningWS = true`) | No | Partially safe |
| **Folder-based** | Yes (record only) | **No** -- no DB binding exists | No | **Not safe** |
| **Category-based** | Yes | Partially (category MM handled via parent overlay) | No | Partially safe |

### Why Folder-Based Collections Break Workspace Isolation

For folder-based collections, the "relation" between the collection and its files is **not a database relation**. The collection record stores only a `folder_identifier` string. When `FolderBasedFileCollection::loadContents()` is called, TYPO3 calls `$storage->getFilesInFolder()` to list files directly from the live storage driver. There is no overlay-capable database row between the collection and its files.

**Consequences:**

- Adding a file to the folder makes it visible in **all workspaces** immediately
- Removing a file from the folder removes it from **all workspaces** immediately
- Changing the `folder_identifier` field in a workspace version points to a different folder, but the folder contents themselves are always live
- The "File links" content element (`CType=uploads`) using a folder-based collection will show different files than intended during workspace preview if the folder contents changed after the workspace version was created

### Static Collections Are Safer

Static collections (`type=static`) bind files via `sys_file_reference` rows. Both `sys_file_collection` and `sys_file_reference` have `versioningWS = true`. When you add or remove a file from a static collection inside a workspace, TYPO3 creates workspace versions of the `sys_file_reference` rows. The binding between collection and file is versioned.

The remaining limitation: physical files (`sys_file`) are still not versioned (see Section 2). If you overwrite a file, it changes everywhere.

### Workarounds for Folder-Based Collections

**1. Prefer static collections when workspace isolation matters:**

Use `type=static` instead of `type=folder`. The file-to-collection binding is a `sys_file_reference` row, which is workspace-versioned.

**2. Use separate folders per workspace version:**

For folder-based collections, create a new folder for the workspace change (e.g. `gallery-v2/`) and change the `folder_identifier` in the workspace version of the collection record. The live version still points to the original folder.

**3. Do NOT modify shared folder contents while workspace drafts reference them:**

If a folder-based collection is used in workspace content, avoid adding or removing files from that folder until the workspace is published.

**4. Clean up old folders after publishing:**

Use `AfterRecordPublishedEvent` to remove obsolete folders after the workspace version is published:

```php
<?php

declare(strict_types=1);

namespace MyVendor\MyExtension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Resource\StorageRepository;
use TYPO3\CMS\Workspaces\Event\AfterRecordPublishedEvent;

#[AsEventListener]
final class CleanupOldCollectionFolderListener
{
    public function __construct(
        private readonly StorageRepository $storageRepository,
    ) {}

    public function __invoke(AfterRecordPublishedEvent $event): void
    {
        if ($event->getTable() !== 'sys_file_collection') {
            return;
        }

        // After publishing a folder-based collection, remove the old folder
        // if it is no longer referenced by any collection.
        // Implementation depends on your naming convention (e.g. gallery-v1/, gallery-v2/).
    }
}
```

### Rules for Workspace-Safe File Collections

- **PREFER** static collections (`type=static`) over folder-based when workspaces are used
- **NEVER** add or remove files from a folder that is referenced by a folder-based collection in an unpublished workspace
- **USE** separate folders per workspace version if folder-based collections are required
- **DOCUMENT** for editors that folder-based collections show live folder contents regardless of workspace state
- **TEST** file collection behavior in workspace preview before relying on it for editorial workflows

## 3. Installation & Setup Checklist

### Installation

```bash
# Composer (TYPO3 v14)
composer require typo3/cms-workspaces

# Non-Composer: activate in Admin Tools > Extensions
```

### Complete Setup Checklist

Use this checklist to verify your workspace setup is complete:

#### Extension & System

- [ ] `typo3/cms-workspaces` is installed and activated
- [ ] Database schema is up to date (`bin/typo3 extension:setup` or your project's equivalent schema-update wrapper)
- [ ] `typo3/cms-scheduler` is installed (required for auto-publish)
- [ ] Scheduler cron job is configured on server

#### Backend User Groups

- [ ] Workspace-specific backend user group created (e.g., "Workspace Editors")
- [ ] Group has **explicit LIVE workspace access** (Mounts and Workspaces tab > "Live" checkbox)
- [ ] Group has access to the custom workspace (assigned as owner or member in workspace record)
- [ ] DB mounts are set correctly (pages the group can edit)
- [ ] File mounts are set correctly (directories the group can access)
- [ ] Group has `tables_modify` permissions for all relevant tables
- [ ] Group has permissions on page types the workspace will contain

#### Backend Users

- [ ] Users are assigned to the workspace user group
- [ ] Users can see the workspace selector in the **backend sidebar** (v14.2+; earlier v14 builds may still show it in the top bar)
- [ ] Non-admin users have LIVE workspace access only if they need it

#### Workspace Record

- [ ] Workspace record created as System Record on root page (pid=0)
- [ ] Title and description set
- [ ] **Owners** assigned (use groups, not individual users)
- [ ] **Members** assigned (use groups, not individual users)
- [ ] Custom stages created if needed (between "Editing" and "Ready to publish")
- [ ] Notification settings configured per stage
- [ ] Mountpoints set if workspace should be restricted to specific page trees
- [ ] Publish date set if auto-publish is desired
- [ ] "Publish access" configured (restrict publishing to owners if needed)

#### Tables (TCA)

- [ ] All custom extension tables have `'versioningWS' => true` in `$GLOBALS['TCA'][<table>]['ctrl']`
- [ ] Tables that must NOT be versioned have `'versioningWS' => false`
- [ ] Tables requiring live-editing in workspace have `'versioningWS_alwaysAllowLiveEdit' => true`
- [ ] `t3ver_*` database columns exist (auto-created when `versioningWS = true`)

> **Inline / IRRE child tables (Deprecation [#106821](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Deprecation-106821-WorkspaceAwareInlineChildTablesAreEnforced.html)):** If `versioningWS` is missing on a child table, Core **logs a deprecation** and may **auto-add** the flag at TCA build time — it does **not** throw a hard error. Set the flag explicitly in TCA; it will become a **hard requirement in v15**.

#### Scheduler Tasks

- [ ] "Workspaces auto-publication" task created and enabled
- [ ] "Workspaces cleanup preview links" task created and enabled
- [ ] Cron frequency is appropriate (e.g., every 15 minutes)

#### TSconfig

- [ ] `options.workspaces.previewLinkTTLHours` set (default: 48)
- [ ] `options.workspaces.allowed_languages.<wsId>` set if language restrictions needed
- [ ] `workspaces.splitPreviewModes` configured if preview modes should be limited
- [ ] `options.workspaces.previewPageId` set for custom record preview pages


## Detailed Reference

Read [the full guide](references/full-guide.md) when the task needs detailed examples, long templates, troubleshooting matrices, appendices, or sections not included above. Keep this file unloaded for narrow tasks so the skill follows progressive disclosure.
