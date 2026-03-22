#!/usr/bin/env python3
"""Generate minimal `agents/openai.yaml` files for all skills.

This is additive only: it does not modify SKILL.md content.
"""

from __future__ import annotations

from pathlib import Path
import re

from audit_skills import SKILLS_DIR, parse_frontmatter, split_frontmatter


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def titleize_directory(directory: str) -> str:
    special = {"typo3": "TYPO3", "ios": "iOS", "ipados": "iPadOS", "macos": "macOS", "tvos": "tvOS", "visionos": "visionOS", "watchos": "watchOS", "ui": "UI", "seo": "SEO", "cro": "CRO", "og": "OG", "php": "PHP", "ab": "A/B"}
    parts = directory.split("-")
    words = []
    for part in parts:
        words.append(special.get(part, part.capitalize()))
    return " ".join(words)


def first_heading(body: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip()


def first_sentence(text: str) -> str:
    normalized = normalize_whitespace(text)
    match = re.match(r"(.+?[.!?])(?:\s|$)", normalized)
    return match.group(1) if match else normalized


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_default_prompt(display_name: str, short_description: str) -> str:
    lead = first_sentence(short_description)
    if lead.endswith("."):
        lead = lead[:-1]
    return f"Help me with {display_name}: {lead.lower()}."


def main() -> None:
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        text = (skill_dir / "SKILL.md").read_text()
        frontmatter_text, body = split_frontmatter(text)
        frontmatter = parse_frontmatter(frontmatter_text)

        description = normalize_whitespace(str(frontmatter.get("description", "")).strip())
        display_name = first_heading(body) or titleize_directory(skill_dir.name)
        short_description = first_sentence(description) if description else f"Use the {display_name} skill."
        default_prompt = build_default_prompt(display_name, short_description)

        agents_dir = skill_dir / "agents"
        agents_dir.mkdir(exist_ok=True)
        content = "\n".join(
            [
                f"display_name: {yaml_quote(display_name)}",
                f"short_description: {yaml_quote(short_description)}",
                f"default_prompt: {yaml_quote(default_prompt)}",
                "",
            ]
        )
        (agents_dir / "openai.yaml").write_text(content)
        print(f"updated {agents_dir / 'openai.yaml'}")


if __name__ == "__main__":
    main()
