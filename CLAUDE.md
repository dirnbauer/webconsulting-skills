# webconsulting Agent Skills

This repository contains 72 Agent Skills for AI-augmented software development.

## Instructions

Follow the instructions in [AGENTS.md](AGENTS.md) — it is the single source of truth for all skills, triggers, usage examples, session profiles, and acknowledgements.


## Skills Location

All skills live in `skills/<skill-name>/SKILL.md`. Installers symlink the whole skill directory, not just `SKILL.md`, so optional `agents/`, `assets/`, `examples/`, `references/`, `rules/`, and `scripts/` folders remain available to clients that support them.

To use a skill, read `skills/<skill-name>/SKILL.md` and follow its instructions. Load referenced files only when the skill asks for them.

## Key Conventions

- TYPO3 skills primarily target TYPO3 v14.x; typo3-translations also covers TYPO3 13/14 translation compatibility.
- Cross-cutting TYPO3/PHP guidance lives in the owning skills, for example `php-modernization`, `typo3-content-blocks`, and `typo3-update`.
- Always review AI-generated code before committing.
- When multiple skills are relevant, combine them, for example `typo3-rector` + `typo3-testing`.
- Keep upstream credits and thank-you text intact, especially Netresearch acknowledgements.

## License

Code: MIT | Content: CC-BY-SA-4.0 | Third-party skills retain their original licenses.
See LICENSE, LICENSE-MIT, and LICENSE-CC-BY-SA-4.0 for full terms.
