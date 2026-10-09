# Reproduce: Cross-Runtime Sharing

This procedure demonstrates the project's strongest property: the same
durable research context moves between two independent runtimes through
Walrus Memory. It was run to completion on 2026-10-09, in both directions.

## Recorded results

| Date | Writer | Writer namespace | Reader | Reader namespace | Result |
|---|---|---|---|---|---|
| 2026-10-09 | Hermes | `hermes/default` | OpenClaw | `hermes/default` | PASS. A live OpenClaw turn recalled the marker and answered with it. |
| 2026-10-09 | OpenClaw | `hermes/default` | Hermes (fresh process) | `hermes/default` | PASS. The marker was recalled at rank one of the result set. |

Marker blob ids:

- Direction 1 (Hermes wrote): `XYR0_uRCwCxkRkBNPq59OaRScii9nPgO5LVeZramQfg`.
- Direction 2 (OpenClaw wrote): `tFAtE8GPE5MlHUcS-Omaot2jiHHGXAhduirAlj2E6O8`.

Both demonstrations ran while the OpenClaw service was running. See the note
at the bottom of this file.

## Preconditions

- Both runtimes configured and healthy.
- Both runtimes pointing at the same account and the same namespace
  (`hermes/default` in this deployment) and the same relayer
  (`https://relayer.memory.walrus.xyz`).

## Procedure

1. **Record the two namespaces.** Same namespace means sharing is expected.
   Different namespaces means recall may not cross them; that outcome is
   itself a result.

2. **Write a uniquely marked record from runtime A.** Use a distinct marker,
   then confirm the write landed and note the blob id:

   ```text
   TARGET: cross-runtime-probe
   CANDIDATE: probe-<timestamp>
   RESULT: marker-<uuid> written from runtime A to test cross-runtime recall
   <other record fields filled as appropriate>
   ```

3. **Recall the marker from runtime B.** Use the other runtime's memory
   surface and search with a distinctive token from the record. Expect the
   marker to be returned.

4. **Repeat in the other direction.** Write a marked record from runtime B
   and recall it from runtime A, including from a freshly started process.

5. **Record the outcome**: namespaces used, whether recall succeeded, and the
   exact query strings.

## Pass / fail

- **Pass**: a record written by one runtime is recalled by the other, with
  matching markers, under the documented namespace.
- **Fail**: no cross-runtime recall under any namespace configuration tried.
  Then the claim of cross-runtime sharing is not supported and must not be
  made.

## Current-state note

The recorded demonstrations above were captured while the OpenClaw service
was running. At the time of writing this document, the OpenClaw service is
stopped. The results stand as a recorded demonstration; they are not a
statement about the current health of that service. Re-running the procedure
requires starting it again.
