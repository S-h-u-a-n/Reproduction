# torch_204033 — Inductor loses conjugate imaginary view aliasing

- **Upstream:** https://github.com/pytorch/pytorch/issues/204033
- **Primary cause:** `tensor_representation` / `alias-replay/conjugate-imaginary-view`
- **Observation:** `incorrect_state`
- **APIs:** `torch.Tensor.conj`, `torch.Tensor.imag`, `torch.compile`
- **Input:** CPU float32 vector `[1, 2, 3, 4]`, fixed, no randomness.
- **Correct behavior:** The returned `base` and `view=base.conj().imag` share storage. Updating `view.add_(100)` changes `base.imag` by `-100` in the eager control.
- **Reported wrong behavior:** Inductor materializes the returned view into distinct storage; `view.add_(100)` does not change `base.imag`.
- **Oracle:** Compares complete pre-mutation values and both eager and compiled post-mutation values, plus storage identity.
- **Versions:** Observed on a separate `2.10.0+cpu` environment; inclusion in this benchmark needs ten independent reproductions on target `2.15.0+cpu`.
- **PASS:** Specific PyTorch bug reproduced (not fixed behavior).
