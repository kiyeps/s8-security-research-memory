# Evidence

This directory holds safe, publishable summaries of the evidence behind this
project's claims. Raw logs, captures, and transcripts stay in the operator's
private archive and are referenced, never copied here.

## What is here

| File | Contents |
|---|---|
| `before-after.md` | What changed when recall was injected: a summarized before/after from a recorded demonstration. |
| `mainnet-proof.md` | The recorded mainnet writes, their job ids, blob ids, and a public retrieval check. |
| `cross-runtime-demo.md` | The two-directional cross-runtime demonstration, summarized. |

## Why raw evidence is kept out

- Raw logs and captures are large and noisy.
- Raw material can contain paths, identifiers, or fragments not meant to be
  public.
- Keeping evidence out keeps this repository publishable and keeps secrets
  out of version control. See `../SECURITY.md`.

## Rules this directory follows

- Every claim in these files is either reproduced inline or points at a blob
  id that can be checked by anyone.
- No credential values, no session tokens, no private keys.
- Blob ids are safe to publish: they address stored, client-side encrypted
  records and are not credentials. See `mainnet-proof.md`.
- If an excerpt is abridged or translated from a raw transcript, it is
  labeled as such.
