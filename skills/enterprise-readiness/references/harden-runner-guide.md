# StepSecurity Harden-Runner Operational Guide

> Harden-Runner provides runtime security for GitHub Actions workflows by monitoring
> and optionally blocking outbound network connections from CI jobs.

## Egress Policy Modes

### Audit Mode (`egress-policy: audit`)

Logs all outbound connections without blocking anything. Use for:

- **Initial deployment** on existing workflows to discover required domains
- **Diagnostics** when debugging CI failures related to network access
- **Incident detection** — audit mode detected the trivy-action supply chain compromise
  by revealing unexpected outbound connections to attacker-controlled domains

```yaml
- name: Harden-Runner
  uses: step-security/harden-runner@<sha> # vX.Y.Z
  with:
    egress-policy: audit
```

### Block Mode (`egress-policy: block`)

Only allows connections to explicitly listed domains. All other outbound traffic is denied.

- **Would have PREVENTED** the trivy-action exfiltration — the compromised action's
  unauthorized outbound connection would have been blocked
- Requires a curated allowlist of domains the job legitimately needs

```yaml
- name: Harden-Runner
  uses: step-security/harden-runner@<sha> # vX.Y.Z
  with:
    egress-policy: block
    allowed-endpoints: >
      github.com:443
      api.github.com:443
      ghcr.io:443
      proxy.golang.org:443
```

## Migration Path: Audit to Block

1. **Deploy audit mode** on all workflow jobs
2. **Review StepSecurity insights** dashboard to identify all legitimate outbound domains
3. **Build domain allowlist** per job type (see patterns below)
4. **Switch to block mode** with the allowlist
5. **Monitor** for false positives — add missing domains as needed

## Domain Allowlist Patterns by Job Type

### Go Builds

```
proxy.golang.org:443
sum.golang.org:443
storage.googleapis.com:443
```

### npm Builds

```
registry.npmjs.org:443
```

### Docker Builds

```
# Docker Hub
registry-1.docker.io:443
auth.docker.io:443
production.cloudflare.docker.com:443

# GitHub Container Registry
ghcr.io:443
```

### Trivy Scans

```
# GitHub Container Registry (trivy-db download)
ghcr.io:443
```

### GitHub Operations

```
# GitHub platform
github.com:443
api.github.com:443
uploads.github.com:443
```

### Composer (PHP)

```
repo.packagist.org:443
packagist.org:443
getcomposer.org:443
```

## Full Configuration Example (Block Mode)

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Harden-Runner
        uses: step-security/harden-runner@<sha> # vX.Y.Z
        with:
          egress-policy: block
          allowed-endpoints: >
            github.com:443
            api.github.com:443
            proxy.golang.org:443
            sum.golang.org:443
            storage.googleapis.com:443
            ghcr.io:443

      - uses: actions/checkout@<sha> # vX.Y.Z

      - name: Build
        run: go build ./...

      - name: Test
        run: go test ./...
```

## Key Points

- Harden-Runner must be the **first step** in every job
- Each job needs its **own** Harden-Runner step with a job-specific allowlist
- Use `:443` port suffix for HTTPS endpoints in the allowlist
- StepSecurity provides a free insights dashboard showing all detected egress for public repos
- Pin the `step-security/harden-runner` action to a commit SHA (not a tag)

## Resources

- [StepSecurity Harden-Runner](https://github.com/step-security/harden-runner)
- [StepSecurity App Dashboard](https://app.stepsecurity.io/)
- [OpenSSF Scorecard — Token Permissions](https://github.com/ossf/scorecard/blob/main/docs/checks.md#token-permissions)
