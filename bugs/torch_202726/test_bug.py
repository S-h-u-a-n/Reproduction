"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/202726 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch
import pytest



class Sub(torch.Tensor):
    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        return super().__torch_function__(func, types, args, kwargs or {})


def f(t):
    return t.real * 2


def test_known_bug_signature():
    inp = torch.tensor([1., -2., 3.]).as_subclass(Sub)
    expected = f(inp)
    assert torch.equal(expected, torch.tensor([2., -4., 6.]))
    compiled = torch.compile(f, backend='eager')
    # The exact message varies across PyTorch releases.
    with pytest.raises(AssertionError) as error:
        compiled(inp)

    assert "source must be None for ValueMutationNew/AttributeMutationNew" in str(error.value)
