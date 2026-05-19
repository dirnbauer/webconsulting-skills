# 19. Security

Continues `typo3-records-list-types` from [full guide](full-guide.md).

## 19. Security

- **SQL Injection Prevention**: All queries use TYPO3's QueryBuilder with parameterized named parameters
- **CSRF Protection**: AJAX endpoints use TYPO3's built-in token handling
- **Access Control**: Full integration with TYPO3's backend user permissions and workspace restrictions
- **Input Validation**: View mode, table names, UIDs, and sort parameters validated and sanitized
- **XSS Prevention**: Fluid templates with proper escaping; no raw HTML output of user data
