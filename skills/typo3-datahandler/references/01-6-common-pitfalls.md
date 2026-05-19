# 6. Common Pitfalls

Continues `typo3-datahandler` from [full guide](full-guide.md).

## 6. Common Pitfalls

### Pitfall 1: Missing PID for New Records

```php
// ❌ WRONG - Missing pid
$data = ['tt_content' => ['NEW_1' => ['header' => 'Test']]];

// ✅ CORRECT - Always include pid
$data = ['tt_content' => ['NEW_1' => ['pid' => 1, 'header' => 'Test']]];
```

### Pitfall 2: Assuming String vs Integer UIDs Matter (Usually They Do Not)

DataHandler uses `MathUtility::canBeInterpretedAsInteger()` for many UID checks. A **numeric string** such as `'123'` is treated like `123` for typical existing-record keys.

```php
// Both are valid for UID 123 in common cases
$data = ['tt_content' => [123 => ['header' => 'Int key']]];
$data = ['tt_content' => ['123' => ['header' => 'String key']]];

// ✅ Prefer integer keys for clarity and static analysis
$data = ['tt_content' => [123 => ['header' => 'Recommended style']]];
```

**Still wrong:** using non-numeric strings as placeholders **without** the `NEW` prefix (e.g. arbitrary slugs instead of `NEW_1`). New records must use `NEW…` placeholders as shown in §2. **Edge case:** strings that are not valid integer strings per `MathUtility::canBeInterpretedAsInteger()` (e.g. some leading-zero forms) — use integers or plain digit strings.

### Pitfall 3: Forgetting process_datamap() / process_cmdmap()

```php
// ❌ WRONG - Nothing happens
$dataHandler->start($data, $cmd);

// ✅ CORRECT - Actually process the data
$dataHandler->start($data, $cmd);
$dataHandler->process_datamap();
$dataHandler->process_cmdmap();
```

### Pitfall 4: Ignoring Error Log

```php
// ❌ WRONG - Silently ignoring errors
$dataHandler->process_datamap();

// ✅ CORRECT - Check for errors
$dataHandler->process_datamap();
if (!empty($dataHandler->errorLog)) {
    // Handle errors appropriately
    throw new \RuntimeException(implode(', ', $dataHandler->errorLog));
}
```
