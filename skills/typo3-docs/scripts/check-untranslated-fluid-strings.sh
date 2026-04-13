#!/usr/bin/env bash
# Check Fluid templates for hardcoded English strings in user-facing attributes
# Flags title, aria-label, alt attributes with >3 English words not using f:translate
set -euo pipefail

# Find all Fluid template files
fluid_files=$(find Resources/Private/ -name '*.html' -type f 2>/dev/null || true)

[ -z "$fluid_files" ] && exit 0

found=0

while IFS= read -r file; do
    [ -z "$file" ] && continue
    # Check for title, aria-label, alt attributes with hardcoded strings (>3 words)
    # Exclude lines that use f:translate or {f:translate()} syntax
    while IFS= read -r match; do
        [ -z "$match" ] && continue
        # Process each attribute match separately (a line may contain multiple attributes)
        while IFS= read -r attr_match; do
            [ -z "$attr_match" ] && continue
            # Extract the attribute value
            value=$(echo "$attr_match" | grep -oP '"[^"]*"' | tr -d '"')
            [ -z "$value" ] && continue
            # Skip if it contains f:translate or LLL: or curly braces (Fluid expression)
            echo "$value" | grep -qP '(f:translate|LLL:|{.*})' && continue
            # Count words
            word_count=$(echo "$value" | wc -w)
            if [ "$word_count" -gt 3 ]; then
                echo "$file: hardcoded string ($word_count words) in attribute: $value"
                found=1
            fi
        done < <(echo "$match" | grep -oP '(title|aria-label|alt)="[^"]*"' || true)
    done < <(grep -nP '(title|aria-label|alt)="[^"]*"' "$file" 2>/dev/null || true)
done <<< "$fluid_files"

exit "$found"
