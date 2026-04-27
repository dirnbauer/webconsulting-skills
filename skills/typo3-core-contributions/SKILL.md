---
name: "typo3-core-contributions"
description: "Use when analyzing TYPO3 Forge issues, submitting patches to Gerrit, contributing core bug fixes, documentation contributions, cherry-pick workflows, or CI debugging on Gerrit. Core `main` branch is v15-in-progress (PHP 8.4/8.5); v14.3 LTS bugfixes land on branch `14.3` and are backported via cherry-pick. Also triggers on: forge.typo3.org, core patch, Gerrit review, TYPO3 Core contribution."
---

# TYPO3 Core Contributions

Guide for contributing to TYPO3 Core: Forge issues, Gerrit patches, CI debugging, and review workflows.

## When to Use

- Forge issue analysis or creation (`forge.typo3.org/issues/*`)
- Patch submission, CI debugging, Gerrit review workflow
- Commit message formatting, cherry-picks, rebasing

## Prerequisites

Run `${CLAUDE_SKILL_DIR}/scripts/verify-prerequisites.sh` to check: TYPO3.org account, Gerrit SSH (`ssh -p 29418 <user>@review.typo3.org`), Git email matching Gerrit. See `references/account-setup.md`.

## Workflow

1. **Setup**: Account + environment (`${CLAUDE_SKILL_DIR}/scripts/setup-typo3-coredev.sh`, `references/ddev-setup-workflow.md`)
2. **Branch**: `git checkout -b feature/<issue>-description`
3. **Analyze**: Understand root cause, reproduction steps, affected versions before coding
4. **Develop**: Implement fix + tests, validate with typo3-conformance-skill
5. **Commit**: Follow format below, include `Resolves: #<issue>` + `Releases:`
6. **Push**: `git push origin HEAD:refs/for/main` (starts as WIP)
7. **CI**: Wait for all jobs. Read actual GitLab logs at `git.typo3.org/typo3/CI/cms/-/jobs/<id>`. Fix ALL failures in one amend+push
8. **Ready**: Mark ready via `git push origin HEAD:refs/for/main%ready` or Gerrit UI "Start Review"
9. **Review**: Address feedback, amend commit, preserve Change-Id. Fetch reviewer's patchset first to preserve their message edits: `git fetch origin refs/changes/XX/NNNNN/N && git reset --soft FETCH_HEAD`
10. **Update**: `git commit --amend && git push origin HEAD:refs/for/main`

## Commit Format

```
[TYPE] Subject (imperative mood, max 52 chars)

How and why (not what). Wrap at 72 chars.

Resolves: #12345
Releases: main, 13.4, 12.4
```

**Types**: `[BUGFIX]`, `[FEATURE]` (main only), `[TASK]`, `[DOCS]`, `[SECURITY]`
**Breaking**: `[!!!][TYPE]` prefix, `Releases: main` only
**Required**: Every commit MUST have `Resolves:` (not just `Related:`)

## CI Debugging

Read ALL failing job logs (never guess). Common jobs: `cgl pre-merge` (code style), `phpstan` (static analysis), `unit`/`functional` (tests). Fix all in one patchset. Local checks:

```bash
./Build/Scripts/runTests.sh -s unit && ./Build/Scripts/runTests.sh -s functional
./Build/Scripts/cglFixMyCommit.sh
./Build/Scripts/runTests.sh -s phpstan
```

## Key Operations

| Task | Command |
|------|---------|
| Push to Gerrit | `git push origin HEAD:refs/for/main` |
| Mark ready | `git push origin HEAD:refs/for/main%ready` |
| Set WIP | `git push origin HEAD:refs/for/main%wip` |
| Rebase | `git fetch origin && git rebase origin/main` |
| Cherry-pick patch | `git fetch origin refs/changes/XX/NNNNN/N && git cherry-pick FETCH_HEAD` |
| Install hook | `cp Build/git-hooks/commit-msg .git/hooks/ && chmod +x .git/hooks/commit-msg` |
| Fix email mismatch | `GIT_COMMITTER_EMAIL="registered@email" git commit --amend --no-edit` |
| Forge API | `${CLAUDE_SKILL_DIR}/scripts/create-forge-issue.sh`, `references/forge-api.md` |

## References

| Topic | File |
|-------|------|
| Account setup | `references/account-setup.md` |
| Commit format | `references/commit-message-format.md` |
| Gerrit workflow | `references/gerrit-workflow.md` |
| Review patterns | `references/gerrit-review-patterns.md` |
| Modern patterns | `references/modern-typo3-patterns.md` |
| DDEV setup | `references/ddev-setup-workflow.md` |
| Forge API | `references/forge-api.md` |
| Commit hook | `references/commit-msg-hook.md` |
| Troubleshooting | `references/troubleshooting.md` |

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-core-contributions-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)

Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their generous open-source contributions to the TYPO3 community, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
