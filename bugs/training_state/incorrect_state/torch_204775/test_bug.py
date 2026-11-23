import torch
from torch import nn


def test_issue_204775():
    bn = nn.BatchNorm1d(2, momentum=None).train()
    reference = nn.BatchNorm1d(2, momentum=None).train()

    with torch.no_grad():
        out_empty = bn(torch.empty(0, 2))
        bn(torch.ones(2, 2))
        reference(torch.ones(2, 2))

    assert out_empty.shape == (0, 2)
    assert int(reference.num_batches_tracked.item()) == 1
    torch.testing.assert_close(reference.running_mean, torch.ones(2), rtol=0, atol=0)
    torch.testing.assert_close(reference.running_var, torch.zeros(2), rtol=0, atol=0)

    # Exact upstream bug: the empty forward counts, but its statistics were never updated.
    assert int(bn.num_batches_tracked.item()) == 2
    torch.testing.assert_close(bn.running_mean, torch.full((2,), 0.5), rtol=0, atol=0)
    torch.testing.assert_close(bn.running_var, torch.full((2,), 0.5), rtol=0, atol=0)
    assert not torch.equal(bn.running_mean, reference.running_mean)
