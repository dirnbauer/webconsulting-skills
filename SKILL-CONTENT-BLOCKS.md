---
name: content-blocks-shared
description: Shared repository guide for TYPO3 Content Blocks usage, migration, and cross-skill routing. Use when Content Blocks is the cross-cutting topic across update, migration, DataHandler, testing, or extension design work.
---

# Shared Content Blocks Guide

Use this root guide when Content Blocks is the shared concern and you need a stable entry point before choosing the domain-specific skill.

## Start Here

Reach for this guide when the task is about:

- creating new Content Blocks
- converting classic TCA and SQL to Content Blocks
- using DataHandler with Content Blocks records
- testing or documenting Content Blocks-based extensions
- deciding whether Content Blocks is the right migration target

Then route to the relevant primary skill:

| Need | Go to |
| --- | --- |
| Core Content Blocks modeling | `skills/typo3-content-blocks/SKILL.md` |
| Migration from classic TCA/SQL | `skills/typo3-content-blocks/SKILL-MIGRATION.md` |
| Programmatic record handling | `skills/typo3-datahandler/SKILL.md` |
| Upgrade planning | `skills/typo3-update/SKILL.md` |
| Extension migration workflow | `skills/typo3-extension-upgrade/SKILL.md` |
| Local DDEV setup and iteration | `skills/typo3-ddev/SKILL.md` |
| Tests for Content Blocks projects | `skills/typo3-testing/SKILL.md` |
| Docs and examples | `skills/typo3-docs/SKILL.md` |

## Core Content Blocks Focus

Prioritize these ideas:

1. Treat `config.yaml` as the single source of truth.
2. Prefer generated structure over hand-maintained duplicate TCA and SQL.
3. Keep field naming, prefixes, and CType naming predictable.
4. Migrate incrementally when replacing classic elements in live projects.

## Decision Rule

Content Blocks is usually the right fit for:

- new content elements
- structured records with mostly declarative fields
- projects that benefit from less duplicated configuration

It is not automatically the right fit for every case. Be more cautious when the feature is dominated by custom domain logic, controller-heavy Extbase behavior, or a time-critical upgrade where reducing migration risk matters more than modernization.

## Migration Checklist

- Inventory current TCA, SQL, TypoScript, templates, and migrations.
- Map old fields to new YAML identifiers before writing data migrations.
- Keep old and new variants side by side during rollout when needed.
- Move one content type at a time.
- Verify backend forms, frontend rendering, and data migration scripts.
- Remove obsolete classic files only after data and rendering are stable.

## Repository References

- `skills/typo3-content-blocks/SKILL.md`
- `skills/typo3-content-blocks/SKILL-MIGRATION.md`
- `skills/typo3-datahandler/SKILL.md`
- `skills/typo3-testing/SKILL.md`

This file replaces the old per-skill `SKILL-CONTENT-BLOCKS.md` copies. Keep shared Content Blocks guidance centralized here and let the owning domain skill provide the implementation detail.
