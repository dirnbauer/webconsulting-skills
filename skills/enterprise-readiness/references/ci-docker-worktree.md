# CI Robustness in Docker/Worktree Environments

Patterns and fixes for CI pipelines that run inside Docker containers
or git worktree checkouts, where common assumptions about the `.git`
directory structure break.

## 1. CaptainHook in Docker

CaptainHook's hook-installer plugin fails in Docker containers and git
worktrees where `.git` is a file (pointing to the bare repo) instead
of a directory. The failure aborts Composer's `post-install-cmd`
scripts, silently preventing subsequent plugins from running.

### Fix

Add `CAPTAINHOOK_DISABLE=true` to every Docker-based Composer command:

```bash
docker run ... -e CAPTAINHOOK_DISABLE=true ... composer install
```

In `runTests.sh` or similar CI scripts, pass the variable into the
container environment:

```bash
docker compose run -e CAPTAINHOOK_DISABLE=true php composer install --no-interaction
```

### Detection

Find Composer commands that are missing the guard:

```bash
grep -n "composer" Build/Scripts/runTests.sh | grep -v "CAPTAINHOOK_DISABLE"
```

Any match indicates a command that will fail when `.git` is not a
directory (Docker, worktrees, CI shallow clones).

## 2. PHPStan Extension Installer Verification

`phpstan/extension-installer` registers extensions during Composer's
`post-install-cmd` phase. If an earlier plugin (such as CaptainHook)
aborts that phase, extension-installer never runs, and PHPStan
operates without the extensions it needs.

### Symptom

PHPStan reports false positives or misses errors that extensions
should catch (e.g., PHPStan for Doctrine, phpstan-phpunit).

### Verification

After `composer install`, check the generated config:

```bash
# Prefer TYPO3-style .Build/vendor if present; otherwise use vendor/ or $VENDOR_DIR
VENDOR_DIR="${VENDOR_DIR:-vendor}"
if [ -d ".Build/vendor" ]; then
  SEARCH_PATH=".Build/vendor/phpstan/extension-installer/src/GeneratedConfig.php"
else
  SEARCH_PATH="$VENDOR_DIR/phpstan/extension-installer/src/GeneratedConfig.php"
fi

grep -F "EXTENSIONS = []" "$SEARCH_PATH"
```

If the output shows `EXTENSIONS = []`, the extension-installer plugin
did not execute. This is almost always caused by CaptainHook (or
another plugin) failing before extension-installer could run.

### Fix

Apply the CaptainHook disable fix from Section 1, then re-run
`composer install`. Verify that `GeneratedConfig.php` now lists the
expected extensions.

## 3. Lint Scope

PHP lint (`php -l`) test suites must scan only project source
directories, not `vendor/` or `.Build/`. Third-party packages may
contain intentional syntax error fixtures (e.g., for their own parser
tests), which cause false lint failures.

### Wrong -- scans vendor too

```bash
find . -name '*.php' ! -path './.Build/*' -exec php -l {} \;
```

This still includes `vendor/` at the project root (if present) and
misses the intent of excluding build artifacts.

### Acceptable -- `find .` with proper exclusions

```bash
find . -name '*.php' \
  ! -path './vendor/*' ! -path './.Build/*' ! -path './var/*' ! -path './node_modules/*' \
  -exec php -l {} \;
```

Using `find .` is fine when it explicitly prunes or excludes
third-party and build directories.

### Best -- scan only source directories

```bash
find Classes Configuration Tests -name '*.php' -exec php -l {} \;
```

Explicitly list the directories that contain project code. This is
faster, deterministic, and immune to third-party fixture files.

### Detection

```bash
grep -n 'find \.' Build/Scripts/runTests.sh | grep -Ei 'php.*-l|lint'
```

If the `find` starts from `.` without `-prune` or `! -path` exclusions
for vendor/, .Build/, var/, etc., the lint scope is too broad.

## 4. Merge Queue Awareness

When branch protection uses GitHub merge queues, several constraints
apply that can surprise CI workflows:

| Constraint | Effect |
|-----------|--------|
| `required_review_thread_resolution: true` | Blocks merge if any review thread is unresolved |
| Queue locks the branch | Commits cannot be pushed to a branch while it is in the merge queue |
| Auto-merge interaction | Auto-merge must be disabled before pushing fixes to a PR, then re-enabled after |

### Workflow

1. Address all review comments and resolve threads
2. If the PR has auto-merge enabled and needs fixes:
   - Disable auto-merge
   - Push the fix commits
   - Wait for CI
   - Re-enable auto-merge
3. Ensure all review threads are resolved before the PR enters the
   queue

### Detection

Check whether a repository uses merge queues:

```bash
gh api repos/{owner}/{repo}/rules/branches/main \
  --jq '.[].parameters.merge_queue_enabled // false'
```

## Related References

- `references/ci-patterns.md` -- CI/CD pipeline design and Git hooks
- `references/general.md` -- Universal enterprise readiness checks
- `references/security-hardening.md` -- Security scanning in CI
