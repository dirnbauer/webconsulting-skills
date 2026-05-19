# v14-only Rector targets

Continues `typo3-rector` from [full guide](full-guide.md).

## v14-only Rector targets

> The following patterns are **v14-focused** migration targets. Prefer `Typo3LevelSetList::UP_TO_TYPO3_14`; apply remaining items manually if Rector skips them.

### New Rector Migration Targets **[v14 only]**

| Removed/Changed | Migration |
|-----------------|-----------|
| `TypoScriptFrontendController` | Use request attributes (`frontend.page.information`, `language`) |
| Extbase annotations (`@validate`, `@ignorevalidation`) | Use PHP attributes (`#[Validate]`, `#[IgnoreValidation]`) |
| `FlexFormService` class | Merged into `FlexFormTools` (#107945) |
| Various `BackendUtility` helpers (#106393) | Deprecated in v14, removal planned for v15 — migrate per changelog for each method |
| `MailMessage->send()` | Inject `TYPO3\CMS\Core\Mail\MailerInterface` and call `$this->mailer->send($email)` |
| `GeneralUtility::createVersionNumberedFilename()` | Use System Resource API |
| `PathUtility::getPublicResourceWebPath()` | Use System Resource API |
| `PathUtility::getRelativePath()` / `getRelativePathTo()` | Use new path resolution |
| `AbstractTypolinkBuilder->build()` | Use `TypolinkBuilderInterface` |
| `DataHandler->userid` / `->admin` / `->storeLogMessages` | Removed, no replacement |

### v14.0 Deprecation Targets (prepare for v15 removal)

| Deprecated | Migration |
|------------|-----------|
| `ButtonBar`/`Menu`/`MenuRegistry` `make*` methods (#107823) | Use `ComponentFactory` |
| Scheduler task registration via `SC_OPTIONS` (#98453) | Use TCA-based registration |
| `Localization parsers` (XliffParser, etc.) (#107436) | Symfony Translation Component |

### v14.2 Deprecation Targets (prepare for v15 removal)

| Deprecated | Migration |
|------------|-----------|
| `PageDoktypeRegistry` config methods | Migrate to TCA `allowedRecordTypes` |
| `PageRenderer->addInlineLanguageDomain()` (#108963) | Use alternative API |
| `ExtensionManagementUtility::addFieldsToUserSettings` (#108843) | Use TCA for user settings |
| `FormEngine "additionalHiddenFields"` key (#109102) | Removed in v15 |

---
