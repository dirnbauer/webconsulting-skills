# TER Publishing Reference

**Purpose:** Document requirements and best practices for publishing TYPO3 extensions to the TER (TYPO3 Extension Repository)

## Overview

The TYPO3 Extension Repository (TER) at [extensions.typo3.org](https://extensions.typo3.org) is the official distribution platform for TYPO3 extensions. Publishing is typically automated via GitHub Actions using the official `typo3/tailor` tool.

---

## Upload Comment Format

The "Last upload comment" field displayed on extension pages has specific format requirements:

### Allowed Content
- **Type:** Plain text only (no HTML, Markdown, or rich formatting)
- **Letters, numbers, whitespace**
- **Basic punctuation:** `" % & [ ] ( ) . , ; : / ? { } ! $ - @`
- **Newlines:** Supported and displayed as line breaks (`<br>`)

### Validation
- **Required:** Cannot be empty (throws `NoUploadCommentException`)
- **Storage:** `TEXT` field in database (no enforced length limit)

### Characters Stripped in XML Export
When exported to `extensions.xml` feed, the following regex filters the comment:
```
/[^\w\s"%&\[\]\(\)\.\,\;\:\/\?\{\}!\$\-\/\@]/u
```

**Stripped characters include:** `# * + = ~ ^ | \ < >` and non-ASCII special characters

### Rendering Contexts
| Context | Processing |
|---------|------------|
| Frontend (extension page) | `<f:format.nl2br>` - newlines become `<br>` |
| Email notifications | Raw text |
| XML feed (extensions.xml) | Sanitized via `xmlentities()` |

### Best Practices
1. **Keep it concise:** Focus on key changes
2. **Use line breaks:** Structure with newlines for readability
3. **Avoid special characters:** Stick to basic punctuation
4. **Be descriptive:** Summarize the release, not just "Bug fixes"

**Good Example:**
```
Fixed critical bug in authentication module
- Resolved token expiration issue
- Updated dependency versions
- Improved error messages for version constraints
```

**Avoid:**
```
Bug fixes & improvements! See CHANGELOG.md for details...
```
(The `&` will be escaped, `...` is not fully supported)

---

## CI TER Compatibility Check

**CRITICAL:** Add this check to your CI workflow to catch ext_emconf.php issues BEFORE release attempts!

**Add to `.github/workflows/ci.yml`:**
```yaml
- id: ter-compatibility
  name: TER Compatibility Check
  run: |
    # ext_emconf.php must NOT contain strict_types - TER cannot parse it
    # Use regex to match actual declaration (not comments mentioning it)
    if grep -qE "^[[:space:]]*declare\(strict_types" ext_emconf.php; then
      echo "::error file=ext_emconf.php::ext_emconf.php contains strict_types declaration which breaks TER publishing"
      exit 1
    fi
    echo "TER compatibility check passed"
```

**Why this matters:** This check runs on every PR and push, catching strict_types issues before they reach a release attempt. Without this, you may only discover the problem when TER upload fails.

---

## Version Synchronization Check

**CRITICAL:** The `typo3/tailor` tool rejects uploads where the tag version does not match `ext_emconf.php` `'version'`. This is a common release failure.

### The Problem

When creating a release tag (e.g. `0.4.1`), `ext_emconf.php` must already contain `'version' => '0.4.1'`. If the version was not bumped before tagging, `tailor ter:publish` fails with "configured version does not match".

GitHub.com does not support custom pre-receive hooks, so server-side tag validation is not possible. Use **defense-in-depth**: local git hook + CI validation step.

### CI Workflow Step

Add this step to your TER publish workflow **after checkout and before publishing**:

```yaml
- name: Validate ext_emconf.php version
  env:
    TAG_VERSION: ${{ env.version }}
  run: |
    EMCONF_VERSION=$(grep -oP "'version'\s*=>\s*'\K[^']+" ext_emconf.php)
    if [[ "${TAG_VERSION}" != "${EMCONF_VERSION}" ]]; then
      echo "::error file=ext_emconf.php::Tag version (${TAG_VERSION}) does not match ext_emconf.php version (${EMCONF_VERSION}). Update ext_emconf.php before tagging."
      exit 1
    fi
    echo "Version validated: ${TAG_VERSION} matches ext_emconf.php"
```

### CaptainHook Pre-Push Hook

For local protection, add a pre-push hook script that checks any semver tag at HEAD:

```bash
#!/usr/bin/env bash
set -euo pipefail

TAGS=$(git tag --points-at HEAD | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' || true)
[[ -z "${TAGS}" ]] && exit 0

EMCONF_VERSION=$(grep -oP "'version'\s*=>\s*'\K[^']+" ext_emconf.php)

while IFS= read -r TAG; do
    if [[ "${TAG}" != "${EMCONF_VERSION}" ]]; then
        echo "ERROR: Tag ${TAG} does not match ext_emconf.php version ${EMCONF_VERSION}"
        exit 1
    fi
done <<< "${TAGS}"
```

Register in `captainhook.json` under `pre-push.actions[]`:
```json
{ "action": "Build/Scripts/check-tag-version.sh" }
```

### Release Process Checklist Addition

```
[ ] ext_emconf.php version bumped BEFORE creating tag
[ ] CI validates ext_emconf.php version matches tag
[ ] Pre-push hook validates locally
```

---

## CRITICAL: Upload Comment Source

**NEVER use git tag message for upload comments!**

### The Problem

When using `gh release create`, GitHub creates a **lightweight tag** (not annotated). Lightweight tags have no message, so `git tag -n1` returns the **commit message** instead:

```bash
# BAD: Gets commit message like "chore(release): v1.2.0 (#123)"
git tag -n1 -l "v${VERSION}" | sed "s/^v[0-9.]*[ ]*//g"
```

This results in TER showing unprofessional upload comments like:
- `chore(release): v13.2.0 (#508)`
- `Merge pull request #123 from feature/xyz`

### The Solution

**Always use `github.event.release.body`** (the GitHub release notes) as the comment source:

```yaml
env:
  RELEASE_BODY: ${{ github.event.release.body }}
run: |
  if [[ -n "${RELEASE_BODY}" ]]; then
    COMMENT=$(echo "${RELEASE_BODY}" | head -c 1000)
    # Strip unsupported characters
    COMMENT=$(echo "${COMMENT}" | sed 's/[#*+=~^|\\<>]//g')
  else
    COMMENT="Released version ${VERSION}"
  fi
```

### Conformance Check

When auditing extensions, verify `publish-to-ter.yml` uses:
- ✅ `github.event.release.body` - Release notes (CORRECT)
- ✅ `github.event.release.name` - Release title (fallback)
- ❌ `git tag -n1` - Tag/commit message (WRONG)

---

## GitHub Actions Workflow

### Recommended Workflow Template

**File:** `.github/workflows/publish-to-ter.yml`

**Template:** Copy from `assets/.github/workflows/publish-to-ter.yml`

```yaml
name: Publish new extension version to TER

on:
  release:
    types: [published]

jobs:
  publish:
    name: Publish new version to TER
    runs-on: ubuntu-latest
    env:
      TYPO3_EXTENSION_KEY: ${{ secrets.TYPO3_EXTENSION_KEY }}
      TYPO3_API_TOKEN: ${{ secrets.TYPO3_TER_ACCESS_TOKEN }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Validate tag format
        run: |
          if ! [[ "${GITHUB_REF_NAME}" =~ ^v[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
            echo "::error::Invalid tag format '${GITHUB_REF_NAME}'. Expected format: v1.2.3"
            exit 1
          fi

      - name: Extract version
        id: version
        run: |
          # Strip 'v' prefix for TER (expects "3.0.1" not "v3.0.1")
          VERSION="${GITHUB_REF_NAME#v}"
          echo "version=${VERSION}" >> $GITHUB_OUTPUT
          echo "Extracted version: ${VERSION}"

      - name: Prepare release comment
        id: comment
        env:
          RELEASE_BODY: ${{ github.event.release.body }}
          RELEASE_NAME: ${{ github.event.release.name }}
          RELEASE_URL: ${{ github.event.release.html_url }}
        run: |
          # Build comment from release body or name
          if [[ -n "${RELEASE_BODY}" ]]; then
            # Preserve newlines for TER display, limit length
            # TER supports newlines - they render as <br> on the frontend
            COMMENT=$(echo "${RELEASE_BODY}" | head -c 1000)
          elif [[ -n "${RELEASE_NAME}" ]]; then
            COMMENT="${RELEASE_NAME}"
          else
            COMMENT="Release ${{ steps.version.outputs.version }}"
          fi

          # Strip characters not supported in TER XML export
          # Allowed: word chars, whitespace, " % & [ ] ( ) . , ; : / ? { } ! $ - @
          COMMENT=$(echo "${COMMENT}" | sed 's/[#*+=~^|\\<>]//g')

          # Append release link on new line
          COMMENT="${COMMENT}

Details: ${RELEASE_URL}"

          # Escape for GitHub Actions output (preserve newlines)
          {
            echo "comment<<EOF"
            echo "${COMMENT}"
            echo "EOF"
          } >> $GITHUB_OUTPUT

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          extensions: intl, mbstring, json, zip, curl
          tools: composer:v2

      - name: Install tailor
        run: composer global require typo3/tailor --prefer-dist --no-progress

      - name: Publish to TER
        run: |
          TAILOR="$(composer global config bin-dir --absolute)/tailor"
          "${TAILOR}" set-version "${{ steps.version.outputs.version }}"
          "${TAILOR}" ter:publish --comment "${{ steps.comment.outputs.comment }}" "${{ steps.version.outputs.version }}"
```

### Required Secrets

| Secret | Description | Where to Get |
|--------|-------------|--------------|
| `TYPO3_EXTENSION_KEY` | Your registered extension key | [my.typo3.org](https://my.typo3.org) |
| `TYPO3_TER_ACCESS_TOKEN` | API token for TER uploads | [extensions.typo3.org/my-extensions](https://extensions.typo3.org/my-extensions) |

### Tag Format Requirements
- **Format:** `vMAJOR.MINOR.PATCH` (e.g., `v1.2.3`)
- **Note:** TER expects version without `v` prefix internally
- **Validation:** Workflow should validate tag format before publishing

---

## MANDATORY: TER Metadata Setup (Sidebar Links)

**CRITICAL:** The TER extension page sidebar links (Extension Manual, Found an Issue?, Code Insights, Packagist.org) are **NOT** populated from `composer.json`. They must be set explicitly via `tailor ter:update`.

Without this step, the TER page looks incomplete — no links to documentation, issues, source code, or Packagist.

### The Problem

New extensions uploaded to TER show an empty sidebar with no links:
- No "Extension Manual" button
- No "Found an Issue?" button
- No "Code Insights" button
- No "Packagist.org" button

This makes the extension appear unprofessional and hard to use.

### The Solution

Run `tailor ter:update` after the first TER upload:

```bash
TYPO3_API_TOKEN=your-token tailor ter:update \
  --composer="vendor/package-name" \
  --manual="https://github.com/vendor/repo" \
  --issues="https://github.com/vendor/repo/issues" \
  --repository="https://github.com/vendor/repo" \
  --tags="tag1,tag2,tag3" \
  extension_key
```

### Available Metadata Fields

| Option | TER Sidebar Button | Required |
|--------|--------------------|----------|
| `--manual` | Extension Manual | **YES** |
| `--issues` | Found an Issue? | **YES** |
| `--repository` | Code Insights | **YES** |
| `--composer` | Packagist.org (auto-linked) | **YES** |
| `--tags` | Search tags | Recommended |
| `--paypal` | Sponsoring link | Optional |

### When to Run

- **First release:** MANDATORY after the first `ter:publish`
- **URL changes:** Only when repository, docs, or issue tracker URLs change
- **Links persist:** Once set, they carry across all future version uploads

### Automation via CI

Add to your TER publish workflow as a post-publish step:

```yaml
- name: Update TER metadata
  if: env.FIRST_RELEASE == 'true'  # or always, idempotent
  run: |
    TAILOR="$(composer global config bin-dir --absolute)/tailor"
    "${TAILOR}" ter:update \
      --composer="${COMPOSER_NAME}" \
      --manual="${REPO_URL}" \
      --issues="${REPO_URL}/issues" \
      --repository="${REPO_URL}" \
      "${TYPO3_EXTENSION_KEY}"
```

### Verification

After setting metadata, verify on the TER page:

```bash
# Check that all 4 sidebar links are present
curl -s "https://extensions.typo3.org/extension/${EXT_KEY}" | \
  grep -c 'Extension Manual\|Found an Issue\|Code Insights\|Packagist\.org'
# Expected: 4
```

---

## Packagist Listing

Extensions with a `composer.json` should be listed on [Packagist](https://packagist.org):

1. **Submit package** at https://packagist.org/packages/submit
2. **Enable auto-update** via GitHub webhook (Packagist Settings > Enable GitHub Hook)
3. **Verify** the package appears with correct description and version

The `--composer` flag in `ter:update` creates the Packagist link on the TER page.

---

## Documentation Rendering on docs.typo3.org

Extensions with a `Documentation/` directory and `guides.xml` can have their documentation rendered at docs.typo3.org:

1. **Create** `Documentation/guides.xml` with project metadata
2. **Add RST files** following TYPO3 documentation standards
3. **Webhook** is automatically triggered when the extension is on Packagist
4. **Verify** at `https://docs.typo3.org/p/vendor/package-name/main/en-us/`

If not using docs.typo3.org, set `--manual` to the GitHub repository URL or a hosted documentation site.

---

## Release Comment Best Practices

### Writing Effective Release Notes

**Structure:**
```
Brief summary of the release (one line)

- Key change 1
- Key change 2
- Key change 3
```

**Do:**
- Start with a clear summary line
- Use bullet points for individual changes
- Group by type (Features, Fixes, Breaking)
- Keep each point concise
- Include TYPO3 version compatibility changes

**Don't:**
- Use Markdown formatting (not rendered)
- Use special characters like `#`, `*`, `<`, `>`
- Write excessively long descriptions
- Just say "Bug fixes" without details

### Example Release Notes

**Good:**
```
TYPO3 13 compatibility and performance improvements

Breaking changes:
- Minimum PHP version is now 8.2
- Removed deprecated API methods

New features:
- Added support for native lazy loading
- Improved caching for list views

Bug fixes:
- Fixed pagination in backend module
- Resolved translation loading issue
```

**Transformed for TER:**
```
TYPO3 13 compatibility and performance improvements

Breaking changes:
- Minimum PHP version is now 8.2
- Removed deprecated API methods

New features:
- Added support for native lazy loading
- Improved caching for list views

Bug fixes:
- Fixed pagination in backend module
- Resolved translation loading issue

Details: https://github.com/vendor/extension/releases/tag/v2.0.0
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "No upload comment" error | Empty comment passed to tailor | Ensure fallback comment in workflow |
| Special characters in XML feed | Unsupported chars in comment | Strip `#*+=~^|\\<>` from comments |
| Version mismatch | Tag doesn't match ext_emconf | Use `tailor set-version` before publish |
| Authentication failed | Invalid/expired API token | Regenerate token at extensions.typo3.org |

### Validation Script

Add to your workflow for pre-publish validation:
```bash
# Validate upload comment format
validate_comment() {
  local comment="$1"

  # Check not empty
  if [[ -z "${comment// }" ]]; then
    echo "::error::Upload comment cannot be empty"
    return 1
  fi

  # Check for unsupported characters
  if [[ "$comment" =~ [#*+=~^\|\\<>] ]]; then
    echo "::warning::Comment contains characters that will be stripped in XML export"
  fi

  return 0
}
```

---

## Technical Details

### TER API Endpoints
- **SOAP API:** Legacy, still supported (`ter_soap` extension)
- **REST API:** Modern interface (`ter_rest` extension)

### Comment Processing Pipeline
1. **Input:** Raw text from tailor CLI
2. **Validation:** Non-empty check (`ExtensionVersion.php`)
3. **Storage:** `TEXT` field in `tx_terfe2_domain_model_version`
4. **Frontend:** Fluid template with `<f:format.nl2br>`
5. **XML Export:** `xmlentities()` sanitization

### Source Code References (TER codebase)
- Validation: `extensions/ter/Classes/Api/ExtensionVersion.php:350`
- Storage: `extensions/ter_fe2/ext_tables.sql:84`
- TCA: `extensions/ter_fe2/Configuration/TCA/tx_terfe2_domain_model_version.php:80`
- Frontend: `extensions/ter_fe2/Resources/Private/Templates/Extension/Show.html:132`
- XML Export: `extensions/ter_fe2/Classes/Service/ExtensionIndexService.php:192`

---

## Conformance Checklist

### TER Publishing Excellence Indicators

```
GitHub Actions Workflow:
[ ] publish-to-ter.yml exists in .github/workflows/
[ ] Triggers on release published event
[ ] Validates tag format (vX.Y.Z)
[ ] Extracts version correctly (strips 'v' prefix)
[ ] Handles release body for comment
[ ] Has fallback comment if body empty
[ ] Uses typo3/tailor for publishing
[ ] Secrets properly configured

TER Metadata (MANDATORY for initial setup):
[ ] tailor ter:update --manual has been run (Extension Manual link)
[ ] tailor ter:update --issues has been run (Found an Issue link)
[ ] tailor ter:update --repository has been run (Code Insights link)
[ ] tailor ter:update --composer has been run (Packagist.org link)
[ ] All 4 sidebar links visible on extensions.typo3.org

Public Listings:
[ ] Extension page exists on extensions.typo3.org
[ ] Package exists on packagist.org
[ ] Documentation available (docs.typo3.org or linked from TER)
[ ] composer.json has support.issues URL
[ ] composer.json has support.source URL
[ ] composer.json has homepage URL

Release Process:
[ ] Semantic versioning followed
[ ] CHANGELOG.md updated before release
[ ] ext_emconf.php version bumped and committed BEFORE tagging
[ ] CI validates ext_emconf.php version matches tag (early fail)
[ ] composer.json version (if present) matches tag
[ ] Release notes follow TER format guidelines
[ ] Pre-push hook validates ext_emconf.php version locally
```

---

## Resources

- **Tailor CLI:** https://github.com/TYPO3/tailor
- **TER API Documentation:** https://extensions.typo3.org/help/api
- **Extension Registration:** https://my.typo3.org
- **TER Frontend:** https://extensions.typo3.org
