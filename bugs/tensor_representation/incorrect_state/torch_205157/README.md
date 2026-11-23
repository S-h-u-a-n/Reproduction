# torch_205157 — Inductor returns a clone and nested-unfold view with different storages; mutating the view no longer mutates the base.

- **Upstream:** https://github.com/pytorch/pytorch/issues/205157
- **Primary cause:** `tensor_representation` / `alias-replay/nested-unfold-view`
- **Observation:** `incorrect_state`
- **API:** `torch.Tensor.unfold / torch.compile / torch.Tensor.clone`
- **Correct behavior / oracle:** A returned nested unfold view shares storage with the returned base and writes through to alternating rows.
- **Bug signature:** Compiled outputs do not share untyped_storage and fill_ of the returned view leaves the compiled base all True; eager aliases.
- **Input:** Fixed values only; no RNG.
- **Scope:** Upstream evidence comes from other versions/platforms; this candidate is accepted only after 10 separate processes observe the exact signature on torch 2.15.0+cpu.
- **PASS meaning:** The PyTorch defect is reproduced, not that the library is correct.
