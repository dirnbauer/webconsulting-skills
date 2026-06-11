# 15. Workspace Support

Continues `typo3-powermail` from [full guide](full-guide.md).

## 15. Workspace Support

Powermail records (forms, pages, fields) fully support TYPO3 workspaces. When EXT:workspaces is
installed, editors can draft form changes in a workspace and publish them after review.

**Key points:**
- All powermail tables gain `t3ver_wsid`, `t3ver_oid`, `t3ver_state`, `t3ver_stage` columns
- Records with `t3ver_wsid > 0` are drafts (not visible in live frontend)
- Use **DataHandler** for workspace operations — it handles versioning automatically
- Raw SQL requires manually setting all `t3ver_*` columns on every INSERT
- Conditions (powermail_cond) must be in the **same workspace** as the form

**Workspace lifecycle:**
1. **Create** records in workspace → `t3ver_wsid = <ws_id>`, `t3ver_state = 1`
2. **Stage** for review → `t3ver_stage = 1`
3. **Publish** via backend module or CLI → records become live (`t3ver_wsid = 0`)

> **Detailed SQL and DataHandler examples:** See [SKILL-EXAMPLES.md](../SKILL-EXAMPLES.md#workspace-support)
> for complete workspace-aware queries, publishing workflows, and CLI options.
