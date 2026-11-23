"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/198052 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import numpy as np
import torch


def f(x):
    return np.fix(x)


def test_known_bug_signature():
    x = np.array([1.5, -1.5, 2.5, -0.5], dtype=np.float32)
    expected = f(x.copy())
    np.testing.assert_array_equal(expected, np.array([1., -1., 2., -0.], dtype=np.float32))
    got = torch.compile(f, backend='eager')(x.copy())
    assert got.shape == expected.shape
    got = np.asarray(got)
    assert got.dtype == expected.dtype == np.float32
    np.testing.assert_array_equal(got, np.array([2., -2., 2., -0.], dtype=np.float32))
    assert np.signbit(got[-1]) and np.signbit(expected[-1])
