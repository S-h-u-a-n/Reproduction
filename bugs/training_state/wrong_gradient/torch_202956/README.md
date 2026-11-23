# torch_202956 — Forward-mode Embedding AD propagates a tangent through padding indices even though reverse-mode masks those rows.

- **Upstream:** https://github.com/pytorch/pytorch/issues/202956
- **Primary cause:** `training_state` / `autograd/embedding-padding-forward-ad`
- **Observation:** `wrong_gradient`
- **API:** `torch.func.jvp / torch.func.vjp / torch.nn.functional.embedding`
- **Correct behavior / oracle:** The padding row contributes zero to forward- and reverse-mode derivatives; dot product adjoint identity holds.
- **Bug signature:** JVP for padding_idx=0 copies the nonzero tangent at row 0 into two padding outputs, while VJP masks that row.
- **Input:** Fixed values only; no RNG.
- **Scope:** Upstream evidence comes from other versions/platforms; this candidate is accepted only after 10 separate processes observe the exact signature on torch 2.15.0+cpu.
- **PASS meaning:** The PyTorch defect is reproduced, not that the library is correct.
