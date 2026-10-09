#!/usr/bin/env python3
"""Secret scan for a staged deliverable tree.

Fatal patterns are credential SHAPES. Public identifiers such as a Sui
address (0x + 64 hex) or an object id are not credentials and are allowed.
A positive control must fire, otherwise the scan aborts as unreliable.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from secret_patterns import CONTROL, FATAL, scan_text  # noqa: E402


def main():
    root = sys.argv[1]
    control_hits = scan_text(CONTROL)
    if not control_hits:
        print("SCAN_ABORT positive control did not fire")
        return 2
    print("positive control fired:", [h[0] for h in control_hits])

    fatal = 0
    files = 0
    for dirpath, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for n in names:
            if n.endswith(".pyc"):
                continue
            p = os.path.join(dirpath, n)
            rel = os.path.relpath(p, root)
            files += 1
            try:
                with open(p, "r", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            hits = scan_text(text)
            if hits:
                fatal += len(hits)
                print("HIT", rel, hits[:3])
    print("files scanned:", files)
    print("fatal hits:", fatal)
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
