# webconsulting Agent Skills

This repository contains 61 Agent Skills for AI-augmented software development.

## Instructions

Follow the instructions in [AGENTS.md](AGENTS.md) — it is the single source of truth for all skills, triggers, usage examples, and session profiles.

## Skills Location

All skills live in `skills/*/SKILL.md`. Each skill has YAML frontmatter with `name`, `description`, `triggers`, and `compatibility`.

To use a skill, read the `SKILL.md` file at `skills/<skill-name>/SKILL.md` and follow its instructions.

## Key Conventions

- TYPO3 skills target v13 LTS and v14.x where documented; **always confirm third-party extensions** (Packagist `require.typo3/cms-core`) for your project
- Most TYPO3 skills include `SKILL-PHP84.md` and `SKILL-CONTENT-BLOCKS.md` supplements
- Always review AI-generated code before committing
- When multiple skills are relevant, combine them (e.g., `typo3-rector` + `typo3-testing`)


## License

Code: MIT | Content: CC-BY-SA-4.0 | Third-party skills retain their original licenses.
See LICENSE, LICENSE-MIT, and LICENSE-CC-BY-SA-4.0 for full terms.
