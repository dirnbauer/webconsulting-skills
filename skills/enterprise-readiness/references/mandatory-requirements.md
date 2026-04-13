# Mandatory Requirements

Every project MUST have ALL of these. Do not skip any.

## README Badges

Every project README.md MUST display these badges at the top:

```markdown
<!-- Row 1: CI/Quality -->
[![CI](https://github.com/ORG/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/ORG/REPO/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ORG/REPO/graph/badge.svg)](https://codecov.io/gh/ORG/REPO)

<!-- Row 2: Security -->
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/ORG/REPO/badge)](https://securityscorecards.dev/viewer/?uri=github.com/ORG/REPO)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/PROJECT_ID/badge)](https://www.bestpractices.dev/projects/PROJECT_ID)
```

| Badge | URL Pattern |
|-------|-------------|
| CI Status | `github.com/ORG/REPO/actions/workflows/ci.yml/badge.svg` |
| Codecov | `codecov.io/gh/ORG/REPO/graph/badge.svg` |
| OpenSSF Scorecard | `api.securityscorecards.dev/projects/github.com/ORG/REPO/badge` |
| OpenSSF Best Practices | `www.bestpractices.dev/projects/PROJECT_ID/badge` |

## CI/CD Workflows

Every GitHub project MUST have these in `.github/workflows/`:

| Workflow | File | Purpose |
|----------|------|---------|
| CI | `ci.yml` | Build, test, lint |
| CodeQL | `codeql.yml` | Security scanning |
| Scorecard | `scorecard.yml` | OpenSSF Scorecard |
| Dependency Review | `dependency-review.yml` | PR CVE check |

## CI Must Include

| Requirement | Implementation |
|-------------|----------------|
| Coverage upload | `codecov/codecov-action` after tests |
| Security audit | `composer audit` / `npm audit` / `govulncheck` |
| SHA-pinned actions | All actions use full SHA with version comment |

## Supply Chain Security (Releases)

Supply chain security controls MUST block releases when violated.

| Control | Implementation | Blocks Release? |
|---------|----------------|-----------------|
| SLSA Provenance | `slsa-github-generator` workflow | **YES** |
| Signed Tags | `git tag -s` before `gh release create` | **YES** |
| SBOM Generation | `anchore/sbom-action` or `cyclonedx` | **YES** |
| Dependency Audit | `composer audit` / `npm audit` fails CI | **YES** |

### Release Workflow Order

```
1. CI passes (tests, lint, security audit)
     ↓
2. Create SIGNED tag locally: git tag -s vX.Y.Z
     ↓
3. Push signed tag: git push origin vX.Y.Z
     ↓
4. Create release on existing tag: gh release create vX.Y.Z
     ↓
5. SLSA provenance workflow triggers (workflow_run)
     ↓
6. Provenance attestation uploaded to release
     ↓
7. SBOM generated and uploaded
```

**NEVER** use `gh release create` without a pre-existing signed tag.

### CI Integration for Supply Chain

Add to `.github/workflows/release.yml`:

```yaml
# Pre-release checks (block release if failed)
- name: Security Audit
  run: |
    composer audit --format=plain || exit 1
    npm audit --audit-level=high || exit 1

# SBOM generation
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    artifact-name: sbom.spdx.json
    output-file: sbom.spdx.json

- name: Upload SBOM to release
  run: gh release upload ${{ github.ref_name }} sbom.spdx.json
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Verification of Supply Chain Artifacts

Before announcing a release, verify:

- [ ] Release tag is GPG/SSH signed: `git tag -v vX.Y.Z`
- [ ] SLSA provenance exists: `multiple.intoto.jsonl` in release assets
- [ ] SBOM exists: `sbom.spdx.json` or `sbom.cyclonedx.json` in release assets
- [ ] No HIGH/CRITICAL CVEs: `composer audit` / `npm audit` clean

See `slsa-provenance.md` for detailed SLSA implementation guide.

## OpenSSF Registration

1. Register at https://www.bestpractices.dev/en/projects/new
2. Note the Project ID assigned after registration
3. Add badge to README with correct PROJECT_ID
4. Run Scorecard workflow to generate initial score

## Codecov Setup

1. Enable Codecov for the repository at codecov.io
2. Collect coverage from ALL test suites (not just unit tests):

| Test Suite | Coverage Command | Output File |
|------------|------------------|-------------|
| Unit | `phpunit -c UnitTests.xml --coverage-clover` | `.Build/coverage/unit.xml` |
| Integration | `phpunit -c IntegrationTests.xml --coverage-clover` | `.Build/coverage/integration.xml` |
| E2E | `phpunit -c E2ETests.xml --coverage-clover` | `.Build/coverage/e2e.xml` |
| Functional | `phpunit -c FunctionalTests.xml --coverage-clover` | `.Build/coverage/functional.xml` |
| JavaScript | `npm run test:coverage` | `coverage/lcov.info` |

3. Upload ALL coverage files to Codecov:

```yaml
- uses: codecov/codecov-action@SHA # vX.Y.Z
  with:
    token: ${{ secrets.CODECOV_TOKEN }}  # MANDATORY
    files: .Build/coverage/unit.xml,.Build/coverage/integration.xml,.Build/coverage/e2e.xml,coverage/lcov.info
    fail_ci_if_error: false
```

### CODECOV_TOKEN

**Never rely on tokenless uploads.** They fail for protected branches and are unreliable.

| Requirement | Implementation | Why |
|-------------|----------------|-----|
| Token in secrets | Add `CODECOV_TOKEN` to repo or org secrets | Authentication |
| Token in workflow | `token: ${{ secrets.CODECOV_TOKEN }}` | Required for protected branches |
| Org-level secret | Preferred for consistency across repos | Single point of management |

Get token from: https://app.codecov.io/gh/ORG/REPO/settings

```bash
# Organization-level (covers all repos)
gh secret set CODECOV_TOKEN --org netresearch --visibility all

# Or repository-level
gh secret set CODECOV_TOKEN --repo OWNER/REPO
```

### JavaScript Coverage (projects with JS/TS)

When a project contains JavaScript or TypeScript files:

1. **vitest.config.js** MUST include lcov reporter:

```javascript
coverage: {
    provider: 'v8',
    reporter: ['text', 'json', 'html', 'lcov'],  // lcov REQUIRED for Codecov
    reportsDirectory: 'coverage',
}
```

2. **CI workflow** MUST include JavaScript test job:

```yaml
- uses: actions/setup-node@SHA # vX.Y.Z
  with:
    node-version: '22'
- run: npm install
- run: npm run test:coverage
```

3. **Codecov upload** MUST include `coverage/lcov.info`

## Verification Checklist

Before marking enterprise-readiness complete, verify ALL:

- [ ] README has CI badge linking to workflow
- [ ] README has Codecov badge (not "unknown")
- [ ] README has OpenSSF Scorecard badge (correct URL with `api.securityscorecards.dev`)
- [ ] README has OpenSSF Best Practices badge (correct PROJECT_ID, not placeholder)
- [ ] `.github/workflows/ci.yml` exists and uploads coverage
- [ ] `.github/workflows/codeql.yml` exists
- [ ] `.github/workflows/scorecard.yml` exists
- [ ] Codecov shows actual coverage percentage
- [ ] Scorecard shows actual score

**If any badge shows "unknown", "invalid", or placeholder ID -- FIX IT. Do not proceed.**
