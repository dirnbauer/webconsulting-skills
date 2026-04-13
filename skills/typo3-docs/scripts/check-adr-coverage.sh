#!/usr/bin/env bash
# Check that extensions with >10 classes have ADR documentation
set -euo pipefail

[ ! -d Classes/ ] && exit 0

# Count PHP classes
class_count=$(find Classes/ -name '*.php' -type f 2>/dev/null | wc -l)

if [ "$class_count" -gt 10 ]; then
    if [ ! -d "Documentation/Developer/Adr" ] && [ ! -d "Documentation/Developer/ADR" ] && \
       [ ! -d "docs/adr" ]; then
        echo "Extension has $class_count classes but no ADR directory (Documentation/Developer/Adr/)"
        echo "Significant architectural decisions should be documented as Architecture Decision Records"
        exit 1
    fi
fi

exit 0
