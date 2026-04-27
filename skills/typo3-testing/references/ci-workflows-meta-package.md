# netresearch/typo3-ci-workflows Meta-Package

## What It Is

`netresearch/typo3-ci-workflows` is a Composer meta-package that bundles the full
set of dev-time tools used across all Netresearch TYPO3 extensions into one
`require-dev` entry. Instead of maintaining 10+ individual version constraints in
each extension's `composer.json`, one line brings everything in:

```bash
composer require --dev netresearch/typo3-ci-workflows
```

## What It Bundles (representative list)

| Package | Purpose |
|---|---|
| `phpunit/phpunit` (transitive via `typo3/testing-framework`) | PHPUnit test runner |
| `phpstan/phpstan` | Static analysis |
| `phpstan/phpstan-phpunit` | PHPUnit-specific rules |
| `phpstan/phpstan-strict-rules` | Strict rule set |
| `phpstan/phpstan-deprecation-rules` | Deprecation detection |
| `phpstan/extension-installer` | Auto-registers PHPStan extensions |
| `phpat/phpat` | Architecture testing |
| `saschaegerer/phpstan-typo3` | TYPO3-specific PHPStan extension |
| `infection/infection` | Mutation testing |
| `captainhook/captainhook` | Git hook automation |
| `friendsofphp/php-cs-fixer` | Code style |
| `rector/rector` | Automated refactoring |

Because `phpunit/phpunit` is transitive, **do not add a direct `phpunit/phpunit`
entry to `require-dev`** — it pins a phpunit version that may conflict with the
PHP version constraint of the extension (phpunit 12.5.8+ requires PHP >= 8.3, which
breaks the PHP-8.2 matrix cell).

## Adoption

Replace individual dev dependencies:

```json
// Before
"require-dev": {
    "phpunit/phpunit": "^11 || ^12",
    "phpstan/phpstan": "^2",
    "phpat/phpat": "^0.11",
    "infection/infection": "^0.29",
    "friendsofphp/php-cs-fixer": "^3"
}

// After
"require-dev": {
    "netresearch/typo3-ci-workflows": "^1"
}
```

## composer install --no-plugins Workaround

`captainhook/hook-installer` (bundled transitively) registers git hooks on every
`composer install`. In git worktree environments the `.git` directory is a file
(pointer), not a directory, which confuses the installer and emits warnings or
errors.

**Workaround for local development in a worktree:**

```bash
composer install --no-plugins
```

This skips all Composer plugins, including the hook installer. Git hooks are
managed by the bare repository's worktree setup instead.

Create a shell alias or Makefile target:

```makefile
composer-install-local:
	composer install --no-plugins
```

## Build/phpstan.no-plugins.neon Pattern

When running PHPStan locally **without** `phpstan/extension-installer` (e.g. after
`composer install --no-plugins`), the auto-registered extensions are absent and
PHPStan will error on unknown rules.

Create `Build/phpstan.no-plugins.neon` for this case:

```neon
# Build/phpstan.no-plugins.neon
# Use this file locally when extension-installer is inactive
# (e.g. after: composer install --no-plugins)
#
# Usage: phpstan analyse --configuration Build/phpstan.no-plugins.neon

includes:
    - phpstan.neon
    - vendor/phpstan/phpstan-phpunit/extension.neon
    - vendor/phpstan/phpstan-phpunit/rules.neon
    - vendor/phpstan/phpstan-strict-rules/rules.neon
    - vendor/phpstan/phpstan-deprecation-rules/rules.neon
    - vendor/saschaegerer/phpstan-typo3/extension.neon

parameters:
    # Override anything set by extension-installer in the main neon
```

**Do not add these `includes:` to the main `phpstan.neon`.** When extension-installer
is active (in CI and standard `composer install`), it already registers them, and
duplicate includes cause PHPStan to exit 1 with "These files are included multiple
times".

## Reusable CI Workflow Integration

Pair the meta-package with the reusable GitHub Actions workflow:

```yaml
# .github/workflows/ci.yml
jobs:
  ci:
    uses: netresearch/typo3-ci-workflows/.github/workflows/extension-ci.yml@<SHA>
    with:
      php-versions: '["8.2", "8.3", "8.4"]'
      typo3-versions: '["13", "14"]'
      upload-coverage: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

Pin to a full 40-character SHA. Checkpoints TT-22, TT-23, TT-24, and TT-41 are
all satisfied by this single workflow call.
