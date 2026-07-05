# Changelog

## 1.0.0

- Final clean repo-ready package for `github.com/dirnbauer/webconsulting-skills`.
- Keeps all v0.3.0 features in one skill folder under `skills/typo3-wcag22-aa-agentic/`.
- Standardizes skill, project template and Chrome extension versions.
- Adds a root install note for unzipping into the skill-extension repository root.

## 0.3.0

- Adds no-build Chrome Manifest V3 manual review helper for human-only WCAG checks.
- Adds full active WCAG 2.2 Level A + Level AA checkpoint base list: 55 active criteria plus legacy 4.1.1 Parsing note.
- Adds structured issue/exception schema and example `.a11y/open-issues.example.yml`.
- Adds `npm run a11y:manual:merge` to merge Chrome helper exports into `.a11y/open-issues.yml`.
- Updates report and statement generators to preserve manual issues and generate the statement from structured issues/exceptions.
- Updates local Codex prompt with manual review workflow and no-free-writing rule for the accessibility statement.

## 0.2.0

- Adds Germany legal examples: `de-public-bgg-bitv` and `de-private-bfsg`.
- Adds Switzerland legal examples: `ch-public-behig-ech0059`.
- Keeps Austria profiles: `at-public-wzg` and `at-private-bafg`.
- Adds cross-jurisdiction legal framework examples and guardrails.
- Adds local Codex app prompt in `prompts/local-codex-app-prompt.md`.
- Updates accessibility statement generator/template to include selected legal profile metadata.
- Packages repo-ready ZIP layout for `skills/typo3-wcag22-aa-agentic/`.

## 0.1.0

- Initial local agentic skill for TYPO3 WCAG 2.2 AA workflows.
- Adds SKILL.md, installer/scaffolder, Playwright + axe-core tests, TYPO3 template checks, report generation, open issue YAML, accessibility statement draft, optional Deque axe MCP examples, CI examples and HITL checklist.
