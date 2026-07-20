#!/usr/bin/env python3
"""Validate an agent-ready ticket written in Textile or Markdown."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED = {
    "goal": ("goal", "outcome"),
    "context": ("context", "current behavior", "current state"),
    "target": ("target", "repository", "component"),
    "scope": ("scope", "requirements"),
    "out of scope": ("out of scope", "non-goals", "non goals"),
    "acceptance criteria": ("acceptance criteria", "definition of done"),
    "validation": ("validation", "test plan", "verification"),
}

OPTIONAL = {
    "constraints": ("technical constraints", "constraints"),
    "delivery": ("delivery notes", "deliverables", "rollout"),
    "dependencies": ("dependencies", "ordering"),
    "sources": ("sources", "references"),
}

VAGUE = re.compile(r"\b(improve|enhance|optimi[sz]e|support|integrate|make it work|etc\.?|as needed)\b", re.I)
PLACEHOLDER = re.compile(r"(?:<[^>\n]{2,}>|\bTBD\b|\bTODO\b|\?\?+)", re.I)
AC = re.compile(r"\bAC[- ]?\d+\b", re.I)
COMMAND = re.compile(r"(?:^|\s)(?:@[^@\n]+@|`[^`\n]+`|(?:composer|npm|pnpm|yarn|vendor/bin|make|ddev|docker)\s+[^\n]+)", re.M)


def headings(text: str) -> list[str]:
    result: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        match = re.match(r"^h[1-6]\.\s+(.+)$", stripped, re.I)
        if not match:
            match = re.match(r"^#{1,6}\s+(.+)$", stripped)
        if match:
            value = re.sub(r"[*_`#]", "", match.group(1)).strip().lower()
            result.append(value)
    return result


def has_section(found: list[str], aliases: tuple[str, ...]) -> bool:
    return any(any(alias == heading or alias in heading for alias in aliases) for heading in found)


def validate(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    found = headings(text)
    errors: list[str] = []
    warnings: list[str] = []

    if len(text.strip()) < 500:
        warnings.append("ticket is very short; verify that context, boundaries, and tests are complete")

    for name, aliases in REQUIRED.items():
        if not has_section(found, aliases):
            errors.append(f"missing required section: {name}")

    for name, aliases in OPTIONAL.items():
        if not has_section(found, aliases):
            warnings.append(f"consider adding section: {name}")

    ac_count = len(set(item.upper().replace(" ", "-") for item in AC.findall(text)))
    if ac_count < 3:
        errors.append("include at least three stable acceptance criteria (AC-1, AC-2, AC-3)")

    if not COMMAND.search(text):
        warnings.append("no concrete validation command found; verify repository-standard checks are named")

    placeholders = sorted(set(PLACEHOLDER.findall(text)))
    if placeholders:
        errors.append("unresolved placeholders: " + ", ".join(placeholders[:8]))

    vague = sorted(set(match.group(0).lower() for match in VAGUE.finditer(text)))
    if vague:
        warnings.append("vague terms require measurable qualification: " + ", ".join(vague))

    if "http" not in text and not has_section(found, ("sources", "references")):
        warnings.append("no source or reference found; verify external and repository context is traceable")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tickets", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    for path in args.tickets:
        if not path.is_file():
            print(f"ERROR {path}: file not found")
            failed = True
            continue

        errors, warnings = validate(path)
        status = "FAIL" if errors else "PASS"
        print(f"{status} {path}")
        for message in errors:
            print(f"  ERROR: {message}")
        for message in warnings:
            print(f"  WARN: {message}")
        failed = failed or bool(errors)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
