# TDD Discipline

The strict loop used for bug fixes and new features. Prevents "tested and verified" claims that turn out to be wishful thinking.

## The Non-Negotiable Loop

For every bug fix, follow this sequence. Do not deviate. Do not ask the user for input mid-loop until the loop is green or until you have tried 5 distinct implementation approaches.

1. **Reproduce** — write a failing test that captures the bug. Commit it on the working branch under a conventional-commit message like `test: reproduce <bug>`.
2. **Confirm the test fails for the expected reason** — not a setup error, not a bootstrapping error, not a missing fixture. The failure message must describe the actual bug.
3. **Implement the minimal fix.** Scope it narrowly to the smallest diff that turns the failing test green.
4. **Run the specific test** via `Build/Scripts/runTests.sh -s unit -- --filter <TestName>` (or functional, as appropriate). Must pass.
5. **Run the full suite** (`-s unit`, `-s functional`) and linters (`-s phpstan`, `-s cgl`). Must all pass.
6. **If anything fails, iterate.** Do not report the fix as done. Try up to 5 distinct approaches before escalating.
7. **Only then open the PR.** The PR description must include the name of the reproduction test and the one-line verification command.

## Forbidden Phrases Without Evidence

These words are banned from assistant output unless the same turn contains the command output backing the claim:

- "tested"
- "verified"
- "confirmed working"
- "passes"
- "all green"

If you cannot run the verification (no DDEV available, no Docker, sandbox constraints), say so explicitly: "I implemented the fix but did not run the test suite because <reason>. The validating command is: `<command>`."

## Evidence Required

"Evidence" means one of:

- Command output pasted in the same turn (stdout or stderr)
- A CI run URL with visible status
- A gist or artifact link with visible content
- A GitHub Actions summary screenshot (for E2E)

A bare assertion from the assistant is not evidence.

## Playwright Hard Timeout

Playwright sessions have hung for 2+ hours when waiting for a selector that never appeared. Set a hard ceiling. The snippet below shows the timeout-relevant fields only — merge into the project's existing `playwright.config.ts` alongside its `projects`, `webServer`, `use`, and reporter settings:

```typescript
// playwright.config.ts — merge into existing defineConfig({...})
import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 120_000,            // 2 min per test — HARD CAP
  expect: { timeout: 15_000 }, // 15 s per expectation
  globalTimeout: 1_800_000,    // 30 min total across all tests
  workers: 4,
  forbidOnly: !!process.env.CI,
  // ... keep existing fields: projects, webServer, use, reporter, etc.
});
```

Individual tests that legitimately need more time must document why in a comment and pass `test.setTimeout(...)` explicitly — never raise the global default.

### If a Playwright run hangs

1. Kill it. Do not wait longer than the configured timeout.
2. Re-run with `DEBUG=pw:api` to see which action stalled.
3. Inspect the trace: `npx playwright show-trace test-results/*.zip`.
4. Add an explicit `waitFor` with a short timeout + meaningful error message to the stalling selector.

## Cross-Version Test Worktree Authority

When testing across TYPO3 v11/v12/v13/v14, use a separate worktree per version — never switch branches in place. The `.bare/` bare-clone layout this assumes (setup commands, absolute-path rules, cache safety) is documented in [`typo3-extension-upgrade-skill/references/multi-version-worktrees.md`](https://github.com/netresearch/typo3-extension-upgrade-skill/blob/main/skills/typo3-extension-upgrade/references/multi-version-worktrees.md) — set that up first, then:

```bash
git -C .bare worktree add ../TYPO3_11 TYPO3_11
git -C .bare worktree add ../TYPO3_12 TYPO3_12
git -C .bare worktree add ../main main

# Run tests in the specific worktree
cd ../TYPO3_11 && Build/Scripts/runTests.sh -s functional -p 8.1
cd ../main     && Build/Scripts/runTests.sh -s functional -p 8.4
```

### Before declaring "tested on v14"

Verify the command ran in the correct worktree:

```bash
pwd                                                      # must match the intended worktree

# composer.json: typo3/cms-core may be declared in require OR require-dev
# depending on whether the extension treats core as a runtime or a dev
# dependency. typo3/testing-framework is typically require-dev. Search the
# union so both forms work.
jq -r '(.require + (."require-dev" // {}))["typo3/cms-core"]'          composer.json
jq -r '(.require + (."require-dev" // {}))["typo3/testing-framework"]' composer.json

# composer.lock: same packages may resolve under .packages or .packages-dev
# per the same runtime/dev split.
jq -r '(.packages + (."packages-dev" // []))[] | select(.name=="typo3/cms-core") | .version'           composer.lock
jq -r '(.packages + (."packages-dev" // []))[] | select(.name=="typo3/testing-framework") | .version' composer.lock
```

All four values should agree on the target major. If you ran tests in the v13 worktree but claimed v14, the claim is false.

## Anti-Patterns

| Anti-pattern | What it looks like | Why it's wrong |
|--------------|--------------------|----------------|
| "Looks fine, should work" | No command run | Zero evidence |
| "Tests pass locally" | No output pasted | Unverifiable claim |
| Sharing a mock DB in a multi-test setup | One DB fixture across tests | Test pollution; flaky failures |
| Same service instance reused across tests | `private static Service $sharedService` at class scope | State bleed between tests |
| Running tests without `-p <php-version>` | `Build/Scripts/runTests.sh -s unit` on multi-PHP project | Silently uses host PHP, misses compat bugs |
| Declaring green on one TYPO3 version, shipping to all | Single `-s functional` run | Different LTSes break differently |

## Reporting a Fix

After the loop completes, report in this format:

```
Fix summary: <one sentence>

Reproduction test: Tests/Unit/<Name>Test.php::<testMethod>
Verification:
  $ Build/Scripts/runTests.sh -s unit -- --filter <Name>
  <pasted output, last 10 lines>

Full suite: green on <versions tested>
Not tested: <any versions or suites not exercised, with reason>
```

The "Not tested" line is mandatory — if every suite ran, write "none".
