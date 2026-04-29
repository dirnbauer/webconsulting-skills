# Release Workflow Validation Before Tagging

Reusable workflows referenced inside `.github/workflows/release.yml` are resolved
at the pinned SHA at the moment the tag is pushed. If that SHA no longer contains
the referenced workflow file (renamed, deleted, or moved upstream), the release
run fails immediately with a "workflow not found" error.

By the time the CI reports the failure, the tag may already have been consumed by
a `gh release create` step that ran earlier in the same job — making the tag
permanently burned on GitHub.

## Validate Before Tagging

Run this helper script locally before `git tag`:

```bash
#!/usr/bin/env bash
# scripts/validate-release-workflow-refs.sh
# Checks every uses: <owner>/<repo>/.github/workflows/*.yml@<sha> reference
# in .github/workflows/release.yml to ensure the file exists at that SHA.

set -euo pipefail

RELEASE_YF=".github/workflows/release.yml"

echo "Validating reusable workflow references in $RELEASE_YF ..."

FAILED=0

while IFS= read -r ref; do
  # ref format: owner/repo/.github/workflows/file.yml@sha
  owner_repo="${ref%%/.github/*}"
  rest="${ref#*/}"
  rest="${rest#*/}"
  sha="${ref##*@}"
  workflow_path="${rest%@*}"

  url="https://raw.githubusercontent.com/${owner_repo}/${sha}/${workflow_path}"
  http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")

  if [ "$http_code" = "200" ]; then
    echo "  OK  $ref"
  else
    echo "  FAIL (HTTP $http_code): $ref"
    echo "       URL checked: $url"
    FAILED=1
  fi
done < <(grep -oP 'uses:\s*\K[^\s#]+' "$RELEASE_YF" | grep '\.github/workflows/')

if [ "$FAILED" -eq 1 ]; then
  echo ""
  echo "ERROR: One or more reusable workflow references are broken."
  echo "Update the SHA references in $RELEASE_YF before tagging."
  exit 1
fi

echo "All reusable workflow references are valid."
```

Run it:

```bash
bash scripts/validate-release-workflow-refs.sh
```

If the script exits 0, proceed with tagging.

## Common Causes of Broken References

- **Upstream consolidation**: `tests.yml` renamed to `ci.yml` in the referenced repo
- **SHA rotation**: The repo pinned a commit that was later force-pushed (rare but possible on non-protected branches)
- **Repo rename or transfer**: The `owner/repo` portion of the `uses:` reference changed
- **Workflow file deleted**: The upstream project removed a workflow as part of restructuring

## Tagging and the "Burned Tag" Problem

**Safe to re-tag**: If the release workflow failed before `gh release create` ran (e.g., the `uses:` reference check is the very first step), the tag exists in git but no GitHub Release was published. You can safely delete and recreate the tag:

```bash
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3
# fix the issue
git tag -s v1.2.3 -m "v1.2.3"
git push origin v1.2.3
```

**Burned tag**: If `gh release create` ran and created a GitHub Release (even a draft), the tag is permanently locked. GitHub will refuse to create a new release on the same tag name, even after deleting the release and the tag. You must use a new patch version (e.g., `v1.2.4`).

## Making the Release Workflow Self-Validating

Add the validation as the first step in the release job:

```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>

      - name: Validate reusable workflow references
        run: bash scripts/validate-release-workflow-refs.sh

      # ... rest of release steps
```

This prevents any release from proceeding if upstream workflow files have shifted,
and it fails fast — before any release assets, tags, or GitHub Releases are created.
