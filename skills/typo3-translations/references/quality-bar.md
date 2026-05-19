# Quality Bar

Continues `typo3-translations` from [full guide](full-guide.md).

## Quality Bar

- The skill starts with TYPO3 13-compatible output unless the task is clearly
  v14-only.
- TYPO3 14 output is preferred when compatibility constraints allow it.
- Shared TYPO3 13+14 branches stay on XLIFF 1.2 and `LLL:EXT:`.
- New or converted v14-only label files use the XLIFF 2.0 structure
  intentionally.
- Source and target files stay structurally aligned.
- Keys are stable, namespaced, and readable.
- ICU strings keep placeholder names intact and use named runtime arguments.
- TYPO3 APIs resolve labels; no custom XML label loader is introduced.
- All changed files parse as XML and labels are smoke-tested after cache flush.
