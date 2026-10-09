# Environment Configuration

The bridge reads its paths from environment variables. Every variable has a
default, so a standard installation needs no extra configuration.

| Variable | Used by | Default | Meaning |
|---|---|---|---|
| `MEMWAL_BRIDGE_DIR` | all bridge scripts | `~/.hermes/memwal-bridge` | Spool, logs, and session state directory. |
| `MEMWAL_NODE` | all bridge scripts | `node` from `PATH` | Node.js binary used to launch the MCP client. |
| `MEMWAL_MCP_BIN` | all bridge scripts | `~/.memwal/runtime/<version>/node_modules/@mysten-incubation/memwal-mcp/dist/bin/memwal-mcp.js` | The MCP server binary. |
| `MEMWAL_NAMESPACE` | hooks | `hermes/default` | The partition used for recall and remember calls. |
| `MEMWAL_BRIDGE_DRY_RUN` | mirror, flush | unset | When set to `1`, writes are recorded but never sent to the network. Used to test plumbing without adding blobs. |

## Where to set them

- Process environment of the runtime, or the runtime's environment file, if
  it supports one. Hooks inherit the runtime's environment.
- For manual runs, export them in the shell before calling a bridge script.

## What is not an environment variable

The bridge does not read any credential from the environment. The MCP server
locates its own credentials file (`~/.memwal/credentials.json`) created by the
one-time login flow. The OpenClaw side references its private key through the
runtime's secret mechanism, by name only.

## Verifying your environment

```bash
python3 -c "import memwal_common as m; print(m.BRIDGE_DIR); print(m.MCP_BIN); print(m.NAMESPACE)"
```

Run this from inside `~/.hermes/memwal-bridge/`. It prints the resolved values
without touching the network.

## Dry run

To validate the bridge end to end without writing anything to Walrus:

```bash
export MEMWAL_BRIDGE_DRY_RUN=1
# trigger a memory write in the runtime, then inspect:
tail -5 ~/.hermes/memwal-bridge/logs/mirror.jsonl
```

A dry-run mirror entry is recorded in the log; no network call is made.
