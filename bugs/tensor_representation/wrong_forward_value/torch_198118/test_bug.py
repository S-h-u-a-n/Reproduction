"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/198118 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch
from torch.utils._python_dispatch import TorchDispatchMode


class Forward(TorchDispatchMode):
    def __torch_dispatch__(self, func, types, args=(), kwargs=None):
        return func(*args, **(kwargs or {}))


def test_known_bug_signature():
    # Non-real, full rank, fixed complex matrix, no RNG.
    a = torch.tensor([[1+2j, 2-1j], [3+1j, 2+4j], [0.5-1j, 1+0.25j]],
                     dtype=torch.complex128)
    expected = torch.linalg.pinv(a)
    assert torch.allclose(a @ expected @ a, a, rtol=1e-8, atol=1e-8)
    with Forward():
        actual = torch.linalg.pinv(a)
    u, singular, vh = torch.linalg.svd(a, full_matrices=False)
    reference = (vh.mH / singular) @ u.mH
    missing_conjugate = (vh.mT / singular) @ u.mH
    # Small full-rank complex128 SVD: tolerance allows LAPACK roundoff.
    torch.testing.assert_close(expected, reference, rtol=1e-10, atol=1e-10)
    torch.testing.assert_close(actual, missing_conjugate, rtol=1e-10, atol=1e-10)
    assert not torch.allclose(actual, reference, rtol=1e-10, atol=1e-10)
    assert not torch.allclose(a @ actual @ a, a, rtol=1e-8, atol=1e-8)
