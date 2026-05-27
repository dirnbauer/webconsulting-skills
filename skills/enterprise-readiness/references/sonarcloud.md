# SonarCloud Integration

> Enterprise-grade continuous code quality and security analysis platform

## Overview

SonarCloud is the cloud-hosted version of SonarQube, providing:
- **Static code analysis** with 5,000+ rules across 30+ languages
- **Security vulnerability detection** (OWASP Top 10, CWE, SANS Top 25)
- **Code smell and maintainability tracking**
- **Test coverage visualization**
- **Quality gates** for automated enforcement
- **PR decoration** for immediate feedback

## Pricing

| Tier | Cost | Scope |
|------|------|-------|
| **Free** | $0 | Unlimited public repos, full features |
| **Team** | From $14/mo | Private repos, based on LOC |
| **Enterprise** | Custom | Advanced features, SSO, support |

**Key**: Free tier provides **full enterprise features** for open-source projects.

## Enterprise Value

### Security Analysis

SonarCloud detects:
- SQL injection, XSS, command injection
- Insecure cryptography and hashing
- Authentication/authorization flaws
- Sensitive data exposure
- Security misconfigurations
- Known vulnerable dependencies

### Compliance Support

Aligns with:
- **OWASP Top 10** - Web application security
- **CWE/SANS Top 25** - Most dangerous software weaknesses
- **PCI DSS** - Payment card security
- **HIPAA** - Healthcare data protection

### Quality Metrics

| Metric | Description | Enterprise Relevance |
|--------|-------------|---------------------|
| Reliability | Bug count and severity | System stability |
| Security | Vulnerabilities and hotspots | Risk management |
| Maintainability | Code smells and tech debt | Long-term costs |
| Coverage | Test coverage percentage | Quality assurance |
| Duplications | Code duplication percentage | Maintainability |

## Setup

### 1. Connect Repository

1. Go to [sonarcloud.io](https://sonarcloud.io)
2. Sign in with GitHub/GitLab/Bitbucket
3. Create organization (matches your GitHub org)
4. Import repository

### 2. Generate Token

1. Account → Security → Generate Token
2. Save as `SONAR_TOKEN` repository secret

### 3. Add Configuration

Create `sonar-project.properties` in repository root:

```properties
sonar.projectKey=org_repo-name
sonar.organization=your-org

# Source configuration
sonar.sources=src,Classes
sonar.tests=tests,Tests
sonar.exclusions=**/vendor/**,**/node_modules/**,**/*.min.js

# Language-specific
sonar.php.coverage.reportPaths=coverage.xml
sonar.php.phpstan.reportPaths=phpstan-report.json
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.go.coverage.reportPaths=coverage.out

# Quality settings
sonar.qualitygate.wait=true
```

### 4. GitHub Actions Workflow

```yaml
name: SonarCloud

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  sonarcloud:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for accurate blame

      - name: Run tests with coverage
        run: |
          # PHP example
          vendor/bin/phpunit --coverage-clover coverage.xml
          # Or Go example
          # go test -coverprofile=coverage.out ./...

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## Quality Gates

### Default "Sonar Way" Gate

| Condition | Threshold | Applies To |
|-----------|-----------|------------|
| New bugs | 0 | New code |
| New vulnerabilities | 0 | New code |
| New security hotspots reviewed | 100% | New code |
| New code coverage | ≥80% | New code |
| New duplicated lines | ≤3% | New code |
| Maintainability rating | A | New code |
| Reliability rating | A | New code |
| Security rating | A | New code |

### Enterprise Custom Gate

For stricter enterprise requirements:

```
Conditions on New Code:
- Coverage ≥ 90%
- Duplicated Lines ≤ 1%
- Maintainability Rating = A
- Reliability Rating = A
- Security Rating = A
- Security Hotspots Reviewed = 100%
- New Bugs = 0
- New Vulnerabilities = 0
- New Code Smells ≤ 5

Conditions on Overall Code:
- Coverage ≥ 80%
- Duplicated Lines ≤ 3%
- Technical Debt Ratio ≤ 5%
```

## PR Decoration

SonarCloud automatically comments on PRs:

```
┌────────────────────────────────────────────────────┐
│ Quality Gate passed                                │
├────────────────────────────────────────────────────┤
│ Coverage: 87.3% (+2.1%)                           │
│                                                    │
│ 0 Bugs (0 new)                                    │
│ 0 Vulnerabilities (0 new)                         │
│ 2 Security Hotspots (1 to review)                 │
│ 5 Code Smells (2 new)                             │
│ 0.5% Duplication (0.0% new)                       │
└────────────────────────────────────────────────────┘
```

## Security Hotspots

Security-sensitive code requiring manual review:

| Category | Examples |
|----------|----------|
| **Authentication** | Password handling, session management |
| **Cryptography** | Encryption, hashing, random number generation |
| **Injection** | SQL, command, LDAP injection risks |
| **File handling** | Path traversal, file uploads |
| **Networking** | HTTP requests, SSL/TLS configuration |

### Hotspot Review Workflow

1. SonarCloud flags security-sensitive code
2. Developer reviews in SonarCloud UI
3. Mark as **Safe**, **Fixed**, or **To Review**
4. Document rationale for **Safe** decisions

## Operational Patterns

Day-to-day workflows for triaging issues, wiring CI, and keeping the project list clean. Token lives in env (`$SONAR_TOKEN`), passed as `Authorization: Bearer $SONAR_TOKEN` (Basic-auth `-u "$SONAR_TOKEN:"` also works, but Bearer keeps secrets out of the URL credential slot and avoids tripping secret-scanners on `-u` patterns).

### Quality Gate vs Annotations vs Required Check

These three concepts are independent — confusing them leads to wrong merge decisions:

- **Quality Gate** (e.g. *0% Coverage on New Code*) — contributes to the `SonarCloud Code Analysis` check status (pass/fail)
- **Annotations** — individual issues flagged on PR-touched lines, shown inline; do **not** affect the QG by themselves
- **Required check** — repository ruleset entry (`gh api repos/OWNER/REPO/rulesets/$ID`); only required checks block merge

A PR can sit at `mergeStateStatus: UNSTABLE` (advisory checks failing, still mergeable) versus `BLOCKED` (a required check failing, not mergeable). Verify which checks actually gate merges:

```bash
# Which checks are required to merge?
gh api repos/OWNER/REPO/rulesets --jq '.[] | select(.name == "default") | .id' \
  | xargs -I{} gh api repos/OWNER/REPO/rulesets/{} \
      --jq '.rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context'
# Is "SonarCloud Code Analysis" in the output? Usually NOT — it is advisory.
```

Refactor-PR gotcha: *0% Coverage on New Code* is **structurally unfixable** when the refactored file cannot be loaded by the test runner (e.g. a JS module with CKEditor top-level imports under vitest). Treat the QG fail as advisory rather than chasing coverage on untestable code.

### Bulk Issue Transitions via API

Single transition (issues):

```bash
curl -s -H "Authorization: Bearer $SONAR_TOKEN" -X POST \
  "https://sonarcloud.io/api/issues/do_transition" \
  --data-urlencode "issue=$KEY" \
  --data-urlencode "transition=wontfix"   # or: falsepositive
```

Add a comment (separate call — `do_transition` does not accept `comment`):

```bash
curl -s -H "Authorization: Bearer $SONAR_TOKEN" -X POST \
  "https://sonarcloud.io/api/issues/add_comment" \
  --data-urlencode "issue=$KEY" \
  --data-urlencode "text=Reason: ..."
```

Available issue transitions: `falsepositive`, `wontfix`, `confirm`, `unconfirm`, `resolve`, `reopen`. Hotspots use a different endpoint:

```bash
curl -s -H "Authorization: Bearer $SONAR_TOKEN" -X POST \
  "https://sonarcloud.io/api/hotspots/change_status" \
  --data-urlencode "hotspot=$KEY" \
  --data-urlencode "status=REVIEWED" \
  --data-urlencode "resolution=SAFE"      # or: FIXED, ACKNOWLEDGED
```

Bulk fetch issue keys for a rule:

```bash
curl -s "https://sonarcloud.io/api/issues/search?componentKeys=$PROJECT&rules=$RULE&issueStatuses=OPEN,CONFIRMED&ps=500" \
  | jq -r '.issues[].key'
```

Sequential loops (one transition + one comment per issue) handle ~120 calls without rate-limit pushback — no client-side throttling needed for typical batch sizes.

### Hotspot Triage — Common False-Positive Classes

Patterns that appear repeatedly and can be marked Safe / False Positive without code changes:

| Rule | Pattern | Decision |
|------|---------|----------|
| `php:S4790` "weak hash" | `substr(md5($url), 0, N)` for cache keys / temp filenames | **Safe** — not crypto, just an identifier |
| `php:S1313` "hardcoded IP" | `'169.254.169.254'` (AWS IMDS) in an SSRF deny-list | **False Positive** — the literal IS the security control |
| `javascript:S3516` "always returns same value" | Returning the same `Promise` object across error and success paths | **False Positive** — Sonar does not model Promise resolution as state change |

Triage flow: read the use-site once, decide, apply via API with an explanatory comment so future reviewers see the rationale.

### Domain-Specific False-Positive Classes

**CKEditor 5 view elements (`javascript:S7761`)** — `getAttribute('data-*')` inside CKE5 upcast/downcast converter callbacks operates on **view elements**, not DOM elements. View elements expose `getAttribute(key)` mirroring the DOM API by name only — they read from an internal attribute map and have **no `.dataset` property**. Refactoring to `.dataset.foo` silently returns `undefined` and drops every `data-*` attribute on upcast. Identify via sibling calls in the same callback: `consumable.consume(viewElement, ...)`, `child.is('element', 'img')`, `figureElement.getChildren()`. Mark all such instances won't-fix in bulk.

**TYPO3 framework signatures (`php:S1172` "unused parameter")** — required by TYPO3 contracts even when params are unused; mark won't-fix, do **not** drop:

- `#[AsAllowedCallable]` methods: `(?string $content, array $conf, ServerRequestInterface $request)` — TypoScript USER callback contract
- DataHandler hooks, e.g. `processDatamap_postProcessFieldArray(string $status, string $table, string $id, array &$fieldArray, DataHandler &$dataHandler)`
- Other documented hook signatures from TYPO3 core

Private methods with unused params are real cleanup — drop the params and update callers (in-file only since they are private).

### Project Hygiene — Archived Repositories

SonarCloud does not auto-prune projects when their GitHub repo is archived. Cross-reference and bulk-delete:

```bash
# All Sonar projects in the org
curl -s "https://sonarcloud.io/api/components/search_projects?organization=$ORG&ps=500" \
  | jq -r '.components[].name' | sort > /tmp/sonar.txt

# All archived GitHub repos (paginate as needed)
gh api "orgs/$ORG/repos?type=all&per_page=100&page=1" \
  --jq '.[] | select(.archived) | .name' \
  | sort > /tmp/archived.txt

# Delete each archived-but-still-in-Sonar project; expect HTTP 204 per delete
comm -12 /tmp/sonar.txt /tmp/archived.txt \
  | while read -r repo; do
      curl -s -H "Authorization: Bearer $SONAR_TOKEN" -X POST \
        "https://sonarcloud.io/api/projects/delete?project=${ORG}_${repo}" \
        -w "$repo: %{http_code}\n"
    done
```

Real-world result on the `netresearch` org (2026-05): 270 → 198 projects after pruning 72 archived entries.

### CI Wiring Gotchas

**Language-agnostic shared workflows cannot carry coverage.** A reusable workflow such as `org/.github/.github/workflows/sonarqube.yml` is intentionally generic — checkout + scan only, no test step. Repos that want coverage must inline the scan in their own workflow:

```yaml
sonarqube:
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    - name: Setup runtime + run tests with coverage
      run: |
        # PHP example
        vendor/bin/phpunit --coverage-clover .Build/logs/clover-unit.xml
        # JS example
        npm ci && npm run test:coverage
    - uses: SonarSource/sonarqube-scan-action@59db25f34e16620e48ab4bb9e4a5dce155cb5432  # v8.0.0 — pin to 40-char SHA, comment with version; or use sonarcloud-github-action
```

Wire the resulting reports in `sonar-project.properties`:

```properties
sonar.php.coverage.reportPaths=.Build/logs/clover-unit.xml
sonar.javascript.lcov.reportPaths=Tests/JavaScript/coverage/lcov.info
```

**Vitest cross-directory coverage requires `allowExternal`.** Production code at `../../Resources/...` from `Tests/JavaScript/` produces an empty `lcov.info` despite tests passing, because v8 silently drops files outside the workspace boundary regardless of include globs:

```js
// vitest.config.js
export default {
  test: {
    coverage: {
      provider: 'v8',
      allowExternal: true,            // required for cross-dir source under test
      include: ['../../Resources/Public/JavaScript/**'],
      reportsDirectory: './coverage',
      reporter: ['lcov', 'text'],
    },
  },
}
```

**Test fixtures duplicating production trigger CPD false positives.** When test files mirror inline production callbacks (e.g. CKE5 upcast/downcast lambdas that cannot be imported in isolation), Sonar's CPD flags the mirrors as duplication. Mitigate with a targeted exclusion:

```properties
sonar.cpd.exclusions=Tests/JavaScript/tests/**
```

This is a legitimate exclusion — the duplication is a testing-pattern necessity, not maintenance debt.

## Integration with Existing Tools

### PHPStan Integration

Export PHPStan results to SonarCloud:

```bash
vendor/bin/phpstan analyze --error-format=json > phpstan-report.json
```

```properties
# sonar-project.properties
sonar.php.phpstan.reportPaths=phpstan-report.json
```

### ESLint Integration

```bash
npx eslint --format json --output-file eslint-report.json .
```

```properties
sonar.eslint.reportPaths=eslint-report.json
```

### Coverage Integration

| Language | Coverage Tool | Property |
|----------|--------------|----------|
| PHP | PHPUnit | `sonar.php.coverage.reportPaths` |
| JavaScript | Istanbul/NYC | `sonar.javascript.lcov.reportPaths` |
| Go | go test | `sonar.go.coverage.reportPaths` |
| Python | Coverage.py | `sonar.python.coverage.reportPaths` |
| Java | JaCoCo | `sonar.coverage.jacoco.xmlReportPaths` |

## Badges

Add to README for visibility:

```markdown
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=org_repo&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=org_repo)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=org_repo&metric=coverage)](https://sonarcloud.io/summary/new_code?id=org_repo)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=org_repo&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=org_repo)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=org_repo&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=org_repo)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=org_repo&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=org_repo)
```

## OpenSSF Badge Alignment

SonarCloud helps satisfy OpenSSF Best Practices criteria:

| Criterion | SonarCloud Feature |
|-----------|-------------------|
| `static_analysis` | ✅ Core feature |
| `static_analysis_fixed` | ✅ Quality Gate enforcement |
| `dynamic_analysis` | ⚠️ Partial (security hotspots) |
| `test_statement_coverage80` | ✅ Coverage tracking |
| `test_branch_coverage80` | ✅ Branch coverage (Gold) |
| `warnings_fixed` | ✅ Code smell tracking |

## Enterprise Best Practices

### 1. Baseline for Legacy Code

For existing projects with technical debt:

```properties
# Focus quality gate on new code only
sonar.leak.period=previous_version
```

### 2. Branch Analysis

```properties
# Analyze feature branches
sonar.branch.name=${BRANCH_NAME}
sonar.branch.target=main
```

### 3. Monorepo Support

```properties
# Multiple projects in one repo
sonar.projectKey=org_monorepo_service-a
sonar.projectBaseDir=services/service-a
```

### 4. Pull Request Analysis

```yaml
# Only analyze PRs to main/develop
on:
  pull_request:
    branches: [main, develop]
```

### 5. Scheduled Full Analysis

```yaml
# Weekly full analysis
on:
  schedule:
    - cron: '0 2 * * 0'  # Sunday 2 AM
```

## Comparison with Alternatives

| Feature | SonarCloud | CodeClimate | Codacy | GitHub CodeQL |
|---------|------------|-------------|--------|---------------|
| Free for OSS | ✅ Full | ✅ Full | ⚠️ Limited | ✅ Full |
| Security rules | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| PHP support | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Coverage | ✅ | ✅ | ✅ | ❌ |
| Quality gates | ✅ | ✅ | ✅ | ❌ |
| PR decoration | ✅ | ✅ | ✅ | ✅ |
| Self-hosted | SonarQube | ❌ | ❌ | ✅ |

## Resources

- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [Security Rules](https://rules.sonarsource.com/)
- [Quality Gates](https://docs.sonarcloud.io/improving/quality-gates/)
- [GitHub Actions Integration](https://docs.sonarcloud.io/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud/)
- [SonarQube (Self-hosted)](https://www.sonarqube.org/)
