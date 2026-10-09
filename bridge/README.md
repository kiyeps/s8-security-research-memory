# Bridge: Hermes to Walrus Memory

The bridge connects a Hermes runtime to Walrus Memory through three scripts
and two hook entries. It is additive: the runtime software is not modified.

## Files

| File | Hook / use | Purpose |
|---|---|---|
| `memwal_inject.py` | `pre_llm_call` | On the first turn of a session, recall top-k records and append a `[Walrus Memory]` block to the user message. Records a skip marker on later turns. |
| `memwal_mirror.py` | `post_tool_call` (`^memory$`) | Mirror qualifying single-action memory writes to the spool. Logs every skip with its reason. |
| `memwal_flush.py` | scheduled (every 12h) | Drain the spool: submit each entry through the MCP client, remove it only after the write lands. |
| `memwal_common.py` | library | Shared helpers: paths, logging, MCP invocation, context building. |
| `mcp_client.mjs` | library | Thin stdio client that drives the `memwal-mcp` server for one command. |

## Design rules

- **Never raise into the agent.** Every function degrades to "no memory
  context" on failure. A broken bridge must not break a turn.
- **Disk before network.** The mirror fsyncs each spool entry before any
  network call, so a crash cannot lose an accepted write.
- **Skips are logged, not silent.** Non-qualifying events are written to
  `logs/mirror.jsonl` with the reason.
- **Dry-run friendly.** `MEMWAL_BRIDGE_DRY_RUN=1` records entries without
  sending anything to the network.

## Install

Copy this directory to `~/.hermes/memwal-bridge/` and add the two hook
entries described in `../docs/installation.md`. Paths are configurable; see
`../docs/environment-configuration.md`.

## Logs and state

```text
~/.hermes/memwal-bridge/
  logs/mirror.jsonl     # one JSON line per mirror event (spooled / skipped)
  logs/inject.jsonl     # one JSON line per inject event (injected / skipped)
  logs/flush.jsonl      # drain runs
  state/pending.jsonl   # spooled, not yet confirmed
  state/synced.jsonl    # confirmed writes
  state/sessions/       # per-session injection markers
```

## Scope note

The mirror covers qualifying single-action writes (`add`, `replace`). It is
not a full replication layer; see `../docs/limitations.md`.
