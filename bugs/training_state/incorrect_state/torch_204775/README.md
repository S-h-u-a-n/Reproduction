# torch_204775 — Empty batches incorrectly increase the cumulative BatchNorm counter and dilute later running statistics.

- **Upstream:** https://github.com/pytorch/pytorch/issues/204775
- **Primary cause:** `training_state` / `batchnorm/empty-batch-running-state`
- **Observation:** `incorrect_state`
- **API:** `torch.nn.BatchNorm1d / num_batches_tracked`
- **Correct behavior / oracle:** An empty batch leaves num_batches_tracked unchanged; the first real batch sets running_mean=1 and running_var=0.
- **Bug signature:** After an empty then a real batch, num_batches_tracked=2 and running_mean=running_var=0.5 instead of counter=1, mean=1, var=0.
- **Input:** Fixed values only; no RNG.
- **Scope:** Upstream evidence comes from other versions/platforms; this candidate is accepted only after 10 separate processes observe the exact signature on torch 2.15.0+cpu.
- **PASS meaning:** The PyTorch defect is reproduced, not that the library is correct.
