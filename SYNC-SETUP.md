# Skill Synchronization Setup

This document explains how to add and manage external skill sources in the webconsulting Claude Marketplace.

## Overview

The marketplace supports two types of skills:

1. **Local Skills**: Created and maintained within this repository
2. **Upstream Skills**: Synced from external Git repositories

## Adding an Upstream Skill

### 1. Edit `.sync-config.json`

Add a new entry to the `skills` array:

```json
{
  "name": "skill-name",
  "source": "https://github.com/org/skill-repo.git",
  "branch": "main",
  "enabled": true
}
```

### 2. Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Directory name under `skills/` |
| `source` | Yes | Git repository URL (HTTPS preferred) |
| `branch` | Yes | Branch to sync from |
| `enabled` | No | Set to `false` to skip during sync |

### 3. Run Sync Manually

```bash
# Trigger GitHub Action manually
gh workflow run sync-skills.yml

# Or sync locally
./update.sh --sync-only
```

## Automatic Synchronization

The GitHub Action `.github/workflows/sync-skills.yml` runs:

- **Weekly**: Every Monday at 06:00 UTC
- **On-demand**: Via workflow dispatch

### What Happens During Sync

1. Each enabled skill source is cloned/pulled
2. The `SKILL.md` file is copied to `skills/{name}/`
3. Any additional skill assets are synchronized
4. A PR is created if changes are detected

## Creating a Local Skill

1. Create a directory under `skills/`:
   ```bash
   mkdir skills/my-custom-skill
   ```

2. Add the required `SKILL.md`:
   ```markdown
   ---
   name: my-custom-skill
   description: Brief description of what this skill teaches
   version: 1.0.0
   ---

   # Skill Title

   ## Instructions
   ...
   ```

3. Run `./install.sh` to deploy

## Skill File Structure

```
skills/
└── skill-name/
    ├── SKILL.md          # Required: Main skill definition
    ├── examples/         # Optional: Code examples
    │   └── example.php
    └── assets/           # Optional: Additional resources
        └── diagram.png
```

## Best Practices

1. **Version Pinning**: Use specific branches or tags for stability
2. **Review Changes**: Always review sync PRs before merging
3. **Local Overrides**: Prefix local skills with `webconsulting-` to avoid conflicts
4. **Documentation**: Keep skill descriptions concise for context efficiency

## Deterministic Publish Flow (GitHub -> skills.sh)

Use this checklist whenever you add or update a local skill and want predictable publication behavior:

1. **Commit and push** your skill change to `main`.
2. **Run local sync** (if needed):
   ```bash
   ./update.sh --sync-only
   ```
3. **Run install** to refresh generated mirrors:
   ```bash
   ./install.sh
   ```
4. **Commit generated changes** (`.cursor/rules/*.mdc`, index docs) and push.
5. **Run GitHub workflow** `skills-sh-publish-check.yml` (manual dispatch) to validate repository state.
6. **Verify on skills.sh** by searching the repository + skill name.

Notes:
- This repository is the source of truth.
- `sync-skills.yml` syncs upstream imported skills only; it does not publish to skills.sh directly.

