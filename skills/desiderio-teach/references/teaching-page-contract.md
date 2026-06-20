# Teaching Page Contract

Use this reference when the `desiderio-teach` skill needs the concrete file formats or the TYPO3 page-building contract.

## Workspace Files

Create or update these files in the teaching workspace. Keep them near the project content they describe, not inside the skill directory.

### `MISSION.md`

Captures why the topic matters.

```md
# Mission: {Topic}

## Why
{1-3 sentences describing the concrete real-world outcome.}

## Success looks like
- {Observable capability}
- {Observable capability}

## Constraints
- {Time, budget, tooling, prior knowledge, language, accessibility, or project constraints}

## Out of scope
- {Adjacent topics to avoid for now}
```

Rules:

- One mission per workspace.
- Prefer concrete outcomes over abstract understanding.
- If the mission is vague, interview the user before creating the page.
- Update the mission when the learning goal changes, and record why.

### `RESOURCES.md`

Curates the sources that ground teaching.

```md
# {Topic} Resources

## Knowledge
- [{Source label}]({url})
  Covers {specific concepts}. Use for {lesson decisions}.

## Wisdom
- [{Community, practitioner, class, forum, or internal reviewer}]({url})
  Use for {real-world feedback the page cannot provide}.

## Gaps
- {Missing source or unresolved question}
```

Rules:

- Prefer primary documentation, recognized experts, peer-reviewed work, high-quality community material, and local project docs.
- Annotate every entry with what it covers and when to use it.
- Remove sources that prove shallow, outdated, or off-mission.

### `learning-records/0001-slug.md`

Create learning records lazily. They are not session logs; they record decision-grade insights.

```md
# {Short title}

{1-3 sentences describing what was learned, demonstrated, corrected, or disclosed, and why it changes future teaching.}
```

Write one only when:

- The user demonstrates genuine understanding.
- The user discloses prior knowledge that should change future lessons.
- A misconception is corrected.
- The mission shifts.

### `reference/*.md` or `reference/*.html`

Use reference documents for durable material the learner should revisit: glossaries, command cheatsheets, flowcharts, checklists, syntax examples, decision rules, formulas, and step sequences.

## Lesson Page Model

Each page should teach one tightly scoped thing. A useful sequence is:

1. Hook: why this topic matters for the mission.
2. Prior knowledge check: one question or self-assessment.
3. Core model: the smallest explanation that unlocks the task.
4. Worked example: a realistic example using the user's context.
5. Practice loop: quiz, checklist, small task, or decision exercise.
6. Reference block: compressed terms, commands, or steps.
7. Next step: what to ask the agent or what to try in the real project.

Avoid:

- Broad encyclopedia pages.
- Marketing-style hero copy that does not teach.
- Long passive articles without retrieval practice.
- Uncited claims when high-quality sources are available.

## Desiderio Content Element Mapping

Before writing records, inspect the project:

```bash
rg -n "description:|name:|title:|fields:" ContentBlocks/ContentElements
find ContentBlocks/ContentElements -maxdepth 2 -name config.yaml -print
```

For each candidate element, read:

- `ContentBlocks/ContentElements/<element>/config.yaml`
- `ContentBlocks/ContentElements/<element>/templates/frontend.fluid.html`
- `ContentBlocks/ContentElements/<element>/templates/backend-preview.fluid.html`
- `ContentBlocks/ContentElements/<element>/fixture.json` when present
- `ContentBlocks/ContentElements/<element>/language/labels.xlf`

Choose elements based on their descriptions and field contracts. Examples:

| Teaching need | Good element fit |
| --- | --- |
| Page purpose and outcome | Hero, intro, page header |
| Concept explanation | Text, text/media, editorial section |
| Process or sequence | Steps, timeline, checklist |
| Compare options | Cards, feature matrix, table |
| Frequently confused points | Accordion, tabs |
| Code or command examples | Code block, snippet, copyable command |
| Retrieval practice | Quiz, checklist, callout, form-like task |
| Sources and next steps | Resource list, CTA, link cards |

Field filling rules:

- Use the element's actual field names and configured types.
- Fill `header`, `subheadline`, `bodytext`, summaries, badges, eyebrow text, and CTAs with lesson-specific copy.
- For `Collection` fields, create one row per teaching unit rather than newline-delimited text.
- For `Link` fields, store URLs in link fields and labels in text fields.
- For `File` fields, use project-approved images or omit the element; do not invent broken file references.
- For `Select` or variant fields, use configured values only.
- For icons, use valid project icon keys or element-supported values.
- Keep empty fields intentional. If an element requires a field for a coherent preview, fill it.

## TYPO3 Page Creation

Use TYPO3 APIs, preferably DataHandler, for persistent changes:

- Create a page with a clear title, slug, parent page, doktype, hidden state, language, and backend layout according to the project.
- Add `tt_content` records in order via `sorting`, `pid`, `colPos`, `CType`, language fields, and Content Block fields.
- Respect workspaces and permissions. Do not write directly to database tables unless the project explicitly uses controlled fixtures or seed scripts.
- For multilingual pages, create the default language first, then translations with correct localization parent fields.
- Clear caches and run database/schema updates if new content types or fields were introduced.

## Verification Checklist

- The page exists in the correct part of the site tree with a readable slug.
- Frontend rendering is complete: no placeholders, empty required fields, broken images, or broken links.
- Backend previews show enough content for editors to recognize each record.
- Content order matches the learning sequence.
- Practice prompts have answers or feedback where the element supports it.
- Claims cite or link to the selected resources.
- The page can be completed quickly and produces one concrete learning win.
- `MISSION.md`, `RESOURCES.md`, `NOTES.md`, references, and learning records are current.

## Upstream Basis

This contract adapts Matt Pocock's `teach` skill concepts:

- mission-grounded lessons
- trusted resources before teaching
- storage strength through retrieval practice, spacing, and desirable difficulty
- learning records for demonstrated understanding
- reference documents for reusable knowledge

Original: https://github.com/mattpocock/skills/tree/main/skills/productivity/teach
