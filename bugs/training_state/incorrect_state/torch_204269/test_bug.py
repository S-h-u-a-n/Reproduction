import torch
from torch.nn.utils import clip_grad_norm_, get_total_norm


def test_issue_204269():
    g1 = torch.tensor([3., -4., 0.])
    g2 = torch.tensor([1., 0.])
    expected_zero_norm = torch.linalg.vector_norm(torch.cat((g1, g2)), ord=0)
    assert expected_zero_norm.item() == 3.0
    observed_zero_norm = get_total_norm((g1, g2), norm_type=0)
    assert observed_zero_norm.item() == 2.0, observed_zero_norm
    assert observed_zero_norm.item() != expected_zero_norm.item()
    # The same bug is exposed through the public gradient-clipping API.
    p = torch.nn.Parameter(torch.zeros(3))
    p.grad = g1.clone()
    used_norm = clip_grad_norm_([p], max_norm=1.0, norm_type=0)
    assert used_norm.item() == 1.0, used_norm
    assert torch.linalg.vector_norm(g1, ord=0).item() == 2.0
