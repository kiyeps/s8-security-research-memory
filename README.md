# Walrus Memory Bridge for Hermes and OpenClaw

Durable research memory for agent runtimes, backed by Walrus Memory (MemWal)
on Sui mainnet. This repository is the bridge layer for a security-research
assistant whose working context survives session boundaries and runtime
changes.

**Two independent agent runtimes share one MemWal owner and namespace and
demonstrated bidirectional research-memory handoff.**

## What this repository contains

- The bridge code that connects the Hermes runtime to Walrus Memory: an MCP
  client wrapper, two shell hooks, and a drain job.
- Configuration shapes for both runtimes, with credentials referenced by
  path or by environment only.
- Reproducible test procedures for the two properties the project relies on:
  cross-session durability and cross-runtime sharing. Both are recorded as
  run, with results.
- The secret scanner used to gate this repository's own publication.

## What this repository does not contain

- No credentials, tokens, or keys. Ever. See `SECURITY.md`.
- No raw logs, captures, or internal paths.
- No unreported security findings and no client material.
- No claim that a namespace is an access-control boundary. It is not, and
  `shared-memory/permissions.md` says so plainly.

## How it works, in one paragraph

Each runtime attaches Walrus Memory. Hermes attaches it as an MCP server
(`memwal-mcp.js`, launched with `--namespace` and `--prod`) and additionally
loads two shell hooks: one injects a bounded recall result into the first
turn of a session, and one mirrors qualifying local memory writes to Walrus
after the fact. OpenClaw attaches the same memory through the
`@mysten-incubation/oc-memwal` plugin. Both runtimes point at the same
account, so a record written by one is a candidate for recall by the other.

```text
Telegram
  -> Hermes gateway (profile: default, bot: @Celiynbot)
     write path: memory tool -> post-tool hook (memwal_mirror.py) -> spool
                 -> memwal-mcp -> relayer -> Walrus mainnet -> blob id
     read path:  pre-turn hook (memwal_inject.py) -> recall (top-k)
                 -> "[Walrus Memory]" block appended to the API-bound message
     drain:      memwal_flush.py on a schedule retries anything still spooled
  -> OpenClaw (bot: @choviybot)
     plugin: @mysten-incubation/oc-memwal (same account, same namespace)
```

## Layout

| Path | Contents |
|---|---|
| `bridge/` | The Hermes-side bridge: hooks, drain job, MCP client wrapper. |
| `hermes/` | How the Hermes runtime attaches memory. |
| `openclaw/` | How the OpenClaw runtime attaches the same memory. |
| `memwal/` | The shared MemWal account and how to reach it. |
| `shared-memory/` | Namespace model, record fields, and the honest limits. |
| `docs/` | Architecture, setup, configuration, tests, limitations. |
| `evidence/` | Safe and publishable evidence summaries. No raw logs. |
| `examples/` | Two sanitized example records with a fictional target. |
| `tools/secret_scan/` | The scanner used to gate this repository. |

## Verified properties

| Property | Recorded result | Where |
|---|---|---|
| Cross-session durability | PASS, 2026-10-09 | `docs/reproduce-cross-session-test.md` |
| Cross-runtime sharing | PASS, 2026-10-09, both directions | `evidence/cross-runtime-demo.md` |
| Live mainnet write with a blob id | PASS, 2026-10-09 | `evidence/mainnet-proof.md` |
| Automatic mirror of every local write | PARTIAL, bounded with logged skips | `docs/limitations.md` |

## Status at the time of writing

- The Hermes runtime bridge was active and verified end to end on
  2026-10-09.
- The OpenClaw demonstration was captured while the OpenClaw service was
  running. The service is stopped at the time of writing; nothing here should
  be read as a statement that it is currently healthy.

## Start here

- New to the project: `docs/architecture.md`.
- Setting it up: `docs/installation.md`.
- Checking the claims: read `docs/limitations.md` first, then the two
  reproduce documents under `docs/`.

## Security

Credentials are never committed. The repository ships the same scanner used
to gate its publication. See `SECURITY.md`.
