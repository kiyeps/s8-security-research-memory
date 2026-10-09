# OpenClaw Runtime: Attaching the Same Memory

This document describes how the OpenClaw runtime attaches the same Walrus
Memory deployment that the Hermes runtime uses. OpenClaw is the second
runtime in this project, not a separate product.

- Runtime: OpenClaw.
- Telegram bot: `@choviybot`.
- Integration path: an OpenClaw plugin, published as the npm package
  `@mysten-incubation/oc-memwal`, installed and resolved by OpenClaw's plugin
  manager.

## How the attachment works

Where Hermes attaches MemWal as a generic MCP server, OpenClaw integrates it
through its own plugin. The plugin gives OpenClaw memory tools that talk to
the same Walrus Memory deployment.

Because both runtimes point at the same account and deployment, a fact
written by the Hermes runtime is a candidate for recall by the OpenClaw
runtime, subject to the namespace both are pointed at and the boundaries
described in `../shared-memory/permissions.md`.

## Config shape

```yaml
plugins:
  entries:
    "memory-memwal":
      enabled: true
      config:
        privateKey: "${MEMWAL_PRIVATE_KEY}"   # secret reference, never a literal
        accountId: "0xf60c01805404c1e3f9fb896e492ff362c0b9a9e4527e8eb4bfa7ffe54afebde8"
        serverUrl: "https://relayer.memory.walrus.xyz"
        defaultNamespace: "hermes/default"
  slots:
    memory: "memory-memwal"

hooks:
  allowConversationAccess: true
```

Two requirements that are easy to miss:

- `privateKey` must be resolved through the runtime's secret mechanism. It
  was historically possible to inline it; that is bad practice and not shown
  here.
- `hooks.allowConversationAccess: true` is mandatory in current OpenClaw
  versions. Without it, the plugin's conversation hooks are blocked and
  recall/capture silently do not run.

## Namespace choice

The OpenClaw runtime in the demonstration is pointed at `hermes/default`, the
same namespace as the primary Hermes profile. That alignment is what makes
cross-runtime sharing work: the plugin accepts its configured namespace and
rejects foreign ones, so the shared namespace must be configured on both
sides.

## Relation to the Hermes attachment

Both runtimes reach the same durable layer:

- Shared MemWal account on Sui mainnet (see `../memwal/README.md`).
- Same relayer: `https://relayer.memory.walrus.xyz`.

The difference is only the integration surface:

- Hermes: MCP server launched with `--namespace` and `--prod`.
- OpenClaw: the `@mysten-incubation/oc-memwal` plugin configured as above.

## Verifying the attachment

1. Confirm the plugin resolves.
2. Trigger a memory write through the bot and confirm it is accepted.
3. In the other runtime, recall the same fact by search.

The cross-runtime reproduction procedure, with its recorded results, is in
`../docs/reproduce-cross-runtime-test.md`.

## Current-state note

The recorded cross-runtime demonstration ran while this service was active.
At the time of writing, the OpenClaw service is stopped; the documentation
above describes the configuration as used during the demonstration, not a
claim about current uptime.
