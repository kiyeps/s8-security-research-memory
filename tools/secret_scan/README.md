# Secret Scanner

The scanner used to gate this repository's own publication. It walks a tree,
matches every file against a small set of high-signal secret patterns, and
prints a verdict.

## Usage

```bash
python3 scan_secrets.py <root>
```

Run it from anywhere; it scans `<root>` recursively.

## Reading the output

```text
positive control fired: ['json-privatekey']
files scanned: 32
fatal hits: 0
```

- `positive control fired`: the scanner planted a synthetic credential and
  found it. This proves the scanner can detect credentials at all. If this
  line reports `SCAN_ABORT` instead, treat the scan as failed even with zero
  findings; a scanner that cannot find a planted key cannot be trusted to
  say a tree is clean.
- `files scanned`: how many files were read.
- `fatal hits`: credentials found. Any hit must be resolved before the tree
  leaves the machine.

Exit codes: `0` clean, `1` at least one fatal hit, `2` the positive control
did not fire (scan unreliable).

## Design notes

- `secret_patterns.py` holds the patterns. Fatal patterns match populated
  credential shapes: a 40+ hex value after a `privateKey` assignment, a
  populated bearer token, provider key prefixes. A bare field name does not
  match.
- Public identifiers are deliberately allowed, for example a Sui account
  address (0x plus 64 hex) or a blob id. Those are not credentials.
- Standard library only. This is a publication gate, not a full secret
  detection suite; use it with review, not instead of review.
