# Namespace Separation: What It Does and Does Not Enforce

This document states plainly what the namespace model enforces and what it
does not. It exists because it is easy to read "separate namespaces" and
assume a security boundary that is not present.

## Summary

Namespace separation is a **routing convention**, not a proven access-control
boundary. It decides where a runtime reads and writes. It does not, on its
own, prove that one runtime cannot see another runtime's records.

## What it does

- **Chooses a partition.** A runtime launched with `--namespace hermes/default`
  reads and writes in `hermes/default`. A runtime launched with another
  namespace reads and writes there. This keeps ordinary work from one
  workstream from cluttering another by default.
- **Keeps private by default.** Because a runtime touches only its configured
  namespace unless changed, per-runtime memory is not pulled into another
  runtime's normal recall queries.
- **Makes sharing a deliberate move.** Sharing across runtimes is done by
  pointing runtimes at the same namespace. It does not happen by accident
  through normal use.

## What it does not enforce

- **It is not a proven isolation boundary.** No test in this repository
  demonstrates that a runtime configured with one namespace is technically
  prevented from reading another namespace's records.
- **It does not gate by identity.** Both runtimes use the **same** MemWal
  account on mainnet. A namespace is a key, not an authentication of the
  caller.
- **It does not encrypt per namespace.** Separating records into namespaces is
  not the same as encrypting each namespace under a different key. Do not
  assume per-namespace confidentiality from the namespace name alone.
- **It does not stop misconfiguration.** A runtime can be pointed at the
  wrong namespace. A typo in a launch command can move a workstream into a
  namespace it was not meant to use.

## Practical consequences

- Treat **everything written to the shared account as potentially visible to
  any runtime holding the account credentials**, until a real boundary is
  proven.
- Do **not** rely on namespace separation to protect sensitive material.
  Keep secrets out of memory records entirely. See `../SECURITY.md`.
- For private material, the safe assumption is that separation is
  organizational, not a security guarantee.
- If a true boundary is required, it must be established and demonstrated
  separately (for example, by distinct accounts or by encryption with
  distinct keys). That is out of scope for this repository.

## What this project verified, and what it did not

- Verified: both runtimes share one account, and records written under a
  namespace are readable by the runtime configured for that namespace
  (that is the cross-runtime demonstration).
- Not verified: any server-enforced boundary between namespaces. This
  project treats the **account**, not the namespace, as the unit of sharing.

## Rule of thumb

Namespace separation is good hygiene. It is not a security control. Document
it as hygiene and assume the shared account is shared.
