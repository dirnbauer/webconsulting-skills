#!/usr/bin/env python3
"""Add explicit source notes to skills without one.

Preserves existing Netresearch attribution lines.
"""

from __future__ import annotations

from pathlib import Path

from audit_skills import ROOT, SKILLS_DIR, discover_source_info, find_attribution_markers


NETRESEARCH_LINE = "Thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their contributions to the TYPO3 community."
REPO_SOURCE_URL = "https://github.com/dirnbauer/webconsulting-skills"


def build_note(skill_name: str) -> str:
    text = (SKILLS_DIR / skill_name / "SKILL.md").read_text()
    owner, url, _ = discover_source_info(skill_name, text)
    if url:
        return f"Adapted from [{owner}]({url})."
    return f"Source: {REPO_SOURCE_URL}"


def insert_source_note(text: str, note: str) -> str:
    if note in text:
        return text
    lines = text.rstrip("\n").splitlines()
    if lines and lines[-1] == NETRESEARCH_LINE:
        lines.insert(len(lines) - 1, "")
        lines.insert(len(lines) - 1, note)
    else:
        lines.extend(["", note])
    return "\n".join(lines) + "\n"


def main() -> None:
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        text = skill_file.read_text()
        if list(find_attribution_markers(text)):
            continue
        note = build_note(skill_dir.name)
        updated = insert_source_note(text, note)
        if updated != text:
            skill_file.write_text(updated)
            print(f"updated {skill_file}")


if __name__ == "__main__":
    main()
