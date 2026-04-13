#!/usr/bin/env bash
# Check that substitutions defined in Includes.rst.txt are used where appropriate
set -euo pipefail

includes_file="Documentation/Includes.rst.txt"
[ ! -f "$includes_file" ] && exit 0

# Extract defined substitutions (e.g., |version|, |php_version|)
substitutions=$(grep -oP '^\.\.\s*\|([^|]+)\|' "$includes_file" 2>/dev/null | grep -oP '\|[^|]+\|' || true)

[ -z "$substitutions" ] && exit 0

found=0

# Check Introduction/Index.rst and Installation/Index.rst for hardcoded values
# that should use substitutions instead
for target in Documentation/Introduction/Index.rst Documentation/Installation/Index.rst; do
    [ ! -f "$target" ] && continue

    while IFS= read -r sub; do
        [ -z "$sub" ] && continue
        # Get the substitution value from Includes.rst.txt
        # Escape pipe characters for use in grep regex
        sub_escaped=$(echo "$sub" | sed 's/|/\\|/g')
        sub_value=$(grep -P "^\.\.\s*${sub_escaped}\s+replace::" "$includes_file" 2>/dev/null | grep -oP '::\s*.*$' | sed 's/^::\s*//' || true)
        [ -z "$sub_value" ] && continue

        # Check if the hardcoded value appears in target but the substitution does not
        if grep -qF "$sub_value" "$target" 2>/dev/null && ! grep -qF "$sub" "$target" 2>/dev/null; then
            echo "$target: hardcoded '$sub_value' found — use substitution $sub instead"
            found=1
        fi
    done <<< "$substitutions"
done

exit "$found"
