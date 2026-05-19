# 15. Best Practices

Continues `typo3-content-blocks` from [full guide](full-guide.md).

## 15. Best Practices

### DO ✅

1. **Use Extbase-compatible table names** for Record Types:
   ```yaml
   table: tx_myextension_domain_model_myrecord
   ```

2. **Reuse existing fields** when possible:
   ```yaml
   - identifier: header
     useExistingField: true
   ```

3. **Group related fields** with Tabs and Palettes:
   ```yaml
   - identifier: settings_tab
     type: Tab
     label: Settings
   ```

4. **Use meaningful identifiers** (snake_case):
   ```yaml
   - identifier: hero_background_image
   ```

5. **Clear caches after changes**:
   ```bash
   ddev typo3 cache:flush -g system
   ddev typo3 extension:setup --extension=my_sitepackage
   ```

6. **Use labels.xlf** for all user-facing labels

### DON'T ❌

1. **Don't use raw SQL** - Content Blocks generates schema automatically

2. **Don't duplicate TCA** - Config.yaml is the single source of truth

3. **Don't use short table names** for Extbase integration:
   ```yaml
   # ❌ Wrong
   table: team_member
   
   # ✅ Correct
   table: tx_mysitepackage_domain_model_teammember
   ```

4. **Don't use dashes in identifiers**:
   ```yaml
   # ❌ Wrong
   identifier: hero-image
   
   # ✅ Correct
   identifier: hero_image
   ```

5. **Don't forget shareAcross options** when using foreign_table in multiple places
