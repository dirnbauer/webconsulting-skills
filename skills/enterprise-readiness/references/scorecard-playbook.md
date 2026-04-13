# OpenSSF Scorecard Optimization Playbook

Proven playbook to raise OpenSSF Scorecard from ~6.8 to ~9.0. Applied successfully on [t3x-rte_ckeditor_image](https://github.com/netresearch/t3x-rte_ckeditor_image).

## Check-by-Check Guide

| Check | Quick Fix | Impact |
|-------|-----------|--------|
| Token-Permissions | Move all `write` perms from workflow-level to job-level | 0->10 |
| Branch-Protection | Set `required_approving_review_count: 1` + auto-approve + protect release branches | 0->8 |
| Code-Review | Automatic after Branch-Protection fix | 5->10 |
| Security-Policy | Private vulnerability reporting + coordinated disclosure | 4->10 |
| Pinned-Dependencies | SHA-pin all actions; use `actions/attest-build-provenance` instead of `slsa-github-generator` | 8->10 |
| Fuzzing | Not practical for PHP/TYPO3 -- skip | 0 (accept) |
| CII-Best-Practices | Complete questionnaire at bestpractices.dev | 2->6+ |

## Token-Permissions (0->10)

The scorecard flags ANY `write` permission at the **workflow-level**. Fix: declare `permissions: contents: read` (or `permissions: {}`) at workflow-level, move all `write` to job-level.

```yaml
# CORRECT
permissions:
    contents: read

jobs:
    deploy:
        permissions:
            contents: write    # only this job gets write
        steps: ...

# WRONG -- Scorecard flags this
permissions:
    contents: read
    pull-requests: write       # write at workflow level!
```

Common violators: `pr-quality.yml`, `release-labeler.yml`, `create-release.yml`.

## Branch-Protection (0->8) for Solo Maintainers

Solo-dev projects need `required_approving_review_count >= 1` but can't wait for human reviewers. Solution: auto-approve workflow + ruleset.

**Default branch ruleset:**

```bash
gh api repos/OWNER/REPO/rulesets/RULESET_ID -X PUT --input - <<'EOF'
{
  "rules": [{
    "type": "pull_request",
    "parameters": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews_on_push": true,
      "require_code_owner_review": true,
      "require_last_push_approval": false,
      "required_review_thread_resolution": true
    }
  }]
}
EOF
```

> **`require_last_push_approval` MUST be `false` with merge queues.** The merge queue creates a new merge commit (a new "push") which dismisses the existing approval. The auto-approve bot cannot re-approve within the merge queue context, permanently blocking PRs. Verified on [netresearch/ofelia#543](https://github.com/netresearch/ofelia/pull/543).

**Release branch ruleset** (e.g., `TYPO3_*`, `release/*`):

```bash
gh api repos/OWNER/REPO/rulesets -X POST --input - <<'EOF'
{
  "name": "release-branches",
  "enforcement": "active",
  "target": "branch",
  "conditions": {"ref_name": {"include": ["refs/heads/TYPO3_*"], "exclude": []}},
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "pull_request", "parameters": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews_on_push": true,
      "require_code_owner_review": true,
      "require_last_push_approval": false,
      "required_review_thread_resolution": true,
      "allowed_merge_methods": ["merge"]
    }},
    {"type": "required_status_checks", "parameters": {
      "required_status_checks": [{"context": "Build", "integration_id": 15368}],
      "strict_required_status_checks_policy": true
    }}
  ]
}
EOF
```

Also enable `enforce_admins` via legacy API (scorecard reads this separately from rulesets):

```bash
gh api repos/OWNER/REPO/branches/main/protection/enforce_admins -X POST
```

Pair with `pr-quality.yml` auto-approve workflow (see `github-project` skill) that approves non-fork PRs via `github-actions[bot]`.

**Codeowner review:** `require_code_owner_review: true` works when the CODEOWNERS file lists the solo maintainer (`@username`) or a team they belong to. The auto-approve bot's approval satisfies the "approved review" requirement, and the codeowner rule is satisfied because the PR author IS the codeowner. Ensure the CODEOWNERS file exists on the default branch BEFORE enabling this rule.

> **Previous finding (outdated):** We previously reported that `require_code_owner_review` was incompatible with bot auto-approve. This was because the CODEOWNERS file didn't exist on the default branch when the rule was enabled. With CODEOWNERS properly configured, it works. Verified on [netresearch/ofelia](https://github.com/netresearch/ofelia) (2026-03-23).

**Unresolved review threads:** `required_review_thread_resolution: true` will block merge if automated reviewers (Gemini Code Assist, Copilot) leave unresolved threads. Resolve via:

```bash
gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "PRRT_xxx"}) { thread { isResolved } } }'
```

**Remaining scorecard warnings (unfixable for solo maintainer):**
- `required approving review count is 1` -- scorecard wants >= 2, impractical without human reviewers

## Security-Policy (4->10)

The scorecard requires SECURITY.md with:
1. Link to private reporting mechanism (not public issues!)
2. Response timeline (e.g., 48h acknowledgment, 7d fix)
3. Coordinated disclosure process

Template:

```markdown
## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, use [GitHub's private vulnerability reporting](https://github.com/ORG/REPO/security/advisories/new).

We will acknowledge receipt within 48 hours and aim to provide a fix
within 7 days for critical vulnerabilities.

## Coordinated Disclosure

After a fix is released, we will:
1. Publish a GitHub Security Advisory
2. Credit the reporter (unless anonymity is requested)
3. Include the fix in the next release with a CVE identifier if applicable
```

Enable private vulnerability reporting:

```bash
gh api repos/OWNER/REPO/private-vulnerability-reporting -X PUT
```

## SLSA Provenance: Migrate from slsa-github-generator to actions/attest

`slsa-framework/slsa-github-generator` can be SHA-pinned (and should be — see `references/slsa-provenance.md`), but its internal actions use tag refs that conflict with SHA-pinning rulesets ([#4440](https://github.com/slsa-framework/slsa-github-generator/issues/4440)). This triggers Scorecard warnings even when the top-level workflow call is correctly pinned.

**Migration path:** Replace with `actions/attest-build-provenance` (v4.1.0+), fully SHA-pinnable. For SLSA Build Level 3, host the build+attest workflow as a **reusable workflow in the org `.github` repo**. This provides true L3 isolation — callers cannot modify the build process. Verification uses `gh attestation verify` instead of `slsa-verifier`.

This eliminates the Pinned-Dependencies gap entirely (score can reach 10/10).

## Checks Not Worth Fixing

| Check | Why Skip |
|-------|----------|
| Fuzzing (0) | OSS-Fuzz doesn't support PHP/TYPO3; ROI too low |
| Packaging (-1) | TER publishing isn't detected as a packaging workflow |
| Signed-Releases (-1) | Detection issue — SLSA provenance exists but isn't recognized |
