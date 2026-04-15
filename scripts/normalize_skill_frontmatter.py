#!/usr/bin/env python3
"""Normalize SKILL.md frontmatter to the required minimal schema.

Keeps only `name` and `description`, which is the shape expected by the
skill-creator contract used across this repository.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from audit_skills import parse_frontmatter, split_frontmatter


REQUIRED_KEYS = ("name", "description")


def normalize_file(path: Path) -> bool:
    text = path.read_text()
    frontmatter_text, body = split_frontmatter(text)
    if not frontmatter_text:
        raise ValueError("missing YAML frontmatter")

    frontmatter = parse_frontmatter(frontmatter_text)
    missing = [key for key in REQUIRED_KEYS if not frontmatter.get(key)]
    if missing:
        raise ValueError(f"missing required frontmatter keys: {', '.join(missing)}")

    normalized = (
        "---\n"
        f"name: {json.dumps(str(frontmatter['name']))}\n"
        f"description: {json.dumps(str(frontmatter['description']))}\n"
        "---\n"
        f"{body}"
    )

    if normalized == text:
        return False

    path.write_text(normalized)
    return True


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: normalize_skill_frontmatter.py <SKILL.md> [...]", file=sys.stderr)
        return 1

    changed = 0
    for raw_path in argv[1:]:
        path = Path(raw_path)
        try:
            updated = normalize_file(path)
        except Exception as exc:  # pragma: no cover - CLI error path
            print(f"error: {path}: {exc}", file=sys.stderr)
            return 1

        if updated:
            changed += 1
            print(f"normalized {path}")

    if changed == 0:
        print("no changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
