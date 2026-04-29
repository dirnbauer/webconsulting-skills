#!/usr/bin/env python3
"""Generate gemini-extension.json from the canonical skills directory.

The manifest should expose every top-level `skills/*/SKILL.md` directory. Trigger
phrases are catalog metadata, so this script reads the richer README skill
reference first and falls back to AGENTS.md when needed.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from audit_skills import parse_frontmatter, split_frontmatter


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
OUTPUT = ROOT / "gemini-extension.json"


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("|").strip())


def split_table_row(line: str) -> list[str]:
    return [clean_cell(cell) for cell in line.strip().strip("|").split("|")]


def extract_section(text: str, start_heading: str, end_heading: str) -> str:
    start = text.find(start_heading)
    if start == -1:
        return ""
    end = text.find(end_heading, start + len(start_heading))
    if end == -1:
        return text[start:]
    return text[start:end]


def parse_readme_skill_reference(text: str) -> dict[str, list[str]]:
    section = extract_section(text, "### Skill Reference", "### Example Prompts")
    triggers_by_skill: dict[str, list[str]] = {}

    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_table_row(line)
        if len(cells) < 3:
            continue
        raw_name, raw_triggers = cells[0], cells[1]
        match = re.fullmatch(r"`([^`/]+)`", raw_name)
        if not match:
            continue
        triggers = [part.strip() for part in raw_triggers.split(",") if part.strip()]
        triggers_by_skill[match.group(1)] = triggers

    return triggers_by_skill


def parse_readme_purposes(text: str) -> dict[str, str]:
    section = extract_section(text, "### Agent Skills", "### Category-Specific Add-ons")
    purposes: dict[str, str] = {}

    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_table_row(line)
        if len(cells) < 3:
            continue
        raw_name, raw_purpose = cells[0], cells[1]
        match = re.fullmatch(r"`([^`/]+)`", raw_name)
        if match:
            purposes[match.group(1)] = raw_purpose

    return purposes


def parse_agents_overview(text: str) -> dict[str, dict[str, object]]:
    section = extract_section(text, "## Skills Overview", "## Skill Categories")
    metadata: dict[str, dict[str, object]] = {}

    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_table_row(line)
        if len(cells) < 4:
            continue
        raw_name, description, _, raw_triggers = cells[:4]
        match = re.fullmatch(r"`([^`/]+)`", raw_name)
        if not match:
            continue
        triggers = [part.strip() for part in raw_triggers.split(",") if part.strip()]
        metadata[match.group(1)] = {
            "description": description,
            "triggers": triggers,
        }

    return metadata


def parse_skill_frontmatter(skill_name: str) -> dict[str, object]:
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    frontmatter_text, _ = split_frontmatter(skill_file.read_text())
    return parse_frontmatter(frontmatter_text)


def skill_names() -> list[str]:
    return sorted(
        path.parent.name
        for path in SKILLS_DIR.glob("*/SKILL.md")
        if path.is_file()
    )


def build_manifest() -> dict[str, object]:
    readme_text = README.read_text()
    agents_text = AGENTS.read_text() if AGENTS.exists() else ""

    readme_triggers = parse_readme_skill_reference(readme_text)
    readme_purposes = parse_readme_purposes(readme_text)
    agents_metadata = parse_agents_overview(agents_text)

    skills: dict[str, dict[str, object]] = {}
    missing_triggers: list[str] = []

    for skill_name in skill_names():
        frontmatter = parse_skill_frontmatter(skill_name)
        description = (
            str(agents_metadata.get(skill_name, {}).get("description") or "").strip()
            or readme_purposes.get(skill_name, "").strip()
            or str(frontmatter.get("description") or "").strip()
        )
        triggers = (
            readme_triggers.get(skill_name)
            or agents_metadata.get(skill_name, {}).get("triggers")
            or []
        )
        if not triggers:
            missing_triggers.append(skill_name)

        skills[skill_name] = {
            "name": skill_name,
            "description": description,
            "triggers": triggers,
            "path": f"${{extensionPath}}/skills/{skill_name}",
        }

    manifest = {
        "name": "webconsulting-skills",
        "version": "2.0.0",
        "description": (
            "Curated Agent Skills for AI-augmented software development — core "
            "installer for Cursor, Claude Code, Gemini CLI, Codex, and Windsurf"
        ),
        "license": "MIT AND CC-BY-SA-4.0",
        "contextFileName": "AGENTS.md",
        "excludeTools": [],
        "skills": skills,
    }

    if missing_triggers:
        print(
            "warning: no trigger metadata found for "
            + ", ".join(missing_triggers)
        )

    return manifest


def main() -> None:
    manifest = build_manifest()
    OUTPUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {OUTPUT} ({len(manifest['skills'])} skills)")


if __name__ == "__main__":
    main()
