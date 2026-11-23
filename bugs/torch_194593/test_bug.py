"""Regression signature for pytorch/pytorch issue #194593.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest
from torch._dynamo.exc import Unsupported
from torch.distributions import Binomial, kl_divergence

def f(pc, pp, qc, qp):
    return kl_divergence(Binomial(total_count=pc, probs=pp), Binomial(total_count=qc, probs=qp))

def test_known_bug_signature():
    args = (torch.tensor([5.]), torch.tensor([0.2]), torch.tensor([3.]), torch.tensor([0.4]))
    eager = f(*args)
    assert torch.isposinf(eager).all().item()
    with pytest.raises(Unsupported) as error:
        torch.compile(f, backend='inductor', fullgraph=True)(*args)

    assert "Data-dependent branching" in str(error.value)
    assert "_kl_binomial_binomial" in str(error.value)
