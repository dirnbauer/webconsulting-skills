#!/bin/bash
# ============================================================================
# webconsulting Agent Skills Installer
# ============================================================================
# 
# Works with: Claude Code, Cursor IDE (tested with Cursor 2.2+)
#
# Usage: ./install.sh
#
# This script installs Agent Skills to ~/.claude/skills (shared by Cursor & Claude Code)
#
# Both Cursor and Claude Code now use the same unified location:
# - ~/.claude/skills/ (user-level, primary - works for both Cursor and Claude Code)
# - .cursor/skills/ (project-level)
# - .cursor/rules/ (legacy .mdc format for backwards compatibility)
#
# We install to ~/.claude/skills as the primary location.
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     webconsulting AI Environment Installer                   ║"
echo "║     TYPO3 Agent Skills for Cursor & Claude                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# =============================================================================
# 1. Environment Detection
# =============================================================================

# Detect if running inside DDEV/Docker container
IS_CONTAINER=false
if [ -n "$DDEV_SITENAME" ] || [ -f "/.dockerenv" ] || [ -n "$DOCKER_CONTAINER" ]; then
    IS_CONTAINER=true
    echo "→ Detected: Running inside container (DDEV/Docker)"
else
    echo "→ Detected: Running on local machine"
fi

# Detect project root (go up from vendor/webconsulting/webconsulting-skills)
if [ -f "$SCRIPT_DIR/../../../composer.json" ]; then
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
    echo "→ Project root: $PROJECT_ROOT"
else
    if [ -f "$PWD/composer.json" ]; then
        PROJECT_ROOT="$PWD"
        echo "→ Project root (from cwd): $PROJECT_ROOT"
    else
        echo "⚠ Warning: Could not detect project root. Using script directory."
        PROJECT_ROOT="$SCRIPT_DIR"
    fi
fi

# =============================================================================
# 2. Sync External Skills (from .sync-config.json)
# =============================================================================

if [ -f "$SCRIPT_DIR/.sync-config.json" ] && command -v jq &> /dev/null && command -v git &> /dev/null; then
    echo ""
    echo "→ Syncing external skills from .sync-config.json..."
    
    # Read enabled skills
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
                
                # Copy examples if exists
                if [ -d "$SOURCE_DIR/examples" ]; then
                    rm -rf "$TARGET_DIR/examples"
                    cp -r "$SOURCE_DIR/examples" "$TARGET_DIR/"
                fi
                
                # Copy rules if exists
                if [ -d "$SOURCE_DIR/rules" ]; then
                    rm -rf "$TARGET_DIR/rules"
                    cp -r "$SOURCE_DIR/rules" "$TARGET_DIR/"
                fi
                
                echo "  ✓ Synced: $name"
            else
                echo "  ⚠ No SKILL.md found in $source (path: $path)"
            fi
        else
            echo "  ⚠ Failed to sync: $name (clone failed)"
        fi
        rm -rf "$TEMP_DIR"
    done
else
    echo ""
    if [ ! -f "$SCRIPT_DIR/.sync-config.json" ]; then
        echo "→ No .sync-config.json found, skipping external sync"
    elif ! command -v jq &> /dev/null; then
        echo "→ jq not installed, skipping external sync (install with: brew install jq)"
    elif ! command -v git &> /dev/null; then
        echo "→ git not installed, skipping external sync"
    fi
fi

# =============================================================================
# 3. Define Installation Paths
# =============================================================================

# Primary: Unified skills directory (works for both Cursor and Claude Code)
USER_SKILLS_DIR="$HOME/.claude/skills"

# Project-level skills (optional, for version-controlled skills)
PROJECT_SKILLS_DIR="$PROJECT_ROOT/.cursor/skills"

# Legacy: Cursor rules directory (for .mdc files - deprecated but still works)
PROJECT_RULES_DIR="$PROJECT_ROOT/.cursor/rules"

# =============================================================================
# 4. Install Agent Skills (Unified Location - Cursor & Claude Code)
# =============================================================================

if [ "$IS_CONTAINER" = "true" ]; then
    echo ""
    echo "→ Skipping user-level skill installation (running in container)"
    echo "  Run this script on your local machine to install skills."
else
    echo ""
    echo "→ Installing Agent Skills to ~/.claude/skills..."
    echo "  (Unified location for Cursor & Claude Code)"
    mkdir -p "$USER_SKILLS_DIR"
    
    for skill_path in "$SCRIPT_DIR/skills"/*; do
        if [ -d "$skill_path" ] && [ -f "$skill_path/SKILL.md" ]; then
            skill_name=$(basename "$skill_path")
            target="$USER_SKILLS_DIR/$skill_name"
            
            # Remove existing links/dirs to prevent conflicts
            if [ -L "$target" ] || [ -d "$target" ]; then
                rm -rf "$target"
            fi
            
            ln -s "$skill_path" "$target"
            echo "  ✓ Installed Skill: $skill_name"
        fi
    done
fi

# =============================================================================
# 5. Install Project-Level Skills (Optional - for version-controlled projects)
# =============================================================================

echo ""
echo "→ Installing project-level skills to .cursor/skills..."
mkdir -p "$PROJECT_SKILLS_DIR"

for skill_path in "$SCRIPT_DIR/skills"/*; do
    if [ -d "$skill_path" ] && [ -f "$skill_path/SKILL.md" ]; then
        skill_name=$(basename "$skill_path")
        target="$PROJECT_SKILLS_DIR/$skill_name"
        
        # Remove existing file/link to prevent conflicts
        if [ -L "$target" ] || [ -d "$target" ]; then
            rm -rf "$target"
        fi
        
        # Symlink to source
        ln -s "$skill_path" "$target"
        echo "  ✓ Linked Skill: $skill_name"
    fi
done

# =============================================================================
# 6. Legacy: Install Cursor Rules (.mdc format - still works in 2.2+)
# =============================================================================

echo ""
echo "→ Installing legacy Cursor rules (.mdc) for backwards compatibility..."
mkdir -p "$PROJECT_RULES_DIR"

for skill_path in "$SCRIPT_DIR/skills"/*; do
    if [ -d "$skill_path" ] && [ -f "$skill_path/SKILL.md" ]; then
        skill_name=$(basename "$skill_path")
        target_rule="$PROJECT_RULES_DIR/${skill_name}.mdc"
        
        # Remove existing file/link
        if [ -L "$target_rule" ] || [ -f "$target_rule" ]; then
            rm -f "$target_rule"
        fi
        
        # Copy SKILL.md to .mdc (legacy format)
        cp "$skill_path/SKILL.md" "$target_rule"
        echo "  ✓ Created Rule: ${skill_name}.mdc"
    fi
done

# =============================================================================
# 7. Copy AGENTS.md to project root (if different from source)
# =============================================================================

if [ -f "$SCRIPT_DIR/AGENTS.md" ] && [ "$SCRIPT_DIR" != "$PROJECT_ROOT" ]; then
    echo ""
    echo "→ Installing AGENTS.md to project root..."
    cp "$SCRIPT_DIR/AGENTS.md" "$PROJECT_ROOT/AGENTS.md"
    echo "  ✓ Installed: AGENTS.md"
fi

# =============================================================================
# 8. Summary
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Installation Complete!"
echo ""
if [ "$IS_CONTAINER" = "true" ]; then
    echo "Skills (project):    $PROJECT_SKILLS_DIR"
    echo "Skills (user):       (skipped - run locally to install)"
else
    echo "Skills (user):       $USER_SKILLS_DIR"
    echo "Skills (project):    $PROJECT_SKILLS_DIR"
fi
echo "Legacy rules:        $PROJECT_RULES_DIR"
echo ""
echo "Both Cursor and Claude Code discover skills from:"
echo "  - ~/.claude/skills/  (user-level, unified location)"
echo "  - .cursor/skills/    (project-level)"
echo ""
echo "Next steps:"
echo "  1. Restart Cursor IDE or Claude Code to load skills"
echo "  2. Type / in Agent chat to see available skills"
if [ "$IS_CONTAINER" = "true" ]; then
    echo "  3. Run install.sh on LOCAL machine for user-level skills"
fi
echo "═══════════════════════════════════════════════════════════════"
