"""Regression signature for pytorch/pytorch issue #198056.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import numpy as np
import torch

def f(x): return np.cumsum(x)

def test_known_bug_signature():
    x = np.array([-128, -100, -3, 0, 5, 100, 127], dtype=np.int8)
    eager = f(x)
    assert eager.dtype == np.int64
    assert eager.tolist() == [-128,-228,-231,-231,-226,-126,1]
    got = torch.compile(f, backend='eager')(x.copy())
    assert np.asarray(got).dtype == np.int8
    assert np.asarray(got).tolist() == [-128,28,25,25,30,-126,1]
