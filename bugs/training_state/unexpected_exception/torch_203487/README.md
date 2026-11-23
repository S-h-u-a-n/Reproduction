# PyTorch Issue #203487

- Source: https://github.com/pytorch/pytorch/issues/203487
- Cause: training_state / fsdp2/optimizer-state-lifecycle
- Observation: unexpected_exception
- API: torch.distributed.fsdp.fully_shard / get_optimizer_state_dict
- Exact signature: a two-rank CPU Gloo test successfully reads optimizer state after a step, then KeyError(0) after a no-grad forward. Both ranks must independently report this.
- No RNG. Tensor and model initialization use fixed values.
- Execution invokes two local subprocess ranks, so this candidate can be slower than others. Do not interpret a timeout as an observed bug.
