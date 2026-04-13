# CaptainHook Setup for TYPO3 Extensions

CaptainHook is the standard git hook framework for TYPO3/PHP projects.
It auto-installs via Composer plugin on `composer install`.

## How It Works

1. `captainhook.json` in project root defines hooks
2. `captainhook/plugin-composer` auto-installs hooks on `composer install`
3. Hooks run standard CI commands locally before commit/push

## Typical captainhook.json for TYPO3

```json
{
  "pre-commit": {
    "actions": [
      {
        "action": "composer ci:test:php:cgl"
      },
      {
        "action": "composer ci:test:php:phpstan"
      }
    ]
  },
  "commit-msg": {
    "actions": [
      {
        "action": "\\CaptainHook\\App\\Hook\\Message\\Action\\Rules",
        "options": {
          "rules": ["\\CaptainHook\\App\\Hook\\Message\\Rule\\MsgNotEmpty"]
        }
      }
    ]
  },
  "pre-push": {
    "actions": [
      {
        "action": "composer ci:test:php:unit"
      }
    ]
  }
}
```

## Setup

```bash
# CaptainHook installs automatically with Composer
composer install

# Verify hooks are installed
ls -la .git/hooks/pre-commit
```

## Troubleshooting

- If hooks don't install: `vendor/bin/captainhook install --force`
- Git worktrees: create hooks dir first: `mkdir -p $(git rev-parse --git-dir)/hooks`
- See typo3-ci-workflows README for the worktree fix
