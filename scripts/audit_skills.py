#!/usr/bin/env python3
"""Audit skill sources and catalog quality.

Generates:
- catalog/skill-sources.json
- catalog/skill-audit.md

The audit is intentionally stdlib-only so it can run in a bare environment.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CATALOG_DIR = ROOT / "catalog"

# Optional per-skill overrides for owner labels or source URLs when auto-discovery
# from explicit attribution text in SKILL.md is not enough on its own.
SOURCE_MAP: dict[str, dict[str, str | None]] = {
    "ab-testing": {
        "owner": "AITYTech",
        "url": "https://github.com/aitytech/agentkits-marketing",
    },
    "agent-md-refactor": {
        "owner": "Softaworks",
        "url": "https://github.com/softaworks/agent-toolkit",
    },
    "ai-search-optimization": {"owner": "webconsulting", "url": None},
    "android-design": {
        "owner": "ehmo",
        "url": "https://github.com/ehmo/platform-design-skills",
    },
    "cli-tools": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/cli-tools-skill",
    },
    "context7": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/context7-skill",
    },
    "cro-funnel": {
        "owner": "AITYTech",
        "url": "https://github.com/aitytech/agentkits-marketing",
    },
    "deepfake-detection": {"owner": "webconsulting", "url": None},
    "document-processing": {
        "owner": "Anthropic",
        "url": "https://github.com/anthropics/skills/tree/main/skills/document-processing",
    },
    "enterprise-readiness": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/enterprise-readiness-skill",
    },
    "find-skills": {
        "owner": "Vercel",
        "url": "https://github.com/vercel-labs/skills",
    },
    "firecrawl": {"owner": "Firecrawl", "url": "https://github.com/firecrawl/cli"},
    "frontend-design": {
        "owner": "Anthropic",
        "url": "https://github.com/anthropics/skills/tree/main/skills/frontend-design",
    },
    "ios-design": {
        "owner": "ehmo",
        "url": "https://github.com/ehmo/platform-design-skills",
    },
    "ipados-design": {
        "owner": "ehmo",
        "url": "https://github.com/ehmo/platform-design-skills",
    },
    "launch-strategy": {
        "owner": "AITYTech",
        "url": "https://github.com/aitytech/agentkits-marketing",
    },
    "legal-impressum": {"owner": "webconsulting", "url": None},
    "macos-design": {
        "owner": "ehmo",
        "url": "https://github.com/ehmo/platform-design-skills",
    },
    "marketing-skills": {
        "owner": "Corey Haines",
        "url": "https://github.com/coreyhaines31/marketingskills",
    },
    "og-image": {
        "owner": "Stevy Smith",
        "url": "https://github.com/stevysmith/og-image-skill",
    },
    "php-modernization": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/php-modernization-skill",
    },
    "postgres-best-practices": {
        "owner": "Supabase",
        "url": "https://github.com/supabase/agent-skills",
    },
    "programmatic-seo": {
        "owner": "AITYTech",
        "url": "https://github.com/aitytech/agentkits-marketing",
    },
    "react-best-practices": {
        "owner": "Vercel",
        "url": "https://github.com/vercel-labs/agent-skills",
    },
    "readiness-report": {
        "owner": "OpenHands",
        "url": "https://github.com/OpenHands/skills",
    },
    "refactor": {
        "owner": "GitHub",
        "url": "https://github.com/github/awesome-copilot",
    },
    "refactor-clean": {
        "owner": "sickn33",
        "url": "https://github.com/sickn33/antigravity-awesome-skills",
    },
    "remotion-best-practices": {
        "owner": "remotion-dev",
        "url": "https://github.com/remotion-dev/skills",
    },
    "security-audit": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/security-audit-skill",
    },
    "security-incident-reporting": {"owner": "webconsulting", "url": None},
    "shadcn-ui": {
        "owner": "Giuseppe Trisciuoglio",
        "url": "https://github.com/giuseppe-trisciuoglio/developer-kit",
    },
    "skill-creator": {
        "owner": "Anthropic",
        "url": "https://github.com/anthropics/skills/tree/main/skills/skill-creator",
    },
    "tvos-design": {
        "owner": "ehmo",
        "url": "https://github.com/ehmo/platform-design-skills",
    },
    "typo3-accessibility": {"owner": "webconsulting", "url": None},
    "typo3-batch": {"owner": "webconsulting", "url": None},
    "typo3-conformance": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/typo3-conformance-skill",
    },
    "typo3-content-blocks": {"owner": "webconsulting", "url": None},
    "typo3-core-contributions": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/typo3-core-contributions-skill",
    },
    "typo3-datahandler": {"owner": "webconsulting", "url": None},
    "typo3-ddev": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/typo3-ddev-skill",
    },
    "typo3-docs": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/typo3-docs-skill",
    },
    "typo3-extension-upgrade": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/typo3-extension-upgrade-skill",
    },
    "typo3-fractor": {"owner": "webconsulting", "url": None},
    "typo3-icon14": {"owner": "webconsulting", "url": None},
    "typo3-powermail": {"owner": "webconsulting", "url": None},
    "typo3-records-list-types": {"owner": "webconsulting", "url": None},
    "typo3-rector": {"owner": "webconsulting", "url": None},
    "typo3-security": {"owner": "webconsulting", "url": None},
    "typo3-seo": {"owner": "webconsulting", "url": None},
    "typo3-simplify": {
        "owner": "webconsulting",
        "url": "https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-simplifier",
    },
    "typo3-solr": {"owner": "webconsulting", "url": None},
    "typo3-testing": {
        "owner": "Netresearch",
        "url": "https://github.com/netresearch/typo3-testing-skill",
    },
    "typo3-update": {"owner": "webconsulting", "url": None},
    "typo3-workspaces": {"owner": "webconsulting", "url": None},
    "ui-design-patterns": {"owner": "webconsulting", "url": None},
    "visionos-design": {
        "owner": "ehmo",
        "url": "https://github.com/ehmo/platform-design-skills",
    },
    "watchos-design": {
        "owner": "ehmo",
        "url": "https://github.com/ehmo/platform-design-skills",
    },
    "web-design-guidelines": {
        "owner": "Vercel",
        "url": "https://github.com/vercel-labs/agent-skills",
    },
    "web-platform-design": {
        "owner": "ehmo",
        "url": "https://github.com/ehmo/platform-design-skills",
    },
    "webconsulting-branding": {"owner": "webconsulting", "url": None},
    "webconsulting-create-documentation": {"owner": "webconsulting", "url": None},
}

GITHUB_OWNER_LABELS = {
    "aitytech": "AITYTech",
    "anthropics": "Anthropic",
    "coreyhaines31": "Corey Haines",
    "ehmo": "ehmo",
    "firecrawl": "Firecrawl",
    "github": "GitHub",
    "giuseppe-trisciuoglio": "Giuseppe Trisciuoglio",
    "netresearch": "Netresearch",
    "openhands": "OpenHands",
    "remotion-dev": "remotion-dev",
    "sickn33": "sickn33",
    "softaworks": "Softaworks",
    "stevysmith": "Stevy Smith",
    "supabase": "Supabase",
    "vercel-labs": "Vercel",
}

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


@dataclass
class SkillAudit:
    directory: str
    skill_name: str | None
    description: str | None
    source_owner: str
    source_url: str | None
    file_path: str
    line_count: int
    frontmatter_keys: list[str]
    pass_1: list[str]
    pass_2: list[str]
    pass_3: list[str]


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5 :]


def parse_frontmatter(frontmatter: str) -> dict[str, object]:
    parsed: dict[str, object] = {}
    lines = frontmatter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("  ") or ":" not in line:
            i += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value in {">-", "|", "|-", ">"}:
            block: list[str] = []
            i += 1
            while i < len(lines):
                nested = lines[i]
                if nested.startswith("  "):
                    block.append(nested[2:])
                    i += 1
                    continue
                break
            parsed[key] = " ".join(part.strip() for part in block if part.strip())
            continue
        if value == "":
            nested_values: list[str] = []
            nested_pairs: dict[str, str] = {}
            i += 1
            while i < len(lines):
                nested = lines[i]
                if not nested.startswith("  "):
                    break
                stripped = nested.strip()
                if stripped.startswith("- "):
                    nested_values.append(stripped[2:].strip())
                elif ":" in stripped:
                    nested_key, nested_value = stripped.split(":", 1)
                    nested_pairs[nested_key.strip()] = nested_value.strip().strip('"')
                i += 1
            if nested_pairs:
                parsed[key] = nested_pairs
            else:
                parsed[key] = nested_values
            continue
        parsed[key] = value.strip('"')
        i += 1
    return parsed


def normalize_name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    return value.strip() or None


def find_attribution_markers(text: str) -> Iterable[str]:
    patterns = [
        r"(?m)^\s*Original repository:\s*(https?://\S+)",
        r"(?m)^\s*(?:>\s*)?Source:\s*(https?://\S+)",
        r"(?m)^\s*(?:>\s*)?(?:\*\*Source:\*\*\s*)?(?:This skill is )?adapted from \[.*?\]\((https?://\S+)\)",
        r"(?m)^\s*(?:>\s*)?Adapted from .*?\((https?://\S+)\)",
        r"(?m)^\s*(?:>\s*)?This skill is adapted from .*?\((https?://\S+)\)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            yield match.group(1) if match.groups() else match.group(0)


def normalize_source_url(url: str) -> str:
    return url.rstrip(").,")


def owner_from_url(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        return None
    return GITHUB_OWNER_LABELS.get(parts[0].lower(), parts[0])


def discover_source_info(skill_name: str, text: str) -> tuple[str, str | None, list[str]]:
    override = SOURCE_MAP.get(skill_name)
    markers = [normalize_source_url(marker) for marker in find_attribution_markers(text)]

    source_url = None
    owner = None
    if override:
        owner = str(override["owner"])
        source_url = override["url"]

    if source_url is None and markers:
        source_url = markers[0]

    if owner is None and source_url:
        owner = owner_from_url(source_url)

    if owner is None and "Netresearch DTT GmbH" in text:
        owner = "Netresearch"

    if owner is None:
        owner = "webconsulting"

    return owner, source_url, markers


def audit_skill(skill_dir: Path, duplicate_names: dict[str, list[str]]) -> SkillAudit:
    text = (skill_dir / "SKILL.md").read_text()
    frontmatter_text, body = split_frontmatter(text)
    frontmatter = parse_frontmatter(frontmatter_text)
    skill_name = normalize_name(frontmatter.get("name"))
    description = normalize_name(frontmatter.get("description"))
    frontmatter_keys = list(frontmatter.keys())
    line_count = text.count("\n") + 1

    pass_1: list[str] = []
    pass_2: list[str] = []
    pass_3: list[str] = []

    if skill_name is None:
        pass_1.append("missing frontmatter name")
    elif skill_name in duplicate_names:
        pass_1.append(
            f"duplicate frontmatter name `{skill_name}` shared by {', '.join(duplicate_names[skill_name])}"
        )

    if skill_name and skill_name != skill_dir.name:
        pass_1.append(f"frontmatter name `{skill_name}` does not match directory `{skill_dir.name}`")

    unexpected = [key for key in frontmatter_keys if key not in ALLOWED_FRONTMATTER_KEYS]
    if unexpected:
        pass_1.append(
            "skill-creator schema drift: unexpected top-level keys "
            + ", ".join(f"`{key}`" for key in unexpected)
        )

    if line_count > 500:
        pass_1.append(f"SKILL.md is {line_count} lines; skill-creator recommends keeping it under 500")

    owner, source_url, markers = discover_source_info(skill_dir.name, text)
    if source_url:
        if not any(source_url in marker or marker in source_url for marker in markers):
            pass_2.append("expected upstream source is not explicitly attributed inside SKILL.md")
    elif owner == "webconsulting" and not markers:
        pass_2.append("no explicit source note; current assumption is webconsulting-original")

    if owner == "webconsulting" and source_url and source_url not in text:
        pass_2.append("repo-level source override exists but the skill body does not mention it")

    if description and description.rstrip().endswith("..."):
        pass_3.append("description appears truncated with an ellipsis")

    if description and len(description) > 1024:
        pass_3.append("description exceeds the 1024 character limit enforced by skill-creator")

    return SkillAudit(
        directory=skill_dir.name,
        skill_name=skill_name,
        description=description,
        source_owner=owner,
        source_url=source_url,
        file_path=str(skill_dir / "SKILL.md"),
        line_count=line_count,
        frontmatter_keys=frontmatter_keys,
        pass_1=pass_1,
        pass_2=pass_2,
        pass_3=pass_3,
    )


def build_audits() -> list[SkillAudit]:
    names: dict[str, list[str]] = {}
    skills = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    for skill_dir in skills:
        text = (skill_dir / "SKILL.md").read_text()
        frontmatter_text, _ = split_frontmatter(text)
        name = normalize_name(parse_frontmatter(frontmatter_text).get("name"))
        if name:
            names.setdefault(name, []).append(skill_dir.name)

    duplicates = {name: dirs for name, dirs in names.items() if len(dirs) > 1}
    return [audit_skill(skill_dir, duplicates) for skill_dir in skills]


def write_json(audits: list[SkillAudit]) -> None:
    payload = [
        {
            "directory": audit.directory,
            "skill_name": audit.skill_name,
            "description": audit.description,
            "source_owner": audit.source_owner,
            "source_url": audit.source_url,
            "file_path": audit.file_path,
            "line_count": audit.line_count,
            "frontmatter_keys": audit.frontmatter_keys,
            "pass_1": audit.pass_1,
            "pass_2": audit.pass_2,
            "pass_3": audit.pass_3,
        }
        for audit in audits
    ]
    (CATALOG_DIR / "skill-sources.json").write_text(json.dumps(payload, indent=2) + "\n")


def write_markdown(audits: list[SkillAudit]) -> None:
    total_issues = sum(len(a.pass_1) + len(a.pass_2) + len(a.pass_3) for a in audits)
    pass_1_count = sum(bool(a.pass_1) for a in audits)
    pass_2_count = sum(bool(a.pass_2) for a in audits)
    pass_3_count = sum(bool(a.pass_3) for a in audits)

    lines = [
        "# Skill Audit",
        "",
        "Generated by `python3 scripts/audit_skills.py`.",
        "",
        "This is a three-pass audit inspired by Anthropic's `skill-creator` skill:",
        "1. Structure and metadata integrity",
        "2. Source attribution and provenance drift",
        "3. Repository optimization gaps",
        "",
        f"- Skills audited: {len(audits)}",
        f"- Total findings: {total_issues}",
        f"- Skills with pass 1 findings: {pass_1_count}",
        f"- Skills with pass 2 findings: {pass_2_count}",
        f"- Skills with pass 3 findings: {pass_3_count}",
        "",
        "## High-Signal Repo Findings",
        "",
        "- `install.sh` previously mutated every `SKILL.md` by appending a Netresearch credit line. That behavior has been removed, but existing Netresearch attributions are preserved per current repo policy.",
        "- `web-platform-design` had a duplicate frontmatter name that collided with `web-design-guidelines`; it now uses `web-platform-design`.",
        "- `refactor-clean` had a mismatched frontmatter name plus a truncated description; both have been corrected.",
        "",
    ]

    for audit in audits:
        lines.extend(
            [
                f"## `{audit.directory}`",
                "",
                f"- Source owner: {audit.source_owner}",
                f"- Source URL: {audit.source_url or 'webconsulting-original / no external upstream recorded'}",
                f"- Frontmatter name: {audit.skill_name or 'missing'}",
                f"- SKILL.md lines: {audit.line_count}",
                "",
                "**Pass 1: Structure**",
            ]
        )
        lines.extend(f"- {issue}" for issue in (audit.pass_1 or ["No pass 1 issues found."]))
        lines.append("")
        lines.append("**Pass 2: Source**")
        lines.extend(f"- {issue}" for issue in (audit.pass_2 or ["No pass 2 issues found."]))
        lines.append("")
        lines.append("**Pass 3: Optimization**")
        lines.extend(f"- {issue}" for issue in (audit.pass_3 or ["No pass 3 issues found."]))
        lines.append("")

    (CATALOG_DIR / "skill-audit.md").write_text("\n".join(lines))


def main() -> None:
    CATALOG_DIR.mkdir(exist_ok=True)
    audits = build_audits()
    write_json(audits)
    write_markdown(audits)
    print(f"Wrote {CATALOG_DIR / 'skill-sources.json'}")
    print(f"Wrote {CATALOG_DIR / 'skill-audit.md'}")


if __name__ == "__main__":
    main()
