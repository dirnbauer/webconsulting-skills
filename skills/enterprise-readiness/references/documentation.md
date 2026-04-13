# Documentation Standards

Language-agnostic documentation patterns for enterprise-ready projects.
Covers ADRs, API references, migration guides, and changelog practices.

## 1. Architecture Decision Records (ADRs)

ADRs document significant architectural decisions with their context and consequences.

### When to Create an ADR

- Choosing between multiple valid approaches
- Making decisions that affect multiple components
- Establishing patterns that will be followed project-wide
- Decisions that are hard to reverse
- Trade-offs that future maintainers need to understand

### ADR Template

```markdown
# ADR-NNN: Title of Decision

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date
YYYY-MM-DD

## Context

What is the issue that we're seeing that is motivating this decision?
What forces are at play (technical, political, social)?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

### Neutral
- Side effect that's neither good nor bad

## Alternatives Considered

### Alternative A: [Name]
- Pros: ...
- Cons: ...
- Why rejected: ...

### Alternative B: [Name]
- Pros: ...
- Cons: ...
- Why rejected: ...
```

### ADR File Organization

```
docs/
└── adr/
    ├── README.md              # Index of all ADRs
    ├── ADR-000-template.md    # Template for new ADRs
    ├── ADR-001-first-decision.md
    ├── ADR-002-another-decision.md
    └── ...
```

### ADR Index (README.md)

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-001](ADR-001-example.md) | Use PostgreSQL for persistence | Accepted | 2026-01-15 |
| [ADR-002](ADR-002-example.md) | Adopt functional options pattern | Accepted | 2026-01-16 |
```

## 2. API Reference Structure

### Organization Pattern

```
docs/
├── API_REFERENCE.md           # Main API reference
├── GETTING_STARTED.md         # Quick start guide
├── COOKBOOK.md                # Common recipes/patterns
└── guides/
    ├── MIGRATION.md           # Version migration guide
    └── ADVANCED.md            # Advanced usage
```

### API Reference Format

```markdown
# API Reference

## Types

### TypeName

Description of what this type represents and when to use it.

**Definition:**
```go
type TypeName struct {
    Field1 string    // Description of field
    Field2 int       // Description of field
}
```

**Example:**
```go
t := TypeName{
    Field1: "value",
    Field2: 42,
}
```

## Functions

### FunctionName

Description of what this function does.

**Signature:**
```go
func FunctionName(param1 Type1, param2 Type2) (ReturnType, error)
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| param1 | Type1 | What this parameter controls |
| param2 | Type2 | What this parameter controls |

**Returns:**
| Type | Description |
|------|-------------|
| ReturnType | What is returned |
| error | When errors occur |

**Example:**
```go
result, err := FunctionName("value", 42)
if err != nil {
    log.Fatal(err)
}
```

**See Also:** [RelatedFunction](#relatedfunction), [RelatedType](#typename)
```

### Documentation Completeness Checklist

- [ ] All public types documented
- [ ] All public functions/methods documented
- [ ] All parameters explained
- [ ] Return values explained
- [ ] At least one example per function
- [ ] Cross-references to related items
- [ ] Error conditions documented

## 3. Migration Guides

### Structure

```markdown
# Migration Guide: vX.Y to vX.Z

## Overview

Brief summary of what changed and why.

## Breaking Changes

### Change 1: [Description]

**Before (vX.Y):**
```go
// Old way
client.OldMethod()
```

**After (vX.Z):**
```go
// New way
client.NewMethod()
```

**Migration steps:**
1. Find all calls to `OldMethod()`
2. Replace with `NewMethod()`
3. Update parameters as needed

### Change 2: [Description]
...

## Deprecations

| Deprecated | Replacement | Removal Version |
|------------|-------------|-----------------|
| `OldFunc()` | `NewFunc()` | v2.0.0 |

## New Features

### Feature 1
Description and example.

## Behavioral Changes

Changes that don't require code modifications but affect runtime behavior.

| Behavior | Before | After |
|----------|--------|-------|
| Default timeout | 30s | 60s |
```

### Migration Guide Checklist

- [ ] All breaking changes listed with before/after examples
- [ ] Step-by-step migration instructions
- [ ] Deprecation warnings with replacement suggestions
- [ ] Behavioral changes documented (even if not breaking)
- [ ] New features highlighted

## 4. Changelog Practices

### Conventional Commits

Use conventional commit format for automated changelog generation:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
| Type | Description | Changelog Section |
|------|-------------|-------------------|
| `feat` | New feature | Added |
| `fix` | Bug fix | Fixed |
| `docs` | Documentation only | Documentation |
| `style` | Formatting, no code change | (usually omitted) |
| `refactor` | Code change, no feature/fix | Changed |
| `perf` | Performance improvement | Performance |
| `test` | Adding tests | (usually omitted) |
| `chore` | Maintenance tasks | (usually omitted) |

**Examples:**
```
feat(parser): add support for year field in cron expressions

fix(scheduler): prevent duplicate job execution on restart

Fixes #123

docs(readme): update installation instructions

BREAKING CHANGE: The `OldMethod` has been removed. Use `NewMethod` instead.
```

### CHANGELOG.md Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New feature description (#PR)

### Fixed
- Bug fix description (#PR)

## [1.2.0] - 2026-01-15

### Added
- Feature A for doing X (#101)
- Feature B for doing Y (#102)

### Changed
- Improved performance of Z by 15% (#103)

### Deprecated
- `OldMethod()` - use `NewMethod()` instead

### Fixed
- Fixed crash when input is empty (#104)

### Security
- Updated dependency X to fix CVE-YYYY-NNNN (#105)

## [1.1.0] - 2026-01-01
...

[Unreleased]: https://github.com/owner/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/owner/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/owner/repo/releases/tag/v1.1.0
```

### Changelog Quality Checklist

- [ ] Every release has an entry
- [ ] Changes categorized correctly (Added, Changed, Fixed, etc.)
- [ ] PR/Issue numbers referenced
- [ ] Breaking changes prominently marked
- [ ] Security fixes highlighted
- [ ] Links to compare views at bottom

## 5. Code Example Quality

### Requirements for Code Examples

1. **Complete** - Include all necessary imports
2. **Runnable** - Can be copy-pasted and executed
3. **Correct** - Actually works as described
4. **Error-handled** - Show proper error handling
5. **Idiomatic** - Follow language conventions

**Bad Example:**
```go
// Missing imports, no error handling
c := cron.New()
c.AddFunc("* * * * *", myJob)
c.Start()
```

**Good Example:**
```go
package main

import (
    "log"
    "time"

    cron "github.com/example/cron"
)

func main() {
    c := cron.New()

    _, err := c.AddFunc("* * * * *", func() {
        log.Println("Job executed at", time.Now())
    })
    if err != nil {
        log.Fatal("Failed to add job:", err)
    }

    c.Start()
    defer c.Stop()

    // Keep running
    select {}
}
```

## Related References

- `references/code-review.md` - Code review checklist (includes doc accuracy)
- `references/quick-start-guide.md` - Getting started patterns
