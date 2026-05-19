# Updating TYPO3 13 To TYPO3 14

Continues `typo3-translations` from [full guide](full-guide.md).

## Updating TYPO3 13 To TYPO3 14

Use this translation-specific checklist during a TYPO3 13-to-14 upgrade:

1. Keep XLIFF 1.2 and `LLL:EXT:` references while the same branch must support
   both TYPO3 13 and 14.
2. Run Rector/Fractor and the project upgrade checklist from `typo3-update`.
3. Inventory all `.xlf` files and note their versions, language prefixes, and
   consumers.
4. Fix invalid XML and duplicate IDs before format conversion.
5. Replace hardcoded labels with `LLL:EXT:` or domain references.
6. Convert label families from XLIFF 1.2 to XLIFF 2.0 only in a v14-only branch.
7. Keep `LLL:EXT:` references unless a domain migration is explicitly
   part of the task.
8. Add ICU only in v14-only runtime code; do not rewrite plain labels into ICU
   strings.
9. Validate source/target parity for every locale.
10. Flush caches, run backend smoke tests, and verify frontend locale rendering.
