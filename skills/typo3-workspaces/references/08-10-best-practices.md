# 10. Best Practices

Continues `typo3-workspaces` from [full guide](full-guide.md).

## 10. Best Practices

### Pages with Content Elements (Standard Workflow)

1. Editor switches to the custom workspace via the backend sidebar selector (v14.2+)
2. Editor navigates to the page and edits content elements
3. TYPO3 automatically creates workspace versions of modified records
4. Editor previews via "View webpage" button (shows workspace version)
5. Editor sends changes to "Ready to publish" stage
6. Reviewer approves or sends back with comments
7. Publisher publishes to live (or auto-publish via Scheduler)

**Key points:**
- `pages` and `tt_content` have `versioningWS = true` by default
- FAL relations (images, media) are versioned via `sys_file_reference` overlays (physical files are not versioned); MM relations (categories) are handled through parent record overlays/DataHandler relation handling; simple fields (links, text) are versioned directly in the record overlay
- Page tree shows modified pages with a highlighting indicator
- The Workspaces module gives a full overview of all changes

### News with Content Elements (EXT:news)

`tx_news_domain_model_news` has `versioningWS = true` by default. Workspace workflows work for news records.

**Watch out for:**

- News categories (`sys_category`): versioned by default, works
- News tags (`tx_news_domain_model_tag`): check if `versioningWS` is enabled
- News detail page preview: configure preview page in TSconfig:

```
# Page TSconfig for news preview in workspace
options.workspaces.previewPageId.tx_news_domain_model_news = 42
```

- Related news: MM relations are handled by DataHandler
- News images: FAL references are versioned, but **physical files are not** (see Section 2)

### Campaign/Seasonal Content with Scheduled Publish

For temporary content (Christmas, Black Friday, product launches):

1. Prepare all campaign content in the workspace
2. Send changes to review and approval stage
3. Publish (or schedule auto-publish) at campaign start
4. Create a follow-up workspace change set to restore baseline content after campaign end
5. Publish the rollback change set when the campaign is over

### Preview Links for External Reviewers

```
# User TSconfig -- set preview link expiry
options.workspaces.previewLinkTTLHours = 72
```

Generate via Workspaces module: "Generate page preview links" button. The link works without any TYPO3 backend access.

### Scheduler Auto-Publish

1. Set a "Publish" date on the workspace record (Publishing tab)
2. Create Scheduler task: "Workspaces auto-publication"
3. Set task frequency (e.g., every 15 minutes)
4. Only content in "Ready to publish" stage gets published

```bash
# Cron job (runs every 15 minutes)
*/15 * * * * /path/to/bin/typo3 scheduler:run
```

### General Rules

- **Use groups, not individual users** for workspace ownership and membership
- **Test workspace workflows** before going live with workspace-based editing
- **Document the review process** for editors (which stages, who approves)
- **Monitor disk space** -- workspace versions accumulate in the database
- **Clean up** old workspace data periodically (discard unused versions)
- **Keep patch level current** -- workspace security advisories are published periodically (SA-2025-022 affected TYPO3 9.0–13.4.17; v14.0.0+ shipped with the fix)
