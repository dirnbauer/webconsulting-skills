# Germany accessibility legal notes

This is project guidance, not legal advice. Germany has different contexts for federal public-sector bodies, state/municipal public-sector bodies and private-sector products/services. Always verify the exact legal basis and competent enforcement body before publishing a statement.

## Public-sector websites/apps: BGG + BITV 2.0

For federal public-sector projects, the usual profile is BGG + BITV 2.0. For state or municipal bodies, verify the relevant Landesrecht and the responsible monitoring/enforcement body.

Typical statement sections:

- scope of the statement;
- status of compliance with BGG/BITV 2.0 and the technical standard used;
- non-accessible content;
- reasons/exceptions, including incompatibility or disproportionate burden where legally reviewed;
- preparation/review method and date;
- feedback mechanism/contact;
- enforcement or arbitration procedure, often Schlichtungsstelle or the relevant state body.

Config profile:

```yaml
legal:
  profile: "de-public-bgg-bitv"
  jurisdiction: "DE"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
statement:
  enforcementBody: "Schlichtungsstelle BGG oder zuständige Landesstelle"
```

Suggested non-final statement intro:

> [Organisation] ist bemüht, diese Website im Einklang mit den Bestimmungen des Behindertengleichstellungsgesetzes (BGG) und der Barrierefreie-Informationstechnik-Verordnung (BITV 2.0) barrierefrei zugänglich zu machen.

## Private-sector products/services: BFSG / EAA

Use this profile only when the product or service is actually in BFSG scope. Do not classify every information-only brochure website as BFSG-relevant without review.

Typical covered website cases may arise when the website is part of a covered service such as e-commerce, banking, passenger transport, e-books or certain electronic communications/customer interaction flows. Always verify exemptions and transitions.

Config profile:

```yaml
legal:
  profile: "de-private-bfsg"
  jurisdiction: "DE"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
statement:
  enforcementBody: "zuständige Marktüberwachungsbehörde / nach Projekt prüfen"
```

Suggested non-final statement intro:

> Für die von dieser Website bereitgestellten Produkte oder Dienstleistungen werden Barrierefreiheitsanforderungen nach dem Barrierefreiheitsstärkungsgesetz (BFSG) geprüft, soweit sie in den gesetzlichen Anwendungsbereich fallen.

## Germany-specific HITL questions

- Is the organisation federal, state/municipal, private, or mixed?
- Is the website/app itself in scope, or only a specific service flow?
- Which state-level law or enforcement body applies if not federal?
- Is a feedback mechanism available from the statement page?
- Is the statement reachable from every page, usually via footer?
- Are German Sign Language and Easy Language requirements relevant for the specific public-sector context?

## Useful official references

- https://www.bundesfachstelle-barrierefreiheit.de/DE/Fachwissen/Informationstechnik/EU-Webseitenrichtlinie/BGG-und-BITV-2-0/bgg-und-bitv_node
- https://www.bfit-bund.de/DE/Downloads/downloads
- https://www.bmas.de/DE/Service/Gesetze-und-Gesetzesvorhaben/barrierefreiheitsstaerkungsgesetz.html
- https://www.barrierefreiheit-dienstekonsolidierung.bund.de/Webs/PB/DE/gesetze-und-richtlinien/barrierefreiheitsstaerkungsgesetz/barrierefreiheitsstaerkungsgesetz-node.html
