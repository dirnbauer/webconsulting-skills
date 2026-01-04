#!/bin/bash
# webconsulting Agent Skills Installer
# Usage: ./install.sh
#
# This script:
# - Symlinks skills to ~/.claude/skills (when running locally, not in DDEV)
# - Installs Cursor rules to the PROJECT's .cursor/rules/ directory
# - Generates .mdc rules from SKILL.md files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     webconsulting AI Environment Installer                   ║"
echo "║     TYPO3 Agent Skills for Claude & Cursor                   ║"
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

# Detect project root (go up from vendor/webconsulting/claude-typo3-skills)
# This works when installed via composer
if [ -f "$SCRIPT_DIR/../../../composer.json" ]; then
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
    echo "→ Project root: $PROJECT_ROOT"
else
    # Fallback: use current working directory if composer.json exists there
    if [ -f "$PWD/composer.json" ]; then
        PROJECT_ROOT="$PWD"
        echo "→ Project root (from cwd): $PROJECT_ROOT"
    else
        echo "⚠ Warning: Could not detect project root. Using script directory."
        PROJECT_ROOT="$SCRIPT_DIR"
    fi
fi

# =============================================================================
# 2. Define Installation Paths
# =============================================================================

CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
PROJECT_RULES_DIR="$PROJECT_ROOT/.cursor/rules"
VENDOR_RULES_DIR="$SCRIPT_DIR/.cursor/rules"

# =============================================================================
# 3. Install Cursor Rules to PROJECT (primary installation)
# =============================================================================

echo ""
echo "→ Installing Cursor rules to project..."
mkdir -p "$PROJECT_RULES_DIR"

# First, generate .mdc files from SKILL.md in vendor directory
mkdir -p "$VENDOR_RULES_DIR"
for skill_file in "$SCRIPT_DIR/skills"/*/SKILL.md; do
    if [ -f "$skill_file" ]; then
        skill_name=$(basename "$(dirname "$skill_file")")
        target_rule="$VENDOR_RULES_DIR/${skill_name}.mdc"
        cp "$skill_file" "$target_rule"
    fi
done

# Now symlink all .mdc rules from vendor to project's .cursor/rules/
for rule_file in "$VENDOR_RULES_DIR"/*.mdc; do
    if [ -f "$rule_file" ]; then
        rule_name=$(basename "$rule_file")
        target="$PROJECT_RULES_DIR/$rule_name"
        
        # Remove existing file/link to prevent conflicts
        if [ -L "$target" ] || [ -f "$target" ]; then
            rm -f "$target"
        fi
        
        # Create symlink (use -f to force overwrite)
        ln -sf "$rule_file" "$target"
        echo "  ✓ Linked Rule: $rule_name"
    fi
done

# =============================================================================
# 4. Install Claude Skills (only on local machine, not in container)
# =============================================================================

if [ "$IS_CONTAINER" = "true" ]; then
    echo ""
    echo "→ Skipping ~/.claude/skills (running in container)"
    echo "  Run this script on your local machine to install skills there."
else
    echo ""
    echo "→ Linking Agent Skills to ~/.claude/skills..."
    mkdir -p "$CLAUDE_SKILLS_DIR"
    
    for skill_path in "$SCRIPT_DIR/skills"/*; do
        if [ -d "$skill_path" ]; then
            skill_name=$(basename "$skill_path")
            target="$CLAUDE_SKILLS_DIR/$skill_name"
            
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
# 5. Summary
# =============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Installation Complete!"
echo ""
echo "Cursor rules at:     $PROJECT_RULES_DIR"
if [ "$IS_CONTAINER" = "true" ]; then
    echo "Skills:              (skipped - run locally to install)"
else
    echo "Skills installed to: $CLAUDE_SKILLS_DIR"
fi
echo ""
echo "Next steps:"
echo "  1. Restart Cursor IDE to load the new rules"
if [ "$IS_CONTAINER" = "true" ]; then
    echo "  2. Run './vendor/webconsulting/claude-typo3-skills/install.sh'"
    echo "     on your LOCAL machine to install ~/.claude/skills"
fi
echo "═══════════════════════════════════════════════════════════════"
