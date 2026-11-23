# PyTorch Issue #206126 — torch.linalg.lu_solve

- GitHub: https://github.com/pytorch/pytorch/issues/206126
- Primary cause: `tensor_representation`
- Primary observation: `wrong_forward_value`
- Source issue version evidence: 2.15.0+cpu
- Target runtime (must verify): `torch 2.15.0+cpu` / `Python 3.14.10` / CPU
- Replaces: `torch_187806` only after independent-process validation

## What happens

Output aliases LU factor, overwriting data required for the solve.

## Expected behavior / wrong behavior

LU factor aliases the out argument and yields a large residual while independent/rhs output are correct.

## Reproducer

Run `python -m pytest test_bug.py -q` in an independent Python process, or use the batch installer from the ZIP. The test includes explicit controls and specific wrong-behavior assertions.

## Limitations

This test has not yet been executed on the user's exact target wheel. It is a **candidate** until ten independent runs pass on that environment and the full 100-case suite still passes. Source issue existence is not evidence of independent root cause. Some compiler codepaths and error messages vary across PyTorch versions.
