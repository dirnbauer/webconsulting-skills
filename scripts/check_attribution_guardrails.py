#!/usr/bin/env python3
"""Enforce attribution guardrails for upstream-derived skills.

This validator exists to keep the Netresearch attribution requested in
https://github.com/dirnbauer/webconsulting-skills/issues/2#issuecomment-4084733460
from drifting out of the repository again and to apply the same guardrail pattern
to other upstream-derived skills in the repository.
"""

from __future__ import annotations

import re

from audit_skills import ROOT, SKILLS_DIR, discover_source_info


README = ROOT / "README.md"

COMMON_REQUIRED_SKILL_SNIPPETS = (
    "## Credits & Attribution",
    "This skill is based on the excellent work by",
    "Original repository:",
    "Special thanks to",
    "Adapted by webconsulting.at for this skill collection",
)
REQUIRED_SKILL_SNIPPETS = (
    "Netresearch DTT GmbH",
    "Copyright (c) Netresearch DTT GmbH",
)


def check_readme_origin_table(readme_text: str, skill_name: str) -> list[str]:
    pattern = re.compile(
        rf"^\| `{re.escape(skill_name)}` \| .* \| Netresearch \|$",
        re.MULTILINE,
    )
    if pattern.search(readme_text):
        return []
    return [f"README origin table does not mark `{skill_name}` as Netresearch"]


def check_readme_origin_owner(readme_text: str, skill_name: str, owner: str) -> list[str]:
    pattern = re.compile(
        rf"^\| `{re.escape(skill_name)}` \| .* \| {re.escape(owner)} \|$",
        re.MULTILINE,
    )
    if pattern.search(readme_text):
        return []
    return [f"README origin table does not mark `{skill_name}` as {owner}"]


def check_readme_upstream_link(readme_text: str, skill_name: str, source_url: str) -> list[str]:
    if source_url in readme_text:
        return []
    return [f"README does not list upstream repository for `{skill_name}`: {source_url}"]


def check_skill_file(skill_name: str, owner: str, source_url: str) -> list[str]:
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    text = skill_file.read_text()
    issues: list[str] = []

    if owner == "webconsulting":
        return issues

    for snippet in COMMON_REQUIRED_SKILL_SNIPPETS:
        if snippet not in text:
            issues.append(
                f"{skill_name}/SKILL.md is missing required attribution text: {snippet}"
            )
    for snippet in REQUIRED_SKILL_SNIPPETS if owner == "Netresearch" else ():
        if snippet not in text:
            issues.append(
                f"{skill_name}/SKILL.md is missing required attribution text: {snippet}"
            )

    expected_repo_line = f"Original repository: {source_url}"
    if expected_repo_line not in text:
        issues.append(
            f"{skill_name}/SKILL.md is missing upstream repository line: {expected_repo_line}"
        )
    if owner not in text:
        issues.append(f"{skill_name}/SKILL.md does not name upstream owner `{owner}`")
    return issues


def main() -> int:
    readme_text = README.read_text()
    issues: list[str] = []
    upstream_skills: list[tuple[str, str, str]] = []

    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        text = (skill_dir / "SKILL.md").read_text()
        owner, source_url, _ = discover_source_info(skill_dir.name, text)
        if not source_url:
            continue
        upstream_skills.append((skill_dir.name, owner, source_url))

    for skill_name, owner, source_url in upstream_skills:
        if owner == "Netresearch":
            issues.extend(check_readme_origin_table(readme_text, skill_name))
        elif owner != "webconsulting":
            issues.extend(check_readme_origin_owner(readme_text, skill_name, owner))
        issues.extend(check_readme_upstream_link(readme_text, skill_name, source_url))
        issues.extend(check_skill_file(skill_name, owner, source_url))

    if issues:
        print("Upstream attribution guardrails failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(
        "Upstream attribution guardrails passed for "
        f"{len(upstream_skills)} upstream-derived skills."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
