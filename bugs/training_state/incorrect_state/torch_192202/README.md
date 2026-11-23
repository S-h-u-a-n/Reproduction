# PyTorch Issue #192202

- **Source:** https://github.com/pytorch/pytorch/issues/192202
- **Candidate replacing:** torch_202526 (only after local 10/10)
- **Cause:** training_state / checkpoint/frozen-optimizer-state
- **Observation:** `incorrect_state`
- **API:** `get_optimizer_state_dict / set_optimizer_state_dict`
- **Correct contract:** Checkpoint optimizer state load drops state owned by frozen parameters.
- **Observed upstream error signature:** An optimizer that originally had two initialized states loads only one state when one parameter is frozen.

PASS here means the specific buggy behavior was reproduced, not that the defect was fixed. Fixed inputs; no RNG. Run independently on torch 2.15.0+cpu before inclusion.
