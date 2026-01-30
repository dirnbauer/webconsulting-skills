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
# This script updates Agent Skills from external sources and reinstalls them.
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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
    
    for skill_b64 in $SKILLS; do
        skill=$(echo "$skill_b64" | base64 --decode)
        name=$(echo "$skill" | jq -r '.name')
        source=$(echo "$skill" | jq -r '.source')
        branch=$(echo "$skill" | jq -r '.branch')
        path=$(echo "$skill" | jq -r '.path // "."')
        note=$(echo "$skill" | jq -r '.note // ""')
        
        echo "  Syncing: $name"
        [ -n "$note" ] && echo "    Note: $note"
        
        if [ "$DRY_RUN" = true ]; then
            echo "    [DRY-RUN] Would clone $source (branch: $branch, path: $path)"
            continue
        fi
        
        TEMP_DIR=$(mktemp -d)
        if git clone --depth 1 --branch "$branch" "$source" "$TEMP_DIR" 2>/dev/null; then
            SOURCE_DIR="$TEMP_DIR/$path"
            TARGET_DIR="$SCRIPT_DIR/skills/$name"
            
            if [ -f "$SOURCE_DIR/SKILL.md" ]; then
                mkdir -p "$TARGET_DIR"
                cp "$SOURCE_DIR/SKILL.md" "$TARGET_DIR/SKILL.md"
                
                # Copy subdirectories if they exist
                for subdir in examples rules references scripts assets; do
                    if [ -d "$SOURCE_DIR/$subdir" ]; then
                        rm -rf "$TARGET_DIR/$subdir"
                        cp -r "$SOURCE_DIR/$subdir" "$TARGET_DIR/"
                    fi
                done
                
                echo "    ✓ Synced successfully"
                ((SYNCED++))
            else
                echo "    ⚠ No SKILL.md found at path: $path"
                ((FAILED++))
            fi
        else
            echo "    ⚠ Failed to clone: $source"
            ((FAILED++))
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
echo "  1. Restart Cursor IDE or Claude Code to load updated skills"
echo "  2. Run './update.sh --help' for more options"
echo "═══════════════════════════════════════════════════════════════"
