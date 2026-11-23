"""https://github.com/pytorch/pytorch/issues/203078 — expanded index strides."""

import torch


def test_issue_203078():
    self_ = torch.zeros(3, 32)
    index = torch.tensor([[0], [2]]).expand(2, 16)
    src = torch.ones(2, 16)
    assert index.stride() == (1, 0)

    actual = self_.scatter_add(0, index, src)
    control = self_.scatter_add(0, index.contiguous(), src)
    reduced = self_.scatter_reduce(0, index, src, "sum")

    # Each of the 16 columns adds one into rows 0 and 2.
    expected = torch.zeros(3, 32)
    expected[0, :16] = 1.
    expected[2, :16] = 1.
    expected_sums = torch.tensor([16., 0., 16.])
    buggy_sums = torch.tensor([16., 16., 0.])
    assert torch.equal(control, expected)
    assert torch.equal(control.sum(1), expected_sums)
    assert torch.equal(actual.sum(1), buggy_sums)
    assert torch.equal(reduced.sum(1), buggy_sums)
    buggy = torch.zeros_like(expected)
    buggy[0,:16] = 1.
    buggy[1,:16] = 1.
    assert torch.equal(actual,buggy)
    assert torch.equal(reduced,buggy)
    assert not torch.equal(actual, expected)
    assert not torch.equal(reduced, expected)
