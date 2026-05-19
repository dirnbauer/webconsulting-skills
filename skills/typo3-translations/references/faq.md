# FAQ

Continues `typo3-translations` from [full guide](full-guide.md).

## FAQ

**Should I start with TYPO3 13 or TYPO3 14?**

Start with the TYPO3 13-compatible baseline when the extension must support both
13 and 14. Move selected label families to TYPO3 14 patterns only when the code
or branch is v14-only.

**Should I use XLIFF 2.0 or 1.2?**

Use XLIFF 1.2 for TYPO3 13+14 compatibility. Use XLIFF 2.0 for new v14-only
work.

**What is the latest XLIFF format to use here?**

For TYPO3 13 compatibility, use XLIFF 1.2. For TYPO3 14-only catalogs, use the
documented XLIFF 2.0 structure.

**Should I create `en.locallang.xlf`?**

No. The unprefixed file is the English source. Use prefixes only for target
languages.

**Are `LLL:EXT:` references deprecated?**

No. TYPO3 14 adds translation domains as a shorter option, but full file-based
references remain valid and useful.

**When should I use translation domains?**

Use them in PHP when shorter references improve readability. Use explicit
`LLL:EXT:` paths where configuration benefits from showing the exact file.

**Can I use ICU MessageFormat in XLIFF 2.0?**

Yes, in TYPO3 14.2+ only. For TYPO3 13-compatible code, keep classic
placeholders and runtime formatting.

**Why does `state="translated"` not show?**

TYPO3 loads approved localizations by default. Use `state="reviewed"` or
`state="final"` for reviewed target strings.

**Can one XLIFF file contain multiple target languages?**

No. Keep one target language per file.

**Are translation files for editorial content?**

No. XLIFF files are for UI labels and short runtime messages. Editorial content
belongs in TYPO3 records and site localization.
