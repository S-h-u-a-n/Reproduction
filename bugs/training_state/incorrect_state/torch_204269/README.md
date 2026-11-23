# PyTorch Issue #204269 — torch.nn.utils.clip_grad_norm_ / get_total_norm

- GitHub: https://github.com/pytorch/pytorch/issues/204269
- Primary cause: `training_state`
- Primary observation: `incorrect_state`
- Source issue version evidence: 2.16.0.dev20261110+cpu
- Target runtime (must verify): `torch 2.15.0+cpu` / `Python 3.14.10` / CPU
- Replaces: `torch_197089` only after independent-process validation

## What happens

The 0-norm of gradients counts nonzero tensors instead of nonzero gradient elements.

## Expected behavior / wrong behavior

A pair of gradient tensors with three nonzero elements returns a total 0-norm of two.

## Reproducer

Run `python -m pytest test_bug.py -q` in an independent Python process, or use the batch installer from the ZIP. The test includes explicit controls and specific wrong-behavior assertions.

## Limitations

This test has not yet been executed on the user's exact target wheel. It is a **candidate** until ten independent runs pass on that environment and the full 100-case suite still passes. Source issue existence is not evidence of independent root cause. Some compiler codepaths and error messages vary across PyTorch versions.
