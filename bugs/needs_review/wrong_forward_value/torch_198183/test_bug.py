import torch
import math


def test_issue_198183():
    values = [1e-8, 1e-7, 2e-7, 5e-7, 1e-6, 1e-5, 1e-4, 1e-3]
    x = torch.tensor(values * 8, dtype=torch.float32)
    eager = torch.erf(x)
    reference = torch.tensor([math.erf(v) for v in x.tolist()], dtype=x.dtype)
    torch.testing.assert_close(eager, reference, rtol=2e-6, atol=0)
    torch._dynamo.reset()
    actual = torch.compile(torch.erf, backend='inductor')(x)
    assert actual.shape == x.shape and actual.dtype == x.dtype
    assert torch.isfinite(actual).all()
    # Check every repeated lane for both source-reported tiny inputs.
    # Other magnitudes are vectorization padding, not claimed exact errors.
    assert torch.equal(actual.reshape(8, 8)[:, :2], torch.zeros(8, 2))
    assert (reference.reshape(8, 8)[:, :2] > 0).all()
