"""https://github.com/pytorch/pytorch/issues/201633 — negative tie gradients."""

import torch


def test_issue_201633():
    # Preserve both reductions and both gradient signs from the CPU reproducer.
    for reduce, values in (("max", [2., 2., 1.]), ("min", [1., 1., 2.])):
        for grad in (1., -1.):
            data = torch.tensor(values, requires_grad=True)
            out = torch.segment_reduce(data, reduce, lengths=torch.tensor([3]))
            out.backward(torch.tensor([grad]))
            ref = torch.tensor(values, requires_grad=True)
            (ref.amax() if reduce == "max" else ref.amin()).backward(torch.tensor(grad))
            expected = torch.tensor([grad / 2, grad / 2, 0.])
            assert torch.equal(ref.grad, expected)
            assert out.item() == (2. if reduce == "max" else 1.)
            if grad > 0:
                assert torch.equal(data.grad, expected)
            else:
                assert torch.equal(data.grad, torch.tensor([-1., -1., 0.]))
                assert not torch.equal(data.grad, expected)
                assert data.grad.sum().item() == -2.
