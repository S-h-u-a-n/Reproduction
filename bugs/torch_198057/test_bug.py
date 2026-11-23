import torch


def test_issue_198057():
    inf = float('inf')
    a = torch.tensor([5.5, -5.5, 0., 1e20, 2147483648., 7., 1., -0.])
    b = torch.tensor([inf, -inf, inf, 3., 3., 0.7, 0.1, 1.])
    fn = lambda u, v: torch.remainder(u, v)
    eager = fn(a, b)
    torch.testing.assert_close(eager[:5], torch.tensor([5.5, -5.5, 0., 2., 2.]), rtol=0, atol=0)
    torch._dynamo.reset()
    actual = torch.compile(fn, backend='inductor')(a, b)
    assert actual.shape == eager.shape and actual.dtype == torch.float32
    assert torch.isnan(actual[:3]).all().item()
    torch.testing.assert_close(actual[3:5], torch.zeros(2), rtol=0, atol=0)
    # Remaining lanes retain vector-loop triggering; their small rounding
    # differences and signed-zero policy are outside this signature.
