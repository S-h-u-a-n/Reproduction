# torch_204024 — A singular 1x1 determinant has an exact derivative 1; forward-mode AD drops it while reverse-mode AD is correct.

- **Upstream:** https://github.com/pytorch/pytorch/issues/204024
- **Primary cause:** `training_state` / `autograd/singular-determinant-jvp`
- **Observation:** `wrong_gradient`
- **API:** `torch.linalg.det / torch.autograd.forward_ad`
- **Correct behavior / oracle:** The derivative of det([[x]]) at x=0 is 1 in both forward and reverse mode.
- **Bug signature:** Forward JVP of det([[0]]) along [[1]] returns scalar 0 while reverse-mode derivative is 1.
- **Input:** Fixed values only; no RNG.
- **Scope:** Upstream evidence comes from other versions/platforms; this candidate is accepted only after 10 separate processes observe the exact signature on torch 2.15.0+cpu.
- **PASS meaning:** The PyTorch defect is reproduced, not that the library is correct.
