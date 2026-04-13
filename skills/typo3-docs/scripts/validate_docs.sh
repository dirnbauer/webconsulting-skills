#!/usr/bin/env bash
#
# Validate TYPO3 documentation RST files
#
# Usage: ./validate_docs.sh [project_root]
#

set -e

PROJECT_ROOT="${1:-.}"
DOC_DIR="$PROJECT_ROOT/Documentation"

if [ ! -d "$DOC_DIR" ]; then
    echo "Error: Documentation/ directory not found at $PROJECT_ROOT"
    echo "Usage: $0 [project_root]"
    exit 1
fi

echo "🔍 Validating TYPO3 documentation..."
echo "   Directory: $DOC_DIR"
echo ""

# Check for RST files
RST_FILES=$(find "$DOC_DIR" -name "*.rst" 2>/dev/null | wc -l)
if [ "$RST_FILES" -eq 0 ]; then
    echo "❌ No RST files found in Documentation/"
    exit 1
fi

echo "Found $RST_FILES RST files"
echo ""

# Check for guides.xml (modern) or Settings.cfg (legacy)
if [ -f "$DOC_DIR/guides.xml" ]; then
    echo "✅ guides.xml found (modern PHP-based rendering)"
elif [ -f "$DOC_DIR/Settings.cfg" ]; then
    echo "✅ Settings.cfg found (legacy Sphinx-based rendering)"
    echo "   ℹ️  Consider migrating to guides.xml for modern rendering"
else
    echo "⚠️  Warning: Neither guides.xml nor Settings.cfg found"
    echo "   One of these files is required for TYPO3 Intercept builds"
    echo "   Recommended: Create guides.xml (modern PHP-based rendering)"
fi

# Check for Index.rst
if [ ! -f "$DOC_DIR/Index.rst" ]; then
    echo "❌ Error: Index.rst not found"
    echo "   This is the main entry point and is required"
    exit 1
fi

echo "✅ Index.rst found"

# Validate RST syntax if rst2html.py is available
if command -v rst2html.py &> /dev/null; then
    echo ""
    echo "Checking RST syntax..."

    ERRORS=0
    while IFS= read -r -d '' file; do
        if ! rst2html.py --strict "$file" > /dev/null 2>&1; then
            echo "❌ Syntax error in: $file"
            ERRORS=$((ERRORS + 1))
        fi
    done < <(find "$DOC_DIR" -name "*.rst" -print0)

    if [ $ERRORS -eq 0 ]; then
        echo "✅ All RST files have valid syntax"
    else
        echo ""
        echo "❌ Found $ERRORS files with syntax errors"
        exit 1
    fi
else
    echo "⚠️  rst2html.py not found - skipping syntax validation"
    echo "   Install with: pip install docutils"
fi

# Check for common issues
echo ""
echo "Checking for common issues..."

# Check for common issues in a single pass over all RST files
WARNINGS=0
HEADING_ERRORS=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while IFS= read -r -d '' file; do
    # Check for :ref: references
    if grep -q ':ref:`[^<]*`' "$file"; then
        REF_COUNT=$(grep -o ':ref:`[^`]*`' "$file" | wc -l)
        if [ "$REF_COUNT" -gt 0 ]; then
            echo "ℹ️  Found $REF_COUNT :ref: references in $(basename "$file")"
        fi
    fi

    # Check for UTF-8 encoding
    if ! file -b --mime-encoding "$file" | grep -qE 'utf-8|us-ascii'; then
        echo "⚠️  Non-UTF-8 encoding in: $file"
        WARNINGS=$((WARNINGS + 1))
    fi

    # Check for trailing whitespace
    if grep -q '[[:space:]]$' "$file"; then
        echo "⚠️  Trailing whitespace in: $file"
        WARNINGS=$((WARNINGS + 1))
    fi

    # Check TYPO3 heading hierarchy (= for h1/h2, - for h3, ~ for h4)
    RESULT=$(python3 "$SCRIPT_DIR/validate_headings.py" "$file" 2>/dev/null)
    if [ -n "$RESULT" ]; then
        echo "❌ Heading hierarchy issue in: $(basename "$file")"
        echo "$RESULT"
        HEADING_ERRORS=$((HEADING_ERRORS + 1))
    fi
done < <(find "$DOC_DIR" -name "*.rst" -print0)

echo ""
echo "Checking heading hierarchy..."
if [ $HEADING_ERRORS -eq 0 ]; then
    echo "✅ Heading hierarchy follows TYPO3 convention"
else
    echo "❌ Found $HEADING_ERRORS files with heading hierarchy issues"
    echo "   TYPO3 heading order: = (h1 title, above+below), = (h2), - (h3), ~ (h4)"
    WARNINGS=$((WARNINGS + HEADING_ERRORS))
fi

echo ""
if [ $WARNINGS -eq 0 ]; then
    echo "✅ No common issues found"
else
    echo "⚠️  Found $WARNINGS warnings (not blocking)"
fi

echo ""
echo "Validation summary:"
echo "  RST files: $RST_FILES"
echo "  Warnings: $WARNINGS"
echo ""
echo "✅ Documentation validation complete"
echo ""
echo "Next step: Render locally to check for broken references"
echo "   ./render_docs.sh $PROJECT_ROOT"
