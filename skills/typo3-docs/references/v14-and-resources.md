# TYPO3 Docs References

## Resources

- **TYPO3 Documentation Guide**: https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/
- **guides.xml reference**: https://docs.typo3.org/permalink/h2document:guides-xml
- **Render Guides** (container + CLI source): https://github.com/TYPO3-Documentation/render-guides
- **Intercept**: https://intercept.typo3.com/

## v14-Only Documentation Changes

> The following documentation-related changes apply **exclusively to TYPO3 v14**.

### XLIFF 2.x Support **[v14 only]**

TYPO3 v14 supports **XLIFF 2.x** translation files ([Feature #107710](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-107710-SupportForXLIFF20TranslationFiles.html)) alongside the existing XLIFF 1.2 format. Document which XLIFF version your extension uses.

### Translation Domain Mapping **[v14 only]**

Translation domain mapping ([Feature #93334](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-93334-TranslationDomainMapping.html)) allows flexible XLIFF file resolution. Extensions can map translation domains to specific XLIFF files without following the convention-based path.

### TranslateViewHelper Domain Syntax **[v14 only]**

The `TranslateViewHelper` (`<f:translate>`) supports translation domain mapping ([Feature #107759](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-107759-TranslateViewHelperSupportsTranslationDomainSyntax.html)) for cross-extension translation references. `LLL:EXT:` itself is long-standing TYPO3 syntax.

### Symfony Translation Component **[v14 only]**

TYPO3's localization system now uses the **Symfony Translation Component** ([Feature #107436](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-107436-SymfonyTranslationIntegration.html)) internally. This affects how translation files are parsed and cached. Custom localization parser implementations are deprecated.

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-docs-skill

**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)
Adapted by webconsulting.at for this skill collection
