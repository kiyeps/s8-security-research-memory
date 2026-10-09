# Record: example-protocol / candidate 001

Sanitized example. Fictional target. No real client material.

```
TARGET:      example-protocol
PROJECT:     example-bounty-program
REPO:        github.com/example-org/example-protocol (public source, fictional)
COMMIT:      example-protocol@0.0.0-example (pinned example tag)
CANDIDATE:   candidate-001 -- reward accounting on repeated claim
HYPOTHESIS:  Claiming a reward for the same epoch twice increments the
             claimant's balance twice while the epoch's emitted total is only
             counted once, producing a surplus that can be withdrawn.
TEST:        Deploy the example-protocol contracts to a local fork. Run the
             claim() flow twice for one epoch with two calls in the same block.
             Read the claimant balance and the epoch emitted-total storage slot
             before and after.
RESULT:      <pending -- this record is written before the test is run>
REPRO:       Steps to run: 1) start local fork at COMMIT. 2) call claim(epoch=7)
             as account A. 3) call claim(epoch=7) as account A again. 4) diff
             balances and emitted-total.
EVIDENCE:    <pending -- see ../evidence/README.md for where artifacts live>
DUPLICATE:   not yet checked against the program's disclosed reports
BLOCKER:     none at record time
DECISION:    run the test before writing any report; do not report on suspicion
NEXT_STEP:   run TEST, then write record 002 with the RESULT
```

## Notes

- This record is written with `RESULT`, `EVIDENCE`, and `DUPLICATE` explicitly
  unfinished, on purpose. It shows how "not yet known" is recorded as such,
  rather than omitted.
- `REPO` and `COMMIT` point at a public source with a pinned reference. The
  commit is what makes the reproduction reproducible.
- Namespace: `hermes/default` (this example is a private working record).
