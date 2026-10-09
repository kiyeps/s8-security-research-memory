# Namespace Model

All memory lives in one Walrus Memory account on Sui mainnet. Inside that
account, records are partitioned by **namespace**. A namespace is a routing
key: a runtime reads and writes within the namespace it was configured with.

Namespaces in use during the demonstration:

| Namespace | Runtime / workstream |
|---|---|
| `hermes/default` | Primary Hermes profile (Telegram `@Celiynbot`) and the OpenClaw runtime used for the shared-memory demonstration |
| `hermes/celty` | Second Hermes profile (separate workstream) |
| `hermes/cronbot` | Scheduled workstream |
| `hermes/cinanimon` | Separate workstream |

Each runtime is launched with exactly one namespace. The namespace is set at
launch (for the Hermes side, the `--namespace` flag on `memwal-mcp.js`) and is
not chosen per call.

## Private vs shared

- **Private per-runtime memory** lives inside a runtime-specific namespace.
  It is intended for one runtime and is not pulled into another runtime's
  ordinary recall.
- **Shared material** is placed in a namespace that more than one runtime
  points at. This is how the cross-runtime demonstration works: both runtimes
  were pointed at `hermes/default`.

The separation between private and shared is achieved by namespace only. It
is a routing convention, not a proven access-control boundary. Read
`../shared-memory/permissions.md` for exactly what that means.

## Structured record fields

Research records are written as structured facts using these fields:

| Field | Meaning |
|---|---|
| `TARGET` | The system or surface under test. |
| `PROJECT` | The project the work belongs to. |
| `REPO` | Source repository or bytecode source, if any. |
| `COMMIT` | Pinned commit, tag, or deployment reference. |
| `CANDIDATE` | The candidate issue or area being examined. |
| `HYPOTHESIS` | What is being claimed or suspected, stated testably. |
| `TEST` | The concrete test or check performed. |
| `RESULT` | The observed outcome. |
| `REPRO` | Steps or inputs to reproduce the observation. |
| `EVIDENCE` | Reference to evidence artifacts. |
| `DUPLICATE` | Whether the finding duplicates known or reported work. |
| `BLOCKER` | Anything preventing progress. |
| `DECISION` | The call made and why. |
| `NEXT_STEP` | The next concrete action. |

Every record should carry all fields. Fields that do not apply are written as
`n/a` with a short reason rather than omitted, so that absence is always
distinguishable from "never recorded".

Two sanitized examples are in `../examples/`. They use a fictional target and
contain no client material.

## How records are written and read

- Write: `memwal_remember` (single) or `memwal_remember_bulk` (many),
  followed by `memwal_remember_status` to confirm the write landed.
- Read: `memwal_recall` with a query.

A record written into a namespace is retrievable from any runtime that reads
the same namespace, provided the account and deployment match. See
`permissions.md` for the caveats on "provided".
