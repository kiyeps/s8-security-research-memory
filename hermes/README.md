# Hermes Runtime: Attaching Walrus Memory

This document describes how a Hermes Agent profile attaches Walrus Memory
(MemWal) as an MCP server so that research context is durable across
sessions.

The demonstration deployment runs multiple Hermes profiles on one host. The
primary profile is `default` (Telegram bot `@Celiynbot`), and its namespace
is `hermes/default`. Other profiles exist for separate workstreams; each uses
its own namespace and attaches memory the same way. The only difference
between profiles is the `--namespace` value passed to the MCP server binary.

## How the attachment works

Hermes attaches MemWal as an MCP server. The server is a node binary named
`memwal-mcp.js`, launched with two flags:

- `--namespace <ns>` selects which memory partition the runtime reads and
  writes.
- `--prod` selects the production Walrus Memory deployment.

`memwal-mcp.js` is installed by npm; a typical location after a global
install is:

```text
~/.memwal/runtime/0.0.14/node_modules/@mysten-incubation/memwal-mcp/dist/bin/memwal-mcp.js
```

Substitute the version you installed.

## Config shape

```yaml
mcp_servers:
  memwal:
    command: node
    args:
      - "~/.memwal/runtime/<version>/node_modules/@mysten-incubation/memwal-mcp/dist/bin/memwal-mcp.js"
      - "--namespace"
      - "hermes/default"
      - "--prod"
```

For a second profile, the only change is the `--namespace` value. The
credentials file (`~/.memwal/credentials.json`, created by the one-time login)
is located by the server itself; no credential value belongs in this config.

## Namespaces in use

- `hermes/default` (the primary profile and the shared demonstration)
- `hermes/cronbot`, `hermes/cinanimon`, `hermes/celty` (other workstreams)

Each namespace is a routing partition inside the same Walrus Memory account.
See `../shared-memory/README.md` for the namespace model and
`../shared-memory/permissions.md` for what namespace separation does and does
not enforce.

## MCP tools exposed

Observed tool names in this deployment:

- `memwal_health` -- connectivity check.
- `memwal_login` -- sign in and persist credentials.
- `memwal_logout` -- remove saved credentials.
- `memwal_remember` -- save a durable fact.
- `memwal_remember_bulk` -- save several facts in one call.
- `memwal_remember_status` -- confirm in-flight writes have landed.
- `memwal_recall` -- search memory for relevant facts.
- `memwal_analyze` -- extract memorable facts from a passage.
- `memwal_restore` -- recovery.

## The bridge on top of the attachment

In the demonstration deployment the MCP attachment is complemented by the
bridge in `../bridge/`: a read-side hook that injects a bounded recall on the
first turn of a session, and a write-side hook that mirrors qualifying local
memory writes. The bridge is optional; the MCP attachment works alone.

## Verifying the attachment

1. Confirm `memwal-mcp.js` resolves at the configured path.
2. Start the runtime and call `memwal_health`. A healthy response means the
   server is attached and reachable.
3. Call `memwal_remember` with a test fact, then `memwal_remember_status` to
   confirm the write landed.
4. Start a new session in the same namespace and call `memwal_recall` for the
   test fact. Recall succeeding here is the durability property this project
   relies on.

See `../docs/reproduce-cross-session-test.md` for the full procedure.
