# Skill Synchronization & Multi-Client Setup

This repository uses one canonical skill layout:

- each skill lives once at `skills/<slug>/SKILL.md`
- optional `references/`, `examples/`, `scripts/`, and `assets/` live next to that skill
- upstream-managed skills are declared once in `.sync-config.json`
- `./install.sh` and `./update.sh` fan skills out to the five core clients automatically

Do not add manual per-client symlinks or duplicate `SKILL.md` files for individual products.

## Core Scripted Clients

### User-Level Skill Paths

| Client | User Path | Notes |
|--------|-----------|-------|
| Cursor | `~/.cursor/skills/` | Auto-discovery in Cursor |
| Claude Code | `~/.claude/skills/` | Primary Claude user skill path |
| Gemini CLI | `~/.gemini/skills/` | Shared with Antigravity |
| OpenAI Codex | `~/.codex/skills/` | User-level Codex discovery |
| Windsurf | `~/.codeium/windsurf/skills/` | Current Windsurf user path |

### Project-Level Skill Paths

| Client | Project Path | Notes |
|--------|--------------|-------|
| Cursor | `.cursor/skills/` | Primary project-level Cursor skills |
| Cursor legacy | `.cursor/rules/*.mdc` | Backwards compatibility copies |
| Gemini CLI | `.gemini/skills/` | Project-level Gemini/Antigravity |
| OpenAI Codex | `.codex/skills/` | Project-level Codex skills |
| Windsurf | `.windsurf/skills/` | Project-level Windsurf skills |

### Native Instruction Files

These are maintained centrally and do not require per-skill install logic:

| File | Used By |
|------|---------|
| `AGENTS.md` | GitHub Copilot, OpenAI Codex, Windsurf, Cline, Aider |
| `CLAUDE.md` | Claude Code |
| `GEMINI.md` | Gemini CLI, Antigravity |
| `.windsurfrules` | Windsurf |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `gemini-extension.json` | Gemini CLI skill triggers |

## Optional Manual Clients

Other tools can still use this repository without adding per-skill install logic to `install.sh`.

If a tool supports a skills directory, mirror `skills/*` into that path once:

```bash
TARGET_DIR="$HOME/.kiro/skills" # replace with the tool's skill path
mkdir -p "$TARGET_DIR"

for skill_dir in "$PWD"/skills/*; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  ln -sfn "$skill_dir" "$TARGET_DIR/$(basename "$skill_dir")"
done
```

If a tool reads instruction files instead of a skills directory, point it at `AGENTS.md` or its native instruction file.

## How Installation Works

`./install.sh` loops over every directory under `skills/` and installs it everywhere it belongs for the five core clients.

```text
skills/typo3-update/SKILL.md          <- source of truth
    ↓ fan-out
~/.claude/skills/typo3-update/        <- Claude Code
~/.cursor/skills/typo3-update/        <- Cursor
~/.gemini/skills/typo3-update/        <- Gemini CLI
~/.codex/skills/typo3-update/         <- OpenAI Codex
~/.codeium/windsurf/skills/typo3-update/ <- Windsurf
.cursor/skills/typo3-update/          <- Cursor project-level
.gemini/skills/typo3-update/          <- Gemini project-level
.codex/skills/typo3-update/           <- Codex project-level
.windsurf/skills/typo3-update/        <- Windsurf project-level
.cursor/rules/typo3-update.mdc        <- Cursor legacy compatibility copy
```

Common commands:

```bash
./install.sh                # full install
./install.sh --user-only    # only user-level paths
./install.sh --project-only # only project-level paths
./install.sh --no-sync      # skip upstream sync, only regenerate/install
./update.sh                 # sync upstream skills, then reinstall
./update.sh --sync-only     # sync upstream skills only
```

## Skill Types

The collection contains two maintenance modes:

1. `Local skills`: maintained directly in this repository.
2. `Upstream-managed skills`: refreshed from external Git repositories listed in `.sync-config.json`.

After upstream sync, the repo restores attribution blocks and refreshes source-owner documentation automatically.

### Netresearch-derived skills

Netresearch-derived skills are currently upstream-managed through `.sync-config.json` and keep their local thank-you and attribution blocks after sync.

## Adding a Local Skill

1. Create `skills/<slug>/SKILL.md`.
2. Add supporting folders only if needed.
3. Update README / AGENTS if the skill changes the public catalog.
4. Run `./install.sh`.

No extra client-specific symlink work is required for the five core clients.

## Adding an Upstream-Managed Skill

1. Add one entry to `.sync-config.json`.
2. Choose the canonical target skill name for `skills/<name>/`.
3. Set `path` to the upstream folder containing `SKILL.md`.
4. Run `./update.sh --sync-only`.
5. Review generated changes and attribution blocks.
6. Run `./install.sh` if you also want local client mirrors regenerated.

Configuration fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Directory name under `skills/` |
| `source` | Yes | Git repository URL |
| `branch` | Yes | Branch to sync from |
| `path` | No | Subdirectory within the upstream repo containing `SKILL.md` |
| `enabled` | No | Set `false` to keep entry disabled |
| `copyMode` | No | Use `repo` only when intentionally mirroring a whole repository |
| `target` | No | Target directory for `copyMode: "repo"` |
| `note` | No | Human-readable maintenance note |

## Automatic Synchronization

The GitHub Action `.github/workflows/sync-skills.yml` can sync enabled upstream skills on schedule or by manual dispatch.

Local sync uses the same source of truth:

```bash
./update.sh --sync-only
```

That command:

1. clones each enabled upstream source
2. refreshes local `skills/<name>/`
3. restores source notes with `scripts/sync_source_notes.py`
4. refreshes README source ownership with `scripts/sync_readme_sources.py`
5. validates attribution with `scripts/check_attribution_guardrails.py`

## Best Practices

1. Add each skill once under `skills/`.
2. Prefer the installer over manual symlink management.
3. Keep `.sync-config.json` as the only upstream sync registry.
4. Review sync changes before merging.
5. Keep generated client mirrors out of design discussions; the canonical source is always `skills/`.

## Deterministic Publish Flow

Use this when you want a predictable publish/update cycle:

1. Commit and push source changes.
2. Run `./update.sh --sync-only` if upstream-managed skills changed.
3. Run `./install.sh` to regenerate local mirrors and generated docs.
4. Commit generated changes.
5. Run any publishing/validation workflow you need.
