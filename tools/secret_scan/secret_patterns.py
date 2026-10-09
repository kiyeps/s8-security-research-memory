#!/usr/bin/env python3
"""Single source of truth for credential-shape detection.

Imported by scan_secrets.py (staging gate), verify_pack.py (archive gate) and
any future builder step, so the scan verdict and the build gate can never
disagree about what counts as a credential.

Fatal patterns are credential SHAPES. Public identifiers are not credentials:
a Sui address (0x + 64 hex), an object id, a blob id, a job id, a uuid and a
sha256 digest are all allowed to appear in a deliverable.

CONTROL is a synthetic value that MUST match at least one pattern. Every
consumer refuses to report a verdict if the control does not fire, because a
silent detector that matches nothing looks identical to a clean tree.
"""
import re

FATAL = [
    ("sui-private-key", re.compile(r"suiprivkey1[0-9a-z]{20,}")),
    ("json-privatekey", re.compile(r'"privateKey"\s*:\s*"[0-9a-fA-F]{40,}"')),
    ("delegate-key", re.compile(r'delegatePrivateKey"\s*:\s*"[0-9a-fA-F]{40,}"')),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{20,}")),
    ("jr-key", re.compile(r"\bjr_cup_[A-Za-z0-9]{10,}")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.")),
    ("bearer", re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}")),
    ("telegram-token", re.compile(r"\b\d{8,12}:AA[A-Za-z0-9_-]{30,}")),
]

# Synthetic, non-functional. Built from repeated nibbles so no real key is
# ever embedded in the tooling itself.
CONTROL = 'zz-"privateKey": "' + ("a1b2c3d4" * 8) + '"'


def scan_text(text):
    """Return [(pattern_name, matched_prefix), ...] for one text blob."""
    hits = []
    for name, rx in FATAL:
        for m in rx.finditer(text):
            hits.append((name, m.group(0)[:12]))
    return hits


def control_fires():
    return bool(scan_text(CONTROL))
