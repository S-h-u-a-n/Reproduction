# PyTorch Issue #205404

- **Source:** https://github.com/pytorch/pytorch/issues/205404
- **Candidate replacing:** torch_197894 (only after local 10/10)
- **Cause:** tensor_representation / aliasing/partial-overlap-cache
- **Observation:** `wrong_forward_value`
- **API:** `torch.compile / Tensor.add_ / StorageOverlapPartition`
- **Correct contract:** Cached graph specialized to full storage overlap is reused for partial overlap.
- **Observed upstream error signature:** After warmup with fully overlapping inputs the partial-overlap compiled result matches full-overlap result instead of the eager partial-overlap reference.

PASS here means the specific buggy behavior was reproduced, not that the defect was fixed. Fixed inputs; no RNG. Run independently on torch 2.15.0+cpu before inclusion.
