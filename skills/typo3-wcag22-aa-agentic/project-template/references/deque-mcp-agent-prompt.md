# Optional Deque axe MCP agent prompt

Use this only when axe MCP is configured in the current IDE/agent.

Suggested prompt:

```text
Use axe MCP to analyze the local TYPO3 page {{URL}} for WCAG 2.2 AA accessibility issues. If violations are found, remediate them in the TYPO3 source files, preferably Fluid/SCSS/JS in the sitepackage. After each fix, re-run the local Playwright/axe test and the axe MCP analyze step for the exact same page state. Do not suppress rules unless you document reason, owner and expiry. Do not claim final WCAG conformance without the HITL checklist.
```

For login-protected pages, pass explicit steps without secrets in the prompt; read credentials from local environment files only when the user permits it.

For cookie banners, ask the MCP analysis to dismiss the configured selector before scanning.
