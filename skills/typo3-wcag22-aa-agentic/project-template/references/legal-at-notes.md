# Austria accessibility legal notes

This is project guidance, not legal advice. Always verify the exact legal basis, competent body and wording before publishing a statement.

## Public-sector websites/apps

For Austrian federal public-sector websites/apps, use a WZG-oriented accessibility statement structure. For state, municipality or public-law bodies, verify the applicable state-level procedure and enforcement body.

Typical statement sections:

- scope of the statement;
- status of compliance;
- non-accessible content;
- reasons/exceptions;
- preparation method and date;
- feedback/contact;
- enforcement procedure;
- regular review/update, usually at least annually or after substantial changes.

Config profile:

```yaml
legal:
  profile: "at-public-wzg"
  jurisdiction: "AT"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
```

## Private-sector BaFG/EAA context

For private organisations, determine whether the service falls under the Austrian Barrierefreiheitsgesetz / European Accessibility Act scope. Do not automatically publish a WZG-style statement unless appropriate. Still, the same structured issue list and WCAG evidence are useful.

Config profile:

```yaml
legal:
  profile: "at-private-bafg"
  jurisdiction: "AT"
  targetStandard: "WCAG 2.2 AA"
  enStandard: "EN 301 549"
```

## Draft wording principle

Describe issues in user language, not only technical WCAG terms.

Better:

> Bei einigen älteren PDF-Dokumenten ist die Lesereihenfolge nicht korrekt ausgezeichnet. Dadurch können Screenreader die Inhalte nicht zuverlässig in der richtigen Reihenfolge vorlesen.

Worse:

> PDF/UA tagging missing, WCAG 1.3.1 failed.

## Useful official references

- https://www.digitalbarrierefrei.at/de/umsetzen/barrierefreiheitserklaerung/mustererklaerung-deutsch
- https://www.ffg.at/en/digital-accessibility/facts/model-accessibility-statement
- https://www.sozialministerium.gv.at/Themen/Soziales/Menschen-mit-Behinderungen/Barrierefreiheitsgesetz.html
