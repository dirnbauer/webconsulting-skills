# Switzerland accessibility legal notes

This is project guidance, not legal advice. Switzerland is not an EU member state, so do not automatically apply EU WZG/BITV/BFSG terminology. Use the Swiss public-sector profile when the project is for federal administration or another Swiss public/public-service context that follows eCH-0059.

## Public-sector / federal administration: BehiG, BehiV, eCH-0059

The Swiss federal administration references BehiG/BehiV and the eCH-0059 Accessibility Standard. eCH-0059 version 3 is based on WCAG 2.1 AA. The skill may still test WCAG 2.2 AA as a stricter internal target, but the statement should accurately name the legal/profile baseline.

Typical statement sections:

- scope of the statement;
- compliance status;
- exceptions / non-accessible content;
- alternatives if available;
- creation and last review date;
- contact for accessibility feedback;
- escalation/enforcement contact if applicable to the project.

Config profile:

```yaml
legal:
  profile: "ch-public-behig-ech0059"
  jurisdiction: "CH"
  targetStandard: "WCAG 2.2 AA" # internal higher target
  enStandard: "eCH-0059 v3 / WCAG 2.1 AA legal baseline; EN 301 549 only if contractually required"
statement:
  enforcementBody: "zuständige Schweizer Stelle nach Projekt prüfen"
```

Suggested non-final statement intro:

> [Organisation] ist bemüht, ihre digitalen Informationen und Dienstleistungen barrierefrei zugänglich zu machen. Grundlage der Prüfung sind die für das Projekt anwendbaren Schweizer Vorgaben, insbesondere BehiG/BehiV und der eCH-0059 Accessibility Standard, soweit einschlägig.

## Private-sector Switzerland

For private-sector Swiss projects, do not automatically claim a formal statutory web accessibility statement obligation unless the project has a specific legal, contractual or sector obligation. Use `voluntary-wcag22aa` or a client-specific profile when the goal is best-practice/contractual WCAG conformance.

Config profile:

```yaml
legal:
  profile: "voluntary-wcag22aa"
  jurisdiction: "CH"
  targetStandard: "WCAG 2.2 AA"
```

## Switzerland-specific HITL questions

- Is the project federal administration, canton/municipality, concessioned/public-service, private or mixed?
- Does the client require eCH-0059 specifically?
- Is WCAG 2.2 AA a stricter internal target while the legal baseline references WCAG 2.1 AA?
- Which contact/escalation body should be named?
- Are German, French, Italian or English statement variants required?

## Useful official references

- https://www.bit.admin.ch/en/accessibility-in-the-federal-administration
- https://www.ech.ch/de/ech/ech-0059/3.0
- https://www.fedlex.admin.ch/eli/cc/2003/667/de
- https://www.fedlex.admin.ch/eli/cc/2003/668/de
