# Legal framework examples for accessibility statement drafts

Use this file to select project wording before generating `.a11y/accessibility-statement-draft.de.md`.

The examples are intentionally conservative. They help classify a project, but they are not legal advice.

## Profile overview

| Profile | Typical use | Notes |
|---|---|---|
| `at-public-wzg` | Austrian public-sector website/app | Verify federal/state/municipal enforcement body. |
| `at-private-bafg` | Austrian private-sector product/service in BaFG/EAA scope | Verify scope before publishing statutory claims. |
| `de-public-bgg-bitv` | German federal public-sector website/app | For states/municipalities, verify Landesrecht. |
| `de-private-bfsg` | German private-sector product/service in BFSG/EAA scope | Verify covered product/service, exemptions and market surveillance body. |
| `ch-public-behig-ech0059` | Swiss public-sector/federal or eCH-0059 project | eCH-0059 v3 references WCAG 2.1 AA; WCAG 2.2 AA can be a stricter internal target. |
| `voluntary-wcag22aa` | Internal, contractual or best-practice WCAG 2.2 AA | Avoid statutory claims unless reviewed. |

## Copy/paste config snippets

### Austria public sector

```yaml
site:
  locale: "de-AT"
legal:
  profile: "at-public-wzg"
  jurisdiction: "AT"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
statement:
  enforcementBody: "FFG-Beschwerdestelle oder zuständige Landesstelle"
```

### Austria private sector / BaFG

```yaml
site:
  locale: "de-AT"
legal:
  profile: "at-private-bafg"
  jurisdiction: "AT"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
statement:
  enforcementBody: "zuständige Marktüberwachungs-/Beschwerdestelle nach Projekt prüfen"
```

### Germany public sector

```yaml
site:
  locale: "de-DE"
legal:
  profile: "de-public-bgg-bitv"
  jurisdiction: "DE"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
statement:
  enforcementBody: "Schlichtungsstelle BGG oder zuständige Landesstelle"
```

### Germany private sector / BFSG

```yaml
site:
  locale: "de-DE"
legal:
  profile: "de-private-bfsg"
  jurisdiction: "DE"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
statement:
  enforcementBody: "zuständige Marktüberwachungsbehörde nach Projekt prüfen"
```

### Switzerland public sector / eCH-0059

```yaml
site:
  locale: "de-CH"
legal:
  profile: "ch-public-behig-ech0059"
  jurisdiction: "CH"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "eCH-0059 v3 / WCAG 2.1 AA legal baseline; WCAG 2.2 AA as internal target"
statement:
  enforcementBody: "zuständige Schweizer Stelle nach Projekt prüfen"
```

### Voluntary / contractual WCAG 2.2 AA

```yaml
legal:
  profile: "voluntary-wcag22aa"
  jurisdiction: "contractual"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549 if contractually required"
statement:
  enforcementBody: "not applicable / internal contact"
```

## Statement wording guardrails

- Do not publish `vollständig vereinbar` unless manual HITL review confirms the sampled states, content, media and documents.
- Do not claim legal applicability of BFSG/BaFG/EAA unless scope was checked.
- For Germany public-sector state or municipal projects, replace BGG/BITV-only wording with the applicable state law if required.
- For Switzerland, do not turn eCH-0059/WCAG 2.1 AA legal baseline into a false WCAG 2.2 legal claim. Treat WCAG 2.2 AA as an internal higher target unless specifically required.
- Keep every exception tied to an owner, affected content, alternative, planned remediation and review date.
