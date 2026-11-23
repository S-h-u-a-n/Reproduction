import torch
from torch.func import jvp, vjp
from torch.nn.functional import embedding


def test_issue_202956():
    # All values and cotangents are fixed; no RNG or stochastic embedding inputs.
    weight = torch.tensor([[2., 3.], [4., 5.], [6., 7.]], dtype=torch.float64)
    idx = torch.tensor([0, 1, 0], dtype=torch.int64)
    tangent = torch.tensor([[11., 13.], [17., 19.], [23., 29.]], dtype=torch.float64)
    fn = lambda w: embedding(idx, w, padding_idx=0)

    out, jv = jvp(fn, (weight,), (tangent,))
    _, backward = vjp(fn, weight)
    (vjp_grad,) = backward(torch.ones_like(out))

    torch.testing.assert_close(out, weight[idx], rtol=0, atol=0)
    torch.testing.assert_close(vjp_grad[0], torch.zeros(2, dtype=weight.dtype), rtol=0, atol=0)
    torch.testing.assert_close(vjp_grad[1], torch.ones(2, dtype=weight.dtype), rtol=0, atol=0)

    # Wrong JVP at padding positions, despite the reverse-mode padding mask.
    torch.testing.assert_close(jv, tangent[idx], rtol=0, atol=0)
    assert not torch.equal(jv[0], torch.zeros_like(jv[0]))
    assert not torch.equal(jv[2], torch.zeros_like(jv[2]))
    assert not torch.equal((jv * torch.ones_like(jv)).sum(), (vjp_grad * tangent).sum())
