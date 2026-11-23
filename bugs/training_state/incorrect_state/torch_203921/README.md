# PyTorch Issue #203921

- **Source:** https://github.com/pytorch/pytorch/issues/203921
- **Candidate replacing:** torch_198189 (only after local 10/10)
- **Cause:** training_state / optim/ema-discrete-buffer
- **Observation:** `incorrect_state`
- **API:** `torch.optim.swa_utils.AveragedModel`
- **Correct contract:** EMA on integer buffers silently preserves obsolete counters instead of copying current discrete state.
- **Observed upstream error signature:** Two EMA updates leave int64 state at 1 instead of latest integer state 2, whereas float parameters are updated.

PASS here means the specific buggy behavior was reproduced, not that the defect was fixed. Fixed inputs; no RNG. Run independently on torch 2.15.0+cpu before inclusion.
