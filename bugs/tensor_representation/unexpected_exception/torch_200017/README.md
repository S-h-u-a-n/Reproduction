# torch_200017 — The legacy vectorized forward-mode Jacobian reports a tangent rank that does not match its 1D matmul output.

- **Upstream:** https://github.com/pytorch/pytorch/issues/200017
- **Primary cause:** `tensor_representation` / `tangent-shape/matmul-vectorized-jacobian`
- **Observation:** `unexpected_exception`
- **API:** `torch.autograd.functional.jacobian / torch.func.jacfwd`
- **Correct behavior / oracle:** The forward-mode Jacobian of exp(x @ W.T) has shape (3,2) and equals reverse Jacobian and jacfwd.
- **Bug signature:** strategy=forward-mode, vectorize=True raises a RuntimeError about a forward gradient having different size for a 1-D input to matmul.
- **Input:** Fixed values only; no RNG.
- **Scope:** Upstream evidence comes from other versions/platforms; this candidate is accepted only after 10 separate processes observe the exact signature on torch 2.15.0+cpu.
- **PASS meaning:** The PyTorch defect is reproduced, not that the library is correct.
