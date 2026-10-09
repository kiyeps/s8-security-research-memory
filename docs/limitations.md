# Limitations

Stated plainly, because each of these is a place where a reader could assume
more than the evidence supports.

## 1. The mirror is bounded

The write-side hook mirrors qualifying single-action memory writes (`add` and
`replace`). Other memory operations are skipped by design, and each skip is
recorded in the hook log. "Every local memory write is mirrored" is not
claimed here and would not be accurate.

## 2. Recall is a ranked search

Recall returns top-k results ranked by relevance, not by recency. A newly
written record is not guaranteed to appear in the first automatic injection.
In one direct check the newest marker was absent from the first automated
top-k and then returned at rank one on a direct recall. Treat recall as "best
matches first", not "everything, always".

## 3. Local memory remains the authoritative injection path

The runtime's local memory files are still injected into every session. The
durable layer powers the first-turn recall; the local files remain the cache
and fallback. This is by design in the current deployment.

## 4. Namespaces are routing, not a boundary

Namespace separation is a routing convention. It is not an access-control
boundary, and this project does not claim otherwise. See
`../shared-memory/permissions.md`.

## 5. A namespace is not per-user

In this deployment namespaces are per runtime profile, not per end user.
Multi-user partitioning was not part of what was tested here.

## 6. The OpenClaw runtime is stopped at the time of writing

The cross-runtime demonstration was captured while the OpenClaw service was
running. It is stopped now. The evidence stands as a recorded demonstration,
not as a statement about the current state of that service.

## 7. The public aggregator answers differently by client

Direct `curl` requests to the public Walrus aggregator retrieve blobs. Some
HTTP clients get rejected by the CDN in front of it with a bot-signature
response. That is a client-detection artifact, not an access policy. If a
script receives 403 where `curl` receives 200, suspect the client signature
first.

## 8. Process ids and timestamps drift

Evidence captured at different times references different process ids for the
same service. Gateways and sessions restart. Hooks re-register at every
start, so compare the hook set and the configuration, not the process id.

## 9. What was not tested

- No multi-user, multi-tenant memory partitioning.
- No load or scale testing beyond ordinary use.
- No guarantee that an old record cannot be crowded out of top-k by newer
  records for some queries.
