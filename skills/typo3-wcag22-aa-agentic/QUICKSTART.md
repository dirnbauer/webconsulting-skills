# Quickstart: add this skill to `webconsulting-skills`

Unzip the final ZIP in the **root** of your skill-extension repository, not inside the `skills/` folder.

```bash
cd /path/to/webconsulting-skills
unzip /path/to/webconsulting-skills-typo3-wcag22-aa-agentic-final.zip

# optional: regenerate/install your local skill registry
./install.sh --generate-only
./install.sh

# review and commit
git status --short
git add skills/typo3-wcag22-aa-agentic
git commit -m "[TASK] Add TYPO3 WCAG 2.2 AA accessibility skill"
```

After commit, use the local Codex prompt:

```text
skills/typo3-wcag22-aa-agentic/prompts/local-codex-app-prompt.md
```

The skill includes all built components:

```text
SKILL.md
README.md
Skills.sh
prompts/local-codex-app-prompt.md
project-template/
  Playwright + axe-core runner
  TYPO3 static template checks
  report and statement generators
  structured .a11y/open-issues.yml workflow
  full WCAG 2.2 A/AA checkpoint list
  Chrome manual-review helper extension
  optional Deque / Cursor / Claude MCP examples
  legal examples for Austria, Germany, Switzerland
```
