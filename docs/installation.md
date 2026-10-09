# Installation

Four parts: install the runtime, install the Walrus Memory tooling, wire the
bridge, and verify. Assumptions: a Linux host, Node.js and Python 3 on
`PATH`, and a Hermes installation whose home directory is `~/.hermes`.

## 1. Walrus Memory tooling

Install the MCP server used by both the bridge and the runtime:

```bash
npm install -g @mysten-incubation/memwal-mcp
```

Log in once so the credentials file is created. Either call `memwal_login`
from the runtime, or run the server binary directly and follow its login
prompt. Credentials land in `~/.memwal/credentials.json` with owner-only
permissions. That file is never committed anywhere.

## 2. Attach MemWal to the Hermes runtime

Add the MCP server entry to the runtime configuration:

```yaml
mcp_servers:
  memwal:
    command: node
    args:
      - "~/.memwal/runtime/0.0.14/node_modules/@mysten-incubation/memwal-mcp/dist/bin/memwal-mcp.js"
      - "--namespace"
      - "hermes/default"
      - "--prod"
```

Replace `0.0.14` with the installed version. The `--namespace` value is the
partition this runtime reads and writes. Restart the runtime so the server is
spawned.

## 3. Install the bridge

Copy `bridge/` to `~/.hermes/memwal-bridge/` on the target host. The scripts
read their paths from environment variables with sane defaults; see
`environment-configuration.md` for the full list.

Add the hook entries to the runtime configuration:

```yaml
hooks:
  pre_llm_call:
    - command: python3 ~/.hermes/memwal-bridge/memwal_inject.py
      timeout: 20
  post_tool_call:
    - command: python3 ~/.hermes/memwal-bridge/memwal_mirror.py
      matcher: "^memory$"
      timeout: 20
```

Hook fields vary by runtime version; the important parts are the event, the
command, and the `^memory$` matcher on the write side. Hooks require opt-in:
set `hooks_auto_accept: true` in the runtime configuration, or pass the
equivalent acceptance flag at start. Without opt-in a non-interactive
gateway silently skips hook registration.

Hooks register once per process at gateway startup. Editing this
configuration does not affect an already-running gateway.

## 4. Schedule the drain

Add a schedule entry that runs the drain every 12 hours:

```cron
17 3,15 * * * python3 /home/<user>/.hermes/memwal-bridge/memwal_flush.py >> /home/<user>/.hermes/memwal-bridge/logs/flush-cron.log 2>&1
```

The drain is silent when the spool is empty.

## 5. Verify

1. Start the runtime. Confirm in its log that the hooks registered.
2. Call `memwal_health`. Expect a healthy result.
3. Write a test fact with `memwal_remember`, then confirm with
   `memwal_remember_status`.
4. Run the cross-session procedure in
   `reproduce-cross-session-test.md`.
