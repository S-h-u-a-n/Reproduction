"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/205682 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch


def f(a, b):
    return torch.cat((a, b), dim=1).split([3, 3], dim=1)


def test_known_bug_signature():
    a = torch.tensor([[1, 2, 3]], dtype=torch.int64)
    b = torch.tensor([[4, 5, 6]], dtype=torch.int64)
    ea, _ = f(a, b)
    assert not torch._C._is_alias_of(ea, a)

    compiled = torch.compile(f, backend="inductor", fullgraph=True)
    x, y = a.clone(), b.clone()
    part, _ = compiled(x, y)
    assert torch.equal(part, a)
    part.add_(10)
    assert torch.equal(x, a + 10), "Known bug: Inductor split part mutates its original input"

    p = torch.tensor([[1, 2, 3]], dtype=torch.int32)
    q = torch.tensor([[4., 5., 6.]], dtype=torch.float32)
    expected = f(p, q)
    actual = compiled(p, q)
    assert expected[0].dtype == torch.float32
    assert actual[0].dtype == torch.int32, "Known bug: first split loses cat dtype promotion"
