#!/usr/bin/env python3
"""Sync README sections that describe upstream owners and repositories."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from audit_skills import ROOT, SKILLS_DIR, discover_source_info, owner_from_url


README = ROOT / "README.md"
SYNC_CONFIG = ROOT / ".sync-config.json"

EXTERNAL_START = "<!-- EXTERNAL_REPOS:START -->"
EXTERNAL_END = "<!-- EXTERNAL_REPOS:END -->"
ACK_START = "<!-- ACKNOWLEDGEMENTS:START -->"
ACK_END = "<!-- ACKNOWLEDGEMENTS:END -->"

REPO_SOURCE_URL = "https://github.com/dirnbauer/webconsulting-skills"

OWNER_DISPLAY = {
    "Netresearch": "Netresearch DTT GmbH",
    "Firecrawl": "Firecrawl / Mendable, Inc.",
    "remotion-dev": "Remotion",
}

OWNER_LINKS = {
    "Netresearch": "https://www.netresearch.de/",
    "Supabase": "https://supabase.com/",
    "Corey Haines": "https://corey.co/",
    "ooiyeefei": "https://github.com/ooiyeefei",
    "Stevy Smith": "https://github.com/stevysmith",
    "Vercel": "https://vercel.com/",
    "Giuseppe Trisciuoglio": "https://github.com/giuseppe-trisciuoglio",
    "Softaworks": "https://github.com/softaworks",
    "HeyGen": "https://www.heygen.com/",
    "Matt Pocock": "https://github.com/mattpocock",
    "GitHub": "https://github.com/github",
    "sickn33": "https://github.com/sickn33",
    "ehmo": "https://github.com/ehmo",
    "AITYTech": "https://github.com/aitytech",
    "Anthropic": "https://anthropic.com/",
    "Firecrawl": "https://www.firecrawl.dev/",
    "remotion-dev": "https://remotion.dev/",
    "OpenHands": "https://github.com/OpenHands",
}

OWNER_COPYRIGHT = {
    "Netresearch": (
        "**Copyright (c) Netresearch DTT GmbH** — TYPO3 development methodology, "
        "PHP modernization, and enterprise best practices (MIT / CC-BY-SA-4.0)\n"
        "See: [netresearch.de](https://www.netresearch.de/)"
    ),
    "Supabase": (
        "**Copyright (c) Supabase** - Postgres performance optimization guidelines\n"
        "See: [Postgres Best Practices for AI Agents](https://supabase.com/blog/postgres-best-practices-for-ai-agents)"
    ),
    "Corey Haines": (
        "**Copyright (c) Corey Haines** - Marketing frameworks and best practices\n"
        "See: [Conversion Factory](https://conversionfactory.co/) | [Swipe Files](https://swipefiles.com/)"
    ),
    "ooiyeefei": (
        "**Copyright (c) ooiyeefei** - Excalidraw architecture diagram generation and export workflow (MIT License)"
    ),
    "Stevy Smith": (
        "**Copyright (c) Stevy Smith** - OG Image generation and social meta tag configuration"
    ),
    "Vercel": (
        "**Copyright (c) Vercel, Inc.** - React/Next.js optimization, web design guidelines, "
        "skill discovery (MIT License)"
    ),
    "Giuseppe Trisciuoglio": (
        "**Copyright (c) Giuseppe Trisciuoglio** - shadcn/ui component patterns with Radix UI and Tailwind CSS"
    ),
    "Softaworks": (
        "**Copyright (c) Softaworks** - Agent instruction file refactoring with progressive disclosure"
    ),
    "HeyGen": (
        "**Copyright (c) HeyGen** - HyperFrames HTML-to-video composition, CLI, "
        "registry, and website-to-video workflows (Apache 2.0)"
    ),
    "Matt Pocock": (
        "**Copyright (c) Matt Pocock** - `grill-me` planning and design stress-test workflow (MIT License)"
    ),
    "GitHub": (
        "**Copyright (c) GitHub** - Code refactoring patterns and best practices"
    ),
    "sickn33": (
        "**Copyright (c) sickn33** - Clean code principles and SOLID design patterns"
    ),
    "ehmo": (
        "**Copyright (c) platform-design-skills** - Apple HIG and Material Design guidelines (MIT License)"
    ),
    "AITYTech": (
        "**Copyright (c) AITYTech** - Enterprise-grade AI marketing automation (MIT License)"
    ),
    "Anthropic": (
        "**Copyright (c) Anthropic** — `frontend-design` and `skill-creator` (Apache-2.0 License);\n"
        "`document-processing` (source-available, see Anthropic's README for terms)"
    ),
    "Firecrawl": (
        "**Copyright (c) Firecrawl / Mendable, Inc.** — CLI (ISC License)\n"
        "Note: The Firecrawl platform is AGPL-3.0; this skill documents CLI usage patterns only."
    ),
    "remotion-dev": (
        "Note: The Remotion library uses a custom license (free for individuals / small companies up to\n"
        "3 employees; company license required for larger organizations). This skill documents usage\n"
        "patterns only and does not include or redistribute Remotion source code."
    ),
}

OWNER_ORDER = [
    "Netresearch",
    "Supabase",
    "Corey Haines",
    "ooiyeefei",
    "Stevy Smith",
    "Vercel",
    "Giuseppe Trisciuoglio",
    "Softaworks",
    "HeyGen",
    "Matt Pocock",
    "GitHub",
    "sickn33",
    "ehmo",
    "AITYTech",
    "Anthropic",
    "Firecrawl",
    "remotion-dev",
    "OpenHands",
]


@dataclass
class OwnerInfo:
    owner: str
    skills_by_url: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    repo_mirrors: list[tuple[str, str, str]] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        return OWNER_DISPLAY.get(self.owner, self.owner)

    @property
    def link(self) -> str:
        if self.owner in OWNER_LINKS:
            return OWNER_LINKS[self.owner]
        if self.skills_by_url:
            return next(iter(sorted(self.skills_by_url)))
        if self.repo_mirrors:
            return self.repo_mirrors[0][1]
        return "#"

    @property
    def skill_names(self) -> list[str]:
        names: set[str] = set()
        for skill_names in self.skills_by_url.values():
            names.update(skill_names)
        return sorted(names)


def canonical_repo_url(url: str) -> str:
    return url.removesuffix(".git").rstrip("/")


def owner_sort_key(owner: str) -> tuple[int, str]:
    try:
        return (OWNER_ORDER.index(owner), owner.lower())
    except ValueError:
        return (len(OWNER_ORDER), owner.lower())


def format_skill_list(skill_names: list[str]) -> str:
    quoted = [f"`{skill}`" for skill in skill_names]
    if not quoted:
        return ""
    if len(quoted) == 1:
        return quoted[0]
    if len(quoted) == 2:
        return f"{quoted[0]} and {quoted[1]}"
    return f"{', '.join(quoted[:-1])}, and {quoted[-1]}"


def build_groups() -> dict[str, OwnerInfo]:
    groups: dict[str, OwnerInfo] = {}

    def get_group(owner: str) -> OwnerInfo:
        return groups.setdefault(owner, OwnerInfo(owner=owner))

    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = skill_file.read_text()
        owner, source_url, _ = discover_source_info(skill_dir.name, text)
        if not source_url or owner == "webconsulting" or source_url == REPO_SOURCE_URL:
            continue
        get_group(owner).skills_by_url[canonical_repo_url(source_url)].add(skill_dir.name)

    sync_config = json.loads(SYNC_CONFIG.read_text())
    for entry in sync_config.get("skills", []):
        if not entry.get("enabled"):
            continue
        if entry.get("copyMode") != "repo":
            continue
        source_url = canonical_repo_url(entry["source"])
        owner = owner_from_url(source_url) or "Unknown"
        target = entry.get("target", "")
        get_group(owner).repo_mirrors.append((entry["name"], source_url, target))

    return groups


def render_external_repositories(groups: dict[str, OwnerInfo]) -> str:
    lines = [EXTERNAL_START]
    for owner in sorted(groups, key=owner_sort_key):
        group = groups[owner]
        detail_parts = []
        if group.skill_names:
            count = len(group.skill_names)
            detail_parts.append(f"{count} skill" + ("" if count == 1 else "s"))
        if group.repo_mirrors:
            count = len(group.repo_mirrors)
            detail_parts.append(f"{count} repo mirror" + ("" if count == 1 else "s"))
        heading = f"### {group.display_name}"
        if detail_parts:
            heading += f" ({' + '.join(detail_parts)})"
        lines.append(heading)

        for url in sorted(group.skills_by_url):
            skill_list = format_skill_list(sorted(group.skills_by_url[url]))
            lines.append(f"- {skill_list}: {url}")

        for mirror_name, url, target in sorted(group.repo_mirrors):
            lines.append(f"- full repo mirror `{mirror_name}`: {url} -> `{target}`")

        lines.append("")

    if lines[-1] == "":
        lines.pop()
    lines.append(EXTERNAL_END)
    return "\n".join(lines)


def render_owner_intro(group: OwnerInfo) -> str:
    if group.owner == "Netresearch":
        return (
            f"We are deeply grateful to **[{group.display_name}]({group.link})** for their\n"
            "foundational contributions to this skill collection. The majority of TYPO3-related skills and\n"
            "several cross-domain skills are based on Netresearch's original open-source skill repositories.\n"
            "Their deep expertise in TYPO3 development, enterprise PHP engineering, and AI-augmented workflows\n"
            "has been instrumental in shaping the quality and depth of these guidelines."
        )

    skill_list = format_skill_list(group.skill_names)
    if skill_list:
        noun = "skill" if len(group.skill_names) == 1 else "skills"
        verb = "builds" if len(group.skill_names) == 1 else "build"
        return (
            f"We also thank **[{group.display_name}]({group.link})** for their excellent open-source work.\n"
            f"The {skill_list} {noun} in this collection {verb} on that contribution."
        )
    return (
        f"We also thank **[{group.display_name}]({group.link})** for their excellent open-source work,\n"
        "which we mirror in this repository for upgradeable sync workflows."
    )


def render_acknowledgements(groups: dict[str, OwnerInfo]) -> str:
    blocks = [ACK_START]
    for index, owner in enumerate(sorted(groups, key=owner_sort_key)):
        group = groups[owner]
        if index:
            blocks.extend(["", "---", ""])

        blocks.append(render_owner_intro(group))
        blocks.append("")

        if group.skill_names:
            blocks.append(
                "Adapted skill"
                + ("" if len(group.skill_names) == 1 else "s")
                + ": "
                + format_skill_list(group.skill_names)
            )
            blocks.append("")

        if group.skills_by_url or group.repo_mirrors:
            blocks.append("Original repositories:")
            for url in sorted(group.skills_by_url):
                skill_list = format_skill_list(sorted(group.skills_by_url[url]))
                blocks.append(f"- {skill_list}: {url}")
            for mirror_name, url, target in sorted(group.repo_mirrors):
                blocks.append(f"- full repo mirror `{mirror_name}`: {url} -> `{target}`")
            blocks.append("")

        copyright_line = OWNER_COPYRIGHT.get(owner)
        if copyright_line:
            blocks.append(copyright_line)

    blocks.extend(["", ACK_END])
    return "\n".join(blocks)


def replace_managed_block(text: str, start_marker: str, end_marker: str, new_block: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        raise RuntimeError(f"Missing README markers: {start_marker} / {end_marker}")
    end += len(end_marker)
    return text[:start] + new_block + text[end:]


def main() -> None:
    readme_text = README.read_text()
    groups = build_groups()
    updated = replace_managed_block(
        readme_text,
        EXTERNAL_START,
        EXTERNAL_END,
        render_external_repositories(groups),
    )
    updated = replace_managed_block(
        updated,
        ACK_START,
        ACK_END,
        render_acknowledgements(groups),
    )

    if updated != readme_text:
        README.write_text(updated)
        print(f"updated {README}")


if __name__ == "__main__":
    main()
