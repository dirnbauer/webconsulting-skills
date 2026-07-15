#!/usr/bin/env python3
"""Validate Markdown and reStructuredText architecture decision records."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ADR_ID = re.compile(r"\bADR[-_ ]?(\d+)\b", re.IGNORECASE)
ADR_TITLE = re.compile(r"^(?:#{1,6}\s+)?ADR[-_ ]?(\d+)\s*:", re.IGNORECASE | re.MULTILINE)
GIT_HASH = re.compile(r"(?<![0-9a-f])([0-9a-f]{7,40})(?![0-9a-f])", re.IGNORECASE)
STATUS = re.compile(
    r"\b(Proposed|Accepted|Rejected|Deprecated|Superseded)\b",
    re.IGNORECASE,
)
REQUIRED = ("status", "context", "decision", "consequences")


@dataclass(frozen=True)
class Heading:
    name: str
    line: int


def normalize_heading(value: str) -> str:
    value = re.sub(r"[`*_:#]", "", value).strip().lower()
    return re.sub(r"\s+", " ", value)


def markdown_headings(lines: list[str]) -> list[Heading]:
    result: list[Heading] = []
    for index, line in enumerate(lines):
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            result.append(Heading(normalize_heading(match.group(1)), index))
    return result


def rst_headings(lines: list[str]) -> list[Heading]:
    result: list[Heading] = []
    adornment = re.compile(r"^([=\-~\"'^#*+])\1{2,}\s*$")
    for index in range(len(lines) - 1):
        title = lines[index].strip()
        underline = lines[index + 1].strip()
        if title and adornment.fullmatch(underline) and len(underline) >= len(title):
            result.append(Heading(normalize_heading(title), index))
    return result


def section_body(lines: list[str], headings: list[Heading], name: str) -> str:
    for position, heading in enumerate(headings):
        if heading.name != name:
            continue
        start = heading.line + 1
        if start < len(lines) and re.fullmatch(r"[=\-~\"'^#*+]{3,}\s*", lines[start]):
            start += 1
        end = headings[position + 1].line if position + 1 < len(headings) else len(lines)
        return "\n".join(lines[start:end]).strip()
    return ""


def adr_number(path: Path, text: str) -> int | None:
    match = ADR_ID.search(path.stem) or ADR_TITLE.search(text)
    return int(match.group(1)) if match else None


def git_commit_exists(repository: Path, revision: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repository), "cat-file", "-e", f"{revision}^{{commit}}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def validate_file(
    path: Path,
    require_history: bool,
    git_repository: Path | None,
    max_line_length: int,
    allow_scoring: bool,
) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = markdown_headings(lines) if path.suffix.lower() == ".md" else rst_headings(lines)
    names = {heading.name for heading in headings}
    errors: list[str] = []

    for required in REQUIRED:
        if required not in names:
            errors.append(f"missing '{required}' section")

    status_body = section_body(lines, headings, "status")
    if "status" in names and not STATUS.search(status_body):
        errors.append("status is not Proposed, Accepted, Rejected, Deprecated, or Superseded")

    history_name = next((name for name in ("history evidence", "evidence") if name in names), None)
    if require_history and history_name is None:
        errors.append("retrospective validation requires a history evidence section")

    if history_name is not None:
        history = section_body(lines, headings, history_name)
        hashes = sorted(set(GIT_HASH.findall(history)))
        if require_history and not hashes:
            errors.append("history evidence contains no abbreviated or full Git commit hash")
        if git_repository is not None:
            for revision in hashes:
                if not git_commit_exists(git_repository, revision):
                    errors.append(f"history references unknown Git commit {revision}")

    if not allow_scoring and re.search(r"\b(net|weighted)\s+score\b", text, re.IGNORECASE):
        errors.append("contains an unexplained net or weighted score")

    if max_line_length > 0:
        for line_number, line in enumerate(lines, start=1):
            if len(line) > max_line_length:
                errors.append(
                    f"line {line_number} is {len(line)} characters; limit is {max_line_length}"
                )

    number = adr_number(path, text)
    if number is None:
        errors.append("cannot determine numeric ADR identifier")
        number = -1

    return number, errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="ADR file or directory")
    parser.add_argument("--require-history", action="store_true")
    parser.add_argument("--git-repo", type=Path)
    parser.add_argument("--max-line-length", type=int, default=0)
    parser.add_argument("--allow-scoring", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    candidates = [args.path] if args.path.is_file() else sorted(args.path.rglob("*"))
    files = [path for path in candidates if path.suffix.lower() in {".md", ".rst"}]
    files = [
        path
        for path in files
        if ADR_ID.search(path.stem)
        or ADR_TITLE.search(path.read_text(encoding="utf-8"))
    ]

    if not files:
        print(f"No numbered ADR files found below {args.path}", file=sys.stderr)
        return 1

    numbers: dict[int, Path] = {}
    failures = 0
    for path in files:
        number, errors = validate_file(
            path,
            args.require_history,
            args.git_repo,
            args.max_line_length,
            args.allow_scoring,
        )
        if number in numbers:
            errors.append(f"duplicates ADR-{number:03d} from {numbers[number]}")
        elif number >= 0:
            numbers[number] = path

        if errors:
            failures += 1
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"OK ADR-{number:03d} {path}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
