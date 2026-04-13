# Mandatory Badges & Workflows

## Mandatory Badges

| Badge | URL Pattern |
|-------|-------------|
| CI Status | `github.com/ORG/REPO/actions/workflows/ci.yml/badge.svg` |
| Codecov | `codecov.io/gh/ORG/REPO/graph/badge.svg` |
| OpenSSF Scorecard | `api.securityscorecards.dev/projects/github.com/ORG/REPO/badge` |
| OpenSSF Best Practices | `www.bestpractices.dev/projects/PROJECT_ID/badge` |
| OpenSSF Baseline | `www.bestpractices.dev/projects/PROJECT_ID/baseline` |

## Mandatory Workflows

| Workflow | File | Purpose |
|----------|------|---------|
| CI | `ci.yml` | Build, test, lint |
| CodeQL | `codeql.yml` | Security scanning |
| Scorecard | `scorecard.yml` | OpenSSF Scorecard |
| Dependency Review | `dependency-review.yml` | PR CVE check |

## Scorecard Quick Wins

| Check | Quick Fix | Impact |
|-------|-----------|--------|
| Token-Permissions | `permissions: {}` at workflow-level, `write` only per-job | 0->10 |
| Branch-Protection | `required_approving_review_count: 1` + auto-approve | 0->8 |
| Security-Policy | SECURITY.md + private vulnerability reporting | 4->10 |
| Pinned-Dependencies | SHA-pin all actions (SLSA generator pinnable but internal actions use tag refs) | 8->10 |
