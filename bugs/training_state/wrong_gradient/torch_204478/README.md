# PyTorch Issue #204478 — F.layer_norm / torch.autograd.grad

- GitHub: https://github.com/pytorch/pytorch/issues/204478
- Primary cause: `training_state`
- Primary observation: `wrong_gradient`
- Source issue version evidence: 2.10.0; 2.16 Issue
- Target runtime (must verify): `torch 2.15.0+cpu` / `Python 3.14.10` / CPU
- Replaces: `torch_197716` only after independent-process validation

## What happens

Built-in layer normalization has incorrect reverse-mode third derivatives.

## Expected behavior / wrong behavior

A parameter gradient of a loss involving second input derivatives differs from an independent formula.

## Reproducer

Run `python -m pytest test_bug.py -q` in an independent Python process, or use the batch installer from the ZIP. The test includes explicit controls and specific wrong-behavior assertions.

## Limitations

This test has not yet been executed on the user's exact target wheel. It is a **candidate** until ten independent runs pass on that environment and the full 100-case suite still passes. Source issue existence is not evidence of independent root cause. Some compiler codepaths and error messages vary across PyTorch versions.
