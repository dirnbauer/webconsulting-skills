# 9a. Workspace Diagnostics and Repair Playbook

Continues `typo3-workspaces` from [full guide](full-guide.md).

## 9a. Workspace Diagnostics and Repair Playbook

Use this when a workspace UI says records are pending but publish does nothing,
records disappear from page-scoped review, preview differs from the database, or
editors report "stuck" workspace changes.

### First Rule: Separate Proven Database Bugs from Manual-Only Risks

Automatic checks can prove malformed workspace rows. They cannot prove editor
intent, overwritten physical files, folder contents, CDN cache state, or external
index state. Run automatic checks first, then work through manual-only risks only
if the database state is clean.

### Automatic Checks to Run

For projects with EXT:webcon_easy_workspace, use the built-in diagnostics module:

```bash
# Optional local seed set for testing the diagnostics module.
# Dry-run first; --execute writes deliberately broken local/demo data.
ddev typo3 webcon-easy-workspace:seed-diagnostics
ddev typo3 webcon-easy-workspace:seed-diagnostics --execute --page=664 --workspace=1
```

Then switch the backend to that workspace and open:

```
Content > Easy Workspace > Testing
Content > Easy Workspace > Diagnostics
```

Use **Testing** first when you want a report-style overview: grouped
health checks, pass/fail badges, seed fixture coverage, inline child publish
risks, manual-only risks, and a short "how to solve it" for each check. Use
**Diagnostics** when a testing report fails and you need exact affected records,
inspection SQL, and the detailed repair candidate list.

If the extension is not installed, run equivalent SQL checks manually:

```sql
-- Set this to the workspace you are inspecting.
SET @workspace_id := 1;

-- Live rows polluted with workspace fields
SELECT uid,pid,t3ver_oid,t3ver_state
FROM tt_content
WHERE t3ver_wsid=0 AND (t3ver_oid<>0 OR t3ver_state<>0);

-- Workspace rows pointing to missing live rows
SELECT ws.uid, ws.pid, ws.t3ver_oid, ws.t3ver_wsid
FROM tt_content ws
LEFT JOIN tt_content live ON live.uid=ws.t3ver_oid AND live.deleted=0
WHERE ws.t3ver_wsid=@workspace_id AND ws.t3ver_oid>0 AND live.uid IS NULL;

-- Duplicate workspace versions for the same live row
SELECT t3ver_wsid, t3ver_oid, COUNT(*) AS duplicate_count, GROUP_CONCAT(uid ORDER BY uid) AS workspace_uids
FROM tt_content
WHERE t3ver_wsid=@workspace_id AND t3ver_oid>0
GROUP BY t3ver_wsid,t3ver_oid
HAVING COUNT(*) > 1;

-- Modified workspace rows with no live identity
SELECT uid,pid,t3ver_oid,t3ver_wsid,t3ver_state
FROM tt_content
WHERE t3ver_wsid=@workspace_id AND t3ver_oid=0 AND t3ver_state<>1;

-- Unsupported TYPO3 v14 workspace state.
-- Valid values are 0=modified/live, 1=new placeholder,
-- 2=delete placeholder, 4=move pointer.
SELECT uid,pid,t3ver_oid,t3ver_wsid,t3ver_state
FROM tt_content
WHERE t3ver_wsid=@workspace_id AND t3ver_state NOT IN (0,1,2,4);

-- Workspace file references whose owning record no longer exists
SELECT ref.uid, ref.pid, ref.uid_local, ref.uid_foreign, ref.tablenames, ref.fieldname
FROM sys_file_reference ref
LEFT JOIN pages owner ON ref.tablenames='pages' AND owner.uid=ref.uid_foreign AND owner.deleted=0
WHERE ref.t3ver_wsid=@workspace_id
  AND ref.tablenames='pages'
  AND ref.uid_foreign>0
  AND owner.uid IS NULL;
```

Repeat these table-specific checks for every workspace-aware TCA table. Include
generated inline child tables such as Content Blocks collection tables
(`accordion_items`, `article_grid_items`, etc.) when they carry `versioningWS`.
For `sys_file_reference`, repeat the owner join per `tablenames` value
(`pages`, `tt_content`, custom records, etc.) or use TYPO3's TCA metadata to
resolve the owner table dynamically.

### Failure Classes and How to Solve Them

| Failure class | How to find it | Why it happens | How to solve it |
|---|---|---|---|
| Publish says success but publishes `0` records | Log or inspect the publish payload and the validated backend selection | Client posted child tables, but the backend allow-list rejected them | Accept workspace-aware hidden child tables intentionally, especially generated Content Blocks tables with `foreign_table_parent_uid`; return an error for empty validated selections |
| Child-only changes shown under a live parent do not publish | Compare UI parent rows with posted `publishRecords`; query child table `t3ver_wsid>0` rows | Parent `tt_content` is already live; only inline child rows are pending | Publish the child rows themselves through DataHandler cmdmap (`$cmd[$childTable][$liveUid]['version'] = ['action' => 'publish', 'swapWith' => $workspaceUid]`) |
| Workspace row points to missing live row | `t3ver_wsid>0 AND t3ver_oid>0` with no live row | Live row was deleted outside the workspace flow or restored incompletely | Restore the live row from backup, reconnect `t3ver_oid` to the correct live UID, or discard the workspace row through DataHandler after editorial review |
| Duplicate workspace versions for one live row | Group by `t3ver_wsid,t3ver_oid` and count > 1 | Concurrent imports, broken repair scripts, or interrupted copy/version operations | Compare history/timestamps, keep the intended draft, then discard or merge the others with DataHandler |
| Workspace row has no live identity | `t3ver_wsid>0 AND t3ver_oid=0 AND t3ver_state<>1` | Row was inserted directly or lost its version state | If it is new workspace content, repair to `t3ver_state=1`; otherwise reconnect to live UID or discard |
| Live row has workspace fields | `t3ver_wsid=0 AND (t3ver_oid<>0 OR t3ver_state<>0)` | Manual SQL repair or bad import polluted live rows | Confirm it is a real live row, then reset `t3ver_oid=0,t3ver_state=0`; rebuild refindex/cache afterwards |
| Unsupported `t3ver_state` | `t3ver_state NOT IN (0,1,2,4)` on TYPO3 v14 | Legacy data or invalid import | Map to the intended v14 state or discard the row. Do not guess without history |
| Inline child missing parent | Child table has `foreign_table_parent_uid` pointing to missing `tt_content` | Parent was deleted/restored independently; generated child row survived | Restore the parent, update the parent UID, or discard the orphan child through DataHandler |
| File reference missing owner | `sys_file_reference.t3ver_wsid>0` where `tablenames:uid_foreign` no longer exists | Page/content owner was deleted or restored incompletely, leaving publishable image/file rows behind | Restore the owner, reconnect `uid_foreign` to the intended record, or discard the orphan file reference through DataHandler |

### Manual-Only Failures

These cannot be reliably detected by record scans:

| Failure | Why automatic checks cannot prove it | How to solve it |
|---|---|---|
| Physical FAL file overwritten | `sys_file` and the file bytes are live, not workspace-versioned | Restore the old file, upload changed files under new names, then update `sys_file_reference` in the workspace |
| Folder-based file collection drift | Folder contents are resolved from live storage at runtime | Use static collections for workspace-controlled lists or separate folders per workspace change |
| External index/cache drift | Search/CDN/render caches are outside workspace DB state | Rebuild indexes, flush affected caches, compare rendered live and workspace URLs |
| Editor intent conflict | Two rows can both be structurally valid | Use record history and editor confirmation before publish/discard/repair |

### Repair Rules

- Prefer TYPO3 DataHandler for publish, discard, move, delete, and relation
  changes. Direct SQL is a last resort for broken metadata that DataHandler
  cannot load anymore.
- Before direct SQL repair, export the affected rows and record the exact
  workspace ID, table, workspace UID, live UID, `t3ver_state`, `pid`, and
  references.
- After direct repair, rebuild reference indexes and flush caches. Then rerun
  diagnostics and compare preview/live output.
- Never "fix" duplicate drafts by deleting random rows. Determine editor intent
  from history, timestamps, field diffs and user confirmation.
