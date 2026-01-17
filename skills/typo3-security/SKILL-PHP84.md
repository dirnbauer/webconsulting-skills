---
name: typo3-security-php84
description: PHP 8.4 security considerations for TYPO3. New security features and potential vulnerabilities.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-security
  - php-modernization
triggers:
  - security php 8.4
  - php84 security
---

# TYPO3 Security with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x
> 
> **Related Skills:**
> - [typo3-security](./SKILL.md) - Main security guide
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. PHP 8.4 Security Benefits

### Asymmetric Visibility for Encapsulation

```php
<?php

declare(strict_types=1);

// Prevent external modification of sensitive data
final class UserSession
{
    public private(set) string $sessionId;
    public private(set) \DateTimeImmutable $createdAt;
    public private(set) bool $authenticated = false;

    public function authenticate(string $token): void
    {
        if ($this->validateToken($token)) {
            $this->authenticated = true;
        }
    }
}

// External code cannot bypass authentication
$session = new UserSession();
$session->authenticated = true; // ❌ Error!
```

### Property Hooks for Input Validation

```php
<?php

declare(strict_types=1);

final class ApiRequest
{
    public string $endpoint {
        set (string $value) {
            // Validate and sanitize on assignment
            if (!str_starts_with($value, '/api/')) {
                throw new \InvalidArgumentException('Invalid API endpoint');
            }
            $this->endpoint = $value;
        }
    }

    public array $parameters {
        set (array $value) {
            // Sanitize all parameters
            $this->parameters = array_map(
                fn($v) => is_string($v) ? htmlspecialchars($v, ENT_QUOTES) : $v,
                $value
            );
        }
    }
}
```

---

## 2. Security Patterns with New Features

### Readonly for Immutable Security Objects

```php
<?php

declare(strict_types=1);

final readonly class SecurityContext
{
    public function __construct(
        public string $userId,
        public array $permissions,
        public \DateTimeImmutable $validUntil,
    ) {}

    public function hasPermission(string $permission): bool
    {
        return in_array($permission, $this->permissions, true);
    }
}
```

### Using array_all() for Permission Checks

```php
<?php

declare(strict_types=1);

final class PermissionChecker
{
    /**
     * @param string[] $requiredPermissions
     * @param string[] $userPermissions
     */
    public function hasAllPermissions(
        array $requiredPermissions,
        array $userPermissions
    ): bool {
        // PHP 8.4: Check all required permissions exist
        return array_all(
            $requiredPermissions,
            fn(string $perm) => in_array($perm, $userPermissions, true)
        );
    }

    /**
     * @param string[] $dangerousFlags
     */
    public function hasAnyDangerousFlag(array $userFlags, array $dangerousFlags): bool
    {
        return array_any(
            $userFlags,
            fn(string $flag) => in_array($flag, $dangerousFlags, true)
        );
    }
}
```

---

## 3. Deprecation Awareness

### Mark Insecure Methods

```php
<?php

declare(strict_types=1);

final class AuthService
{
    #[\Deprecated(
        message: 'Use authenticateWithMFA() for secure authentication',
        since: '2.0.0'
    )]
    public function authenticateBasic(string $user, string $pass): bool
    {
        trigger_error(
            'authenticateBasic() is deprecated. Use MFA.',
            E_USER_DEPRECATED
        );
        return $this->authenticateWithMFA($user, $pass, '');
    }

    public function authenticateWithMFA(
        string $user,
        string $pass,
        string $mfaToken
    ): bool {
        // Secure implementation
    }
}
```

---

## 4. Security Checklist for PHP 8.4

- [ ] Use asymmetric visibility for sensitive properties
- [ ] Implement validation in property hooks
- [ ] Use `readonly` for immutable security contexts
- [ ] Mark legacy auth methods with `#[\Deprecated]`
- [ ] Update password hashing if needed
- [ ] Review session handling for PHP 8.4 changes

---

## References

- [typo3-security SKILL.md](./SKILL.md)
- [php-modernization SKILL-PHP84](../php-modernization/SKILL-PHP84.md)
- [PHP 8.4 Release Notes](https://www.php.net/releases/8.4/)

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
