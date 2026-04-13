# CI/CD Patterns

Comprehensive CI/CD patterns for enterprise-ready projects.
Covers Git hooks, pipeline design, and quality gates.

## 1. Git Hooks Strategy

### Pre-commit vs Pre-push Division

**Principle:** Fast feedback locally, thorough verification before sharing.

| Hook | Purpose | Speed Target | What to Run |
|------|---------|--------------|-------------|
| **pre-commit** | Catch obvious issues | < 5 seconds | Format, lint, build, secrets |
| **pre-push** | Thorough verification | < 2 minutes | Full test suite, security scans |

### Lefthook Configuration Example

```yaml
# .lefthook.yml

pre-commit:
  parallel: true
  commands:
    fmt:
      glob: "*.{go,php,ts,js}"
      run: |
        # Language-specific formatters
        gofmt -w {staged_files} 2>/dev/null || true
        prettier --write {staged_files} 2>/dev/null || true

    lint:
      glob: "*.{go,php,ts}"
      run: |
        golangci-lint run --new-from-rev=HEAD~1 || true
        phpstan analyse --no-progress || true
        eslint {staged_files} || true

    build:
      run: |
        go build ./... || make build

    secrets:
      run: gitleaks protect --staged --no-banner

pre-push:
  parallel: true
  commands:
    test:
      run: |
        go test -race ./...
        # Or: phpunit, npm test, etc.

    lint-full:
      run: golangci-lint run --timeout 5m

    security:
      run: |
        govulncheck ./...
        # Or: composer audit, npm audit, etc.
```

### Hook Bypass Policy

- **Never** bypass hooks in normal workflow
- Use `--no-verify` only for:
  - Emergency hotfixes (document why)
  - WIP commits on feature branches (squash before PR)
- CI must run same checks as hooks (no bypass possible)

## 2. Comprehensive CI Pipeline

### Pipeline Structure

```
┌─────────────────────────────────────────────────────────────┐
│                        CI Pipeline                          │
├─────────────────────────────────────────────────────────────┤
│  Stage 1: Fast Feedback (parallel)                          │
│  ├── lint (golangci-lint, phpstan, eslint)                 │
│  ├── format-check (gofmt, prettier)                        │
│  ├── build                                                  │
│  └── secrets-scan (gitleaks, trufflehog)                   │
├─────────────────────────────────────────────────────────────┤
│  Stage 2: Testing (parallel by OS/version)                  │
│  ├── unit-tests (ubuntu, macos, windows)                   │
│  ├── integration-tests                                      │
│  ├── fuzz-tests (if applicable)                            │
│  └── benchmarks (optional, for tracking)                   │
├─────────────────────────────────────────────────────────────┤
│  Stage 3: Security (parallel)                               │
│  ├── sast (CodeQL, semgrep)                                │
│  ├── dependency-scan (govulncheck, npm audit)              │
│  ├── container-scan (trivy, if applicable)                 │
│  └── license-check                                          │
├─────────────────────────────────────────────────────────────┤
│  Stage 4: Coverage & Quality (depends on tests)             │
│  ├── coverage-report                                        │
│  └── quality-gate (fail if below threshold)                │
├─────────────────────────────────────────────────────────────┤
│  Stage 5: Artifacts (depends on all above)                  │
│  ├── build-artifacts                                        │
│  └── attestations (SLSA provenance)                        │
└─────────────────────────────────────────────────────────────┘
```

### Preventing Duplicate CI Runs

When a workflow triggers on both `push:` and `pull_request:`, pushing to a PR branch
causes every job to run **twice** -- once for the push event and once for the
pull_request event. This wastes CI minutes and clutters the checks list.

**Fix:** Restrict `push:` to protected branches only:

```yaml
on:
  push:
    branches: [main]      # Only run on pushes to main (merge commits)
  pull_request:            # Runs on PR open/sync — covers feature branches
```

**Anti-pattern** (causes duplicate runs):
```yaml
on:
  push:                    # BAD: triggers on ALL branch pushes including PR branches
  pull_request:
```

This applies to all workflow files, not just `ci.yml`. Audit every `.github/workflows/*.yml`
for unscoped `push:` triggers.

### GitHub Actions Example

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  # Stage 1: Fast Feedback
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: golangci/golangci-lint-action@971e284b6050e8a5849b72094c50ab08da042db8 # v6.1.1
        with:
          version: latest

  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@ff98106e4c7b2bc287b24eaf42907196329070c7 # v2.3.8
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # Stage 2: Testing (matrix)
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        go-version: ['1.25.x']
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-go@d35c59abb061a4a6fb18e82ac0862c26744d6ab5 # v5.5.0
        with:
          go-version: ${{ matrix.go-version }}
      - run: go test -race -coverprofile=coverage.txt ./...
      - uses: codecov/codecov-action@ad3126e916f78f00edff4ed0317cf185271ccc2d # v5.4.2
        if: matrix.os == 'ubuntu-latest'

  # Stage 3: Security
  codeql:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: github/codeql-action/init@v3
        with:
          languages: go
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3

  vulnerability-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-go@d35c59abb061a4a6fb18e82ac0862c26744d6ab5 # v5.5.0
      - run: go install golang.org/x/vuln/cmd/govulncheck@latest
      - run: govulncheck ./...

  # Stage 4: Quality Gate
  quality-gate:
    needs: [lint, test, codeql, vulnerability-scan]
    runs-on: ubuntu-latest
    steps:
      - run: echo "All checks passed"
```

## 3. Quality Gates

### Coverage Thresholds

| Level | Statement Coverage | Branch Coverage | Use Case |
|-------|-------------------|-----------------|----------|
| Minimum | 60% | - | Legacy projects |
| Standard | 80% | - | Most projects |
| High | 80% | 70% | Critical systems |
| Enterprise | 90% | 80% | Financial, medical |

### Multi-Suite Coverage (MANDATORY)

Coverage must be collected from ALL test suites, not just unit tests:

```yaml
# PHP: Collect coverage from each test suite
- name: Unit Tests
  run: php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/UnitTests.xml --coverage-clover .Build/coverage/unit.xml

- name: Integration Tests
  run: php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/IntegrationTests.xml --coverage-clover .Build/coverage/integration.xml

- name: E2E Tests
  run: php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/E2ETests.xml --coverage-clover .Build/coverage/e2e.xml

# Upload ALL coverage files
- uses: codecov/codecov-action@SHA # vX.Y.Z
  with:
    files: .Build/coverage/unit.xml,.Build/coverage/integration.xml,.Build/coverage/e2e.xml
```

### Polyglot Coverage (PHP + JavaScript)

Projects with both PHP and JavaScript MUST collect coverage from both:

```yaml
# PHP Tests
- name: PHP Tests with Coverage
  run: |
    php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/UnitTests.xml --coverage-clover .Build/coverage/unit.xml
    php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/IntegrationTests.xml --coverage-clover .Build/coverage/integration.xml

# JavaScript Tests (vitest/jest)
- uses: actions/setup-node@SHA # vX.Y.Z
  with:
    node-version: '22'

- run: npm install

- name: JavaScript Tests with Coverage
  run: npm run test:coverage  # Must output coverage/lcov.info

# Upload ALL coverage
- uses: codecov/codecov-action@SHA # vX.Y.Z
  with:
    files: .Build/coverage/unit.xml,.Build/coverage/integration.xml,coverage/lcov.info
```

**vitest.config.js MUST include lcov reporter:**
```javascript
coverage: {
    provider: 'v8',
    reporter: ['text', 'json', 'html', 'lcov'],  // lcov REQUIRED
    reportsDirectory: 'coverage',
}
```

### Enforcing Coverage

```yaml
# In CI workflow
- name: Check coverage threshold
  run: |
    COVERAGE=$(go tool cover -func=coverage.txt | grep total | awk '{print $3}' | tr -d '%')
    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
      echo "Coverage $COVERAGE% is below 80% threshold"
      exit 1
    fi

# For patch coverage (new code only)
- name: Check patch coverage
  run: |
    diff-cover coverage.xml --compare-branch=origin/main --fail-under=90
```

### Codecov Patch Coverage Configuration

Codecov's `patch` target checks coverage on **new/changed lines only**. Set a
realistic threshold -- lines that require specific PHP extensions (GD, Imagick) or
a full TYPO3 bootstrap may be uncoverable in some CI matrix entries but covered in
others.

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%
    patch:
      default:
        target: 60%          # Realistic for extension code with environment deps
        threshold: 5%        # Allow 5% drop before failing
```

**Key considerations:**
- Lines behind `extension_loaded('gd')` guards may show as uncovered in matrix
  entries without that extension
- TYPO3 integration tests may cover code that unit tests cannot reach
- Set `patch.target` based on what your CI matrix actually covers, not aspirational goals
- Use Codecov flags to separate unit vs integration coverage for clearer reporting

### PR Quality Requirements

```yaml
# Branch protection rules
branch_protection:
  required_status_checks:
    strict: true
    contexts:
      - lint
      - test (ubuntu-latest)
      - test (macos-latest)
      - test (windows-latest)
      - codeql
      - vulnerability-scan

  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true

  required_linear_history: true  # Enforce rebase

  required_signatures: true      # Signed commits
```

## 4. PHPStan Baseline Management

### Generating a Baseline

Capture all existing issues so new code is held to a higher standard:

```bash
# Generate baseline from current state
vendor/bin/phpstan analyse --generate-baseline

# When codebase is already clean, allow empty baseline
vendor/bin/phpstan analyse --generate-baseline --allow-empty-baseline
```

This creates `phpstan-baseline.neon` (or the configured path) containing all
currently-known errors, which PHPStan then ignores on subsequent runs.

### Baseline CI Strategy

The baseline should **shrink over time, never grow**. Track this in CI:

```yaml
- name: PHPStan analysis
  run: vendor/bin/phpstan analyse --no-progress

- name: Check baseline size
  run: |
    if [ -f phpstan-baseline.neon ]; then
      IGNORED=$(grep -c 'message:' phpstan-baseline.neon || echo 0)
      echo "PHPStan baseline: $IGNORED ignored errors"
      # Optional: fail if baseline grew
      # Compare against a known count stored in a tracking file
    fi
```

### Baseline Best Practices

| Practice | Description |
|----------|-------------|
| **Goal: empty baseline** | `ignoreErrors: []` means all issues resolved |
| **Never add new entries** | Fix new issues immediately; only existing code gets a pass |
| **Review baseline in PRs** | Any PR that increases baseline size needs justification |
| **Track count over time** | Log baseline error count as a CI metric |
| **Use `--allow-empty-baseline`** | Required when generating baseline on a clean codebase |

### PHPStan Configuration Example

```neon
# phpstan.neon
includes:
    - phpstan-baseline.neon

parameters:
    level: max
    paths:
        - Classes
    tmpDir: .Build/phpstan
```

## 5. Multi-Platform Testing

### OS Matrix Strategy

```yaml
strategy:
  fail-fast: false  # Don't cancel other jobs on failure
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    include:
      # OS-specific configurations
      - os: ubuntu-latest
        artifact-suffix: linux-amd64
      - os: macos-latest
        artifact-suffix: darwin-amd64
      - os: windows-latest
        artifact-suffix: windows-amd64.exe
```

### Version Matrix Strategy

```yaml
strategy:
  matrix:
    # Test oldest supported and latest
    version: ['1.21', '1.25']  # Or PHP: ['8.1', '8.4']
    include:
      - version: '1.25'
        latest: true  # Upload coverage only from latest
```

## 6. Flaky Test Prevention

### CI-Specific Test Configuration

```yaml
# Increase timeouts in CI
- name: Run tests
  run: go test -race -timeout 10m ./...
  env:
    CI: true
    TEST_TIMEOUT_MULTIPLIER: 3
```

### Retry Strategy for Known Flaky Tests

```yaml
- name: Run tests with retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: go test -race ./...
```

### Detecting Flaky Tests

```yaml
# Run tests multiple times to detect flakiness
- name: Flaky test detection
  if: github.event_name == 'schedule'  # Nightly only
  run: |
    for i in {1..10}; do
      go test -race ./... || exit 1
    done
```

## 7. Caching Strategy

### Go Caching

```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.25'
    cache: true  # Caches go mod and build cache
```

### PHP Caching

```yaml
- name: Cache Composer
  uses: actions/cache@v4
  with:
    path: vendor
    key: ${{ runner.os }}-composer-${{ hashFiles('composer.lock') }}
```

### Node Caching

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '22'
    cache: 'npm'
```

## 8. Signed Commits Enforcement

### Problem: GitHub Can't Sign Rebase Merges

When repository requires signed commits AND only allows rebase merge:

```yaml
# This fails because GitHub can't sign rebased commits
gh pr merge 123 --rebase
# Error: Base branch requires signed commits
```

### Solution: Local Merge Workflow

```bash
# 1. Fetch and checkout main
git checkout main
git pull origin main

# 2. Fast-forward merge (preserves signatures)
git merge feature-branch --ff-only

# 3. Push to main
git push origin main
```

### Automating with PR Labels

```yaml
# Workflow triggered by 'ready-to-merge' label
on:
  pull_request:
    types: [labeled]

jobs:
  merge:
    if: github.event.label.name == 'ready-to-merge'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.MERGE_TOKEN }}  # PAT with push access

      - name: Merge PR
        run: |
          git checkout main
          git merge origin/${{ github.head_ref }} --ff-only
          git push origin main
```

## 9. Reusable Workflow Pinning

### Supply Chain Security for Reusable Workflows

All `uses:` references to **third-party** reusable workflows must be pinned to
commit SHAs, just like regular actions:

```yaml
# BAD: branch reference is mutable (supply chain risk)
jobs:
  ci:
    uses: org/shared-workflows/.github/workflows/ci.yml@main

# BAD: tag reference is also mutable
jobs:
  ci:
    uses: org/shared-workflows/.github/workflows/ci.yml@v2

# GOOD: SHA-pinned (immutable reference)
jobs:
  ci:
    uses: org/shared-workflows/.github/workflows/ci.yml@a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2 # v2.1.0
```

### Exception: Org-Internal Workflows

Org-internal reusable workflows (maintained by the same organization) **should use
`@main` or `@tag`**, not SHAs. SHA-pinning org-internal workflows is an
**anti-pattern** because it breaks centralized security update propagation.

See `checkpoints.yaml` ER-33 for the enforcement rule.

### Auditing Workflow References

```bash
# Find all reusable workflow references
grep -rn 'uses:.*\.github/workflows/.*\.yml@' .github/workflows/

# Find unpinned references (tag or branch, no SHA)
grep -rn 'uses:.*\.github/workflows/.*\.yml@' .github/workflows/ | grep -v '@[a-f0-9]\{40\}'
```

## Related References

- `references/ci-docker-worktree.md` - Docker/worktree CI robustness (CaptainHook, lint scope, merge queues)
- `references/security-hardening.md` - Security scanning details
- `references/code-review.md` - Code quality checklist
- `references/signed-releases.md` - Release signing
- `assets/workflows/` - Ready-to-use workflow templates
