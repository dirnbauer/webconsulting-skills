# Redmine backlog restructuring patterns

Use the smallest structure that lets one agent complete one coherent outcome and prove it works.

## Decision table

| Signal | Action | Reason |
|---|---|---|
| Same outcome, repeated issues | Merge or mark duplicates | Preserve one source of truth |
| Several independently releasable outcomes | Split into vertical slices | Each ticket can ship and be verified alone |
| Research question mixed with production work | Create a spike, then implementation ticket(s) | Prevent unmade decisions from leaking into code |
| Multiple repositories with separate release cycles | Split by repository and connect with relations | Ownership and completion remain clear |
| Large coordinated initiative | Create a parent epic plus executable children | The parent tracks outcome; children carry implementation |
| Bug report actually requests new behavior | Reclassify as feature | Tracker semantics stay meaningful |
| Task only says “document/test/build layer X” | Fold into its vertical feature | Avoid horizontal slices with no user-visible completion |
| Prerequisite produces no independent value but is required | Keep inside the consuming ticket | Reduce coordination overhead |

## Vertical slice test

A child ticket is a valid slice when it has:

1. one user or operator outcome
2. its own acceptance criteria
3. an independently reviewable change
4. no hidden dependency on unfinished sibling internals
5. a bounded target repository or component

Do not split only by architecture layers such as database, service, UI, tests, and docs. Keep those together when they jointly deliver one outcome.

## Epic pattern

An epic description contains:

- desired end state and success measure
- shared constraints and decisions
- ordered child issue list
- dependency graph
- explicit statement that implementation happens in children

Do not duplicate each child's full contract in the epic. Summarize the outcome and link to the child.

## Dependency relations

Use the Redmine relation that expresses the real constraint:

- `precedes` / `follows`: ordering without hard technical blocking
- `blocks` / `blocked by`: work cannot complete without the other issue
- `duplicates` / `duplicated by`: one issue replaces the other
- parent/child: shared outcome and reporting hierarchy

Avoid parent/child merely because tickets mention the same technology.

## Preservation rules

- Preserve ticket history and IDs when the core outcome survives.
- Add a short comment explaining a major reclassification or split when audit history matters.
- Move authoritative requirements into descriptions; comments are historical context.
- Do not close an original issue until replacement tickets exist and relations are verified.
- Retain attachments on the issue whose implementation needs them; link them from children when Redmine cannot reattach safely.
