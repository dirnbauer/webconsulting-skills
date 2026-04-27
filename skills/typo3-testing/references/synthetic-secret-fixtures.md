# Synthetic Secret Fixtures in Tests

When writing fuzz or detection tests that must contain fake secrets (to prove the
detector recognises them), two independent systems will refuse to let you commit
obvious literals.

## The Two Blockers

### 1. GitHub Push Protection

GitHub scans pushed commits for known secret patterns. Literals like:

- `sk_live_...` (Stripe live key)
- `AKIA...` (AWS access key)
- `ghp_...` (GitHub personal access token)
- `SG....` (SendGrid API key)
- `xoxb-...` (Slack bot token)
- `AIza...` (Google API key)

…trigger a push block, even inside test files. The block cannot be bypassed with
a comment or annotation — only by never having the full literal in any committed
blob.

### 2. PHP-CS-Fixer `no_useless_concat_operator` Rule

Even if you try to split the literal with string concatenation:

```php
// Attempt — will be COLLAPSED by php-cs-fixer
$key = 'sk' . '_live_XYZ123';
```

The `no_useless_concat_operator` fixer detects that both operands are string
literals and merges them into `'sk_live_XYZ123'` on the next `composer cgl` run.
This restores the full literal, re-triggering GitHub's push protection.

## Correct Pattern: Use `implode()` or a Closure

Function calls **cannot** be collapsed by `no_useless_concat_operator` because the
fixer only operates on compile-time constants.

### Option A — `implode()` directly

```php
// Stripe-style live key fixture
$stripeKey = implode('', ['sk', '_live_', 'XXXXXXXXXXXXXXXXXXXXXXXX']);

// AWS access key fixture
$awsKey = implode('', ['AKIA', 'IOSFODNN7EXAMPLE']);

// GitHub PAT fixture
$ghpToken = implode('', ['ghp', '_', 'abcdefgh1234567890abcdefgh1234567890']);
```

`implode('', [...])` is semantically equivalent to concatenation but is a runtime
call — the fixer leaves it alone, and GitHub sees only array literals, not a full
key pattern.

### Option B — Helper Closure (preferred for many fixtures)

```php
// Define in setUp(), or extract to a private static function make(...), or use a top-level helper function
$make = static fn(string ...$parts): string => implode('', $parts);

// Usage in tests
$stripeKey  = $make('sk', '_live_', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX');
$awsKey     = $make('AKIA', 'IOSFODNN7', 'EXAMPLE');
$slackToken = $make('xoxb', '-', '123456789012', '-', 'AbCdEfGhIjKlMnOpQrStUvWx');
```

The closure approach is cleaner when a test class contains many synthetic secrets.

### Option C — Use Clearly Fake Prefixes That Don't Match Real Patterns

For detectors that test on _format_ rather than _content_, substitute prefix
characters so the literal never matches the real pattern:

```php
// Replace prefix characters so the literal never matches the real pattern.
// Real pattern: sk_live_[a-zA-Z0-9]{24}
// Fake live key: use a clearly-fake prefix that doesn't match the scanner regex
$stripeFakeKey = 'XX_live_XXXXXXXXXXXXXXXXXXXXXXXX';

// Real AWS: AKIA[0-9A-Z]{16}
// Fake: Use ZZIA prefix — not a valid AWS key ID prefix
$fakeAwsKey = 'ZZIAIOSFODNN7EXAMPLE';
```

Only use this approach when your detector tests format/entropy, not specific prefixes.

## Summary

| Technique | Safe from push-protection | Safe from no_useless_concat |
|---|---|---|
| `'sk' . '_live_X'` | No | No (fixer collapses it) |
| `implode('', ['sk', '_live_', 'X'])` | Yes | Yes |
| `$make('sk', '_live_', 'X')` (closure) | Yes | Yes |
| Clearly fake prefix (e.g. `ZZIA...`) | Yes | Yes |
| `str_split` + `implode` gymnastics | Yes (but ugly) | Yes |

Always use `implode()` or a closure factory as the default approach. Document in
the test file that the fragmentation is intentional:

```php
// Fragmented via implode() to avoid GitHub push-protection on fake secret
// literals and php-cs-fixer's no_useless_concat_operator rule.
$fixture = implode('', ['sk', '_live_', 'XXXXXXXXXXXXXXXXXXXXXXXX']);
```
