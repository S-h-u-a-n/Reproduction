# PyTorch Issue #192202_1 — Partial optimizer state not initialized

- **Source:** https://github.com/pytorch/pytorch/issues/192202
- **Candidate replacing:** torch_202526 (only after local 10/10)
- **Cause:** training_state / checkpoint/partial-optimizer-state
- **Observation:** `incorrect_state`
- **API:** `get_optimizer_state_dict`
- **Correct contract:** When optimizer state is partially initialized, exporting should preserve existing state and initialize missing state for trainable parameters.
- **Observed upstream error signature:** After only p0 receives optimizer state and is then frozen, exporting produces state keys `{"0.weight"}` instead of `{"0.weight", "1.weight"}`, omitting the still-trainable p1.
- **Assertion scope:** Verify only p0 has state before exporting and p1 remains trainable; verify the exported state contains exactly `0.weight`. State values are not checked.

PASS means the specific buggy behavior was reproduced, not that the defect was fixed.
Model initialization uses RNG, but the gradients and asserted behavior do not depend on the initial weights.
Validate independently on torch 2.15.0+cpu with 10/10 successful reproductions before inclusion.
