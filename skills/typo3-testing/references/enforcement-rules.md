# Enforcement Rules

This skill enforces the following patterns. Violations should be flagged and corrected.

## PHPUnit Quality Checks (MANDATORY)

| Rule | Enforcement |
|------|-------------|
| **Use `createStub()` for test doubles without expectations** | Flag any `createMock()` call that has no corresponding `expects()` |
| **Use `createMock()` only when verifying calls** | Mock objects MUST have at least one `expects()` call |
| **Use `self::` for static assertions** | Flag `$this->assertSame()`, use `self::assertSame()` instead |
| **Use `#[Test]` attribute** | Flag `@test` annotation and `test` method prefix in new tests |
| **Use `#[CoversClass()]` or `#[CoversNothing]` attribute** | All test classes MUST declare either which class they cover or `#[CoversNothing]` for tests that intentionally do not cover application code (e.g. PHP/libxml behavior) |
| **camelCase test method names** | Flag inconsistent capitalization at word boundaries |

**Detection:**

```bash
# Find mocks without expectations (per-variable detection)
grep -rn '\$[A-Za-z_][A-Za-z0-9_]*\s*=\s*\$this->createMock(' Tests/ | while IFS=: read -r file line rest; do
  # Extract variable name on the left-hand side of the assignment
  var=$(echo "$rest" | sed -n 's/^\s*\(\$[A-Za-z_][A-Za-z0-9_]*\)\s*=.*/\1/p')
  if [ -n "$var" ]; then
    # Check whether this specific mock variable is ever used with expects()
    if ! grep -q "$var->expects(" "$file"; then
      echo "NOTICE: $file:$line: mock $var created with createMock() but has no expects() calls"
    fi
  fi
done

# Alternatively, rely on PHPUnit's runtime notice for mocks without expectations:
# vendor/bin/phpunit --display-notices | grep 'does not set up any expectations'

# Find $this-> assertions that should use self::
grep -rn '\$this->assert' Tests/

# Find legacy @test annotations
grep -rn '@test' Tests/ | grep -v 'vendor'
```

## DDEV and Test Execution (MANDATORY)

| Rule | Enforcement |
|------|-------------|
| **NEVER use DDEV for running tests** | Not in CI, not in runTests.sh, not in documentation examples |
| **NEVER use DDEV in CI/CD** | Flag any `.github/workflows/*.yml` or `.gitlab-ci.yml` using `ddev` commands |
| **Use PHP built-in server for E2E** | E2E workflows MUST use `php -S` for HTTP, not DDEV |
| **Use Docker containers for functional tests** | Functional tests requiring DB MUST use service containers (MariaDB/MySQL) |
| **Dual-mode Playwright config** | `playwright.config.ts` MUST use `TYPO3_BASE_URL` env var |

**Why:** DDEV is for local development environments only. Using DDEV for running tests is slow (2-3+ min startup), complex (Docker-in-Docker in CI), resource-heavy, and fragile. The TYPO3 community standard is direct PHP or testing containers. Use PHP built-in server for E2E tests, Docker containers for functional tests.

**Correct pattern:**
```yaml
# GitHub Actions E2E
services:
  db:
    image: mariadb:11.4
    # ...

steps:
  - name: Start PHP server
    run: php -S 0.0.0.0:8080 -t .Build/Web &

  - name: Run Playwright
    env:
      TYPO3_BASE_URL: http://localhost:8080
    run: npm run test:e2e
```

**Incorrect pattern (flag this):**
```yaml
# WRONG - Never do this in CI
- run: ddev start
- run: ddev exec vendor/bin/phpunit
```

## Troubleshooting Test Failures

### E2E Tests Fail

When E2E tests fail, debug systematically:

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| **Timeout on page load** | TYPO3 not started, wrong URL | Check `TYPO3_BASE_URL` env var, verify `php -S` is running |
| **Element not found** | Page not rendered, JS error | Add `await page.waitForLoadState('networkidle')`, check browser console |
| **Login fails** | Missing fixture, wrong credentials | Verify `be_users.csv` fixture loaded, check password hash |
| **Screenshot shows blank page** | PHP error, 500 response | Check `var/log/typo3_*.log`, enable debug mode |
| **Works locally, fails in CI** | See CI debugging section below | Environment differences |

**Debugging steps:**

1. **Capture screenshot on failure** (Playwright does this automatically)
2. **Check Playwright trace** for network requests: `npx playwright show-trace trace.zip`
3. **Verify TYPO3 is accessible**: `curl -I $TYPO3_BASE_URL`
4. **Check TYPO3 logs**: `cat .Build/Web/var/log/typo3_*.log`

### Tests Pass Locally But Fail in CI

This is a common frustration. Use this checklist:

| Check | Local vs CI Difference | Resolution |
|-------|------------------------|------------|
| **PHP version** | Local may differ from CI matrix | Ensure local PHP matches CI target |
| **Database state** | Local has data, CI starts fresh | Add missing fixtures to test setup |
| **File permissions** | Local user differs from CI runner | Avoid hardcoded paths, use `sys_get_temp_dir()` |
| **Timing** | Local is fast, CI is slow | Add explicit waits, avoid `sleep()` |
| **Environment vars** | Local `.env`, CI lacks it | Define all required vars in CI workflow |
| **Extensions loaded** | Local has extra PHP extensions | Check `php -m` output in CI logs |
| **Filesystem case** | macOS case-insensitive, Linux case-sensitive | Fix `require 'MyClass.php'` vs `myclass.php` |

**CI debugging workflow:**

```bash
# 1. Reproduce locally with CI-like conditions
docker run --rm -it php:8.3-cli php -m  # Check extensions

# 2. Add debug output to failing test
$this->markTestSkipped('DEBUG: ' . var_export($actualValue, true));

# 3. Check CI logs for environment differences
# Look for: PHP version, loaded extensions, env vars

# 4. Use GitHub Actions debug logging
env:
  ACTIONS_STEP_DEBUG: true
```

**Golden rule:** If tests pass locally but fail in CI, the bug is in your test's assumptions about the environment, not in the CI.
