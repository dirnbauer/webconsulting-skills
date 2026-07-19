---
name: typo3-14-update
description: Upgrade TYPO3 extensions, sitepackages, and full projects from v12 or v13 to TYPO3 14.3 LTS as v14-only code, including Composer metadata, Rector and Fractor migrations, PHPStan, workspaces, security, frontend performance, tests, documentation, deployment checks, and production-readiness verification. Use when asked for a complete TYPO3 v14 upgrade, a reusable v14 updater prompt, removal of legacy or dual-version compatibility, a production rollout, post-upgrade SEO or security verification, or a publication-ready TYPO3 14.3 extension.
---

# TYPO3 14 update

> Source: https://github.com/dirnbauer/webconsulting-skills

Upgrade one extension, sitepackage, or full project to supported TYPO3 14.3 LTS. Produce v14-only code; do not retain v12/v13 compatibility branches or shims.

## Operating contract

- Read the repository instructions and inspect the worktree before editing. Preserve unrelated and pre-existing changes.
- Work locally on a development copy. Never update production, push, tag, publish, open a pull request, or rewrite history unless the user explicitly requests it.
- Ask before destructive database changes, bulk deletion, feature removal, or discarding user changes. Prefer a clean v14 implementation; propose removing an impossible legacy feature before acting.
- Verify every TYPO3 class, method, event, attribute, configuration key, and CLI command against the TYPO3 14.3 documentation and installed v14 source. Use a TYPO3 API lookup tool when available. Never rely on memory or invent replacement APIs.
- Use Core APIs and documented extension points before custom implementations.
- Treat tool output as evidence. Do not claim a command, installation, test, or browser flow passed unless it ran successfully.
- Create commits only when requested. If commits are requested, use small phase commits after their quality gate passes; never push them automatically.

## Route the existing skills

Use only the skills relevant to the detected codebase, and run them sequentially so each pass sees the previous fixes.

| Order | Skill | Apply when |
|---|---|---|
| 1 | `typo3-extension-upgrade` | Always; inventory, dependency planning, upgrade sequence |
| 2 | `typo3-rector` | Always; PHP migration, first dry-run and then reviewed apply |
| 3 | `typo3-fractor` | Always; Fluid, TypoScript, FlexForm, YAML, and other non-PHP migration |
| 4 | `php-modernization` | PHP types, language level, Rector, PHPStan, and code-style tooling |
| 5 | `typo3-workspaces` | Always audit workspace safety; add explicit workspace behavior when records, previews, files, or publishing are involved |
| 6 | `typo3-conformance` and `typo3-simplify` | Always; v14 architecture, obsolete files, Core API reuse, and code clarity |
| 7 | `typo3-security` and `security-audit` | Always; extension-specific and general security review |
| 8 | `typo3-testing` | Always; preserve behavior and add missing unit, functional, integration, workspace, and E2E coverage as appropriate |
| 9 | `typo3-docs` | Always; README, TYPO3 documentation, upgrade notes, and changelog |

Select additional TYPO3 skills after inventory: `typo3-ddev`, `typo3-batch`, `typo3-content-blocks`, `typo3-datahandler`, `typo3-translations`, `typo3-accessibility`, `typo3-wcag22-aa-agentic`, `typo3-webcomponents`, `typo3-vite`, `typo3-icon14`, `typo3-visual-editor`, `typo3-powermail`, `typo3-solr`, and `typo3-seo`. Do not run unrelated domain skills merely because they exist.

## Verification references

- [TYPO3 14.3 extension upgrade documentation](https://docs.typo3.org/m/typo3/reference-coreapi/14.3/en-us/Administration/Upgrade/UpgradingExtensions/Index.html)
- [TYPO3 version support](https://docs.typo3.org/m/typo3/reference-coreapi/14.3/en-us/Security/Versions/Index.html)
- [TYPO3 `composer.json` reference](https://docs.typo3.org/m/typo3/reference-coreapi/14.3/en-us/ExtensionArchitecture/FileStructure/ComposerJson.html)
- [`saschaegerer/phpstan-typo3` releases](https://packagist.org/packages/saschaegerer/phpstan-typo3)

## Phase 1: Discover and establish a baseline

1. Determine whether the target is an extension, sitepackage, or full project. Keep project infrastructure outside scope unless required to prove the extension works.
2. Determine the current TYPO3/PHP versions from `composer.json`, `composer.lock`, CI, DDEV, and legacy metadata. Do not infer versions from filenames alone.
3. Inventory PHP, TCA, schema, Extbase, hooks/events, backend modules, commands, upgrade wizards, Fluid, TypoScript, FlexForms, YAML, JavaScript/import maps, translations, Content Blocks, DataHandler/FAL usage, workspaces, and third-party dependencies.
4. Run the repository's existing install, lint, static analysis, and tests on the current branch when feasible. Record pre-existing failures separately from regressions.
5. Produce a short plan with detected risks, conditional skills, verification commands, and any decision that needs user approval.

## Phase 2: Set the supported target and dependencies

1. Target `typo3/cms-core: ^14.3`, not `^14.0`, because 14.3 is the supported LTS line. Require PHP `^8.2` or a narrower supported range justified by dependencies. For full-project production rollouts using the strict production gate below, support only PHP 8.3; keep a broader PHP range only for reusable packages that test and document it.
2. Audit every required and development package using Composer and the package's current release metadata. Upgrade, replace, or explicitly block incompatible packages before changing application code.
3. For TYPO3 v14-only extensions, migrate metadata to `composer.json` and remove deprecated `ext_emconf.php` unless the user explicitly requires a temporary v13 compatibility bridge.
4. Keep `type: typo3-cms-extension`, PSR-4 autoloading, and `extra.typo3/cms.extension-key` valid. For Classic-mode compatibility, set `extra.typo3/cms.version` to the intended release version and add `extra.typo3/cms.Package.providesPackages`, including an empty object when no Composer packages are provided. The version must match the future Git tag; do not create the tag.
5. Remove obsolete `replace` entries for `typo3-ter/*` or the extension key when Composer validation flags them.
6. Update PHPStan to the newest release compatible with the resolved v14 dependency set. Include `saschaegerer/phpstan-typo3` through `phpstan/extension-installer` or its documented `extension.neon`; do not copy stale configuration from the repository.
7. Run `composer validate --strict`, update dependencies with the narrowest justified command, and inspect the lockfile diff.

## Phase 3: Apply mechanical migrations

1. Configure TYPO3 Rector for the actual source-to-v14 path. Run a dry-run, review the diff, apply, and run a second dry-run.
2. Configure Fractor for the same path. Run a dry-run, review non-PHP changes, apply, and run a second dry-run.
3. Run code style and syntax checks immediately after each tool.
4. Never accept a bulk transformation blindly. Split ambiguous DBAL, Extbase, TCA, Fluid, or dependency changes into independently verifiable units.

## Phase 4: Complete the manual v14 migration

1. Resolve v14 changelog items and extension-scanner findings for every used API surface, including changes not covered by Rector or Fractor.
2. Remove `TYPO3_version` branches, v12/v13 constraints, compatibility helpers, deprecated hooks with documented event replacements, legacy backend module registration, obsolete TypoScript, unused XLF keys, and dead imports.
3. Keep legitimate DataHandler hooks when no real PSR-14 event exists. Never replace a hook with a guessed event name.
4. Make TCA and schema v14-compliant, preserve localization and relations, and add upgrade wizards for persisted data changes. Test migrations with representative data.
5. Make record reads, writes, previews, overlays, file handling, and rendering workspace-aware. Add tests for create, edit, preview, publish, discard, localization, and relation handling where applicable. Account explicitly for FAL's workspace limitations.
6. Preserve extension behavior unless the user approved a breaking feature change. Add regression tests before risky rewrites.

## Phase 5: Raise quality gates

1. Run PHPStan at level 9 or higher; never lower an existing stricter level. Do not add suppressions or a new baseline for new or touched code. Existing baselines may remain only for untouched legacy findings and must shrink when findings are fixed.
2. Run PHP lint, code style, Rector dry-run, Fractor dry-run, static analysis, unit tests, functional/integration tests, and E2E tests through the repository's canonical commands.
3. Run conformance, simplification, TYPO3 security, and general security passes. Fix verified actionable findings, then rerun the affected gate.
4. Test a clean Composer install in a fresh TYPO3 14.3 environment. Exercise backend and frontend behavior, CLI commands, caches, database schema comparison, upgrade wizards, translations, permissions, and workspaces relevant to the extension.
5. Use the project's supported CI matrix. A v14-only extension needs a TYPO3 14.3 job and every PHP version it claims to support.

### Full-project production readiness

Apply this gate when the target is a complete project, site distribution, or production rollout. Skip only the items that are demonstrably inapplicable to an extension-only package, and record every skip.

1. Prefer TYPO3 Core and v14 integrations over parallel custom implementations. Audit `EXT:seo`, Sites configuration, TYPO3 CSP, FAL/Image Processing, `PageTitleProvider`, and PSR-15 middleware at their documented integration points.
2. Run `composer validate --strict` and `composer audit`; unresolved security advisories block completion. Run the repository's canonical lint, PHPStan, Rector dry-run, and test commands in CI or an equivalent clean environment.
3. In a development or staging copy, run the verified TYPO3 14.3 equivalents of `vendor/bin/typo3 extension:setup`, `vendor/bin/typo3 database:updateschema --dry-run`, and `vendor/bin/typo3 upgrade:list`. Review the output before any non-dry-run database change and keep a recoverable backup for production migrations.
4. Inspect the deployed nginx, reverse-proxy, load-balancer, and CDN configuration separately from application files. `.htaccess` does not control nginx. Verify TLS redirects, trusted forwarded hosts, cache behavior, security headers, and TYPO3 CSP without creating conflicting header policies at multiple layers.
5. Verify `robots.txt`, XML sitemaps, `noindex` rules, canonicals, unique page titles, meta descriptions, Open Graph metadata and preview images, X/Twitter card metadata, and site-level and article JSON-LD on representative page types. Use `EXT:seo` and TYPO3 rendering APIs where they cover the requirement.
6. After deployment, explicitly flush and warm the applicable TYPO3 and proxy caches with commands verified in the installed project. Reload backend modules and representative frontend pages after warmup. When Sites YAML, TypoScript, environment values, or `EXT:solr` configuration changed, invalidate the site-configuration and TypoScript caches; confirm the Apache Solr backend Info module recognizes the intended site as active instead of accepting frontend search alone as proof.
7. Smoke-test the homepage, a standard content page, article/news detail, issue or edition pages when present, search including empty and paginated results, login and password recovery, Powermail or other production forms, the 404 response, `robots.txt`, and every sitemap entry point. Use safe test recipients and do not send customer-facing messages or submit live business workflows without explicit permission.
8. Recrawl production after deployment. Recheck response headers, status codes, canonicals, titles/descriptions, Open Graph/X metadata and preview images, JSON-LD, sitemap membership, robots directives, and indexability. Do not close the upgrade while a critical or high-severity finding remains.

### Frontend performance evidence

When the upgraded package renders a public frontend, include Lighthouse and
resource-delivery checks in the quality gate:

1. Run Lighthouse against representative page types in a clean, extension-free
   browser profile. Record the Lighthouse version, URL, viewport/device mode,
   timestamp, category scores, Core Web Vitals, and report artifact.
2. Inspect every audit URL before creating work. Treat `chrome-extension://`
   JavaScript as contaminated measurement data rather than application code.
   Separate same-origin findings from third-party services whose cache or
   execution policy the project does not control, and rerun cleanly before
   making code changes.
3. Use TYPO3 v14's native
   `$GLOBALS['TYPO3_CONF_VARS']['GFX']['imageFileConversionFormats']` and
   `avif_quality` settings for processed raster images when the installed image
   processor reports AVIF write support. Preserve animated GIF and SVG behavior,
   verify the generated `.avif` response MIME type and dimensions, and retain a
   different format when AVIF is larger or unsupported for that asset path.
4. Preload only resources that are critical to the measured LCP. Font preloads
   need `as="font"`, `type="font/woff2"`, and `crossorigin`; image preloads need
   the same processed AVIF URL and dimensions as the rendered image. The preload
   URL must match the requested resource exactly, including cache-busting query
   strings. Do not preload later carousel slides or below-the-fold images.
5. Give the measured LCP image eager loading and `fetchpriority="high"`; keep
   noncritical images lazy with asynchronous decoding. Confirm the final HTML
   contains one preload for each intended resource and no duplicate downloads.
6. TYPO3 v14 removed `config.compressCss`, `config.compressJs`, and frontend
   concatenation. Resolve verified minification findings at build time (for
   example through the repository's existing Vite pipeline) instead of adding
   obsolete TypoScript. Keep a small render-blocking stylesheet when its measured
   cost is lower than the complexity or regressions of asynchronous loading.

## Phase 6: Finish documentation and delivery

1. Rewrite `README.md` as the concise public entry point: purpose, value, features, TYPO3/PHP requirements, installation, quick start, configuration, workspace behavior, testing, limitations, and links to detailed docs.
2. Update `Documentation/` using TYPO3 documentation conventions. Add a v12/v13-to-v14 upgrade guide, migration commands, data upgrade steps, breaking changes, and removed features.
3. Add a `CHANGELOG.md` entry describing the v14.3-only requirement, dropped versions, dependency changes, workspace support, and migrations. Do not invent a release date or tag.
4. Produce one consolidated final report with changed files, dependency decisions, verification commands and results, remaining risks, skipped checks, and user approvals. Persist it under `docs/audits/` only when the repository already uses that convention or the user requests an audit artifact.

## Completion gate

Finish only when all applicable items are true:

- A clean install resolves against TYPO3 14.3 LTS and the claimed PHP versions.
- Composer validation, lint, code style, PHPStan level 9+, Rector dry-run, Fractor dry-run, and all applicable tests pass.
- Workspace create/edit/preview/publish/discard behavior passes where the extension handles versionable records or content.
- No v12/v13 compatibility remains in executable code or configuration; historical mentions may remain in upgrade documentation and changelog.
- Security, conformance, and documentation passes have no unresolved critical findings.
- Frontend projects have a clean-profile Lighthouse report; same-origin findings
  are resolved or explicitly justified, processed raster output is verified as
  AVIF where beneficial, and every critical preload exactly matches its consumer.
- Full-project rollouts pass the production-readiness gate: Composer and TYPO3 CLI checks, database dry-run review, post-deployment cache flush and warmup, infrastructure/header checks, representative smoke tests, and a production recrawl have no unresolved critical or high-severity findings; every applicable security-header, social-metadata, SEO, indexing, and structured-data item is complete.
- `README.md`, `Documentation/`, and `CHANGELOG.md` agree with `composer.json` and actual behavior.
- No push, tag, publication, or pull request occurred without explicit user authorization.

If a gate cannot run, state exactly why, show the evidence available, and leave the task incomplete rather than claiming success.
