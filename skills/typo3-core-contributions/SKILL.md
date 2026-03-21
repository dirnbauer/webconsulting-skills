---
name: typo3-core-contributions
description: >-
  TYPO3 Core contribution workflow. Use when working with Forge issues, submitting patches
  to Gerrit, or contributing docs.
compatibility: TYPO3 14.x
metadata:
  version: "1.0.0"
license: MIT / CC-BY-SA-4.0
---

# TYPO3 Core Contributions Skill

Guide for TYPO3 Core contribution workflow from account setup to patch submission.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in TYPO3 v14 by checking the official TYPO3 documentation.

## When to Use

- Forge issue URLs (e.g., `https://forge.typo3.org/issues/105737`)
- Contributing patches, fixing TYPO3 bugs
- Gerrit review workflow, rebasing, CI failures

## Prerequisites

Before contributing, ensure you have:

1. **TYPO3.org Account**: Register at https://my.typo3.org/
2. **Gerrit SSH Key**: Upload to https://review.typo3.org/settings/#SSHKeys
3. **Git Config**: Email must match your Gerrit account

```bash
# Verify git config
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# See "Clone TYPO3 Core" below for Gerrit remote setup
```

## Environment Setup

### Clone TYPO3 Core

**Recommended:** clone the public Git repository, then add Gerrit as a **push** remote (see the [official Contribution Guide](https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/) for the current URLs and the `git remote set-url origin --push …` variant).

```bash
git clone https://github.com/typo3/typo3.git typo3
cd typo3
# Official guide: configure origin’s *push* URL to Gerrit (preferred over a second remote):
#   git remote set-url --push origin "ssh://<username>@review.typo3.org:29418/Packages/TYPO3.CMS.git"
# Alternative: extra remote named `gerrit`
#   git remote add gerrit ssh://<username>@review.typo3.org:29418/Packages/TYPO3.CMS.git
```

From the Core root directory, set **`COMPOSER_ROOT_VERSION`** **before** `composer install` (required for a correct checkout), e.g. `export COMPOSER_ROOT_VERSION=14.0.x-dev` — see the [Contribution Guide](https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/) for the value matching your branch, then run `composer install`.

### Install Commit Hook (Change-Id)

Prefer Core’s documented methods — for example:

```bash
# After composer install in the Core clone:
composer gerrit:setup
# or copy the hook from the repository:
cp Build/git-hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

Avoid relying on `scp` from Gerrit unless you are following an explicit, up-to-date snippet from the guide.

## Contribution Workflow

### 1. Find or Create Issue

- Check existing issues: https://forge.typo3.org/projects/typo3cms-core/issues
- Create new issue if needed with detailed description

### 2. Create Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/105737-fix-cache-issue
```

### 3. Implement Changes

- Follow TYPO3 coding guidelines
- Write tests (unit, functional)
- Update documentation if needed

### 4. Commit with Proper Format

```bash
git add .
git commit
```

**Commit Message Format:**

```
[TYPE] Subject line (imperative; aim ~52 chars, **hard max 72**)

Description explaining how and why the change was made.
Can be multiple paragraphs.

Resolves: #12345
Releases: main
```

### 5. Push to Gerrit

Many developers use a dedicated remote (often named `gerrit`). The [Contribution Guide](https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/) also documents configuring **`origin`** with a separate **push** URL to Gerrit (`git remote set-url origin --push …`), in which case you push with `git push origin HEAD:refs/for/main` instead of a `gerrit` remote. **Use the remote name and ref your checkout actually uses.**

```bash
# Push for review (example: dedicated remote named "gerrit")
git push gerrit HEAD:refs/for/main
```

## Commit Message Format

### Types

| Type | Description |
|------|-------------|
| `[BUGFIX]` | Bug fix |
| `[FEATURE]` | New feature |
| `[TASK]` | Refactoring, cleanup, maintenance |
| `[DOCS]` | Documentation only |

### Flags (combine with a primary type)

| Flag | Meaning |
|------|---------|
| `[SECURITY]` | Coordinated security fix — use with a normal type, usually `[BUGFIX][SECURITY]`, per Security Team process (not a standalone “type” on its own) |
| `[!!!]` | Breaking change prefix (e.g., `[!!!][TASK]`) |

### Required Footer

```
Resolves: #12345
Releases: main
```

- `Resolves:` - Issue number on forge.typo3.org
- `Releases:` - Target branches (`main` for current development; stable backport branches per Forge issue)

### Example Commit Messages

**Bug Fix:**
```
[BUGFIX] Fix cache invalidation for page translations

The cache was not properly invalidated when updating
translated page properties. This patch ensures the
cache is cleared for all language variants.

Resolves: #105737
Releases: main
```

**Breaking Change (illustrative — match the real changelog entry):**
```
[!!!][TASK] Remove deprecated XYZ API

Describe the actual breaking change and the supported
replacement (Core event, new service API, etc.).

DataHandler datamap/cmdmap reactions often remain on
`SC_OPTIONS` hook classes unless a documented Core event exists.

Resolves: #98765
Releases: main
```

## Gerrit Workflow

### Update Existing Patch

When changes are requested:

```bash
# Make changes
# ...

# Amend commit (keep same Change-Id!)
git add .
git commit --amend

# Push again
git push gerrit HEAD:refs/for/main
```

### Rebase on Latest Main

```bash
# Fetch latest
git fetch origin main

# Rebase
git rebase origin/main

# Force push (allowed for your own patches)
git push gerrit HEAD:refs/for/main --force
```

### Backporting to a Stable Branch

After the patch is merged on `main`, backports follow **Forge + Gerrit** rules for the target branch (e.g. `13.4`, next patch-level branch). Typical flow:

```bash
git fetch origin
git checkout <target-branch>   # e.g. stable branch named in the issue
git pull origin <target-branch>

git cherry-pick -x <merge-commit-on-main>

# Push for review on THAT branch (not main)
git push <push-remote> HEAD:refs/for/<target-branch>
```

Use the remote name your checkout uses (`gerrit` or an `origin` push URL). See the [Contribution Guide](https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/) for the exact branch naming policy.

## Code Review

### Review States

| Vote | Meaning |
|------|---------|
| +2 | **Core Merger** approval — ready to merge into the target branch |
| +1 | You approve of the patch (non-binding for merge) |
| 0 | Comment only |
| -1 | You do not approve / request changes |
| -2 | **Core Merger** veto — do not merge (serious issues) |

**+2 / −2** are only available to Core Mergers; regular contributors use +1 / −1 / 0.

### CI Requirements

All patches must pass:
- [ ] Coding standards (PHP-CS-Fixer)
- [ ] PHPStan at the level enforced by Core CI for your branch (verify the **actual** config path in your checkout — it may move between releases)
- [ ] Unit tests
- [ ] Functional tests
- [ ] Acceptance tests (if applicable)

## Troubleshooting

### Push Rejected

```bash
# Missing Change-Id — reinstall the hook (see "Install Commit Hook" above), then:
git commit --amend
```

### Merge Conflicts

```bash
# Rebase on latest
git fetch origin main
git rebase origin/main

# Resolve conflicts
# Edit conflicting files
git add .
git rebase --continue

# Push updated patch
git push gerrit HEAD:refs/for/main --force
```

### CI Failures

1. Check CI output at review.typo3.org
2. Run tests locally:

```bash
# Run specific test suite (official Core helper)
Build/Scripts/runTests.sh -s unit
Build/Scripts/runTests.sh -s functional

# Composer meta-target (name may be `composer tests` plural — check composer.json)
composer tests

# Run PHP-CS-Fixer
Build/Scripts/runTests.sh -s cgl
```

## Related Skills

- **typo3-ddev**: Local development environment
- **typo3-testing**: Writing tests for patches
- **typo3-conformance**: Code quality validation

## Resources

- **Gerrit**: https://review.typo3.org/
- **Forge**: https://forge.typo3.org/
- **Contribution Guide**: https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/
- **Git Setup**: https://docs.typo3.org/m/typo3/guide-contributionworkflow/main/en-us/Setup/Git/

## v14-Only Contribution Notes

> The following notes are relevant when contributing to **TYPO3 v14 (main branch)**.

### v14 Branch and Feature Freeze **[v14 only]**

- v14 development targets the `main` branch.
- Feature freeze for v14 is **March 31, 2026**. After this date, only bug fixes are accepted.
- v14.3 LTS release planned for **April 21, 2026**.
- Patches for v14-specific features should target `main`.
- Bug fixes should be applied to the oldest affected branch and cherry-picked forward.

### Key v14 API Changes for Patches **[v14 only]**

When writing Core patches for v14, be aware of:
- **`$GLOBALS['TSFE']`:** direct global access was removed (see changelog). Prefer request attributes / PSR-7; `TypoScriptFrontendController` may still exist internally while APIs migrate — verify current Core for your branch.
- **`$GLOBALS['TCA']`:** loading base TCA from `$GLOBALS['TCA']` inside static TCA files was restricted; **`Configuration/TCA/Overrides/*.php` and runtime adjustments via documented APIs remain the normal place** for extension TCA changes. Do not confuse “no hacks in base TCA files” with “TCA is immutable everywhere.”
- Fluid 5.0 with strict typing.
- Backend modals use native `<dialog>` instead of Bootstrap Modal.
- Symfony Translation Component replaces custom localization parsers.

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-core-contributions-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
