#!/usr/bin/env bash
# Check that CHANGELOG.md has entries for all git tags
set -euo pipefail

changelog=""
for f in CHANGELOG.md Changelog.md changelog.md Documentation/ChangeLog/Index.rst; do
    [ -f "$f" ] && changelog="$f" && break
done

[ -z "$changelog" ] && echo "No changelog file found" && exit 1

# Get all version-like tags
tags=$({ git tag -l 2>/dev/null | grep -P '^\d+\.\d+' || true; git tag -l 2>/dev/null | grep -P '^v\d+\.\d+' | sed 's/^v//' || true; })

[ -z "$tags" ] && exit 0

missing=()

while IFS= read -r tag; do
    [ -z "$tag" ] && continue
    # Strip leading 'v' for matching
    version=$(echo "$tag" | sed 's/^v//')
    if ! grep -qF "[${version}]" "$changelog" 2>/dev/null; then
        missing+=("$version")
    fi
done <<< "$tags"

if [ ${#missing[@]} -gt 0 ]; then
    echo "Versions missing from $changelog: ${missing[*]}"
    exit 1
fi

exit 0
