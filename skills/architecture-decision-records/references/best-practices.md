# ADR best practices

## Standards landscape

There is no universal ADR syntax or mandatory file format.
ISO/IEC/IEEE 42010:2022 defines requirements for architecture descriptions but
explicitly does not prescribe their format or medium. ADR formats are therefore
team conventions rather than an ISO document template.

Use these established sources together:

- [Michael Nygard's original ADR proposal](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  supplies the compact baseline: title, status, context, decision, and
  consequences; one significant decision; immutable sequential records.
- [MADR](https://adr.github.io/madr/) supplies a richer Markdown template for
  decision drivers, considered options, and tradeoffs.
- [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
  describes team review, ownership, lifecycle, and supersession.
- [AWS ADR best practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html)
  emphasize preserving history and keeping the decision log centrally visible.
- [Microsoft Azure Well-Architected guidance](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
  explicitly supports retrospective ADRs for brownfield systems and recommends
  concise, factual, append-only records.
- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) is the
  adjacent formal standard for architecture descriptions.

## Default anatomy

Use Nygard's sections as the portable minimum:

1. **Title:** a numbered decision statement, not a topic label.
2. **Status:** proposed, accepted, rejected, deprecated, or superseded.
3. **Context:** the problem, constraints, and forces in tension.
4. **Decision:** the chosen approach in active, assertive language.
5. **Consequences:** positive and negative results, including new obligations.

Common optional sections are date, owners or deciders, decision drivers,
options considered, evidence, links, and confidence. Add only sections that
improve a later reader's ability to understand or review the choice.

## Lifecycle

- Draft a new record as `Proposed` and allow it to change during review.
- On approval, record the acceptance date and set it to `Accepted`.
- Preserve accepted and rejected content as decision history.
- If circumstances change, create a new record. Set the old status to
  `Superseded by ADR-NNN` and link the new record back to it.
- Use `Deprecated` when the decision should no longer guide new work but no
  single replacement exists.
- Keep identifiers monotonic. Gaps are less harmful than reused identities.

## Retrospective records

A retrospective ADR reconstructs a known past decision; it does not recreate
an undocumented meeting. Use this evidence order:

1. Find the implementation commits and their dates.
2. Read commit messages, diffs, tests, issues, and documentation from that time.
3. Inspect reverts and follow-up fixes; they often reveal rejected approaches.
4. Verify that the stated decision still matches the current implementation.
5. Check unstable external constraints in authoritative current documentation.
6. State the retrospective recording date and list the supporting commits.
7. Label uncertain intent as an inference or omit it.

Commit chronology proves what changed, not necessarily every reason why.
Alternatives are credible only when a diff, discussion, revert, constraint, or
technical incompatibility supports them.

## Plausibility review

Ask these questions before accepting a record:

- Is this one choice with architectural impact or merely implementation detail?
- Does the context avoid assuming the decision it is meant to justify?
- Can each factual claim be traced to code, configuration, tests, history, or
  authoritative documentation?
- Does the current implementation conform to the decision?
- Are material security, privacy, durability, cost, latency, and failure-mode
  consequences included?
- Are alternatives technically viable and evaluated fairly?
- Could a maintainer tell when the decision no longer applies?
- Are measurements dated and reproducible?

Avoid arbitrary net scores. A numeric comparison is meaningful only when the
record defines criteria, weights, measurements, uncertainty, and calculation.
Otherwise prose tradeoffs are more honest and durable.

## Repository integration

- Store ADRs beside the code or in the canonical documentation repository.
- Maintain an index with identifier, title, and status.
- Link related and superseding records in both directions.
- Use the repository's normal review process for status changes.
- Render ReST and lint Markdown; validate links and referenced Git commits.
- Do not maintain duplicate Markdown and ReST copies unless one is generated
  deterministically from the other.
