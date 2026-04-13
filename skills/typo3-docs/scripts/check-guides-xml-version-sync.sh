#!/usr/bin/env bash
# Check that guides.xml version AND release attributes both match ext_emconf.php version
set -euo pipefail

[ ! -f Documentation/guides.xml ] && exit 0
[ ! -f ext_emconf.php ] && exit 0

guides_version=$(grep -oP 'version="[^"]*"' Documentation/guides.xml 2>/dev/null | head -1 | grep -oP '"[^"]*"' | tr -d '"')
guides_release=$(grep -oP 'release="[^"]*"' Documentation/guides.xml 2>/dev/null | head -1 | grep -oP '"[^"]*"' | tr -d '"')
emconf_ver=$(grep -oP "'version'\s*=>\s*'[^']*'" ext_emconf.php 2>/dev/null | grep -oP "'[^']*'$" | tr -d "'")

errors=0

if [ -n "$guides_version" ] && [ -n "$emconf_ver" ] && [ "$guides_version" != "$emconf_ver" ]; then
    echo "Version mismatch: guides.xml version=\"$guides_version\" != ext_emconf.php version='$emconf_ver'"
    errors=1
fi

if [ -n "$guides_release" ] && [ -n "$emconf_ver" ] && [ "$guides_release" != "$emconf_ver" ]; then
    echo "Release mismatch: guides.xml release=\"$guides_release\" != ext_emconf.php version='$emconf_ver'"
    errors=1
fi

if [ -n "$guides_version" ] && [ -n "$guides_release" ] && [ "$guides_version" != "$guides_release" ]; then
    echo "Internal mismatch: guides.xml version=\"$guides_version\" != release=\"$guides_release\""
    errors=1
fi

exit "$errors"
