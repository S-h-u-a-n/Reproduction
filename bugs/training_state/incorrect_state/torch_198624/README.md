# PyTorch Issue #198624

- **Source:** https://github.com/pytorch/pytorch/issues/198624
- **Candidate replacing:** torch_197087 (only after local 10/10)
- **Cause:** training_state / autograd/detach-alias-history
- **Observation:** `incorrect_state`
- **API:** `torch.Tensor.detach / add_ / torch.compile`
- **Correct contract:** Detached alias updated with differentiable value loses its grad_fn under AOTAutograd replay.
- **Observed upstream error signature:** Eager return requires grad and has AddBackward; compiled return has requires_grad=False and grad_fn=None.

PASS here means the specific buggy behavior was reproduced, not that the defect was fixed. Fixed inputs; no RNG. Run independently on torch 2.15.0+cpu before inclusion.
