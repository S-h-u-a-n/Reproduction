import torch
from torch.distributions import Normal, TransformedDistribution, kl_divergence
from torch.distributions.transforms import AbsTransform


def test_issue_202967():
    p = TransformedDistribution(Normal(-1.0, 1.0), [AbsTransform()])
    q = TransformedDistribution(Normal(1.0, 1.0), [AbsTransform()])
    actual = kl_divergence(p, q)
    assert torch.isclose(actual, torch.tensor(2.0), rtol=0, atol=1e-6)
    assert not torch.isclose(actual, torch.tensor(0.0), rtol=0, atol=1e-6)
