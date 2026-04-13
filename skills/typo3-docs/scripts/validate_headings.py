#!/usr/bin/env python3
"""
Validate TYPO3 RST heading hierarchy.

TYPO3 heading convention:
  h1: = above AND below (overline)
  h2: = below only
  h3: - below only
  h4: ~ below only
  h5: " below only
  h6: ' below only

Usage: python3 validate_headings.py <file.rst>
Exit code 0 = no issues, output contains error lines if any.
"""

import sys

EXPECTED_ORDER = ["=", "-", "~", '"', "'"]
UNDERLINE_CHARS = set(EXPECTED_ORDER + ["^", "#", "\\"])


def _is_adornment(line):
    """Return True if line is an RST adornment (all same char, length >= 3)."""
    return (
        bool(line)
        and len(line) >= 3
        and all(c == line[0] for c in line)
        and line[0] in UNDERLINE_CHARS
    )


def parse_headings(lines):
    headings = []
    i = 0
    # Track which lines are already consumed as part of an overline heading
    consumed = set()
    while i < len(lines):
        line = lines[i].rstrip()
        if _is_adornment(line) and i not in consumed:
            char = line[0]
            # Check if this is an overline (title) or underline
            if i + 2 < len(lines):
                next_line = lines[i + 1].rstrip()
                next_next = lines[i + 2].rstrip()
                if (
                    next_line
                    and not _is_adornment(next_line)
                    and _is_adornment(next_next)
                    and next_next[0] == char
                    and len(line) >= len(next_line.strip())
                    and len(next_next) >= len(next_line.strip())
                ):
                    # Overline+underline = title (h1), skip all three lines
                    headings.append(("h1", char, next_line, i + 1))
                    consumed.add(i + 2)
                    i += 3
                    continue
            # Underline only - check previous line for title text
            if i > 0 and i - 1 not in consumed:
                prev = lines[i - 1].rstrip()
                if prev and not _is_adornment(prev) and len(line) >= len(prev.strip()):
                    headings.append(("section", char, prev, i))
        i += 1
    return headings


def check_headings(headings):
    errors = []
    sections = [h for h in headings if h[0] == "section"]

    # Check 1: First section heading must use = (h2)
    if sections and sections[0][1] != "=":
        char = sections[0][1]
        title = sections[0][2]
        lineno = sections[0][3]
        errors.append(
            f'  L{lineno + 1}: "{title}" - first section heading '
            f'must use "=" (h2), not "{char}"'
        )

    # Check 2: Detect nesting violations (e.g. h4 directly under h2, skipping h3)
    depth_stack = []
    for kind, char, title, lineno in headings:
        if kind == "h1":
            depth_stack = []
            continue
        if char not in EXPECTED_ORDER:
            errors.append(
                f'  L{lineno + 1}: "{title}" uses non-standard underline char "{char}"'
            )
            continue
        char_idx = EXPECTED_ORDER.index(char)
        # Pop stack back to find where this heading fits
        while depth_stack and depth_stack[-1] >= char_idx:
            depth_stack.pop()
        # Check for skipped levels
        if depth_stack:
            parent_idx = depth_stack[-1]
            if char_idx > parent_idx + 1:
                skipped = EXPECTED_ORDER[parent_idx + 1]
                errors.append(
                    f'  L{lineno + 1}: "{title}" uses "{char}" '
                    f"(h{char_idx + 2}) directly under "
                    f'"{EXPECTED_ORDER[parent_idx]}" (h{parent_idx + 2}), '
                    f'skipping "{skipped}" (h{parent_idx + 3})'
                )
        depth_stack.append(char_idx)

    return errors


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.rst>", file=sys.stderr)
        sys.exit(2)

    filepath = sys.argv[1]
    with open(filepath) as f:
        lines = f.readlines()

    headings = parse_headings(lines)
    if not headings:
        sys.exit(0)

    errors = check_headings(headings)
    for e in errors:
        print(e)


if __name__ == "__main__":
    main()
