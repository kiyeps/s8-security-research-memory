# Record: example-protocol / candidate 001 (follow-up)

Sanitized example. Fictional target. No real client material. Follow-up to
[record-001](record-001-hypothesis-and-test.md) in the same namespace.

```
TARGET:      example-protocol
PROJECT:     example-bounty-program
REPO:        github.com/example-org/example-protocol (public source, fictional)
COMMIT:      example-protocol@0.0.0-example (pinned example tag)
CANDIDATE:   candidate-001 -- reward accounting on repeated claim
HYPOTHESIS:  Claiming a reward for the same epoch twice increments the
             claimant's balance twice while the epoch's emitted total is only
             counted once, producing a surplus that can be withdrawn.
TEST:        Ran the local-fork double-claim in one block per record-001 REPRO.
RESULT:      The second claim reverted with EpochAlreadyClaimed. The emitted
             total was unchanged. The hypothesised surplus did not occur.
REPRO:       1) start local fork at COMMIT. 2) call claim(epoch=7) as A. 3) call
             claim(epoch=7) as A again -> revert EpochAlreadyClaimed. 4) balance
             and emitted-total unchanged on the first call's amount only.
EVIDENCE:    fork run logs and the revert trace are stored outside the repo; see
             ../evidence/README.md for the directory. Not copied into the repo.
DUPLICATE:   n/a -- no finding resulted, so nothing to deduplicate
BLOCKER:     none
DECISION:    close candidate-001 as not-a-vulnerability. The guard at the claim
             entry point is sufficient for this path.
NEXT_STEP:   open candidate-002: check whether a cross-epoch claim with a stale
             epoch argument reaches a different branch
```

## Notes

- This record shows the arc from record-001: hypothesis in, result out, decision
  taken, next step named.
- The interesting negative result (the guard holds) is recorded, not discarded.
  Knowing a guard works is durable knowledge.
- Namespace: `hermes/default`.
