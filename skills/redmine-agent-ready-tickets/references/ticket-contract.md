# Agent-ready ticket contract

Use this contract for implementation tickets. Omit optional sections only when they are genuinely irrelevant. Keep the result concise enough to scan, but complete enough that a coding agent does not need private conversation context.

## Canonical content

### Subject

Use an imperative or outcome-led subject that names the affected capability. Avoid starting with a tool name unless adopting that tool is itself the outcome.

Good: `Protect the TYPO3 metrics endpoint and expose OpenMetrics data`

Weak: `Prometheus`, `Improve monitoring`, `codebase MCP`

### Goal

State who benefits, what changes, and why it matters in two to four sentences.

### Context / current behavior

State only verified facts needed to implement the change. Link source issues, repositories, docs, attachments, incidents, or accepted ADRs. For bugs, include reproducible actual behavior.

### Target

Name the repository, service, extension key, package, or a deterministic discovery rule. Include supported runtime versions when compatibility is part of the work.

### Scope

List required behavior and deliverables. Prefer observable vertical slices. Separate functional requirements from technical constraints.

### Out of scope

Name tempting adjacent work that must not expand the ticket. Do not use this section to exclude essential quality, security, or tests.

### Acceptance criteria

Use stable IDs. Each criterion must be observable and decidable.

- `AC-1`: Given the precondition, when the action occurs, then the expected outcome is observable.
- `AC-2`: State a failure, permission, empty-state, or rollback path when relevant.
- `AC-3`: State compatibility or regression behavior.

Avoid criteria that merely restate internal tasks. “A service class exists” is not acceptance unless that class is a public compatibility contract.

### Validation

List repository-standard commands for tests, static analysis, linting, build, and smoke tests. Add manual verification only for behavior that cannot reasonably be automated. Never invent command names: inspect the repository or tell the agent how to discover them.

### Delivery notes

Identify required documentation, migration, configuration example, changelog, dashboard, rollout, or rollback artifacts. State whether an ADR is required and what decision it must capture.

### Dependencies and ordering

Name blocking issues and external prerequisites. Use Redmine relations after child IDs exist. If there are no dependencies, say so only when that fact reduces ambiguity.

## Textile template

```textile
h2. Goal

<Who benefits, what changes, and why.>

h2. Context / current behavior

* <Verified fact and source>
* <Existing behavior or limitation>

h2. Target

* Repository: <URL or deterministic discovery rule>
* Component: <package, extension, service, or directory>
* Compatibility: <supported versions>

h2. Scope

* <Required behavior>
* <Required deliverable>

h2. Out of scope

* <Adjacent work deliberately excluded>

h2. Technical constraints

* <Accepted architecture, security, platform, or compatibility constraint>

h2. Acceptance criteria

* *AC-1:* <Observable success condition>
* *AC-2:* <Failure or permission condition>
* *AC-3:* <Regression or compatibility condition>

h2. Validation

* Automated: @<repository command>@
* Smoke test: <steps and expected signal>

h2. Delivery notes

* <Docs, config, migration, rollout, rollback, ADR>

h2. Dependencies

* <Blocking issue, external prerequisite, or none>

h2. Sources

* "<Descriptive source>":<https://example.com>
```

## Bug-only additions

Add these before Scope:

- Reproduction steps using a minimal deterministic case
- Expected behavior
- Actual behavior, including exact error or evidence
- Regression boundary: last known good version or explicitly unknown

## Spike-only contract

Replace implementation Scope with:

- questions to answer
- alternatives to compare
- evidence required
- timebox
- decision owner
- output: recommendation, prototype, benchmark, and/or ADR

A spike is complete when the decision can be made, not when production code is shipped.

## Readiness scoring

Score out of 100:

- Goal and user value: 10
- Verified context and target: 15
- Coherent scope and non-goals: 15
- Technical constraints without overdesign: 10
- Observable acceptance criteria: 25
- Validation and regression coverage: 15
- Dependencies, delivery, security, and operations: 10

Require at least 85 and no blocker. A missing target, unmade product decision, untestable acceptance criteria, or mixed research/implementation scope is a blocker regardless of score.
