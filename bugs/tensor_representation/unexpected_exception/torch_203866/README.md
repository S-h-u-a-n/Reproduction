# PyTorch Issue #203866 — DTensor storage offset / serialization

- GitHub: https://github.com/pytorch/pytorch/issues/203866
- Cause: `tensor_representation` (wrapper storage-offset and data pointer interpretation)
- Observation: `unexpected_exception`
- API: `DTensor.from_local`, `torch.save`
- Source evidence: CPU, 2.14.1 and main code investigation in the Issue
- Target: PyTorch 2.15.0+cpu / Python 3.14.10 (requires local confirmation)

## Trigger

The DTensor wrapper uses placeholder storage. The wrapper has a nonzero storage offset inherited from its local tensor. A serialization code path checks `Tensor.data_ptr() == 0` to detect wrappers; offset arithmetic makes that pointer appear nonzero, and it incorrectly tries to read invalid backing storage.

## Expected / actual

The same content with offset 0 saves normally, but a wrapper at offset 2 raises a RuntimeError mentioning an invalid Python storage data pointer. A Gloo world_size=1 process group is used, with no network or GPU.

## Reproducer

`test_bug.py` tests both cases and always tears down the process group. No random values are used. The case remains a candidate until it passes ten independent target-wheel runs and the complete 100-case suite.
