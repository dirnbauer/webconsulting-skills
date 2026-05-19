# What To Do If Something Fails

Continues `typo3-translations` from [full guide](full-guide.md).

## What To Do If Something Fails

Use this checklist before changing code paths:

1. Parse every changed `.xlf` file as XML.
2. Confirm the source file is unprefixed English and the target file is prefixed.
3. Confirm version-specific language attributes:
   `source-language` / `target-language` for XLIFF 1.2,
   `srcLang` / `trgLang` for XLIFF 2.0.
4. Confirm every referenced unit ID exists exactly once.
5. Confirm target files contain matching unit IDs and approved target segments.
6. Confirm the `LLL:EXT:` path uses the extension key, not the Composer package.
7. Clear TYPO3 caches, including localization/domain mapping caches.
8. If domains are used, verify the project is v14-only, run
   `language:domain:list`, and check filename conflicts.
9. If ICU does not interpolate, verify the project is v14.2+, named arguments
   are passed, and `translate()` is used.
10. If Content Blocks labels differ from YAML, inspect `labels.xlf` first.
11. Reproduce in the correct language context; backend user language and site
    language can differ.
12. Revert only the smallest recent translation change when isolating a failure.
