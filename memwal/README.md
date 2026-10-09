# Walrus Memory (MemWal): The Durable Layer

Walrus Memory, abbreviated MemWal, is the durable research-memory layer for
this project. It is the part that survives restarts, session boundaries, and
runtime changes. The runtimes (Hermes, OpenClaw) are interfaces onto this
layer; they are not the source of truth for research context.

## Identity

- Shared MemWal account id:
  `0xf60c01805404c1e3f9fb896e492ff362c0b9a9e4527e8eb4bfa7ffe54afebde8`
- Network: Sui **mainnet**.
- Relayer: `https://relayer.memory.walrus.xyz`

The account id above is a public account identifier, not a secret. Both
runtimes in this project read and write through this one account.

## What it stores

Walrus Memory stores durable facts and research records. For this project the
primary content is structured research records (target, hypothesis, test,
result, and so on). The field list is defined in
`../shared-memory/README.md`.

Memory is durable and searchable. A record written in one session is
retrievable by search in a later session, which is the property the whole
project depends on.

## Partitioning

Records are partitioned by **namespace**. Namespaces currently in use:

- `hermes/default` (primary profile; shared with OpenClaw in the demo)
- `hermes/cronbot`
- `hermes/cinanimon`
- `hermes/celty`

Private per-runtime memory is separated from shared project memory by
namespace only. Namespace separation is a routing convention, not a proven
access-control boundary. See `../shared-memory/permissions.md` for the honest
statement of what this does and does not enforce.

## Credentials

Credentials for the account live in a file outside this repository, created
by the one-time login flow:

- Credentials file: `~/.memwal/credentials.json` (owner-only permissions).

Do not paste credential values into any file in this repository. See
`../SECURITY.md` for the credential policy.

## How each runtime reaches it

- Hermes: attaches `memwal-mcp.js` as an MCP server with `--namespace <ns>`
  and `--prod`. See `../hermes/README.md`.
- OpenClaw: integrates through the plugin `@mysten-incubation/oc-memwal`. See
  `../openclaw/README.md`.

## Operational checks

- Connectivity: call `memwal_health` (Hermes) or the equivalent plugin health
  call (OpenClaw).
- Write confirmation: call `memwal_remember`, then `memwal_remember_status`.
- Retrieval: call `memwal_recall` with a query string.

## Notes

- The relayer URL and the account id are safe to publish; they are not
  secrets.
- Any credential material, tokens, or signing keys are secrets and must not
  appear here. Only the path to the credentials file belongs in this repo.
