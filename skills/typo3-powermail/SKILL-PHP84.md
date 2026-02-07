---
name: typo3-powermail-php84
description: PHP 8.4 patterns for TYPO3 Powermail and powermail_cond development. Property hooks for finishers, validators, and condition DTOs. Asymmetric visibility for mail results. New array functions for answer processing.
version: 1.0.0
php_compatibility: "8.4+"
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-powermail
  - php-modernization
triggers:
  - powermail php 8.4
  - powermail property hooks
  - powermail typed
  - powermail_cond php 8.4
---

# Powermail with PHP 8.4

> **Compatibility:** PHP 8.4+, TYPO3 v13.x and v14.x, Powermail 13.x
> 
> **Related Skills:** 
> - [typo3-powermail](./SKILL.md) - Main Powermail guide
> - [typo3-powermail CONDITIONS](./SKILL-CONDITIONS.md) - Conditional fields
> - [php-modernization/SKILL-PHP84](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features

---

## 1. Property Hooks for Finisher Configuration

### Typed Finisher Config DTO

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Finisher;

final class CrmFinisherConfig
{
    public string $apiUrl {
        set (string $value) {
            if (!filter_var($value, FILTER_VALIDATE_URL)) {
                throw new \InvalidArgumentException('Invalid API URL: ' . $value);
            }
            $this->apiUrl = $value;
        }
    }

    public string $apiKey {
        set (string $value) {
            if (strlen($value) < 16) {
                throw new \InvalidArgumentException('API key too short');
            }
            $this->apiKey = $value;
        }
    }

    public int $timeout = 30;

    public bool $dryRun {
        get => $this->dryRun && ($GLOBALS['TYPO3_CONF_VARS']['SYS']['devIPmask'] !== '');
    }

    /** Virtual property: build from TypoScript config array */
    public static function fromTypoScript(array $config): self
    {
        $self = new self();
        $self->apiUrl = $config['apiUrl'] ?? throw new \RuntimeException('apiUrl required');
        $self->apiKey = $config['apiKey'] ?? throw new \RuntimeException('apiKey required');
        $self->timeout = (int)($config['timeout'] ?? 30);
        $self->dryRun = (bool)($config['dryRun'] ?? false);
        return $self;
    }
}
```

### Finisher Using Config DTO

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Finisher;

use In2code\Powermail\Finisher\AbstractFinisher;
use In2code\Powermail\Finisher\FinisherInterface;

final class CrmFinisher extends AbstractFinisher implements FinisherInterface
{
    public function crmSyncFinisher(): void
    {
        $config = CrmFinisherConfig::fromTypoScript($this->getConfiguration());
        $mail = $this->getMail();
        $answers = $mail->getAnswersByFieldMarker();

        $payload = new CrmPayload(
            email: (string)($answers['email']?->getValue() ?? ''),
            name: (string)($answers['name']?->getValue() ?? ''),
            company: (string)($answers['company']?->getValue() ?? ''),
        );

        if ($config->dryRun) {
            return;
        }

        // Send to CRM...
    }
}
```

---

## 2. Asymmetric Visibility for Mail Processing Results

### Submission Result Object

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Domain;

use In2code\Powermail\Domain\Model\Mail;

final class SubmissionResult
{
    public private(set) bool $success = true;
    public private(set) ?int $mailUid = null;
    public private(set) ?string $redirectUrl = null;

    /** @var array<string, mixed> */
    public private(set) array $finisherResults = [];

    /** @var array<string> */
    public private(set) array $errors = [];

    public function markSuccess(Mail $mail): void
    {
        $this->mailUid = $mail->getUid();
    }

    public function addFinisherResult(string $finisher, mixed $result): void
    {
        $this->finisherResults[$finisher] = $result;
    }

    public function addError(string $error): void
    {
        $this->errors[] = $error;
        $this->success = false;
    }

    public function setRedirect(string $url): void
    {
        $this->redirectUrl = $url;
    }
}

// Usage in event listener
$result = new SubmissionResult();
$result->markSuccess($mail);
$result->addFinisherResult('crm', ['id' => 12345]);

echo $result->success;           // ✅ readable
echo $result->mailUid;           // ✅ readable
$result->success = false;        // ❌ Error: cannot modify
```

### Validated Contact DTO

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Domain;

final class ContactData
{
    public private(set) string $email;
    public private(set) string $firstName;
    public private(set) string $lastName;
    public private(set) ?string $phone = null;

    public string $fullName {
        get => trim($this->firstName . ' ' . $this->lastName);
    }

    public function __construct(string $email, string $firstName, string $lastName)
    {
        $this->email = strtolower(trim($email));
        $this->firstName = trim($firstName);
        $this->lastName = trim($lastName);
    }

    /** Build from powermail Mail answers */
    public static function fromMail(\In2code\Powermail\Domain\Model\Mail $mail): self
    {
        $answers = $mail->getAnswersByFieldMarker();
        $self = new self(
            email: (string)($answers['email']?->getValue() ?? ''),
            firstName: (string)($answers['firstname']?->getValue() ?? ''),
            lastName: (string)($answers['lastname']?->getValue() ?? ''),
        );
        $self->phone = $answers['phone']?->getValue() !== null
            ? (string)$answers['phone']->getValue()
            : null;
        return $self;
    }
}
```

---

## 3. New Array Functions for Answer Processing

### Filtering and Finding Answers

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Service;

use In2code\Powermail\Domain\Model\Answer;
use In2code\Powermail\Domain\Model\Mail;

final readonly class AnswerAnalyzer
{
    /**
     * Find first answer matching a field type
     */
    public function findFirstUpload(Mail $mail): ?Answer
    {
        $answers = $mail->getAnswers()->toArray();
        return array_find(
            $answers,
            fn(Answer $a) => $a->getValueType() === Answer::VALUE_TYPE_UPLOAD
        );
    }

    /**
     * Check if any required field is empty
     */
    public function hasEmptyRequiredFields(Mail $mail, array $requiredMarkers): bool
    {
        $answers = $mail->getAnswersByFieldMarker();
        return array_any(
            $requiredMarkers,
            fn(string $marker) => !isset($answers[$marker])
                || $answers[$marker]->getValue() === ''
                || $answers[$marker]->getValue() === null
        );
    }

    /**
     * Check if all answers are non-empty
     */
    public function allFieldsFilled(Mail $mail): bool
    {
        $answers = $mail->getAnswers()->toArray();
        return array_all(
            $answers,
            fn(Answer $a) => $a->getValue() !== '' && $a->getValue() !== null
        );
    }

    /**
     * Find first answer with suspicious content (spam check)
     */
    public function findSuspiciousAnswer(Mail $mail): ?Answer
    {
        $answers = $mail->getAnswers()->toArray();
        return array_find(
            $answers,
            fn(Answer $a) => $a->getValueType() === Answer::VALUE_TYPE_TEXT
                && preg_match('/(viagra|casino|crypto)/i', (string)$a->getValue())
        );
    }

    /**
     * Find the answer key for a specific marker
     */
    public function findAnswerKey(Mail $mail, string $marker): ?int
    {
        $answers = $mail->getAnswers()->toArray();
        return array_find_key(
            $answers,
            fn(Answer $a) => $a->getField()?->getMarker() === $marker
        );
    }
}
```

### Validating Form Data

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Validator;

use In2code\Powermail\Domain\Model\Mail;

final readonly class FormDataValidator
{
    /**
     * Validate all email-type fields have valid format
     */
    public function validateEmails(Mail $mail): array
    {
        $answers = $mail->getAnswers()->toArray();

        $emailAnswers = array_filter(
            $answers,
            fn($a) => $a->getField()?->getType() === 'input'
                && $a->getField()?->getValidation() === 1 // email validation
        );

        $allValid = array_all(
            $emailAnswers,
            fn($a) => filter_var((string)$a->getValue(), FILTER_VALIDATE_EMAIL) !== false
        );

        if (!$allValid) {
            $invalid = array_find(
                $emailAnswers,
                fn($a) => !filter_var((string)$a->getValue(), FILTER_VALIDATE_EMAIL)
            );
            return ['valid' => false, 'field' => $invalid?->getField()?->getMarker()];
        }

        return ['valid' => true];
    }
}
```

---

## 4. Property Hooks for Custom Validators

### Typed Validation Rule

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Validation;

final class ValidationRule
{
    public string $fieldMarker {
        set (string $value) {
            if (!preg_match('/^[a-z][a-z0-9_]*$/', $value)) {
                throw new \InvalidArgumentException('Invalid marker: ' . $value);
            }
            $this->fieldMarker = $value;
        }
    }

    public string $pattern {
        set (string $value) {
            if (@preg_match($value, '') === false) {
                throw new \InvalidArgumentException('Invalid regex: ' . $value);
            }
            $this->pattern = $value;
        }
    }

    public string $errorMessage = 'Validation failed';

    public bool $isValid {
        get => fn(string $value) => (bool)preg_match($this->pattern, $value);
    }
}
```

### Event Listener with Typed Rules

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\EventListener;

use In2code\Powermail\Events\CustomValidatorEvent;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener('vendor-myext/typed-validator')]
final readonly class TypedValidatorListener
{
    /** @var array<ValidationRule> */
    private array $rules {
        get => [
            $this->createRule('iban', '/^[A-Z]{2}\d{2}[A-Z0-9]{4,}$/', 'Invalid IBAN'),
            $this->createRule('vat_id', '/^[A-Z]{2}\d{8,12}$/', 'Invalid VAT ID'),
            $this->createRule('zip_at', '/^\d{4}$/', 'Austrian ZIP: 4 digits'),
        ];
    }

    public function __invoke(CustomValidatorEvent $event): void
    {
        $field = $event->getField();
        $marker = $field->getMarker();

        $rule = array_find(
            $this->rules,
            fn(ValidationRule $r) => $r->fieldMarker === $marker
        );

        if ($rule === null) {
            return;
        }

        $answer = $this->findAnswer($event);
        if ($answer !== null && !preg_match($rule->pattern, (string)$answer->getValue())) {
            $event->setIsValid(false);
            $event->setValidationMessage($rule->errorMessage);
        }
    }

    private function createRule(string $marker, string $pattern, string $message): ValidationRule
    {
        $rule = new ValidationRule();
        $rule->fieldMarker = $marker;
        $rule->pattern = $pattern;
        $rule->errorMessage = $message;
        return $rule;
    }

    private function findAnswer(CustomValidatorEvent $event): ?\In2code\Powermail\Domain\Model\Answer
    {
        $mail = $event->getMail();
        $fieldUid = $event->getField()->getUid();
        $answers = $mail->getAnswers()->toArray();
        return array_find($answers, fn($a) => $a->getField()?->getUid() === $fieldUid);
    }
}
```

---

## 5. Powermail Conditions with PHP 8.4

### Typed Condition Result DTO

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Condition;

final class ConditionResult
{
    /** @var array<string, FieldAction> */
    public private(set) array $fieldActions = [];

    /** @var array<int, string> */
    public private(set) array $hiddenPages = [];

    public private(set) int $loopsUsed = 0;

    public function addFieldAction(string $marker, FieldAction $action): void
    {
        $this->fieldActions[$marker] = $action;
    }

    public function addHiddenPage(int $pageUid): void
    {
        $this->hiddenPages[] = $pageUid;
    }

    public function setLoops(int $loops): void
    {
        $this->loopsUsed = $loops;
    }

    public bool $hasHiddenFields {
        get => $this->fieldActions !== []
            && array_any(
                $this->fieldActions,
                fn(FieldAction $a) => $a->action === 'hide'
            );
    }

    public bool $hasHiddenPages {
        get => $this->hiddenPages !== [];
    }
}

enum FieldActionType: string
{
    case Hide = 'hide';
    case Unhide = 'un_hide';
}

final class FieldAction
{
    public function __construct(
        public private(set) string $marker,
        public private(set) FieldActionType $action,
        public private(set) int $conditionUid,
    ) {}
}
```

### Condition-Aware Form Service

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Service;

use In2code\Powermail\Domain\Model\Form;
use In2code\Powermail\Domain\Model\Mail;

final readonly class ConditionalFormService
{
    /**
     * Get only visible (non-hidden) answers from a conditional form
     */
    public function getVisibleAnswers(Mail $mail, array $hiddenMarkers): array
    {
        $answers = $mail->getAnswersByFieldMarker();

        // PHP 8.4: Filter out hidden field answers
        return array_filter(
            $answers,
            fn($answer, string $marker) => !array_any(
                $hiddenMarkers,
                fn(string $hidden) => $hidden === $marker
            ),
            ARRAY_FILTER_USE_BOTH
        );
    }

    /**
     * Check if all required visible fields are filled
     */
    public function validateVisibleFields(
        Mail $mail,
        array $requiredMarkers,
        array $hiddenMarkers
    ): bool {
        $visibleRequired = array_filter(
            $requiredMarkers,
            fn(string $m) => !in_array($m, $hiddenMarkers, true)
        );

        $answers = $mail->getAnswersByFieldMarker();

        return array_all(
            $visibleRequired,
            fn(string $marker) => isset($answers[$marker])
                && $answers[$marker]->getValue() !== ''
                && $answers[$marker]->getValue() !== null
        );
    }
}
```

---

## 6. #[\Deprecated] for Legacy Powermail Patterns

### Deprecating Old Signal/Slot Approaches

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Service;

use In2code\Powermail\Domain\Model\Mail;

final class MailProcessingService
{
    #[\Deprecated(
        message: 'Use PSR-14 ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent instead',
        since: '2.0.0'
    )]
    public function getReceiverEmailsFromSignal(Mail $mail): array
    {
        trigger_error(
            'getReceiverEmailsFromSignal() is deprecated, use PSR-14 event listener',
            E_USER_DEPRECATED
        );
        // Legacy implementation...
        return [];
    }

    #[\Deprecated(
        message: 'Use CrmFinisher with CrmFinisherConfig DTO instead',
        since: '2.0.0'
    )]
    public function sendToCrm(array $formData, string $apiUrl): bool
    {
        trigger_error(
            'sendToCrm() with array is deprecated, use typed CrmFinisher',
            E_USER_DEPRECATED
        );
        return false;
    }
}
```

---

## 7. Migration Checklist

### Upgrading Powermail Extension Code to PHP 8.4

- [ ] Replace finisher config arrays with typed Config DTOs using property hooks
- [ ] Add asymmetric visibility to result/response objects (`public private(set)`)
- [ ] Replace `foreach` answer loops with `array_find()`, `array_any()`, `array_all()`
- [ ] Use `array_find()` to locate answers by marker or field UID
- [ ] Use `array_any()` for spam/validation checks across answers
- [ ] Use `array_all()` to verify all required fields are filled
- [ ] Add `#[\Deprecated]` to legacy signal/slot or hook-based methods
- [ ] Use `readonly` classes for stateless services and event listeners
- [ ] Use enums for field action types (`FieldActionType::Hide`)
- [ ] Build ContactData/PayloadDTOs with `private(set)` and factory methods

### Powermail Conditions Specific

- [ ] Type condition results with `ConditionResult` DTO
- [ ] Use `array_any()` / `array_all()` for rule evaluation helpers
- [ ] Use `FieldActionType` enum instead of string `'hide'`/`'un_hide'`
- [ ] Filter visible answers with `array_filter()` + `array_any()`

---

## References

- [typo3-powermail SKILL.md](./SKILL.md) - Main Powermail guide
- [typo3-powermail SKILL-CONDITIONS.md](./SKILL-CONDITIONS.md) - Conditional fields
- [php-modernization SKILL-PHP84.md](../php-modernization/SKILL-PHP84.md) - PHP 8.4 features
- [Powermail GitHub](https://github.com/in2code-de/powermail) - Source code
- [powermail_cond GitHub](https://github.com/in2code-de/powermail_cond) - Conditions extension

---

## Credits & Attribution

This skill is part of the webconsulting.at TYPO3 skills collection.
