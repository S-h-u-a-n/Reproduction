"""PyTorch known bug signature, issue #205991.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch

class K:
    n = 0

def fn(t):
    K.n = 5
    return t + K().n

def test_known_bug_signature():
    previous = K.n
    try:
        _check_signature()
    finally:
        K.n = previous


def _check_signature():
    x = torch.zeros(1)
    K.n = 0
    assert fn(x).item() == 5.0
    K.n = 0
    torch._dynamo.reset()
    got = torch.compile(fn, backend='eager')(x)
    assert K.n == 5
    # This build treats torch/torch.*/torch_* module names as internal in
    # UserDefinedClassVariable.get_value_for_setattr. pytest importlib with
    # rootdir=bugs gives torch_205991.test_bug and returns the correct 5.
    # Keep the actual call above visible; do not rewrite __module__ to
    # force a result. Run from the project root (module bugs.torch_...)
    # or as an isolated default-mode test (module test_bug).
    internal_namespace = K.__module__ == 'torch' or K.__module__.startswith(('torch.', 'torch_'))
    assert not internal_namespace, (
        f'Outside this signature: module={K.__module__}, output={got.item()}; '
        'use project-root collection; the torch_* namespace takes another Dynamo path'
    )
    assert got.item() == 0.0, (
        f'Known class attribute issue did not reproduce: module={K.__module__}, output={got}'
    )
