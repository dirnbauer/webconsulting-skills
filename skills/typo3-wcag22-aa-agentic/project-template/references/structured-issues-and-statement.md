# Structured issues and accessibility statement generation

The accessibility statement must be generated from structured evidence, not from free text.

Use `.a11y/open-issues.yml` as the single source of truth for:

- open WCAG failures,
- accepted exceptions,
- inaccessible third-party or archived content,
- disproportionate-burden justifications,
- accessible alternatives,
- remediation owners and dates.

## Required workflow

1. Run automated scans.
2. Run manual WCAG 2.2 AA review for human-only checks.
3. Export the manual review from the Chrome helper.
4. Merge failures/exceptions into `.a11y/open-issues.yml`.
5. Generate the statement draft from `.a11y/open-issues.yml`.
6. Human/legal owner reviews the final public wording.

## Status values

Use these values for checklist items:

- `not_tested`: not reviewed yet.
- `pass`: reviewed and no issue found.
- `fail`: confirmed issue.
- `not_applicable`: criterion does not apply to the page/content.
- `cannot_determine`: reviewer cannot decide; expert review needed.
- `needs_expert_review`: requires specialist judgement, for example captions/audio description or legal scope.

## Statement categories

Use these values for issue/exception statement mapping:

- `non_conformance`: a known accessibility failure.
- `disproportionate_burden`: documented exception; requires careful legal review.
- `outside_scope`: content/functionality is outside the relevant legal scope.
- `third_party_content`: third-party content not controlled by the organisation.
- `archived_content`: archived content not updated after the relevant date/scope.
- `accessible_alternative_available`: an alternative is available.
- `legacy_non_conformance`: legacy WCAG 2.0/2.1-only issue, such as 4.1.1 Parsing.

## Minimum issue fields

```yaml
id: "A11Y-001"
title: "Short human-readable issue title"
wcag:
  id: "2.4.7"
  title: "Focus Visible"
  level: "AA"
affected:
  pages:
    - "https://www.example.at/"
  selectors:
    - ".main-nav a:nth-child(3)"
  typo3:
    components:
      - "navigation.main"
    templates:
      - "EXT:sitepackage/Resources/Private/Partials/Navigation/Main.html"
evidence:
  actual: "Keyboard focus is not visible on the third navigation item."
  expected: "Keyboard focus is visible on every focusable component."
impact:
  severity: "serious"
  userImpact: "Keyboard users can lose their position."
statement:
  includeInAccessibilityStatement: true
  category: "non_conformance"
  publicText: "Bei einzelnen Navigationselementen ist der Tastaturfokus noch nicht ausreichend sichtbar."
status: "open"
```

## Do not publish claims from automation alone

Axe/Playwright/Deque findings are evidence. They do not by themselves prove full WCAG 2.2 AA conformance. Manual checks remain necessary for semantic quality, keyboard logic, media alternatives, legal exceptions, and the final statement wording.
