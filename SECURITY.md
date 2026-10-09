# Security Policy

## Scope

This repository contains bridge code, configuration shapes with placeholders,
documentation, and sanitized examples. It contains no credentials, no client
material, and no descriptions of unreported security findings.

## Credential handling rules

- No credential value is committed to this repository, ever. Not in code, not
  in configuration examples, not in documentation, not in commit messages.
- Credentials are referenced by path or by environment variable name only.
  The MemWal credential file lives outside the repository, in the operator's
  home directory, with owner-only permissions.
- Configuration examples use placeholders such as
  `<MEMWAL_CREDENTIALS_PATH>` and `<YOUR_API_KEY>`. If you fork this
  repository, keep it that way.
- Treat anything written to memory as potential publication material: memory
  records are durable and stored under a shared account. Keep secrets out of
  memory records entirely.

## What must never appear here

- Private keys, seed phrases, API keys, session tokens, cookies.
- Absolute paths from a contributor's machine.
- Raw logs, captures, or traces from real targets.
- Unreported security findings, private source fragments, or client material.

## The scanner

This repository includes the scanner that gates its own publication
(`tools/secret_scan/`). Run it before any push:

```bash
python3 tools/secret_scan/scan_secrets.py .
```

The scanner reports two things:

- `control fired`: its own positive control. This proves the scanner can
  actually find a planted credential. If the control does not fire, treat the
  scan as failed even when no findings are reported.
- findings: text matching the fatal patterns. A scan that reports findings
  must not be pushed.

## Reporting a problem with this repository

For a problem in this repository itself, open a GitHub issue or a private
security advisory on the repository. Do not include credential values or
private material in the report.

## Rotation

If a credential is ever committed by accident: rotate it first, then remove it
from the tree. Rewriting history is not a substitute for rotation.
