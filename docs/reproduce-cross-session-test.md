# Reproduce: Cross-Session Durability

This procedure demonstrates the property the project relies on: a fact
written in one session is retrievable in a later session, because it lives in
Walrus Memory rather than in the session.

Run this inside a single namespace. It does not exercise cross-runtime
sharing (that is `reproduce-cross-runtime-test.md`).

## Recorded result

- Result: **PASS, 2026-10-09.**
- Marker write: job `212de1b5-f4d7-4c9b-ac9d-1ff070e60df5`, blob
  `Htzm9C3BsvyGjyralT8ya_YEdwffE_S_0x-pldjs4zM`.
- Recall: a fresh session retrieved the record; the first turn of that
  session received the injected `[Walrus Memory]` block, and a direct recall
  returned the record at rank one.
- Note: the automated recall for one query returned other records first; the
  marker surfaced on a direct recall. See `limitations.md`, item 2.

## Preconditions

- A configured runtime in one namespace, for example `hermes/default`.
- `memwal_health` returns healthy.
- The relayer `https://relayer.memory.walrus.xyz` is reachable.

## Procedure

1. **Confirm health.** Call `memwal_health`. Expect a healthy result.

2. **Write a uniquely marked fact in session 1.** Call `memwal_remember` with
   a record whose content includes a unique marker:

   ```text
   TARGET: cross-session-probe
   CANDIDATE: probe-<timestamp>
   RESULT: marker-<uuid> written to confirm durability
   <other record fields filled as appropriate>
   ```

   Use a fresh, hard-to-guess marker so a later recall cannot match by
   accident.

3. **Confirm the write landed.** Call `memwal_remember_status`. Expect the
   write to be reported as landed, with a blob id.

4. **End the session.** Close session 1 so that no in-memory state carries
   over. Do not rely on the same process.

5. **Start a new session in the same namespace.** Open session 2, same
   runtime, same namespace.

6. **Recall the marker.** Call `memwal_recall` with a query for the marker.
   Expect the record written in session 1 to be returned.

7. **Record the outcome.** Note the marker, the query used, and where the raw
   recall output was stored.

## Pass / fail

- **Pass**: the marker written in session 1 is returned in session 2.
- **Fail**: the marker is not returned. Check: was the write confirmed landed
  (step 3)? Was session 2 in the same namespace? Did the recall query contain
  a distinctive token from the record?
