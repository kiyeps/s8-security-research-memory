# Walrus Memory Configuration

Two runtimes, two attachment mechanisms, one Walrus Memory account. All
credential values below are placeholders; the real values live outside this
repository and are never committed.

## Shared identity

- Account id: `0xf60c01805404c1e3f9fb896e492ff362c0b9a9e4527e8eb4bfa7ffe54afebde8`
  (a public account identifier, not a secret)
- Network: Sui mainnet
- Relayer: `https://relayer.memory.walrus.xyz`
- Credentials file: `~/.memwal/credentials.json` (owner-only permissions)

## Hermes: MCP server entry

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

The `--namespace` value is fixed at server launch; the runtime does not
choose it per call. One runtime, one namespace.

## Hermes: bridge hooks

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

## OpenClaw: plugin entry

OpenClaw attaches the same memory through the `@mysten-incubation/oc-memwal`
plugin:

```yaml
plugins:
  entries:
    "memory-memwal":
      enabled: true
      config:
        privateKey: "${MEMWAL_PRIVATE_KEY}"   # a secret reference, not a literal
        accountId: "0xf60c01805404c1e3f9fb896e492ff362c0b9a9e4527e8eb4bfa7ffe54afebde8"
        serverUrl: "https://relayer.memory.walrus.xyz"
        defaultNamespace: "hermes/default"    # the namespace shared for the demo
  slots:
    memory: "memory-memwal"

hooks:
  allowConversationAccess: true   # required; without it the plugin's hooks are blocked
```

Notes:

- `privateKey` must be a secret reference resolved from the environment or a
  secret store. Never inline the literal value in configuration that could be
  committed.
- `allowConversationAccess` is mandatory. Without it the plugin's
  before-model and before-prompt hooks are blocked, and recall/capture do not
  run.
- `defaultNamespace` selects the shared partition. The plugin's own gate
  accepts the configured namespace and rejects foreign ones.

## Where credentials live

| Runtime | Credential | Reference |
|---|---|---|
| Hermes | MCP server credentials | `~/.memwal/credentials.json` |
| OpenClaw | Plugin private key | environment / secret store, referenced by name only |

No credential value appears in this repository, in any example, or in any
log snippet that ships with it.
