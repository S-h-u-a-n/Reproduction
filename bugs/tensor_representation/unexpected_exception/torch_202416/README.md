# PyTorch Issue #202416 — torch.compile / torch.Tensor.detach

- GitHub: https://github.com/pytorch/pytorch/issues/202416
- Primary cause: `tensor_representation`
- Primary observation: `unexpected_exception`
- Source issue version evidence: 2.16.0.dev20261026+cu132
- Target runtime (must verify): `torch 2.15.0+cpu` / `Python 3.14.10` / CPU
- Replaces: `torch_193757` only after independent-process validation

## What happens

AOTAutograd mishandles ViewMeta replay when returning both a view and detached alias.

## Expected behavior / wrong behavior

Inductor raises a ViewMeta output-shape assertion while eager works.

## Reproducer

Run `python -m pytest test_bug.py -q` in an independent Python process, or use the batch installer from the ZIP. The test includes explicit controls and specific wrong-behavior assertions.

## Limitations

This test has not yet been executed on the user's exact target wheel. It is a **candidate** until ten independent runs pass on that environment and the full 100-case suite still passes. Source issue existence is not evidence of independent root cause. Some compiler codepaths and error messages vary across PyTorch versions.
