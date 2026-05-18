# npm / pnpm Supply-Chain Hardening

Lifecycle-script execution, version quarantine, and lockfile defenses for JavaScript dependencies. Applies to any repo using `npm`, `pnpm`, or `yarn`, with concrete pnpm 10.26+ / 11+ configuration.

## Why this matters

Lifecycle scripts (`preinstall`, `install`, `postinstall`) are the #1 npm supply-chain attack vector. A compromised maintainer account or hijacked publish lets the attacker run arbitrary code on every developer machine and CI runner that installs the package — without any source change visible in the repo.

Defenses must be layered. No single control catches every attack class:

| Layer | Stops |
|-------|-------|
| Committed lockfile + `--frozen-lockfile` | Version substitution: a hijacked **new** version cannot be installed without a lockfile diff visible in PR review |
| Lifecycle-script allowlist (`allowBuilds`) | Newly added transitive dep with a malicious postinstall — install fails for unlisted names |
| Lifecycle-script **denylist** (`allowBuilds.foo: false`) | A hijacked version of a known dep that previously needed scripts but no longer does (because prebuilt platform binaries make the postinstall redundant) |
| Release-age quarantine (`minimumReleaseAge`) | A freshly hijacked version that hasn't been flagged yet — buys time for the community to detect and unpublish |
| Dep-PR human review | Integrity-hash changes are visible in the lockfile diff |
| npm provenance (`--require-attestation`, sigstore) | Tampering between source and registry — but most packages still don't publish provenance, so tree-wide enforcement isn't yet practical |

## pnpm 11+ canonical configuration

Settings live in `pnpm-workspace.yaml` (not `.npmrc` / `.pnpmrc` — those are for client behavior).

```yaml
packages:
  - '.'
  # other workspaces

# Fail install when any dependency wants to run lifecycle scripts that
# aren't explicitly handled in allowBuilds. Default since pnpm 11.
strictDepBuilds: true

# Per-package, per-version allow/deny map for lifecycle scripts.
# - true:  scripts may run
# - false: scripts must NOT run (preferred for packages with prebuilt binaries)
# Supports version ranges: "nx@21.6.4 || 21.6.5: true"
allowBuilds:
  esbuild: false
  "@parcel/watcher": false
  # electron: true   # genuinely needs its postinstall

# 7-day quarantine on freshly published versions (value is in MINUTES).
# Reduces the window where a hijacked publish can land before npm/the
# community removes it. Use minimumReleaseAgeExclude for hotfixes.
minimumReleaseAge: 10080

minimumReleaseAgeExclude:
  - package-with-critical-hotfix@1.2.3
```

### Why deny scripts for esbuild and @parcel/watcher

Both ship per-platform prebuilt binaries via `optionalDependencies`:

- `@esbuild/linux-x64`, `@esbuild/darwin-arm64`, `@esbuild/linux-x64-musl`, …
- `@parcel/watcher-linux-x64-glibc`, `@parcel/watcher-darwin-arm64`, …

pnpm/npm install only the matching optional dep for the current platform. The wrapper package's `postinstall` is a fallback for environments where the optional dep didn't install — when it does install (the normal case), the postinstall is redundant.

Setting `allowBuilds.esbuild: false` (the `esbuild: false` entry in the `allowBuilds` map) means **even a hijacked future release of `esbuild` cannot execute code at install time**, because pnpm refuses to run its scripts regardless of version. The prebuilt binary still works because it's resolved through a separate package whose tarball is integrity-checked by the lockfile.

A name-only allowlist (the deprecated `onlyBuiltDependencies: ["esbuild"]`) does NOT have this property: it permits scripts for any version named `esbuild`, including a hijacked one.

## Engine constraints must track feature floor

If your config uses `allowBuilds` (added in pnpm 10.26) or `minimumReleaseAge` (added in 10.16), require those versions in `package.json`:

```json
{
  "engines": {
    "node": ">= 22.0.0",
    "pnpm": ">= 10.26.0"
  }
}
```

Without this, an older pnpm silently ignores the new keys and the hardening becomes a no-op. Combined with `engine-strict=true` in `.npmrc` / `.pnpmrc`, pnpm will refuse to install on too-old versions instead of degrading silently.

## Deprecated fields (avoid)

The following pnpm 10 settings were superseded by `allowBuilds` and **removed in pnpm 11**:

| Removed (pnpm 11) | Replacement |
|---|---|
| `onlyBuiltDependencies: ["esbuild"]` | `allowBuilds: { esbuild: true }` |
| `neverBuiltDependencies: ["core-js"]` | `allowBuilds: { core-js: false }` |
| `ignoredBuiltDependencies: ["esbuild"]` | `allowBuilds: { esbuild: false }` |
| `onlyBuiltDependenciesFile: "..."` | n/a — inline in `pnpm-workspace.yaml` |

`ignoredBuilds` is **not** a valid pnpm setting (despite occasional AI reviewer suggestions). The legacy field was named `ignoredBuiltDependencies`.

## Reproducibility — pin the package manager

`corepack prepare pnpm@latest --activate` in Dockerfiles or CI is a CI-stability footgun **only when** you also fail to adopt the new security defaults that come with each major. The right move is both:

1. **Pin the version** so upgrades are explicit PRs, not silent breakage on the next image build:

   ```json
   {
     "packageManager": "pnpm@11.0.9"
   }
   ```

   Then in the Dockerfile:

   ```dockerfile
   RUN corepack enable && corepack prepare --activate
   ```

   (no version argument — corepack reads `packageManager` from `package.json`).

2. **Adopt the new security defaults** as they ship. pnpm 11 flipped `strictDepBuilds` to default-true, which is the right behavior — projects that hadn't configured `allowBuilds` saw CI break immediately. That break was the system working as designed; the fix is to configure `allowBuilds`, not to revert pnpm.

## Verification

A working hardened config produces this on `pnpm install --frozen-lockfile`:

```
Done in 3.3s using pnpm v11.0.9
```

No `[ERR_PNPM_IGNORED_BUILDS]` warning, no `Run "pnpm approve-builds"` prompt. If either appears, `allowBuilds` is missing entries or the pnpm version is too old.

To audit a repo end-to-end:

```bash
# Settings are present
yq -e '.strictDepBuilds == true and .allowBuilds and .minimumReleaseAge' pnpm-workspace.yaml

# Engine floor is high enough
jq -e '.engines.pnpm | test("\\^?(10\\.(2[6-9]|[3-9][0-9])|[1-9][0-9]+)")' package.json

# Lockfile is committed and frozen install works
test -f pnpm-lock.yaml && pnpm install --frozen-lockfile
```

## npm and yarn equivalents

| Capability | pnpm 11+ | npm | yarn (Berry) |
|---|---|---|---|
| Block scripts globally | `allowBuilds` (deny by omission with `strictDepBuilds`) | `ignore-scripts=true` in `.npmrc` (all-or-nothing) | `enableScripts: false` in `.yarnrc.yml` |
| Per-package allow | `allowBuilds: { pkg: true }` | n/a | `--ignore-scripts` plus selective post-install |
| Per-version pinning | `allowBuilds: { "pkg@1.2.3": true }` | n/a | n/a |
| Release-age quarantine | `minimumReleaseAge` | n/a (proposed; not landed) | n/a |
| Provenance verification | `verify-deps-before-run` (limited) | `npm install --require-attestation` | n/a |

For npm, the practical hardening today is:

```ini
# .npmrc
ignore-scripts=true
audit-level=high
```

…then explicitly run any required postinstalls in CI/build scripts. This trades convenience for safety; pnpm's per-package `allowBuilds` is the more ergonomic answer when you have the choice.

## Related

- `slsa-provenance.md` — provenance and attestations for your **own** releases (counterpart to consuming attested upstream packages)
- `signed-releases.md` — cosign / GPG signing for release artifacts
- `reproducible-builds.md` — locked toolchains and dependency pinning
- `mandatory-requirements.md` — checklist incorporation
