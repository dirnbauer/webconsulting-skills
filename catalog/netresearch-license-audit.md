# Netresearch License Audit

Audit date: 2026-03-22

Scope: the 11 skills documented in this repository as adapted from Netresearch.

## Result

Current evidence supports the existing split-license attribution pattern for these upstream repositories:

- Code: MIT
- Content: CC-BY-SA-4.0

I did not find evidence in the checked upstream repository pages that these 11 repositories are GPL-2 licensed.

## Repository Checks

- `php-modernization`
  Upstream: https://github.com/netresearch/php-modernization-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`, and the repo is labeled `MIT license`.

- `enterprise-readiness`
  Upstream: https://github.com/netresearch/enterprise-readiness-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`; README license section says code is MIT and content is CC-BY-SA-4.0.

- `security-audit`
  Upstream: https://github.com/netresearch/security-audit-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`, and the repo is labeled `MIT license`.

- `cli-tools`
  Upstream: https://github.com/netresearch/cli-tools-skill
  Evidence: GitHub repository page shows `LICENSE-MIT`; repo page is labeled `MIT license`.

- `context7`
  Upstream: https://github.com/netresearch/context7-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`; README license section says code is MIT and content is CC-BY-SA-4.0.

- `typo3-ddev`
  Upstream: https://github.com/netresearch/typo3-ddev-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`, and the repo is labeled `MIT license`.

- `typo3-testing`
  Upstream: https://github.com/netresearch/typo3-testing-skill
  Evidence: README license section says code is MIT and content is CC-BY-SA-4.0. GitHub sidebar currently reports `Unknown, MIT licenses found`, which appears to be metadata ambiguity caused by multiple top-level license files rather than evidence of GPL.

- `typo3-conformance`
  Upstream: https://github.com/netresearch/typo3-conformance-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`; README license section says code is MIT and content is CC-BY-SA-4.0.

- `typo3-docs`
  Upstream: https://github.com/netresearch/typo3-docs-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`; README license section says code is MIT and content is CC-BY-SA-4.0.

- `typo3-core-contributions`
  Upstream: https://github.com/netresearch/typo3-core-contributions-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`; README license section says code is MIT and content is CC-BY-SA-4.0.

- `typo3-extension-upgrade`
  Upstream: https://github.com/netresearch/typo3-extension-upgrade-skill
  Evidence: GitHub repository page shows `LICENSE-MIT` and `LICENSE-CC-BY-SA-4.0`; README license section says code is MIT and content is CC-BY-SA-4.0.

## Residual Risk

- This audit checked the current public GitHub repository pages and visible license declarations, not the full git history of each upstream repository.
- `typo3-testing` has a GitHub sidebar ambiguity (`Unknown, MIT licenses found`) despite an explicit split-license section in the README. That should be treated as a metadata quirk, but if you want zero ambiguity, the next step is a file-level audit of the upstream `LICENSE`, `LICENSE-MIT`, and `LICENSE-CC-BY-SA-4.0` contents for all 11 repos.
