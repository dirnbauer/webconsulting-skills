#!/usr/bin/env bash
# Check that Documentation contains required sections
set -euo pipefail

[ ! -d Documentation/ ] && echo "Documentation/ directory missing" && exit 1

missing=()

# Core required sections
for section in Introduction Installation Configuration Usage; do
    if [ ! -d "Documentation/$section" ] || [ ! -f "Documentation/$section/Index.rst" ]; then
        missing+=("$section")
    fi
done

# Developer section (recommended)
if [ ! -d "Documentation/Developer" ] || [ ! -f "Documentation/Developer/Index.rst" ]; then
    missing+=("Developer")
fi

# Troubleshooting/FAQ (either name accepted)
if [ ! -d "Documentation/Troubleshooting" ] && [ ! -d "Documentation/FAQ" ] && \
   [ ! -d "Documentation/KnownProblems" ]; then
    missing+=("Troubleshooting/FAQ")
fi

# Security section only required if extension deals with security
# Check ext_emconf.php category or extension key for security indicators
is_security=0
if [ -f ext_emconf.php ]; then
    if grep -qiP "'category'\s*=>\s*'(security|auth)'" ext_emconf.php 2>/dev/null; then
        is_security=1
    fi
fi
if [ -f composer.json ]; then
    if grep -qiP '"keywords".*\b(security|authentication|encryption)\b' composer.json 2>/dev/null; then
        is_security=1
    fi
fi

if [ "$is_security" -eq 1 ]; then
    if [ ! -d "Documentation/Security" ] && [ ! -f "Documentation/Security/Index.rst" ]; then
        missing+=("Security (security-related extension)")
    fi
fi

if [ ${#missing[@]} -gt 0 ]; then
    echo "Missing documentation sections: ${missing[*]}"
    exit 1
fi

exit 0
