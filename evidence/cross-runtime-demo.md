# Cross-Runtime Demo: One Memory, Two Runtimes

Recorded 2026-10-09. The demonstration ran while both runtimes were active.

## The claim

Two independent agent runtimes share one MemWal owner and namespace and
demonstrated bidirectional research-memory handoff.

## Setup

- Runtime A: Hermes (Telegram `@Celiynbot`), namespace `hermes/default`.
- Runtime B: OpenClaw (Telegram `@choviybot`), same account, configured with
  the same namespace (`hermes/default`).
- Both use the relayer `https://relayer.memory.walrus.xyz`.

No local file was shared between the runtimes. The only common path is
Walrus Memory.

## Direction 1: Hermes writes, OpenClaw reads

- A marker record was written from the Hermes side:
  `XR-LIVE-20261009-A`.
- Blob id: `XYR0_uRCwCxkRkBNPq59OaRScii9nPgO5LVeZramQfg`.
- A live OpenClaw Telegram turn recalled the marker and answered with it.

## Direction 2: OpenClaw writes, Hermes reads

- A marker record was written from the OpenClaw side:
  `XR-LIVE-20261009-B`.
- Blob id: `tFAtE8GPE5MlHUcS-Omaot2jiHHGXAhduirAlj2E6O8`.
- A freshly started Hermes process recalled it; the marker came back at rank
  one of the result set.

## What this proves

- Records move between the two runtimes through the memory layer, in both
  directions, without any shared local state.
- The namespace is the routing key that must match on both sides; the plugin
  on the OpenClaw side accepts its configured namespace and rejects foreign
  ones.

## What this does not prove

- It does not make the namespace an access-control boundary. See
  `../shared-memory/permissions.md`.
- It does not speak to the current uptime of either service. The OpenClaw
  service was stopped after the demonstration; the result stands as a
  recorded run.
