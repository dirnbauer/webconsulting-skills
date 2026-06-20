---
name: "desiderio-teach"
description: "Turns a learning topic into a stateful teaching workspace and a TYPO3 page built with Desiderio Content Blocks. Use when the user asks to add a topic to teach, create lesson content, teach a concept inside TYPO3, create a Desiderio learning page, or fill Desiderio content elements from their descriptions."
compatibility: "TYPO3 14.x, Content Blocks 2.x, EXT:desiderio"
metadata:
  version: "1.0.0"
  origin: "webconsulting"
  based_on: "Matt Pocock teach skill"
license: "MIT / CC-BY-SA-4.0"
---

# Desiderio Teach

> Source: https://github.com/mattpocock/skills

Create teaching content as real TYPO3 page content. This adapts Matt Pocock's stateful `teach` workflow to Desiderio: the mission, sources, and learning records drive the lesson, while the final artifact is a TYPO3 page composed from existing Desiderio content elements.

## Default Workflow

1. **Establish the topic and mission.**
   - If the user supplied only a topic, ask for the concrete reason they want to learn it unless it is obvious from the project context.
   - Store one topic per teaching workspace. Use `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `reference/`, and `learning-records/` as described in `references/teaching-page-contract.md`.
   - Tie every page section to the mission; avoid broad survey pages that do not create one tangible learning win.

2. **Acquire trustworthy source material.**
   - Prefer primary docs, high-trust tutorials, domain references, and existing project docs over model memory.
   - Write or update `RESOURCES.md` with annotated Knowledge and Wisdom sources.
   - Surface source gaps explicitly before writing content that depends on them.

3. **Design the lesson page.**
   - Pick one tightly scoped learning outcome.
   - Teach the minimum knowledge needed, then add retrieval practice or a concrete task.
   - Include a quick-reference artifact when the topic has durable terms, commands, steps, or decision rules.
   - Keep the page short enough to complete quickly, but useful enough to revisit.

4. **Map content to Desiderio elements.**
   - Inspect the available Desiderio content elements before creating page records.
   - Read each element `config.yaml`, `description`, fields, fixtures, and frontend/backend preview intent.
   - Choose elements whose descriptions match the teaching job: hero/intro, explainer, steps, cards, accordion, code block, checklist, quiz/task, CTA, reference/resource list.
   - Fill every relevant field with specific teaching content. Use structured fields for links, files, repeatables, icons, badges, and CTAs; do not pack multiple values into one textarea.

5. **Create the TYPO3 page.**
   - Add the page via TYPO3 APIs or DataHandler, respecting the project's site tree, language, backend layout, permissions, and slug conventions.
   - Add `tt_content` records in the learning sequence, using the selected Desiderio Content Block `CType` values.
   - Use the `typo3-datahandler` skill when creating or updating TYPO3 records programmatically.
   - Use the `typo3-shadcn-content-elements` skill for Desiderio field coverage, seed quality, labels, previews, icons, and visual verification.

6. **Verify and record learning state.**
   - Clear caches, inspect the frontend page, and check backend layout previews.
   - Confirm content renders without empty fields, placeholder copy, broken links, or mismatched element variants.
   - Add a learning record only when the user demonstrated understanding, disclosed prior knowledge, corrected a misconception, or shifted the mission.

## Content Rules

- Write like a teacher, not a marketer. The page should teach one thing and ask the learner to do something with it.
- Prefer retrieval prompts, short exercises, worked examples, and decision checks over passive explanation.
- Every claim that matters should trace to `RESOURCES.md` or local project documentation.
- Make element choices from the actual Desiderio element descriptions, not from generic names.
- Keep copy concrete: replace placeholder phrases with topic-specific examples, commands, terms, questions, and answers.
- For quizzes or multiple-choice checks, keep answer options similar in length so formatting does not reveal the answer.
- Do not inline scripts or invent one-off CSS for the lesson page. Use existing Desiderio components and shared runtime behavior.

## References

- `references/teaching-page-contract.md`: workspace files, content model, Desiderio mapping, and verification checklist.
- `../typo3-shadcn-content-elements/SKILL.md`: Desiderio Content Blocks contract.
- `../typo3-datahandler/SKILL.md`: creating TYPO3 pages and `tt_content` records safely.

---

## Credits & Attribution

This skill is based on the excellent work by
**[Matt Pocock](https://github.com/mattpocock)**.

Original repository: https://github.com/mattpocock/skills

**Copyright (c) Matt Pocock** - Agent skills for real engineering workflows (MIT License)

Special thanks to [Matt Pocock](https://github.com/mattpocock) for his generous open-source contributions, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
