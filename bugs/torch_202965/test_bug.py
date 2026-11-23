"""Known-bug signature for pytorch/pytorch#202965 (CPU, torch 2.15.0).

This test PASSES only when the published NaN-gradient bug reproduces.
"""

import torch
from torch.distributions import Categorical, kl_divergence


def test_issue_202965():
    neg_inf = float("-inf")
    logits_p = torch.tensor([0.5, -1.0, 2.0, neg_inf], requires_grad=True)
    logits_q = torch.tensor([0.0, 1.0, -0.5, neg_inf])

    loss = kl_divergence(Categorical(logits=logits_p), Categorical(logits=logits_q))
    (observed_grad,) = torch.autograd.grad(loss, logits_p)

    # Reference: remove the masked class and recompute the same KL.
    z = logits_p.detach()[:3].clone().requires_grad_(True)
    log_p = torch.log_softmax(z, dim=-1)
    log_q = torch.log_softmax(logits_q[:3], dim=-1)
    reference_loss = (log_p.exp() * (log_p - log_q)).sum()
    (reference_unmasked_grad,) = torch.autograd.grad(reference_loss, z)
    reference_grad = torch.cat([reference_unmasked_grad, torch.zeros(1)])

    assert bool(torch.isfinite(loss))
    torch.testing.assert_close(loss, reference_loss, rtol=1e-6, atol=1e-7)
    assert bool(torch.isfinite(reference_grad).all())
    assert reference_grad[-1].item() == 0.0

    # Issue's error signature: finite forward loss, all-NaN backward gradient.
    assert bool(torch.isnan(observed_grad).all())
