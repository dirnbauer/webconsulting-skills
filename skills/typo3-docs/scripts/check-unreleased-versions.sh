#!/usr/bin/env bash
# Check that versionadded/versionchanged directives reference released versions only
set -euo pipefail

grep -rn 'versionadded\|versionchanged' Documentation/ 2>/dev/null \
    | grep -oP '\d+\.\d+\.\d+' \
    | sort -u \
    | while read ver; do
        grep -q "$ver" ext_emconf.php 2>/dev/null && continue
        git tag -l "$ver" 2>/dev/null | grep -q . && continue
        git tag -l "v$ver" 2>/dev/null | grep -q . && continue
        echo "Unreleased version referenced: $ver"
        exit 1
    done

exit 0
