# Before and After: Session Context With and Without Walrus Memory

A summarized, abridged before/after from a recorded demonstration on
2026-10-09. Raw transcripts stay in the operator's private archive; the
excerpts here are safe to publish and carry no client material.

## Why this demonstration exists

The runtime keeps local memory files. Those files are a working cache: they
only contain what was saved locally. The demonstration shows what changes
when a durable layer sits behind them: a question about earlier work finds an
answer even in a session that has never seen that work.

## Before the bridge (local cache only)

A fresh session was asked about an earlier work item and the state of a
running process.

- The session could not answer from its own context.
- The item was not in the session, and the local cache did not carry it.
- The session said so plainly instead of inventing an answer.

That is the baseline: session boundaries wipe working context.

## After the bridge (recall injected on the first turn)

The same class of question, asked in a fresh session after the bridge was
active:

- The first turn carried a `[Walrus Memory]` block, injected automatically
  before the API call, containing the recalled record for the item.
- The session answered with the record's content and the current process id,
  which it had no other way of knowing.
- A direct recall of the marker returned the record at rank one of the
  result set.

Mechanically verified: the injected text is visible in the API-bound request
that the model actually received (the runtime stores those exact bytes for
each message). That is what rules out the answer having come from somewhere
else in the local context.

## Limits (read these)

- The mirror is bounded to qualifying single-action writes; some memory
  operations are skipped by design, and skips are logged. See
  `../docs/limitations.md`.
- The newest marker was absent from the first automated top-k recall in one
  check and surfaced at rank one on a direct recall. Recall is a ranked
  search, not a guarantee of presence.
