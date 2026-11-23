import torch
from torch.autograd import forward_ad as fwAD


def test_issue_204024():
    x = torch.zeros((1, 1), dtype=torch.float64)
    d = torch.ones_like(x)

    with fwAD.dual_level():
        output = torch.linalg.det(fwAD.make_dual(x, d))
        tangent = fwAD.unpack_dual(output).tangent
    assert tangent is not None
    assert tuple(tangent.shape) == ()

    # Independent analytic oracle: det([[t]]) = t, so its exact derivative is 1 at t=0.
    # A reverse-mode control at the singular point is not required: older Torch
    # builds can have a separate reverse-mode error at that same point.
    with fwAD.dual_level():
        control = fwAD.unpack_dual(torch.linalg.det(fwAD.make_dual(torch.ones_like(x), d))).tangent
    assert control is not None
    torch.testing.assert_close(control, torch.tensor(1.0, dtype=x.dtype), rtol=0, atol=0)

    # Bug signature: the singular-matrix forward derivative is silently dropped.
    torch.testing.assert_close(tangent, torch.tensor(0.0, dtype=x.dtype), rtol=0, atol=0)
    assert not torch.equal(tangent, torch.tensor(1.0, dtype=x.dtype))
