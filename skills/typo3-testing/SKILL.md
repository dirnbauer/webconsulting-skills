---
name: "typo3-testing"
description: "Use when setting up TYPO3 extension test infrastructure, writing unit/functional/E2E tests, configuring PHPUnit, mutation testing, mocking, CI/CD test pipelines, or debugging CI failures. For existing test suites, run the automated-assessment skill first to identify gaps. Also triggers on: ensure proper testing, test matrix, integration testing, e2e testing, coverage, test generation."
---

# TYPO3 Testing Skill

## Assessment-First Rule

**When enhancing an existing test suite** (not setting up from scratch), run the automated-assessment skill FIRST:

```bash
automated-assessment typo3-testing
```

> Install additional skills (e.g. `typo3-conformance`, `enterprise-readiness`) for broader assessment coverage.

This generates a gap report from 73+ checkpoints covering PHPUnit config, PHPStan level, runTests.sh, CaptainHook hooks, architecture tests, mutation thresholds, CI matrix, and coverage per class.

**Use the assessment report as the task list.** Resolve mechanical checkpoint failures before manual test writing.

### When This Rule Applies
- "enhance/improve/strengthen tests", "increase coverage/mutation score"
- "enterprise grade", "A+ testing", "fix all findings"

### When This Rule Does NOT Apply
- Setting up from scratch, writing a specific test, debugging a failing test

---

References for TYPO3 extension testing.

## Test Type Selection

| Type | Use When | Speed |
|------|----------|-------|
| **Unit** | Pure logic, no DB, validators, utilities | Fast |
| **Functional** | DB interactions, repositories, controllers | Medium |
| **Architecture** | Layer constraints, dependency rules (phpat) | Fast |
| **E2E (Playwright)** | User workflows, browser, accessibility | Slow |
| **Integration** | HTTP client, API mocking, OAuth flows | Medium |
| **Mutation** | Test quality verification, 70%+ coverage | CI/Release |

## runTests.sh - Mandatory

`Build/Scripts/runTests.sh` is mandatory. Must be executable, support `-s` (suite) and `-p` (PHP version).

## Git Hooks

Verify: `ls captainhook.json .git/hooks/pre-commit 2>/dev/null` (see `references/captainhook-setup.md`)

## Commands

```bash
# Setup (from skill dir)
scripts/setup-testing.sh [--with-e2e]
scripts/validate-setup.sh
scripts/generate-test.sh <Type> <Class>

# Run (always via runTests.sh)
Build/Scripts/runTests.sh -s unit|functional|phpstan|cgl|mutation|ci
```

Verify tests fail before fix, pass after. Bug fixes use the strict TDD loop in `references/tdd-discipline.md` — no "tested/verified" claims without pasted output.

## Scoring Requirements

Unit tests required (70%+ coverage). Functional tests required for DB operations. **phpat required** for architecture points. PHPStan level 10.

## References (in `references/`)

`unit-testing.md` | `functional-testing.md` | `functional-test-patterns.md` | `integration-testing.md` | `e2e-testing.md` | `accessibility-testing.md` | `ddev-testing.md` | `test-runners.md` | `architecture-testing.md` | `ci-debugging.md` | `ci-cd.md` | `quality-tools.md` | `mutation-testing.md` | `fuzz-testing.md` | `performance-testing.md` | `typo3-v14-final-classes.md` | `mock-validity.md` | `javascript-testing.md` | `captainhook-setup.md` | `enforcement-rules.md` | `event-dispatch-testing.md` | `crypto-testing.md` | `test-environment-guards.md` | `sonarcloud.md` | `typo3-ci-config-patterns.md` | `tdd-discipline.md`

### Content Triggers

- CI test failures across TYPO3 versions: load `ci-debugging.md`
- Functional tests with TSFE context: load `functional-testing.md`
- Mock failures across dependency versions: load `mock-validity.md`
- Image processing or extension-dependent tests: load `test-environment-guards.md`
- Event dispatcher testing with try/catch: load `event-dispatch-testing.md`

## Links

[TYPO3 Testing Docs](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Testing/) |
[Tea Extension](https://github.com/TYPO3BestPractices/tea) |
[phpat](https://github.com/carlosas/phpat) |
[Infection](https://infection.github.io/)

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-testing-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)

Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their generous open-source contributions to the TYPO3 community, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
