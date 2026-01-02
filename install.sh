#!/bin/bash
# webconsulting Agent Skills Installer
# Usage: ./install.sh
#
# This script symlinks skills to Claude's skill directory and
# generates Cursor rules from SKILL.md files.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     webconsulting AI Environment Installer                   ║"
echo "║     TYPO3 Agent Skills for Claude & Cursor                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Define Standard Paths
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
CURSOR_RULES_DIR="$SCRIPT_DIR/.cursor/rules"

# 2. Create Directory Structures
echo "→ Creating directory structures..."
mkdir -p "$CLAUDE_SKILLS_DIR"
mkdir -p "$CURSOR_RULES_DIR"

# 3. Symlink Agent Skills (Anthropic Standard)
echo ""
echo "→ Linking Agent Skills to ~/.claude/skills..."
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

# 4. Generate Cursor Rules from Skills (Bridge Logic)
# Cursor does not natively read SKILL.md, so we generate .mdc rules
echo ""
echo "→ Bridging Skills to Cursor Rules..."
for skill_file in "$SCRIPT_DIR/skills"/*/SKILL.md; do
    if [ -f "$skill_file" ]; then
        skill_name=$(basename "$(dirname "$skill_file")")
        target_rule="$CURSOR_RULES_DIR/${skill_name}.mdc"
        
        # Copy SKILL.md content to .mdc file
        cp "$skill_file" "$target_rule"
        echo "  ✓ Generated Rule: ${skill_name}.mdc"
    fi
done

# 5. Verify Installation
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Installation Complete!"
echo ""
echo "Skills installed to: $CLAUDE_SKILLS_DIR"
echo "Cursor rules at:     $CURSOR_RULES_DIR"
echo ""
echo "Next steps:"
echo "  1. Restart Cursor IDE to load the new rules"
echo "  2. Configure MCP servers in .cursor/mcp.json"
echo "  3. Run 'git pull && ./install.sh' to update skills"
echo "═══════════════════════════════════════════════════════════════"

