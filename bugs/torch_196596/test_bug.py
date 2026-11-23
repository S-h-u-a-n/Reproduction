"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/196596 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch


def f(x, a, b):
    return torch.addmm(x, a, b, beta=0)


def test_known_bug_signature():
    ignored = torch.full((1, 2), float('nan'), dtype=torch.float64)
    a = torch.tensor([[2., 3.]], dtype=torch.float64)
    b = torch.tensor([[1., 2.], [4., 5.]], dtype=torch.float64)
    reference = a @ b
    eager = f(ignored, a, b)
    assert torch.allclose(eager, reference, rtol=0, atol=0)
    got = torch.compile(f, backend='inductor', fullgraph=True)(ignored, a, b)
    assert got.shape == (1,2) and got.dtype == torch.float64
    assert torch.isnan(got).all().item(), 'Known bug: both beta=0 outputs retain NaNs'
