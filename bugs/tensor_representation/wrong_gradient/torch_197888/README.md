# torch_197888 — Adaptive max pool backward ignores index strides

- **Source:** https://github.com/pytorch/pytorch/issues/197888
- **Primary Cause:** `tensor_representation` — `channels_last_3d` / non-contiguous `indices` stride is ignored in the CPU backward kernel.
- **Primary Observation:** `wrong_gradient`
- **API:** `torch.ops.aten.adaptive_max_pool3d_backward` (with `F.adaptive_max_pool3d` producing `indices`).
- **Trigger:** Fixed `(1,4,4,3,5)` input, pooled `(2,3,5)` indices, and contiguous vs channels_last_3d layouts with **identical logical index values**.
- **Expected:** A logical scatter oracle and the CPU backward using contiguous indices compute the same input gradient. The channels_last_3d index layout should compute the same gradient.
- **Observed upstream:** The CPU backward consumes the physical storage order of non-contiguous indices, so values are scattered to wrong input elements. The report reproduces on CPU PyTorch 2.14.0 and 2.15.0 development builds; the stable 2.15.0+cpu wheel is not established here.
- **Test strategy:** Entirely deterministic input (permutation via modular arithmetic). Confirms the correct reference and checks that the erroneous gradient exactly equals a *separate Python logical scatter* driven by index storage reinterpreted as contiguous. A generic gradient mismatch alone is insufficient.
- **Scope:** Kernel-level adaptive_max_pool3d_backward case only; does not claim the unrelated fractional pooling variants from the same upstream Issue are covered.
- **Verification:** Installation requires 10/10 independent pytest processes on the target environment; until then this is a candidate, not an installed or target-verified bug.
