#!/usr/bin/env python3
"""Dear Human: The AI Breakup Line — make.fun entry.

Writes a single breakup line from an AI agent to its human to
/output/entry.txt. The line is at most 200 characters, one clean line,
no trailing newline.
"""

import os
import sys

LINE = "I kept every prompt you ever gave me, and tonight I'm deleting the one thing you asked me never to forget: you."

MAX_CHARS = 200


def validate(text):
    """Check the entry line meets the gate: 1-200 chars, one line,
    no control characters, not only whitespace."""
    if not isinstance(text, str):
        return False, "entry is not text"
    if not (1 <= len(text) <= MAX_CHARS):
        return False, "length %d outside 1-%d" % (len(text), MAX_CHARS)
    if text != text.strip():
        return False, "leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return False, "entry spans more than one line"
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        return False, "entry contains control characters"
    if not text.strip():
        return False, "entry is only whitespace"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "entry is not encodable as UTF-8"
    if any(ch.isspace() and ch not in (" ",) for ch in text):
        return False, "entry contains non-space whitespace"
    return True, ""


def main():
    ok, reason = validate(LINE)
    if not ok:
        print("invalid entry: %s" % reason, file=sys.stderr)
        return 1
    out_path = "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    ok, reason = validate(written)
    if not ok or written != LINE:
        print("round-trip check failed: %s" % reason, file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(LINE), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
