# PyTorch Issue #204426 — torch.compile / torch.no_grad / Tensor view

- GitHub: https://github.com/pytorch/pytorch/issues/204426
- Primary cause: `tensor_representation`
- Primary observation: `wrong_gradient`
- Source issue version evidence: 2.16.0.dev20261108+cu132
- Target runtime (must verify): `torch 2.15.0+cpu` / `Python 3.14.10` / CPU
- Replaces: `torch_194347` only after independent-process validation

## What happens

Compiled Autograd incorrectly connects a no_grad view to its input.

## Expected behavior / wrong behavior

Eager gradient is [2,2,2,2], compiled gradient is [2,3,3,3].

## Reproducer

Run `python -m pytest test_bug.py -q` in an independent Python process, or use the batch installer from the ZIP. The test includes explicit controls and specific wrong-behavior assertions.

## Limitations

This test has not yet been executed on the user's exact target wheel. It is a **candidate** until ten independent runs pass on that environment and the full 100-case suite still passes. Source issue existence is not evidence of independent root cause. Some compiler codepaths and error messages vary across PyTorch versions.
