"""https://github.com/pytorch/pytorch/issues/204446 — offset applied twice."""

import torch


def test_issue_204446():
    # Use only the issue's three-row, in-bounds numeric reproducer.
    # Do not execute its separate two-row heap-corruption reproducer.
    coo = torch.ones(8).to_sparse()
    base = torch.zeros(3, 8)
    assert base[1].is_contiguous()
    assert base[1].storage_offset() == 8
    assert coo.is_coalesced()
    base[1].add_(coo)

    expected = torch.zeros(3, 8)
    expected[1].fill_(1.)
    control = torch.zeros(3, 8)
    control[1].add_(coo.to_dense())
    assert torch.equal(control, expected)
    buggy = torch.zeros(3, 8)
    buggy[2].fill_(1.)
    assert torch.equal(base, buggy)
    assert not torch.equal(base, expected)
