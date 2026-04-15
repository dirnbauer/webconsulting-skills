#!/bin/bash
# ============================================================================
# webconsulting Agent Skills Updater
# ============================================================================
#
# Usage: ./update.sh [options]
#
# Options:
#   --sync-only    Only sync external skills, don't reinstall
#   --pull         Pull latest from git before updating
#   --force        Force overwrite local changes
#   --dry-run      Show what would be done without making changes
#   --help         Show this help message
#
# This script updates Agent Skills from external sources and reinstalls the core client mirrors.
#
# License: MIT (code) / CC-BY-SA-4.0 (content)
# Third-party skills retain their original licenses — see LICENSE for details.
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NORMALIZE_SKILL_FRONTMATTER="$SCRIPT_DIR/scripts/normalize_skill_frontmatter.py"
SYNC_ONLY=false
PULL=false
FORCE=false
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --sync-only)
            SYNC_ONLY=true
            shift
            ;;
        --pull)
            PULL=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            head -n 17 "$0" | tail -n 15
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     webconsulting Agent Skills Updater                       ║"
echo "║     Core — Cursor · Claude · Gemini · Codex · Windsurf      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# =============================================================================
# 1. Check for Required Tools
# =============================================================================

MISSING_TOOLS=()

if ! command -v git &> /dev/null; then
    MISSING_TOOLS+=("git")
fi

if ! command -v jq &> /dev/null; then
    MISSING_TOOLS+=("jq")
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo "⚠ Missing required tools: ${MISSING_TOOLS[*]}"
    echo ""
    echo "Install with:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew install ${MISSING_TOOLS[*]}"
    else
        echo "  sudo apt-get install ${MISSING_TOOLS[*]}"
    fi
    exit 1
fi

# =============================================================================
# 2. Check Git Status
# =============================================================================

if [ "$PULL" = true ]; then
    echo "→ Checking git status..."
    cd "$SCRIPT_DIR"
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        if [ "$FORCE" = true ]; then
            echo "  ⚠ Stashing local changes..."
            if [ "$DRY_RUN" = false ]; then
                git stash
            fi
        else
            echo "  ⚠ You have uncommitted changes."
            echo "  Use --force to stash them, or commit/discard manually."
            echo ""
            git status --short
            exit 1
        fi
    fi
    
    # Pull latest changes
    echo "→ Pulling latest changes from origin..."
    if [ "$DRY_RUN" = false ]; then
        git pull origin main
    else
        echo "  [DRY-RUN] Would run: git pull origin main"
    fi
    echo ""
fi

# =============================================================================
# 3. Sync External Skills
# =============================================================================

if [ -f "$SCRIPT_DIR/.sync-config.json" ]; then
    echo "→ Syncing external skills from .sync-config.json..."
    
    # Get total count of enabled skills
    ENABLED_COUNT=$(jq '[.skills[] | select(.enabled == true)] | length' "$SCRIPT_DIR/.sync-config.json")
    echo "  Found $ENABLED_COUNT enabled external skill sources"
    echo ""
    
    # Read enabled skills
    SKILLS=$(jq -r '.skills[] | select(.enabled == true) | @base64' "$SCRIPT_DIR/.sync-config.json" 2>/dev/null)
    
    SYNCED=0
    FAILED=0

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
        note=$(echo "$skill" | jq -r '.note // ""')
        
        echo "  Syncing: $name"
        [ -n "$note" ] && echo "    Note: $note"
        
        if [ "$DRY_RUN" = true ]; then
            if [ "$copy_mode" = "repo" ]; then
                TARGET_DIR=$(resolve_target_dir "$target")
                echo "    [DRY-RUN] Would clone $source (branch: $branch, path: $path) and mirror into $TARGET_DIR"
            else
                echo "    [DRY-RUN] Would clone $source (branch: $branch, path: $path)"
            fi
            continue
        fi
        
        TEMP_DIR=$(mktemp -d)
        if git clone --depth 1 --branch "$branch" "$source" "$TEMP_DIR" 2>/dev/null; then
            SOURCE_DIR="$TEMP_DIR/$path"

            if [ "$copy_mode" = "repo" ]; then
                TARGET_DIR=$(resolve_target_dir "$target")
                if [ -d "$SOURCE_DIR" ]; then
                    copy_repo_tree "$SOURCE_DIR" "$TARGET_DIR"
                    echo "    ✓ Mirrored repository successfully"
                    SYNCED=$((SYNCED + 1))
                else
                    echo "    ⚠ No directory found at path: $path"
                    FAILED=$((FAILED + 1))
                fi
            else
                TARGET_DIR="$SCRIPT_DIR/skills/$name"

                if [ -f "$SOURCE_DIR/SKILL.md" ]; then
                mkdir -p "$TARGET_DIR"
                cp "$SOURCE_DIR/SKILL.md" "$TARGET_DIR/SKILL.md"
                if command -v python3 &> /dev/null; then
                    python3 "$NORMALIZE_SKILL_FRONTMATTER" "$TARGET_DIR/SKILL.md"
                else
                    echo "    ⚠ python3 not installed, skipping SKILL.md frontmatter normalization for $name"
                fi
                
                # Copy subdirectories if they exist
                for subdir in examples rules references scripts assets; do
                    if [ -d "$SOURCE_DIR/$subdir" ]; then
                        rm -rf "$TARGET_DIR/$subdir"
                        cp -r "$SOURCE_DIR/$subdir" "$TARGET_DIR/"
                    fi
                done
                
                echo "    ✓ Synced successfully"
                SYNCED=$((SYNCED + 1))
                else
                    echo "    ⚠ No SKILL.md found at path: $path"
                    FAILED=$((FAILED + 1))
                fi
            fi
        else
            echo "    ⚠ Failed to clone: $source"
            FAILED=$((FAILED + 1))
        fi
        rm -rf "$TEMP_DIR"
    done
    
    echo ""
    echo "  Sync complete: $SYNCED synced, $FAILED failed"
    
    # Update lastSync timestamp
    if [ "$DRY_RUN" = false ]; then
        TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        jq --arg ts "$TIMESTAMP" '.lastSync = $ts' "$SCRIPT_DIR/.sync-config.json" > "$SCRIPT_DIR/.sync-config.json.tmp"
        mv "$SCRIPT_DIR/.sync-config.json.tmp" "$SCRIPT_DIR/.sync-config.json"

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
    else
        echo ""
        echo "  [DRY-RUN] Would run: python3 scripts/normalize_skill_frontmatter.py <synced-skill>"
        echo "  [DRY-RUN] Would run: python3 scripts/sync_source_notes.py"
        echo "  [DRY-RUN] Would run: python3 scripts/sync_readme_sources.py"
        echo "  [DRY-RUN] Would run: python3 scripts/check_attribution_guardrails.py"
    fi
else
    echo "→ No .sync-config.json found, skipping external sync"
fi

echo ""

# =============================================================================
# 4. Reinstall Skills (unless --sync-only)
# =============================================================================

if [ "$SYNC_ONLY" = false ]; then
    echo "→ Reinstalling skills..."
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would run: ./install.sh"
    else
        "$SCRIPT_DIR/install.sh"
    fi
else
    echo "→ Skipping reinstall (--sync-only mode)"
fi

# =============================================================================
# 5. Summary
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Update Complete!"
echo ""
echo "Skills directory: $SCRIPT_DIR/skills"
echo "Sync config:      $SCRIPT_DIR/.sync-config.json"
if [ -f "$SCRIPT_DIR/.sync-config.json" ]; then
    LAST_SYNC=$(jq -r '.lastSync // "never"' "$SCRIPT_DIR/.sync-config.json")
    echo "Last synced:      $LAST_SYNC"
fi
echo ""
echo "Next steps:"
echo "  1. Restart your IDE / CLI to discover updated skills"
echo "  2. Run './update.sh --help' for more options"
echo "═══════════════════════════════════════════════════════════════"
