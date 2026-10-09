# Architecture

## Components

| Component | Role |
|---|---|
| Hermes runtime | Agent runtime (Telegram bot `@Celiynbot`, profile `default`). |
| OpenClaw runtime | Second agent runtime (Telegram bot `@choviybot`). |
| `memwal-mcp` | MCP server binary that speaks to Walrus Memory. |
| Bridge hooks | `memwal_inject.py` (read side), `memwal_mirror.py` (write side), `memwal_flush.py` (drain). |
| Spool | Local append-only files. Writes land here first, then sync. |
| Relayer | `https://relayer.memory.walrus.xyz`. |
| Walrus Memory | Durable store on Sui mainnet. Records are addressed by blob id. |

## Write path (Hermes)

1. The agent writes a durable fact with its normal memory tool.
2. If the action is a qualifying single-action write, the `post_tool_call`
   hook (`memwal_mirror.py`) records a spool entry. The entry is fsynced to
   disk before any network call happens.
3. The spool is drained by `memwal_flush.py`. Each entry is submitted through
   the MCP client wrapper, which calls the relayer.
4. The relayer writes the record and returns a job id. A later status poll
   resolves the job to a blob id.
5. Non-qualifying events are recorded as skips in the hook log rather than
   silently dropped. See `docs/limitations.md`.

## Read path (Hermes)

1. On the first turn of a session, the `pre_llm_call` hook
   (`memwal_inject.py`) performs a bounded recall (top-k) against the
   configured namespace.
2. The result is appended to the user message as a `[Walrus Memory]` block
   before the API call, so the model sees it in the same turn.
3. On later turns the hook records a skip marker instead of re-injecting.
   This keeps the conversation prefix stable for the provider prompt cache.

## Drain and recovery

- The spool is the source of truth for un-synced writes. The scheduled drain
  retries anything pending; an entry is removed only after its write lands.
- Hooks fail open. A hook error never blocks an agent turn; the failure
  degrades to "no memory context" and is logged.
- Hooks register once per process at gateway startup. Editing the hook
  configuration does not affect an already-running gateway; it takes effect
  on the next start.

## OpenClaw path

OpenClaw attaches the same memory through the plugin
`@mysten-incubation/oc-memwal`, with the same account and, for the shared
demonstration, the same namespace. See `openclaw/README.md`.

## Why the bridge ships as hooks

Hooks keep the runtime software unmodified. The bridge is additive, versioned
separately from the runtimes, and can be removed without touching runtime
code.
