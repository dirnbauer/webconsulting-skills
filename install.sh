#!/bin/bash
# ============================================================================
# webconsulting Agent Skills Installer
# ============================================================================
#
# Universal installer for 10+ AI coding clients.
#
# Usage: ./install.sh [options]
#
# Options:
#   --user-only     Only install user-level skills (skip project-level)
#   --project-only  Only install project-level skills (skip user-level)
#   --no-sync       Skip external skill sync
#   --help          Show this help message
#
# Supported Clients (user-level skills via symlinks):
#   Tier 1 — Major clients:
#     • Cursor IDE        ~/.cursor/skills/
#     • Claude Code       ~/.claude/skills/
#     • Gemini CLI        ~/.gemini/skills/
#     • OpenAI Codex CLI  ~/.codex/skills/
#     • Windsurf          ~/.codeium/windsurf/skills/
#     • GitHub Copilot    (reads AGENTS.md natively)
#
#   Tier 2 — Additional clients:
#     • Kiro              ~/.kiro/skills/
#     • Cline             (reads AGENTS.md natively)
#     • Continue.dev      (project-level only)
#     • Aider             (reads CONVENTIONS.md via --read flag)
#     • Antigravity       (shares Gemini CLI paths)
#
# Project-level skills (symlinks in project root):
#     • .cursor/skills/       (Cursor)
#     • .cursor/rules/*.mdc   (Cursor legacy)
#     • .gemini/skills/       (Gemini CLI / Antigravity)
#     • .codex/skills/        (OpenAI Codex)
#     • .windsurf/skills/     (Windsurf)
#     • .kiro/skills/         (Kiro)
#
# Cross-client files (read natively by multiple clients):
#     • AGENTS.md                       → Copilot, Codex, Windsurf, Cline, Kiro, Aider
#     • CLAUDE.md                       → Claude Code
#     • GEMINI.md                       → Gemini CLI, Antigravity
#     • .windsurfrules                  → Windsurf
#     • .github/copilot-instructions.md → GitHub Copilot
#     • gemini-extension.json           → Gemini CLI (skill triggers)
#
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

USER_ONLY=false
PROJECT_ONLY=false
NO_SYNC=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --user-only)   USER_ONLY=true; shift ;;
        --project-only) PROJECT_ONLY=true; shift ;;
        --no-sync)     NO_SYNC=true; shift ;;
        --help|-h)     head -n 48 "$0" | tail -n 46; exit 0 ;;
        *)             echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     webconsulting Agent Skills Installer                     ║"
echo "║     Universal — Cursor · Claude · Gemini · Codex · more     ║"
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

    for skill_b64 in $SKILLS; do
        skill=$(echo "$skill_b64" | base64 --decode)
        name=$(echo "$skill" | jq -r '.name')
        source=$(echo "$skill" | jq -r '.source')
        branch=$(echo "$skill" | jq -r '.branch')
        path=$(echo "$skill" | jq -r '.path // "."')

        echo "  Syncing: $name..."

        TEMP_DIR=$(mktemp -d)
        if git clone --depth 1 --branch "$branch" "$source" "$TEMP_DIR" 2>/dev/null; then
            SOURCE_DIR="$TEMP_DIR/$path"
            TARGET_DIR="$SCRIPT_DIR/skills/$name"

            if [ -f "$SOURCE_DIR/SKILL.md" ]; then
                mkdir -p "$TARGET_DIR"
                cp "$SOURCE_DIR/SKILL.md" "$TARGET_DIR/SKILL.md"

                for subdir in examples rules references scripts assets; do
                    if [ -d "$SOURCE_DIR/$subdir" ]; then
                        rm -rf "$TARGET_DIR/$subdir"
                        cp -r "$SOURCE_DIR/$subdir" "$TARGET_DIR/"
                    fi
                done

                echo "  ✓ Synced: $name"
            else
                echo "  ⚠ No SKILL.md found in $source (path: $path)"
            fi
        else
            echo "  ⚠ Failed to sync: $name (clone failed)"
        fi
        rm -rf "$TEMP_DIR"
    done
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
# Helper: Install skills via symlinks to a target directory
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

    # ── Tier 1: Major clients ──────────────────────────────────────────────

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

    # ── Tier 2: Additional clients ─────────────────────────────────────────

    # Kiro (AWS)
    install_skills_to "$HOME/.kiro/skills" "Kiro (~/.kiro/skills)"

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

    # Kiro
    install_skills_to "$PROJECT_ROOT/.kiro/skills" "Kiro (.kiro/skills)"
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
        echo "  ✓ AGENTS.md (Copilot, Codex, Windsurf, Cline, Kiro, Aider)"
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
    echo "  ~/.kiro/skills/                (Kiro)"
    echo ""
fi

if [ "$USER_ONLY" != "true" ]; then
    echo "Project-level skills installed to:"
    echo "  .cursor/skills/    .gemini/skills/    .codex/skills/"
    echo "  .windsurf/skills/  .kiro/skills/      .cursor/rules/*.mdc"
    echo ""
fi

echo "Cross-client instruction files:"
echo "  AGENTS.md                        → Copilot, Codex, Windsurf, Cline, Kiro, Aider"
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
