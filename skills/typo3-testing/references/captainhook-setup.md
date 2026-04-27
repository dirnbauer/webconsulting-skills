# CaptainHook Setup for TYPO3 Extensions

CaptainHook is the standard git hook framework for TYPO3/PHP projects.
It auto-installs via a Composer plugin on `composer install`.

## Netresearch Default: `Build/captainhook.json`

Keep testing/CI config under `Build/` so the repo root stays focused on
end-user files (README, LICENSE, composer.json, ext_emconf.php).
`captainhook/hook-installer` reads the config path from composer.json, so
`Build/captainhook.json` is a fully supported, equivalent location.

## How It Works

1. `Build/captainhook.json` defines hooks (pre-commit, commit-msg, pre-push).
2. `composer.json` declares the path via `extra.captainhook.config`:

   ```json
   {
     "config": {
       "allow-plugins": {
         "captainhook/hook-installer": true
       }
     },
     "extra": {
       "captainhook": {
         "config": "Build/captainhook.json"
       }
     }
   }
   ```

3. `captainhook/hook-installer` (transitive via `captainhook/captainhook` or
   `netresearch/typo3-ci-workflows`) auto-installs hooks on every
   `composer install`, reading the Build/ path automatically.
4. Hooks run standard CI commands locally before commit/push.

## Typical Build/captainhook.json for TYPO3

```json
{
  "pre-commit": {
    "actions": [
      {"action": "composer ci:test:php:cgl"},
      {"action": "composer ci:test:php:phpstan"}
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
      {"action": "composer ci:test:php:unit"}
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

## Migrating from root `captainhook.json`

```bash
git mv captainhook.json Build/captainhook.json
# then add to composer.json:
#   "extra": {"captainhook": {"config": "Build/captainhook.json"}}
composer install   # reinstalls hooks from the new path
```

## Troubleshooting

- If hooks don't install: `vendor/bin/captainhook install --force --configuration=Build/captainhook.json`
- Git worktrees: create the hooks dir first: `mkdir -p $(git rev-parse --git-dir)/hooks`
- See `typo3-ci-workflows` README for the worktree workaround.
