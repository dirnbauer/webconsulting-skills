---
id: fluid-strict-viewhelper-args
title: "Declare every ViewHelper argument; Fluid v5 rejects undeclared ones"
category: fluid
severity: error
appliesTo: ["**/Classes/**/ViewHelpers/**/*.php", "**/Resources/Private/**/*.html"]
typo3: ">=14.0"
php: ">=8.2"
trigger: "Use when writing a ViewHelper or passing arguments to one in a template."
---
# Declare every ViewHelper argument; Fluid v5 rejects undeclared ones

TYPO3 v14 ships Fluid v5, which is strict about arguments: passing an argument a
ViewHelper did not register throws `UndeclaredArgumentException`. Register every
argument in `initializeArguments()` via `registerArgument()`; pass only declared
arguments from templates.

**Do:** declare each argument with `registerArgument(name, type, description, required, default)`.
**Don't:** rely on `handleAdditionalArguments`/`additionalArguments`, or pass ad-hoc attributes a ViewHelper never declared.

```php
final class GreetingViewHelper extends AbstractViewHelper
{
    public function initializeArguments(): void
    {
        $this->registerArgument('name', 'string', 'Person to greet', true);
        $this->registerArgument('polite', 'bool', 'Add a salutation', false, false);
    }

    public function render(): string
    {
        return ($this->arguments['polite'] ? 'Dear ' : '') . $this->arguments['name'];
    }
}
```

```html
<webcon:greeting name="{user.name}" polite="1" />
```

> Why: Fluid v5 `AbstractViewHelper::validateAdditionalArguments()` throws
> `UndeclaredArgumentException` for any non-registered argument (verified in
> typo3fluid/fluid 5.x); the old lax-argument behavior is gone.
