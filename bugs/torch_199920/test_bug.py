"""Regression signature for pytorch/pytorch issue #199920.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
from torch._subclasses.fake_tensor import FakeTensorMode

def make_args(x):
    return (x,
            torch.ones(1, dtype=torch.long),
            torch.ones(1, dtype=torch.long),
            torch.empty(0), torch.empty(0),
            torch.ones(1), torch.zeros(1, dtype=torch.int32),
            0.01, -128, 127, 0, True, True)

def test_known_bug_signature():
    op = torch.ops.aten._fused_moving_avg_obs_fq_helper_functional
    x = torch.ones(8, 4)
    real = op(*make_args(x))
    assert all(t.shape == (8,) for t in real[2:])
    with FakeTensorMode() as mode:
        args = tuple(mode.from_tensor(v) if isinstance(v, torch.Tensor) else v for v in make_args(x))
        fake = op(*args)
    assert [tuple(t.shape) for t in fake[2:]] == [(0,), (0,), (1,), (1,)], 'Known issue: fake/meta observer state shape is stale'
