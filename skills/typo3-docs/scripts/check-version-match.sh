#!/usr/bin/env bash
# Check that guides.xml version matches ext_emconf.php version
set -euo pipefail

guides_ver=$(grep -oP 'version="[^"]*"' Documentation/guides.xml 2>/dev/null | head -1 | grep -oP '"[^"]*"' | tr -d '"')
emconf_ver=$(grep -oP "'version'\s*=>\s*'[^']*'" ext_emconf.php 2>/dev/null | grep -oP "'[^']*'$" | tr -d "'")

if [ -n "$guides_ver" ] && [ -n "$emconf_ver" ] && [ "$guides_ver" != "$emconf_ver" ]; then
    echo "Version mismatch: guides.xml=$guides_ver ext_emconf.php=$emconf_ver"
    exit 1
fi

exit 0
