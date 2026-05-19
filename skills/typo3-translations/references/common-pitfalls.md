# Common Pitfalls

Continues `typo3-translations` from [full guide](full-guide.md).

## Common Pitfalls

| Symptom | Likely Cause | First Fix |
|---------|--------------|-----------|
| Raw `LLL:EXT:` appears | Wrong path, filename, extension key, or unit ID | Copy the exact installed path, parse XML, flush caches |
| English fallback appears | Missing or wrongly named target file | Place `de.*.xlf` beside the source and set `trgLang="de"` |
| German target is ignored | Target segment is unapproved | Use `state="reviewed"` or `state="final"` |
| ICU plural stays literal | Fetched with `sL()` or positional arguments | Use `translate()` or Fluid named arguments |
| Domain resolves wrong file | Filename conflict or stale cache | Rename conflicting files and clear `cache.l10n` |
| Content Blocks inline label is ignored | `labels.xlf` takes precedence | Edit or regenerate the block language file |
| XLIFF 2.0 breaks TYPO3 13 | XLIFF 2.0 is a TYPO3 14 feature | Keep shared branches on XLIFF 1.2 |
| Translation domain breaks | Domain syntax used in TYPO3 13-compatible code | Use full `LLL:EXT:` until v14-only |
