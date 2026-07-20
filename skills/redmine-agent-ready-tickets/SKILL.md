---
name: redmine-agent-ready-tickets
description: Turn vague, mixed-scope, or underspecified Redmine issues into implementation contracts that Claude, ChatGPT, Codex, or another coding agent can execute with minimal clarification. Use when auditing a Redmine backlog; rewriting todos, bugs, features, spikes, or epics; splitting or merging tickets; defining parent/child relationships and dependencies; adding acceptance criteria and verification commands; preparing tickets for autonomous implementation; or reviewing whether existing tickets are agent-ready.
---

# Redmine Agent-Ready Tickets

Convert issue history and product intent into small, evidence-backed implementation contracts. Preserve why the work exists while removing ambiguity about what must be delivered and how completion will be verified.

## Load the supporting material

- Read [references/ticket-contract.md](references/ticket-contract.md) before drafting or rewriting any ticket.
- Read [references/restructuring-patterns.md](references/restructuring-patterns.md) when a backlog contains duplicates, research mixed with implementation, more than one independently releasable outcome, or unclear parent/child relationships.
- Run `scripts/validate_ticket.py` against each final draft when the ticket body is available as a file.

## Workflow

### 1. Establish scope and authority

Identify the Redmine project, requested ticket set, target language, and whether the user asked for an audit, drafts, or live updates. Treat reading and drafting separately from changing Redmine.

Prefer a purpose-built Redmine connector, API, or CLI. Use browser interaction only when no suitable integration exists or the user explicitly requests it. Follow the active tool's confirmation policy before saving live changes.

### 2. Capture the source of truth

For every issue, record:

- ID, subject, tracker, status, priority, assignee, parent, relations, and custom fields
- full description, comments, attachments, and relevant history
- linked repository, project wiki, deployment, design, ADR, or external dependency
- the original user outcome, even if the proposed implementation is weak

Do not discard useful context. Keep a local draft or change table containing old subject, new subject, structural action, and reason.

### 3. Resolve facts before writing requirements

Inspect the target repository and its local instructions when available. Verify current package names, versions, APIs, compatibility, and platform limits in primary sources. Read relevant attachments. Distinguish facts from proposals.

Do not turn a missing fact into an invented requirement. If the coding agent can discover it safely inside the target repository, state the discovery rule. If different answers would materially change the product, security model, or architecture, mark the ticket as blocked instead of pretending it is ready.

### 4. Classify and restructure

Choose the correct tracker:

- **Bug**: observed behavior violates an existing contract; include reproduction, expected result, actual result, and regression proof.
- **Feature**: adds a new capability; include user outcome, boundaries, acceptance criteria, and rollout implications.
- **Spike**: resolves a decision with evidence; its deliverable is a recommendation, prototype, benchmark, or ADR—not production code.
- **Epic/parent**: coordinates independently deliverable child tickets; do not ask an agent to implement an epic directly.

Split an issue when it contains independently testable or releasable outcomes, mixes research with implementation, spans unrelated repositories, or cannot be completed in one coherent change. Prefer vertical slices over component-layer tasks. Use the decision rules in [references/restructuring-patterns.md](references/restructuring-patterns.md).

### 5. Draft the implementation contract

Use the canonical template in [references/ticket-contract.md](references/ticket-contract.md). Adapt the formatting to the Redmine text formatter; do not paste Markdown into a Textile project without conversion.

Write requirements as observable behavior. Give the implementation agent autonomy inside explicit constraints. Name required files or architecture only when the repository or an accepted decision already establishes them.

Use stable acceptance-criterion IDs such as `AC-1`. Make every criterion independently verifiable. Include exact validation commands when they are known; otherwise name the repository-standard checks the agent must discover and run.

### 6. Apply the readiness gate

A ticket is ready only when all of these are true:

- one issue has one coherent outcome
- the target repository or discovery rule is explicit
- scope and non-goals prevent predictable expansion
- dependencies and ordering are visible
- acceptance criteria describe externally observable completion
- tests cover success, failure, and regressions proportional to risk
- security, data, deployment, and observability concerns are addressed or explicitly not applicable
- no blocking product decision is hidden inside an implementation note
- the ticket can be understood without private conversation context

Run:

```bash
python3 scripts/validate_ticket.py path/to/ticket.txt
```

Treat the validator as a floor, not proof of quality. Resolve every error and review warnings deliberately.

### 7. Review and update Redmine

Present a compact change plan before live mutation when required by the active tool. Preserve ticket IDs where possible. Create child tickets before adding relationships that depend on their IDs. Update parent subjects and descriptions last so they can reference the final child set.

After saving, reopen every changed issue and verify subject, tracker, description, hierarchy, relations, status, and any changed custom fields. Report exact issue IDs and any intentionally deferred items.

## Writing rules

- Lead with the outcome, not a tool or guessed solution.
- Replace “improve,” “support,” “integrate,” and “make it work” with measurable behavior.
- Do not hide research tasks such as “find the best three features” inside a build ticket; use a spike or make the decisions before drafting.
- Avoid acceptance criteria that only say code exists, tests pass, or documentation is updated.
- Do not require a specific class structure merely to make the ticket look precise.
- Include source URLs and version dates when current external behavior matters.
- Keep comments for audit history; keep the authoritative contract in the description.

## Output

Return:

1. a backlog change table with keep/rewrite/split/merge/reclassify decisions
2. complete ticket bodies in Redmine-compatible formatting
3. parent/child and dependency relationships
4. readiness results and unresolved blockers
5. live Redmine links after updates, when mutation was requested and completed
