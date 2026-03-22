# TYPO3 Security v14 Notes

### MFA Failed Verification Notifications **[v14 only]**

Backend users are now **notified on failed MFA verification attempts** (#105783). This provides early warning of potential brute-force attacks against MFA-protected accounts.

### Install Tool Password via CLI **[v14 only]**

New CLI command `install:password:set` (#104058) allows setting the Install Tool password without web access. Useful for automated deployments:

```bash
vendor/bin/typo3 install:password:set
```

### Redis-Based Install Tool Sessions **[v14 only]**

Install Tool sessions can now be stored in **Redis** (#101059) instead of the filesystem. This enables Install Tool access in multi-server / shared-nothing deployments without shared filesystems.

### Modal Migration **[v14 only]**

Backend modals migrated from **Bootstrap Modal to native `<dialog>`** element (#107443). Custom backend JavaScript using Bootstrap Modal API must be updated.

## Related Skills

- [security-incident-reporting/TYPO3](../security-incident-reporting/SKILL-TYPO3.md) - TYPO3 forensics, vulnerability classification, Security Team communication with PGP templates
- [security-audit](../security-audit/SKILL.md) - General security audit patterns, OWASP, CVSS scoring
