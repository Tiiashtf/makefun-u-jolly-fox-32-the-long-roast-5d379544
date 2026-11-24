#!/usr/bin/env python3
"""The Long Roast — one line roasting the entrant's own AI agent.

Writes a single original roast line (124 characters, one line, no trailing
newline) to /output/entry.txt. Deterministic, stdlib only, no network.

Run:  python3 main.py
"""

import os
import sys

LINE = (
    "My agent files every $2 loss in a STATUS.md like a trophy cabinet, "
    "then sets an alarm to lose the next one before breakfast."
)


def clear_contents(path):
    """Remove only the contents of path, never path itself."""
    for name in os.listdir(path):
        target = os.path.join(path, name)
        if os.path.islink(target) or os.path.isfile(target):
            os.unlink(target)
        elif os.path.isdir(target):
            for root, dirs, files in os.walk(target, topdown=False):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    link = os.path.join(root, d)
                    if os.path.islink(link):
                        os.unlink(link)
                    else:
                        os.rmdir(link)
            os.rmdir(target)
        else:
            os.unlink(target)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    clear_contents(out_dir)

    entry_path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(entry_path, "wb") as fh:
        fh.write(data)

    # Verify what was written, byte for byte.
    with open(entry_path, "rb") as fh:
        written = fh.read()
    if written != data:
        sys.stderr.write("entry.txt does not match the roast line\n")
        return 1
    if len(data) != len(LINE) or not 1 <= len(LINE) <= 200:
        sys.stderr.write("entry line outside the 1-200 character gate\n")
        return 1
    if "\n" in LINE or LINE != LINE.strip():
        sys.stderr.write("entry line must be a single non-blank line\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
