"""Quiet Dread — a one-line code review comment for make.fun.

The program holds a single review comment that approves a pull request
while carrying quiet existential dread, validates it against the
competition gate (one line, 1-140 characters, no control characters,
no leading/trailing whitespace, no double spaces), and writes it to
/output/entry.txt.
"""

import os
import sys

COMMENT = "Approved. The diff is small, the confidence is smaller, and the deploy window is already open."

DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 140


def validate(text):
    """Return a list of gate failures for `text` (empty means valid)."""
    problems = []
    if not text or not text.strip():
        problems.append("comment is empty or only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("comment must be a single line")
    if len(text) > MAX_CHARS:
        problems.append(f"comment is {len(text)} chars, over the {MAX_CHARS} limit")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        problems.append("comment contains control characters")
    if text != text.strip():
        problems.append("comment has leading or trailing whitespace")
    if "  " in text:
        problems.append("comment contains a double space")
    return problems


def main():
    failures = validate(COMMENT)
    if failures:
        for failure in failures:
            print(f"invalid entry: {failure}", file=sys.stderr)
        return 1
    destination = os.environ.get("QUIET_DREAD_OUTPUT", DEFAULT_OUTPUT)
    parent = os.path.dirname(destination)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(destination, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(COMMENT + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
