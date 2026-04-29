#!/bin/bash
# ============================================================================
# webconsulting Agent Skills Installer
# ============================================================================
#
# Core installer for the 5 most-used AI coding clients.
#
# Usage: ./install.sh [options]
#
# Skill authoring standard:
#   • Add each skill once under skills/<name>/SKILL.md
#   • Optionally add one .sync-config.json entry for upstream-managed skills
#   • Do not add per-client symlink code for individual skills
#   • The installer fans every skill out to supported clients automatically
#
# Options:
#   --user-only     Only install user-level skills (skip project-level)
#   --project-only  Only install project-level skills (skip user-level)
#   --no-sync       Skip external skill sync
#   --generate-only Regenerate cross-client files and manifests, then exit
#   --help          Show this help message
#
# Core scripted clients (user-level skills via symlinks):
#     • Cursor IDE        ~/.cursor/skills/
#     • Claude Code       ~/.claude/skills/
#     • Gemini CLI        ~/.gemini/skills/
#     • OpenAI Codex CLI  ~/.codex/skills/
#     • Windsurf          ~/.codeium/windsurf/skills/
#     • Antigravity       (shares Gemini CLI paths)
#
# Native / optional clients:
#     • GitHub Copilot    (reads AGENTS.md natively)
#     • Cline             (reads AGENTS.md natively)
#     • Aider             (reads AGENTS.md natively)
#     • Other tools       (manual link to their skills directory; see README)
#
# Project-level skills (symlinks in project root):
#     • .cursor/skills/       (Cursor)
#     • .cursor/rules/*.mdc   (Cursor legacy)
#     • .gemini/skills/       (Gemini CLI / Antigravity)
#     • .codex/skills/        (OpenAI Codex)
#     • .windsurf/skills/     (Windsurf)
#
# Cross-client files (read natively by multiple clients):
#     • AGENTS.md                       → Copilot, Codex, Windsurf, Cline, Aider
#     • CLAUDE.md                       → Claude Code
#     • GEMINI.md                       → Gemini CLI, Antigravity
#     • .windsurfrules                  → Windsurf
#     • .github/copilot-instructions.md → GitHub Copilot
#     • gemini-extension.json           → Gemini CLI (skill triggers)
#
# License: MIT (code) / CC-BY-SA-4.0 (content)
# Third-party skills retain their original licenses — see LICENSE for details.
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NORMALIZE_SKILL_FRONTMATTER="$SCRIPT_DIR/scripts/normalize_skill_frontmatter.py"

USER_ONLY=false
PROJECT_ONLY=false
NO_SYNC=false
GENERATE_ONLY=false
SYNC_SUBDIRS=(agents assets examples references rules scripts)

while [[ $# -gt 0 ]]; do
    case $1 in
        --user-only)   USER_ONLY=true; shift ;;
        --project-only) PROJECT_ONLY=true; shift ;;
        --no-sync)     NO_SYNC=true; shift ;;
        --generate-only) GENERATE_ONLY=true; shift ;;
        --help|-h)     head -n 54 "$0" | tail -n 52; exit 0 ;;
        *)             echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     webconsulting Agent Skills Installer                     ║"
echo "║     Core — Cursor · Claude · Gemini · Codex · Windsurf      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# =============================================================================
# 1. Environment Detection
# =============================================================================

IS_CONTAINER=false
if [ -n "$DDEV_SITENAME" ] || [ -f "/.dockerenv" ] || [ -n "$DOCKER_CONTAINER" ]; then
    IS_CONTAINER=true
    echo "→ Detected: Running inside container (DDEV/Docker)"
else
    echo "→ Detected: Running on local machine"
fi

if [ -f "$SCRIPT_DIR/../../../composer.json" ]; then
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
    echo "→ Project root (vendor): $PROJECT_ROOT"
elif [ -f "$SCRIPT_DIR/../composer.json" ] || [ -d "$SCRIPT_DIR/../src" ]; then
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    echo "→ Project root (parent): $PROJECT_ROOT"
elif [ -f "$PWD/composer.json" ]; then
    PROJECT_ROOT="$PWD"
    echo "→ Project root (from cwd): $PROJECT_ROOT"
else
    echo "⚠ Warning: Could not detect project root. Using script directory."
    PROJECT_ROOT="$SCRIPT_DIR"
fi

# =============================================================================
# 2. Sync External Skills (from .sync-config.json)
# =============================================================================

if [ "$NO_SYNC" = false ] && [ -f "$SCRIPT_DIR/.sync-config.json" ] && command -v jq &> /dev/null && command -v git &> /dev/null; then
    echo ""
    echo "→ Syncing external skills from .sync-config.json..."

    SKILLS=$(jq -r '.skills[] | select(.enabled == true) | @base64' "$SCRIPT_DIR/.sync-config.json" 2>/dev/null)

    resolve_target_dir() {
        local target="$1"
        if [ -z "$target" ]; then
            return 1
        fi
        case "$target" in
            /*) printf '%s\n' "$target" ;;
            *) printf '%s\n' "$SCRIPT_DIR/$target" ;;
        esac
    }

    copy_repo_tree() {
        local source_dir="$1"
        local target_dir="$2"
        rm -rf "$target_dir"
        mkdir -p "$target_dir"
        (
            cd "$source_dir" || exit 1
            shopt -s nullglob dotglob
            for item in * .[!.]* ..?*; do
                [ "$item" = ".git" ] && continue
                cp -R "$item" "$target_dir/"
            done
        )
    }

    for skill_b64 in $SKILLS; do
        skill=$(echo "$skill_b64" | base64 --decode)
        name=$(echo "$skill" | jq -r '.name')
        source=$(echo "$skill" | jq -r '.source')
        branch=$(echo "$skill" | jq -r '.branch')
        path=$(echo "$skill" | jq -r '.path // "."')
        copy_mode=$(echo "$skill" | jq -r '.copyMode // "skill"')
        target=$(echo "$skill" | jq -r '.target // ""')

        echo "  Syncing: $name..."

        TEMP_DIR=$(mktemp -d)
        if git clone --depth 1 --branch "$branch" "$source" "$TEMP_DIR" 2>/dev/null; then
            SOURCE_DIR="$TEMP_DIR/$path"

            if [ "$copy_mode" = "repo" ]; then
                TARGET_DIR=$(resolve_target_dir "$target")
                if [ -d "$SOURCE_DIR" ]; then
                    copy_repo_tree "$SOURCE_DIR" "$TARGET_DIR"
                    echo "  ✓ Mirrored repo: $name"
                else
                    echo "  ⚠ No directory found in $source (path: $path)"
                fi
            else
                TARGET_DIR="$SCRIPT_DIR/skills/$name"

                if [ -f "$SOURCE_DIR/SKILL.md" ]; then
                    mkdir -p "$TARGET_DIR"
                    cp "$SOURCE_DIR/SKILL.md" "$TARGET_DIR/SKILL.md"
                    if command -v python3 &> /dev/null; then
                        python3 "$NORMALIZE_SKILL_FRONTMATTER" "$TARGET_DIR/SKILL.md"
                    else
                        echo "  ⚠ python3 not installed, skipping SKILL.md frontmatter normalization for $name"
                    fi

                    for subdir in "${SYNC_SUBDIRS[@]}"; do
                        if [ -d "$SOURCE_DIR/$subdir" ]; then
                            rm -rf "$TARGET_DIR/$subdir"
                            cp -r "$SOURCE_DIR/$subdir" "$TARGET_DIR/"
                        fi
                    done

                    echo "  ✓ Synced: $name"
                else
                    echo "  ⚠ No SKILL.md found in $source (path: $path)"
                fi
            fi
        else
            echo "  ⚠ Failed to sync: $name (clone failed)"
        fi
        rm -rf "$TEMP_DIR"
    done

    if command -v python3 &> /dev/null; then
        echo ""
        echo "→ Restoring source attribution blocks..."
        python3 "$SCRIPT_DIR/scripts/sync_source_notes.py"
        echo "→ Refreshing README source owners..."
        python3 "$SCRIPT_DIR/scripts/sync_readme_sources.py"
        echo "→ Validating attribution guardrails..."
        python3 "$SCRIPT_DIR/scripts/check_attribution_guardrails.py"
    else
        echo ""
        echo "→ python3 not installed, skipping attribution restoration and validation"
    fi
elif [ "$NO_SYNC" = true ]; then
    echo ""
    echo "→ Skipping external sync (--no-sync)"
else
    echo ""
    if [ ! -f "$SCRIPT_DIR/.sync-config.json" ]; then
        echo "→ No .sync-config.json found, skipping external sync"
    elif ! command -v jq &> /dev/null; then
        echo "→ jq not installed, skipping external sync (install with: brew install jq)"
    fi
fi

# =============================================================================
# 3. Generate Cross-Client Instruction Files
# =============================================================================

echo ""
echo "→ Generating cross-client instruction files..."

# Count skills
SKILL_COUNT=$(find "$SCRIPT_DIR/skills" -mindepth 2 -maxdepth 2 -name SKILL.md -type f | wc -l | tr -d ' ')

# ── Generate CLAUDE.md ────────────────────────────────────────────────────────
cat > "$SCRIPT_DIR/CLAUDE.md" <<CLAUDE_EOF
# webconsulting Agent Skills

This repository contains $SKILL_COUNT Agent Skills for AI-augmented software development.

## Instructions

Follow the instructions in [AGENTS.md](AGENTS.md) — it is the single source of truth for all skills, triggers, usage examples, and session profiles.

## Skills Location

All skills live in \`skills/*/SKILL.md\`. Each skill has YAML frontmatter with \`name\`, \`description\`, \`triggers\`, and \`compatibility\`.

To use a skill, read the \`SKILL.md\` file at \`skills/<skill-name>/SKILL.md\` and follow its instructions.

## Key Conventions

- TYPO3 skills target **TYPO3 v14.x only** (verify third-party extensions on Packagist)
- Cross-cutting TYPO3/PHP guidance lives in the owning skills (for example \`php-modernization\`, \`typo3-content-blocks\`, \`typo3-update\`)
- Always review AI-generated code before committing
- When multiple skills are relevant, combine them (e.g., \`typo3-rector\` + \`typo3-testing\`)

## License

Code: MIT | Content: CC-BY-SA-4.0 | Third-party skills retain their original licenses.
See LICENSE, LICENSE-MIT, and LICENSE-CC-BY-SA-4.0 for full terms.
CLAUDE_EOF
echo "  ✓ CLAUDE.md ($SKILL_COUNT skills)"

# ── Generate GEMINI.md ────────────────────────────────────────────────────────
cat > "$SCRIPT_DIR/GEMINI.md" <<GEMINI_EOF
# webconsulting Agent Skills

This repository contains $SKILL_COUNT Agent Skills for AI-augmented software development.

## Instructions

Follow the instructions in [AGENTS.md](AGENTS.md) — it is the single source of truth for all skills, triggers, usage examples, and session profiles.

## Gemini CLI Integration

Skills are registered in \`gemini-extension.json\` with trigger-based activation. The extension manifest maps each skill to its trigger keywords and \`skills/\` directory path.

## Skills Location

All skills live in \`skills/*/SKILL.md\`. Each skill has YAML frontmatter with \`name\`, \`description\`, \`triggers\`, and \`compatibility\`.

To use a skill, read the \`SKILL.md\` file at \`skills/<skill-name>/SKILL.md\` and follow its instructions.

## Key Conventions

- TYPO3 skills target **TYPO3 v14.x only** (verify third-party extensions on Packagist)
- Cross-cutting TYPO3/PHP guidance lives in the owning skills (for example \`php-modernization\`, \`typo3-content-blocks\`, \`typo3-update\`)
- Always review AI-generated code before committing
- When multiple skills are relevant, combine them (e.g., \`typo3-rector\` + \`typo3-testing\`)

## License

Code: MIT | Content: CC-BY-SA-4.0 | Third-party skills retain their original licenses.
See LICENSE, LICENSE-MIT, and LICENSE-CC-BY-SA-4.0 for full terms.
GEMINI_EOF
echo "  ✓ GEMINI.md ($SKILL_COUNT skills)"

# ── Generate .windsurfrules ───────────────────────────────────────────────────
cat > "$SCRIPT_DIR/.windsurfrules" <<WINDSURF_EOF
# webconsulting Agent Skills

This repository contains $SKILL_COUNT Agent Skills for AI-augmented software development.

## Instructions

Follow the instructions in AGENTS.md — it is the single source of truth for all skills, triggers, usage examples, and session profiles.

## Skills Location

All skills live in \`skills/*/SKILL.md\`. Each skill has YAML frontmatter with \`name\`, \`description\`, \`triggers\`, and \`compatibility\`.

To use a skill, read the \`SKILL.md\` file at \`skills/<skill-name>/SKILL.md\` and follow its instructions.

## Key Conventions

- TYPO3 skills target **TYPO3 v14.x only** (verify third-party extensions on Packagist)
- Cross-cutting TYPO3/PHP guidance lives in the owning skills (for example \`php-modernization\`, \`typo3-content-blocks\`, \`typo3-update\`)
- Always review AI-generated code before committing
- When multiple skills are relevant, combine them (e.g., \`typo3-rector\` + \`typo3-testing\`)

## License

Code: MIT | Content: CC-BY-SA-4.0 | Third-party skills retain their original licenses.
See LICENSE, LICENSE-MIT, and LICENSE-CC-BY-SA-4.0 for full terms.
WINDSURF_EOF
echo "  ✓ .windsurfrules ($SKILL_COUNT skills)"

# ── Generate .github/copilot-instructions.md ──────────────────────────────────
mkdir -p "$SCRIPT_DIR/.github"
cat > "$SCRIPT_DIR/.github/copilot-instructions.md" <<COPILOT_EOF
# webconsulting Agent Skills

This repository contains $SKILL_COUNT Agent Skills for AI-augmented software development.

## Instructions

Follow the instructions in [AGENTS.md](../AGENTS.md) — it is the single source of truth for all skills, triggers, usage examples, and session profiles.

## Skills Location

All skills live in \`skills/*/SKILL.md\`. Each skill has YAML frontmatter with \`name\`, \`description\`, \`triggers\`, and \`compatibility\`.

To use a skill, read the \`SKILL.md\` file at \`skills/<skill-name>/SKILL.md\` and follow its instructions.

## Key Conventions

- TYPO3 skills target **TYPO3 v14.x only** (verify third-party extensions on Packagist)
- Cross-cutting TYPO3/PHP guidance lives in the owning skills (for example \`php-modernization\`, \`typo3-content-blocks\`, \`typo3-update\`)
- Always review AI-generated code before committing
- When multiple skills are relevant, combine them (e.g., \`typo3-rector\` + \`typo3-testing\`)

## License

Code: MIT | Content: CC-BY-SA-4.0 | Third-party skills retain their original licenses.
See LICENSE, LICENSE-MIT, and LICENSE-CC-BY-SA-4.0 for full terms.
COPILOT_EOF
echo "  ✓ .github/copilot-instructions.md ($SKILL_COUNT skills)"

# ── Generate gemini-extension.json ────────────────────────────────────────────
# The manifest is generated from `skills/*/SKILL.md`, with trigger metadata read
# from README.md / AGENTS.md. That keeps new top-level skills from being missed.
if command -v python3 &> /dev/null; then
    python3 "$SCRIPT_DIR/scripts/generate_gemini_manifest.py"

    if command -v jq &> /dev/null; then
        if jq empty "$SCRIPT_DIR/gemini-extension.json" 2>/dev/null; then
            echo "  ✓ JSON validation passed"
        else
            echo "  ⚠ JSON validation failed — check gemini-extension.json manually"
        fi
    fi
else
    echo "  ⚠ python3 not installed — skipping gemini-extension.json generation"
fi

if [ "$GENERATE_ONLY" = true ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "Generation Complete!"
    echo "Generated cross-client files for $SKILL_COUNT skills."
    echo "═══════════════════════════════════════════════════════════════"
    exit 0
fi

# =============================================================================
# Helper: Install skills via symlinks to a target directory.
# Adding a new skill should not require client-specific edits here; this helper
# fans out every directory under skills/ automatically.
# =============================================================================

install_skills_to() {
    local target_dir="$1"
    local label="$2"
    local count=0

    mkdir -p "$target_dir"

    for skill_path in "$SCRIPT_DIR/skills"/*; do
        if [ -d "$skill_path" ] && [ -f "$skill_path/SKILL.md" ]; then
            local skill_name
            skill_name=$(basename "$skill_path")
            local target="$target_dir/$skill_name"

            if [ -L "$target" ] || [ -d "$target" ]; then
                rm -rf "$target"
            fi

            ln -s "$skill_path" "$target"
            count=$((count + 1))
        fi
    done

    # Clean up broken symlinks
    for link in "$target_dir"/*; do
        if [ -L "$link" ] && [ ! -e "$link" ]; then
            rm "$link"
            echo "  ✗ Removed stale: $(basename "$link")"
        fi
    done

    echo "  ✓ $label: $count skills installed"
}

# =============================================================================
# 3. User-Level Skills (symlinks — available across all projects)
# =============================================================================

if [ "$IS_CONTAINER" = "true" ] || [ "$PROJECT_ONLY" = true ]; then
    echo ""
    if [ "$IS_CONTAINER" = "true" ]; then
        echo "→ Skipping user-level installation (running in container)"
    else
        echo "→ Skipping user-level installation (--project-only)"
    fi
else
    echo ""
    echo "→ Installing user-level skills..."
    echo "  (Symlinks from skills/ → each client's discovery directory)"

    # ── Core scripted clients ──────────────────────────────────────────────

    # Claude Code + Cursor (shared location)
    install_skills_to "$HOME/.claude/skills" "Claude Code + Cursor (~/.claude/skills)"

    # Cursor user-level (some Cursor versions also check here)
    install_skills_to "$HOME/.cursor/skills" "Cursor (~/.cursor/skills)"

    # Gemini CLI + Google Antigravity
    install_skills_to "$HOME/.gemini/skills" "Gemini CLI (~/.gemini/skills)"

    # OpenAI Codex CLI
    install_skills_to "$HOME/.codex/skills" "OpenAI Codex (~/.codex/skills)"

    # Windsurf (Codeium)
    install_skills_to "$HOME/.codeium/windsurf/skills" "Windsurf (~/.codeium/windsurf/skills)"

    echo ""
    echo "  Note: GitHub Copilot, Cline, and Aider read AGENTS.md directly"
    echo "        — no separate skill installation needed for those clients."
fi

# =============================================================================
# 4. Project-Level Skills (symlinks in project root)
# =============================================================================

if [ "$USER_ONLY" = true ]; then
    echo ""
    echo "→ Skipping project-level installation (--user-only)"
else
    echo ""
    echo "→ Installing project-level skills..."

    # Cursor (primary project-level location)
    install_skills_to "$PROJECT_ROOT/.cursor/skills" "Cursor (.cursor/skills)"

    # Gemini CLI / Antigravity
    install_skills_to "$PROJECT_ROOT/.gemini/skills" "Gemini CLI (.gemini/skills)"

    # OpenAI Codex
    install_skills_to "$PROJECT_ROOT/.codex/skills" "Codex (.codex/skills)"

    # Windsurf
    install_skills_to "$PROJECT_ROOT/.windsurf/skills" "Windsurf (.windsurf/skills)"

fi

# =============================================================================
# 5. Legacy: Cursor Rules (.mdc format)
# =============================================================================

if [ "$USER_ONLY" = false ]; then
    echo ""
    echo "→ Installing Cursor rules (.mdc) for backwards compatibility..."
    PROJECT_RULES_DIR="$PROJECT_ROOT/.cursor/rules"
    mkdir -p "$PROJECT_RULES_DIR"

    mdc_count=0
    for skill_path in "$SCRIPT_DIR/skills"/*; do
        if [ -d "$skill_path" ] && [ -f "$skill_path/SKILL.md" ]; then
            skill_name=$(basename "$skill_path")
            target_rule="$PROJECT_RULES_DIR/${skill_name}.mdc"

            if [ -L "$target_rule" ] || [ -f "$target_rule" ]; then
                rm -f "$target_rule"
            fi

            cp "$skill_path/SKILL.md" "$target_rule"
            mdc_count=$((mdc_count + 1))
        fi
    done
    echo "  ✓ Cursor rules: $mdc_count .mdc files created"
fi

# =============================================================================
# 6. Cross-Client Instruction Files
# =============================================================================

if [ "$SCRIPT_DIR" != "$PROJECT_ROOT" ] && [ "$USER_ONLY" = false ]; then
    echo ""
    echo "→ Installing cross-client instruction files..."

    # AGENTS.md → always overwrite (canonical source of truth)
    if [ -f "$SCRIPT_DIR/AGENTS.md" ]; then
        cp "$SCRIPT_DIR/AGENTS.md" "$PROJECT_ROOT/AGENTS.md"
        echo "  ✓ AGENTS.md (Copilot, Codex, Windsurf, Cline, Aider)"
    fi

    # CLAUDE.md → Claude Code primary instructions
    if [ -f "$SCRIPT_DIR/CLAUDE.md" ] && [ ! -f "$PROJECT_ROOT/CLAUDE.md" ]; then
        cp "$SCRIPT_DIR/CLAUDE.md" "$PROJECT_ROOT/CLAUDE.md"
        echo "  ✓ CLAUDE.md (Claude Code)"
    elif [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
        echo "  · CLAUDE.md already exists (skipped)"
    fi

    # GEMINI.md → Gemini CLI primary instructions
    if [ -f "$SCRIPT_DIR/GEMINI.md" ] && [ ! -f "$PROJECT_ROOT/GEMINI.md" ]; then
        cp "$SCRIPT_DIR/GEMINI.md" "$PROJECT_ROOT/GEMINI.md"
        echo "  ✓ GEMINI.md (Gemini CLI, Antigravity)"
    elif [ -f "$PROJECT_ROOT/GEMINI.md" ]; then
        echo "  · GEMINI.md already exists (skipped)"
    fi

    # .windsurfrules → Windsurf project rules
    if [ -f "$SCRIPT_DIR/.windsurfrules" ] && [ ! -f "$PROJECT_ROOT/.windsurfrules" ]; then
        cp "$SCRIPT_DIR/.windsurfrules" "$PROJECT_ROOT/.windsurfrules"
        echo "  ✓ .windsurfrules (Windsurf)"
    elif [ -f "$PROJECT_ROOT/.windsurfrules" ]; then
        echo "  · .windsurfrules already exists (skipped)"
    fi

    # .github/copilot-instructions.md → GitHub Copilot
    if [ -f "$SCRIPT_DIR/.github/copilot-instructions.md" ] && [ ! -f "$PROJECT_ROOT/.github/copilot-instructions.md" ]; then
        mkdir -p "$PROJECT_ROOT/.github"
        cp "$SCRIPT_DIR/.github/copilot-instructions.md" "$PROJECT_ROOT/.github/copilot-instructions.md"
        echo "  ✓ .github/copilot-instructions.md (GitHub Copilot)"
    elif [ -f "$PROJECT_ROOT/.github/copilot-instructions.md" ]; then
        echo "  · .github/copilot-instructions.md already exists (skipped)"
    fi

    # gemini-extension.json → Gemini CLI extension manifest
    if [ -f "$SCRIPT_DIR/gemini-extension.json" ] && [ ! -f "$PROJECT_ROOT/gemini-extension.json" ]; then
        cp "$SCRIPT_DIR/gemini-extension.json" "$PROJECT_ROOT/gemini-extension.json"
        echo "  ✓ gemini-extension.json (Gemini CLI skill triggers)"
    elif [ -f "$PROJECT_ROOT/gemini-extension.json" ]; then
        echo "  · gemini-extension.json already exists (skipped)"
    fi
elif [ "$SCRIPT_DIR" = "$PROJECT_ROOT" ] && [ "$USER_ONLY" = false ]; then
    echo ""
    echo "→ Cross-client files already in place (standalone install)"
    echo "  AGENTS.md, CLAUDE.md, GEMINI.md, .windsurfrules,"
    echo "  .github/copilot-instructions.md, gemini-extension.json"
fi

# =============================================================================
# 7. Summary
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Installation Complete!"
echo ""

if [ "$IS_CONTAINER" != "true" ] && [ "$PROJECT_ONLY" != "true" ]; then
    echo "User-level skills installed to:"
    echo "  ~/.claude/skills/              (Claude Code + Cursor)"
    echo "  ~/.cursor/skills/              (Cursor)"
    echo "  ~/.gemini/skills/              (Gemini CLI + Antigravity)"
    echo "  ~/.codex/skills/               (OpenAI Codex)"
    echo "  ~/.codeium/windsurf/skills/    (Windsurf)"
    echo ""
fi

if [ "$USER_ONLY" != "true" ]; then
    echo "Project-level skills installed to:"
    echo "  .cursor/skills/    .gemini/skills/    .codex/skills/"
    echo "  .windsurf/skills/  .cursor/rules/*.mdc"
    echo ""
fi

echo "Cross-client instruction files:"
echo "  AGENTS.md                        → Copilot, Codex, Windsurf, Cline, Aider"
echo "  CLAUDE.md                        → Claude Code"
echo "  GEMINI.md                        → Gemini CLI, Antigravity"
echo "  .windsurfrules                   → Windsurf"
echo "  .github/copilot-instructions.md  → GitHub Copilot"
echo "  gemini-extension.json            → Gemini CLI (skill triggers)"
echo ""
echo "Next steps:"
echo "  1. Restart your IDE / CLI to discover skills"
echo "  2. Cursor: type / in Agent chat"
echo "  3. Gemini CLI: run 'gemini skills list'"
echo "  4. Codex: skills appear automatically"
echo "  5. Windsurf: @skill-name or auto-activation"
if [ "$IS_CONTAINER" = "true" ]; then
    echo "  6. Run install.sh on LOCAL machine for user-level skills"
fi
echo "═══════════════════════════════════════════════════════════════"
