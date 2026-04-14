# webconsulting Agent Skills

This repository contains 62 Agent Skills for AI-augmented software development.

## Instructions

Follow the instructions in [AGENTS.md](AGENTS.md) — it is the single source of truth for all skills, triggers, usage examples, and session profiles.

## Gemini CLI Integration

Skills are registered in `gemini-extension.json` with trigger-based activation. The extension manifest maps each skill to its trigger keywords and `skills/` directory path.

## Skills Location

All skills live in `skills/*/SKILL.md`. Each skill has YAML frontmatter with `name`, `description`, `triggers`, and `compatibility`.

To use a skill, read the `SKILL.md` file at `skills/<skill-name>/SKILL.md` and follow its instructions.

## Key Conventions

- TYPO3 skills target **TYPO3 v14.x only** (verify third-party extensions on Packagist)
- Cross-cutting TYPO3/PHP guidance lives in the owning skills (for example `php-modernization`, `typo3-content-blocks`, `typo3-update`)
- Always review AI-generated code before committing
- When multiple skills are relevant, combine them (e.g., `typo3-rector` + `typo3-testing`)

## License

Code: MIT | Content: CC-BY-SA-4.0 | Third-party skills retain their original licenses.
See LICENSE, LICENSE-MIT, and LICENSE-CC-BY-SA-4.0 for full terms.
