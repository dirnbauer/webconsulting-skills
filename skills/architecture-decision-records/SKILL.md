---
name: architecture-decision-records
description: Creates and reviews architecture decision records (ADRs), decision logs, and supersession histories using established conventions and verifiable evidence. Use when users ask to write, reconstruct, audit, standardize, validate, or maintain ADRs, architecture decisions, decision logs, or ADR templates in Markdown or reStructuredText.
---

# Architecture decision records

Write ADRs as a durable record of why one architecturally significant choice
was made. Prefer a small factual record over a broad design guide.

## Workflow

1. Read repository instructions, existing ADRs, documentation tooling, and the
   implementation affected by the decision.
2. Decide whether the record is prospective or retrospective. Never present a
   reconstructed decision as if it had been written when the choice was made.
3. Identify one significant decision. Split independent, phased, or separately
   reversible choices into separate records.
4. Use the repository's established template. Without one, use Nygard's minimal
   anatomy: status, context, decision, and consequences. Add alternatives when
   they explain the choice; use MADR when option comparison needs more detail.
5. For a retrospective ADR, inspect Git history first. Record relevant commit
   hashes and dates, then verify every claim against current code, tests,
   configuration, and authoritative platform documentation.
6. Write context as forces and constraints, not a disguised solution. State the
   decision assertively. Include material benefits, costs, risks, and limits.
7. Use `Proposed`, `Accepted`, `Rejected`, `Deprecated`, or `Superseded by
   ADR-NNN`. Preserve accepted and rejected records; supersede them with a new
   ADR instead of rewriting history.
8. Update the decision-log index and reciprocal supersession links. Render or
   lint the documentation using the repository's native toolchain.
9. Run the bundled validator and report unresolved evidence gaps honestly.

## Quality rules

- Use monotonic identifiers and never reuse a removed number.
- Keep one decision per record and make the title describe that decision.
- Separate observed facts, the selected decision, and expected consequences.
- Include credible alternatives; do not create straw-man options.
- Do not assign net scores or weights unless the ADR defines a scoring model
  and cites the measurements behind it.
- Distinguish verified history from inference and current policy from past fact.
- Keep secrets, personal data, and internal credentials out of evidence.
- Keep the record concise, standalone, linkable, and reviewable in a code diff.

## Validation

```bash
python3 skills/architecture-decision-records/scripts/validate_adrs.py docs/adr \
  --git-repo . --require-history
```

Omit `--require-history` for prospective records. Add the repository's own
renderer, link checker, or Markdown/ReST linter after this structural check.

## Resources

- Read [references/best-practices.md](references/best-practices.md) for the
  standards landscape, lifecycle, evidence method, and review rubric.
- Copy [assets/adr-template.md](assets/adr-template.md) for Markdown projects.
- Copy [assets/AdrTemplate.rst](assets/AdrTemplate.rst) for TYPO3 or other ReST
  documentation projects.
