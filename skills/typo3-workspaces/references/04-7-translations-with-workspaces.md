# 7. Translations with Workspaces

Continues `typo3-workspaces` from [full guide](full-guide.md).

## 7. Translations with Workspaces

### How the Dual Overlay Works

When rendering a page in a workspace with a non-default language:

```
Live Record (lang=0, ws=0)
  └─► Workspace Overlay (lang=0, ws=1)     ← workspace version of default language
  └─► Language Overlay (lang=1, ws=0)       ← translation of live record
        └─► Workspace Overlay (lang=1, ws=1) ← workspace version of translation
```

TYPO3 handles this automatically when using `PageRepository->versionOL()` and `PageRepository->getLanguageOverlay()`.

### Creating Translations in Workspace Context

When working in a workspace:

1. The **default language record** is versioned first (if modified)
2. Translations created in a workspace are single records with `t3ver_state = 1` (workspace-new)
3. The `l10n_parent` field points to the **live** default language record UID
4. Modified translations have `t3ver_oid` pointing to the live translation UID

Database example for a tt_content record translated to French in workspace 1:

| uid | pid | t3ver_wsid | t3ver_oid | t3ver_state | l10n_parent | sys_language_uid | header |
|-----|-----|------------|-----------|-------------|-------------|------------------|--------|
| 11 | 20 | 0 | 0 | 0 | 0 | 0 | Article #1 |
| 31 | 20 | 1 | 0 | 1 | 11 | 1 | Article #1 (fr) |

> **Note:** On TYPO3 v14, workspace-new records are a **single row** with `t3ver_state = 1` and real `pid`. The old two-row pattern (placeholder + version with `pid = -1` and `t3ver_state = -1`) was removed in v11.

### Language Restrictions per Workspace

Restrict which languages a user can edit in a specific workspace:

```
# User TSconfig
# Allow only French (uid=1) and German (uid=2) in workspace 3
options.workspaces.allowed_languages.3 = 1,2
```

### File Translations with Workspaces

The same file limitation applies to translations:

- **Translated file references** (`sys_file_reference` with `sys_language_uid > 0`) ARE versioned
- **Physical files** are NOT versioned
- If a translation needs a different PDF/image, upload it as a **new file** with a unique name
- Do NOT overwrite files shared between language versions
