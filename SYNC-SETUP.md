# Skill Synchronization & Multi-Client Setup

This document explains how to add and manage external skill sources, and how skills are
installed across all supported AI coding clients.

## Supported Clients

### Tier 1 — Major Clients

| Client | User Skills | Project Skills | Instruction File |
|--------|-------------|----------------|------------------|
| **Cursor** | `~/.cursor/skills/` + `~/.claude/skills/` | `.cursor/skills/` + `.cursor/rules/*.mdc` | — |
| **Claude Code** | `~/.claude/skills/` | — | `CLAUDE.md` |
| **Gemini CLI** | `~/.gemini/skills/` | `.gemini/skills/` | `GEMINI.md` |
| **OpenAI Codex** | `~/.codex/skills/` | `.codex/skills/` | `AGENTS.md` |
| **Windsurf** | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` | `AGENTS.md` |
| **GitHub Copilot** | — | — | `AGENTS.md` + `.github/copilot-instructions.md` |

### Tier 2 — Additional Clients

| Client | User Skills | Project Skills | Instruction File |
|--------|-------------|----------------|------------------|
| **Kiro** | `~/.kiro/skills/` | `.kiro/skills/` | `AGENTS.md` |
| **Antigravity** | `~/.gemini/skills/` (shared) | `.gemini/skills/` (shared) | `GEMINI.md` |
| **Cline** | — | `.clinerules/` | `AGENTS.md` |
| **Continue.dev** | `~/.continue/rules/` | `.continue/rules/` | — |
| **Aider** | — | — | `CONVENTIONS.md` (via `--read`) |

### Cross-Client Instruction Files

These files are read natively by multiple clients — no installation step needed:

- **`AGENTS.md`** → GitHub Copilot, OpenAI Codex, Windsurf, Cline, Kiro
- **`CLAUDE.md`** → Claude Code (create manually per-project if needed)
- **`GEMINI.md`** → Gemini CLI, Antigravity (create manually per-project if needed)

## How Installation Works

All skills share the same `SKILL.md` format (YAML frontmatter + Markdown instructions).
The installer creates symlinks from `skills/<name>/` to each client's discovery directory.

```
skills/typo3-update/SKILL.md          ← Source of truth
    ↓ symlink
~/.claude/skills/typo3-update/        ← Claude Code + Cursor
~/.gemini/skills/typo3-update/        ← Gemini CLI
~/.codex/skills/typo3-update/         ← OpenAI Codex
~/.codeium/windsurf/skills/typo3-update/ ← Windsurf
~/.kiro/skills/typo3-update/          ← Kiro
.cursor/skills/typo3-update/          ← Cursor (project-level)
.cursor/rules/typo3-update.mdc       ← Cursor (legacy copy)
```

Run `./install.sh` to install to all locations. Options:

```bash
./install.sh                # Full install (user + project level)
./install.sh --user-only    # Only user-level symlinks
./install.sh --project-only # Only project-level symlinks
./install.sh --no-sync      # Skip external skill sync
```

## Overview

The collection supports two types of skills:

1. **Local Skills**: Created and maintained within this repository
2. **Upstream Skills**: Synced from external Git repositories

### Netresearch-derived skills (in-repo only)

The following skills were **adapted from** [Netresearch DTT GmbH](https://www.netresearch.de/) and are **maintained exclusively in this repository**. They must **not** be wired to automatic sync from `github.com/netresearch` (no refetch / overwrite from upstream):

`php-modernization`, `enterprise-readiness`, `security-audit`, `cli-tools`, `context7`, `typo3-ddev`, `typo3-testing`, `typo3-conformance`, `typo3-docs`, `typo3-core-contributions`, `typo3-extension-upgrade`

Gratitude and historical links to the original Netresearch repositories stay in **AGENTS.md**, **README.md**, and the credits sections of those skills.

## Adding an Upstream Skill

### 1. Edit `.sync-config.json`

Add a new entry to the `skills` array:

```json
{
  "name": "skill-name",
  "source": "https://github.com/org/skill-repo.git",
  "branch": "main",
  "path": "skills/skill-name",
  "enabled": true
}
```

### 2. Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Directory name under `skills/` |
| `source` | Yes | Git repository URL (HTTPS preferred) |
| `branch` | Yes | Branch to sync from |
| `path` | No | Subdirectory within repo containing SKILL.md |
| `enabled` | No | Set to `false` to skip during sync |
| `note` | No | Documentation note (not used by scripts) |

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
3. Any additional skill assets (examples, scripts, references) are synchronized
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
   metadata:
     version: "1.0.0"
   ---

   # Skill Title

   ## Instructions
   ...
   ```

3. Run `./install.sh` to deploy to all clients

## Skill File Structure

```
skills/
└── skill-name/
    ├── SKILL.md          # Required: Main skill definition
    ├── scripts/          # Optional: Executable scripts
    │   └── setup.sh
    ├── references/       # Optional: Static documentation
    │   └── api-guide.md
    ├── examples/         # Optional: Code examples
    │   └── example.php
    └── assets/           # Optional: Templates, diagrams
        └── diagram.png
```

## Client-Specific Setup Notes

### Cursor

Skills are discovered from both `~/.claude/skills/` (shared with Claude Code) and
`.cursor/skills/` (project-level). Legacy `.cursor/rules/*.mdc` files are also created
for backward compatibility with older Cursor versions.

### Gemini CLI / Antigravity

Skills are discovered from `~/.gemini/skills/` (user-level) and `.gemini/skills/`
(project-level). Both `.gemini/` and `.agents/` paths are supported; we use `.gemini/`.

You can also install individual skills with:
```bash
gemini skills install /path/to/skills/typo3-update
```

### OpenAI Codex CLI

Skills are discovered from `~/.codex/skills/` (user-level) and `.codex/skills/`
(project-level). Codex also reads `AGENTS.md` for project-wide instructions.

### Windsurf

Skills are discovered from `~/.codeium/windsurf/skills/` (user-level) and
`.windsurf/skills/` (project-level). Windsurf also reads `AGENTS.md` for
directory-scoped instructions.

### GitHub Copilot

Copilot reads `AGENTS.md` natively from the repository root and any subdirectories.
It also supports `.github/copilot-instructions.md` for repo-wide instructions and
`.github/instructions/*.instructions.md` for path-specific rules.

No skill directory installation is needed — `AGENTS.md` is the integration point.

### Kiro

Skills are discovered from `~/.kiro/skills/` (user-level) and `.kiro/skills/`
(project-level). Kiro also reads `AGENTS.md` for project instructions.

### Cline

Cline reads `AGENTS.md` natively. It also supports `.clinerules/` directory with
markdown files for fine-grained rule control.

### Continue.dev

Continue uses `.continue/rules/` for project-level rules and `~/.continue/rules/`
for global rules. Rules are markdown files loaded into agent context.

### Aider

Aider uses `CONVENTIONS.md` loaded via `--read` flag or `.aider.conf.yml`:
```yaml
read: CONVENTIONS.md
```

## Best Practices

1. **Version Pinning**: Use specific branches or tags for stability
2. **Review Changes**: Always review sync PRs before merging
3. **Local Overrides**: Prefix local skills with `webconsulting-` to avoid conflicts
4. **Documentation**: Keep skill descriptions concise for context efficiency
5. **`.gitignore`**: All client skill directories (`.gemini/skills/`, `.codex/skills/`,
   etc.) should be gitignored since they contain symlinks

## Deterministic Publish Flow (GitHub → skills.sh)

Use this checklist whenever you add or update a local skill and want predictable
publication behavior:

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
5. **Run GitHub workflow** `skills-sh-publish-check.yml` (manual dispatch) to validate.
6. **Verify on skills.sh** by searching the repository + skill name.

Notes:
- This repository is the source of truth.
- `sync-skills.yml` syncs upstream imported skills only; it does not publish to
  skills.sh directly.
