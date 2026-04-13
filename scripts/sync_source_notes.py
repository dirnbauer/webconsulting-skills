#!/usr/bin/env python3
"""Restore canonical Credits & Attribution blocks after syncing upstream skills.

Preserves the existing Netresearch thank-you wording while generating the same
style of thank-you block for other upstream-derived skills.
"""

from __future__ import annotations

import re

from audit_skills import SKILLS_DIR, discover_source_info


NETRESEARCH_LINE = (
    "Special thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their "
    "generous open-source contributions to the TYPO3 community, which helped shape this "
    "skill collection."
)
LEGACY_NETRESEARCH_LINES = {
    NETRESEARCH_LINE,
    "Thanks to [Netresearch DTT GmbH](https://www.netresearch.de/) for their contributions to the TYPO3 community.",
    "Thanks to Netresearch DTT GmbH for their contributions to the TYPO3 community.",
}
ADAPTED_LINE = "Adapted by webconsulting.at for this skill collection"
REPO_SOURCE_URL = "https://github.com/dirnbauer/webconsulting-skills"
LINK_OVERRIDES = {
    "Netresearch": "https://www.netresearch.de/",
}
DISPLAY_NAME_OVERRIDES = {
    "Netresearch": "Netresearch DTT GmbH",
}
COPYRIGHT_LINES = {
    "Netresearch": "**Copyright (c) Netresearch DTT GmbH** — Methodology and best practices (MIT / CC-BY-SA-4.0)",
}
FOOTER_LINE_PATTERNS = (
    r"^## Credits & Attribution$",
    r"^Adapted from ",
    r"^Original repository:",
    r"^Source:",
    r"^Special thanks to ",
    r"^Adapted by webconsulting\.at",
    r"^This skill is based on the excellent work by$",
    r"^\*\*Copyright \(c\)",
    r"^\*\*\[.+\]\(.+\)\*\*\.$",
)


def upstream_link(owner: str, source_url: str) -> str:
    return LINK_OVERRIDES.get(owner, source_url)


def display_name(owner: str) -> str:
    return DISPLAY_NAME_OVERRIDES.get(owner, owner)


def canonical_thanks_line(owner: str, source_url: str) -> str:
    if owner == "Netresearch":
        return NETRESEARCH_LINE
    return (
        f"Special thanks to [{display_name(owner)}]({upstream_link(owner, source_url)}) for their "
        "generous open-source contributions, which helped shape this skill collection."
    )


def strip_existing_footer(text: str) -> str:
    lines = text.rstrip("\n").splitlines()
    start: int | None = None

    for index in range(len(lines) - 1, -1, -1):
        if lines[index].strip() == "## Credits & Attribution":
            start = index
            break

    if start is None:
        tail_start = max(0, len(lines) - 40)
        for index in range(tail_start, len(lines)):
            stripped = lines[index].strip()
            if any(re.match(pattern, stripped) for pattern in FOOTER_LINE_PATTERNS):
                start = index
                break

    if start is None:
        while lines and not lines[-1].strip():
            lines.pop()
        return "\n".join(lines) + ("\n" if lines else "")

    while start > 0 and not lines[start - 1].strip():
        start -= 1
    if start > 0 and lines[start - 1].strip() == "---":
        start -= 1
        while start > 0 and not lines[start - 1].strip():
            start -= 1

    kept = lines[:start]
    while kept and not kept[-1].strip():
        kept.pop()
    return "\n".join(kept) + ("\n" if kept else "")


def remove_wrong_netresearch_thanks(text: str, owner: str) -> str:
    if owner == "Netresearch":
        return text

    lines = [line for line in text.rstrip("\n").splitlines() if line not in LEGACY_NETRESEARCH_LINES]
    while len(lines) >= 2 and not lines[-1].strip() and not lines[-2].strip():
        lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")


def build_credits_block(owner: str, source_url: str) -> str:
    lines = [
        "---",
        "",
        "## Credits & Attribution",
        "",
        "This skill is based on the excellent work by",
        f"**[{display_name(owner)}]({upstream_link(owner, source_url)})**.",
        "",
        f"Original repository: {source_url}",
        "",
    ]
    copyright_line = COPYRIGHT_LINES.get(owner)
    if copyright_line:
        lines.extend([copyright_line, ""])
    lines.extend(
        [
            canonical_thanks_line(owner, source_url),
            ADAPTED_LINE,
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        text = skill_file.read_text()
        owner, source_url, _ = discover_source_info(skill_dir.name, text)

        updated = remove_wrong_netresearch_thanks(text, owner)

        is_upstream_skill = (
            bool(source_url)
            and source_url != REPO_SOURCE_URL
            and owner != "webconsulting"
        )
        if is_upstream_skill:
            base = strip_existing_footer(updated).rstrip("\n")
            block = build_credits_block(owner, source_url)
            updated = f"{base}\n\n{block}" if base else block

        if updated != text:
            skill_file.write_text(updated)
            print(f"updated {skill_file}")


if __name__ == "__main__":
    main()
