# PyTorch Issue #192202_2 — Frozen parameter state lost during loading

- **Source:** https://github.com/pytorch/pytorch/issues/192202
- **Candidate replacing:** torch_202526 (only after local 10/10)
- **Cause:** training_state / checkpoint/frozen-optimizer-state
- **Observation:** `incorrect_state`
- **API:** `set_optimizer_state_dict`
- **Correct contract:** Loading must restore saved optimizer state for both parameters, including the parameter frozen at load time.
- **Observed upstream error signature:** The exported checkpoint contains `0.weight` and `1.weight`, but loading into a fresh optimizer drops the frozen parameter's state, leaving state keys `{1}` instead of `{0, 1}`.
- **Assertion scope:** Verify both states exist before loading, verify exactly the frozen parameter's state is missing afterward, and verify the surviving parameter's state values match the original.

PASS means the specific buggy behavior was reproduced, not that the defect was fixed.
Model initialization uses RNG, but the gradients and asserted behavior do not depend on the initial weights.
Validate independently on torch 2.15.0+cpu with 10/10 successful reproductions before inclusion.