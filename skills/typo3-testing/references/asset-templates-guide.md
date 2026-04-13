# Asset Templates Guide

Templates and configuration files for setting up TYPO3 extension testing infrastructure.

## Infrastructure Setup

To set up Docker-based test orchestration, copy `assets/Build/Scripts/runTests.sh` to your extension. This is the **required** foundation for all test execution.

To initialize test bootstrapping, use these templates:
- `assets/bootstrap.php` - General test bootstrap with autoloader detection
- `assets/UnitTestsBootstrap.php` - Unit test bootstrap with optional TYPO3 stub autoloader
- `assets/FunctionalTestsBootstrap.php` - Functional test bootstrap for TYPO3 testing framework

## PHPUnit Configuration

To configure PHPUnit, copy and customize:
- `assets/UnitTests.xml` - Unit test suite configuration
- `assets/FunctionalTests.xml` - Functional test suite configuration

## Code Quality Tools

To set up static analysis and code style, use:
- `assets/phpstan.neon` - PHPStan level 10 configuration
- `assets/phpstan-baseline.neon` - Baseline template for legacy code migration
- `assets/phpat.php` - Architecture test rules for layer enforcement
- `assets/phpat.neon` - PHPat PHPStan extension configuration
- `assets/.php-cs-fixer.dist.php` - PHP-CS-Fixer code style rules
- `assets/rector.php` - Rector automated refactoring configuration

**CGL Enforcement:** TYPO3 CGL is strict about alignment (e.g., `binary_operator_spaces` in `setUp()` methods). Always run `composer ci:cgl` or the project's CS fixer before committing. Do not rely on manual formatting.

## Mutation Testing & Coverage

To configure mutation testing, copy `assets/infection.json5` and adjust mutator settings and MSI thresholds.

To configure coverage reporting, copy `assets/codecov.yml` for Codecov integration.

## CI/CD Workflows

To set up GitHub Actions, use:
- `assets/github-actions-tests.yml` - Main CI workflow (lint, phpstan, unit, functional tests)
- `assets/github-actions-e2e.yml` - E2E workflow with **GitHub Services + PHP built-in server** (NOT DDEV)

## E2E Testing Setup

To set up Playwright E2E testing, copy the `assets/Build/playwright/` directory containing:
- `package.json` - Node.js dependencies
- `playwright.config.ts` - Playwright configuration
- `tests/playwright/` - Test structure with login setup, fixtures, and example specs

## Development Shortcuts

To add common command shortcuts, copy `assets/Makefile` for make-based task execution.

## Docker Services

To configure additional Docker services for testing, use templates from `assets/docker/`:
- `docker-compose.yml` - Base Docker Compose configuration
- `codeception.yml` - Codeception-specific Docker setup

## Example Tests

To see test patterns in action, review examples in `assets/example-tests/`:
- `ExampleUnitTest.php` - Unit test structure and assertions
- `ExampleFunctionalTest.php` - Functional test with fixtures
- `ExampleAcceptanceCest.php` - Codeception acceptance test

## Database Fixtures

To set up test data, use CSV fixtures from `assets/fixtures/`:
- `be_users.csv` - Backend user fixture with password hashes
- `pages.csv` - Page tree structure
- `tt_content.csv` - Content elements
- `sys_category.csv` - Category hierarchy

Consult `assets/fixtures/README.md` for fixture format documentation.

## AI Agent Documentation

To document AI agent behavior for your extension, use `assets/AGENTS.md` as a template.
