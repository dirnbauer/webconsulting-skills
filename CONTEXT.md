# Webconsulting Skills

Shared glossary for reusable webconsulting skill workflows.

## Language

**Binding Angebot**:
A customer-facing TYPO3 update offer with concrete scope and price. It requires repository access, `composer.lock`, and either staging or a runnable local DDEV environment. Without those inputs, the skill must produce only an explicitly labeled indicative range.
_Avoid_: fixed price from public URL only, blind estimate

**Indicative Range**:
A non-binding cost range for a TYPO3 update when the agent only has partial information, such as a public website URL without repository, lockfile, or staging/DDEV access.
_Avoid_: Angebot, fixed quote

**TYPO3 Update Package**:
The default scope for a TYPO3 14.3+ update Angebot. It includes Core/DDEV/database/site settings/third-party extension updates, frontend build migration to Vite with speed optimization, security hardening with mandatory security headers, SEO/GEO/schema improvements, and Playwright visual regression from `sitemap.xml`.
_Avoid_: optional module list, minimal core-only update

**Custom Extension Nachtrag**:
Separate offer line for customer-specific or webconsulting-specific TYPO3 extensions and sitepackage compatibility work. Custom extensions are not included in the fixed TYPO3 Update Package.
_Avoid_: include own extensions in core package, hidden buffer

**Third-Party Extension Update**:
Part of the TYPO3 Update Package. It covers all non-TYPO3-core, non-custom Composer or TER extensions from `composer.json` and `composer.lock`, upgraded to TYPO3 14.3+ compatible releases where available, including setup commands and smoke checks.
_Avoid_: selected major extensions only, vague extension update

**Extension Blocker**:
A third-party extension without a TYPO3 14.3+ compatible path, or with a replacement/removal decision required before a Binding Angebot can be finalized.
_Avoid_: silently include unsupported extension, assume compatibility

**Sitemap QA Gate**:
Requirement that `sitemap.xml` responds successfully and parses as valid XML before the skill prices or runs sitemap-based Playwright visual regression. If the sitemap is broken, the skill must mark the URL set as provisional and include sitemap repair in scope.
_Avoid_: visual regression scope from unchecked sitemap, silent fallback

**Tiered Playwright Scope**:
Visual regression scope selected from `sitemap.xml`: up to 100 URLs means all sitemap URLs; 101 to 500 URLs means a stratified sample capped at 50 URLs; more than 500 URLs means a stratified sample capped at 50 URLs with optional Nachtrag for additional coverage.
_Avoid_: arbitrary screenshot list, full-site screenshot promise on large sites

**Security Header Gate**:
Acceptance requirement that staging and production responses include the agreed security headers after delivery: HSTS, CSP or CSP report-only during rollout, X-Frame-Options or CSP `frame-ancestors`, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy.
_Avoid_: headers as optional best effort, complete without verification
