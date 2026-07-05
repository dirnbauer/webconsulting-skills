#!/usr/bin/env bash
set -euo pipefail

mkdir -p .a11y/raw

if [[ ! -f .a11y/a11y.config.yml ]]; then
  echo "Missing .a11y/a11y.config.yml"
  echo "Create it with: cp .a11y/a11y.config.example.yml .a11y/a11y.config.yml"
  exit 1
fi

npm run a11y:discover
npm run a11y:templates
A11Y_REPORT_ONLY=1 npm run a11y:test
npm run a11y:report
npm run a11y:statement

echo
echo "Done. Open:"
echo "  .a11y/report.md"
echo "  .a11y/open-issues.yml"
echo "  .a11y/accessibility-statement-draft.de.md"
