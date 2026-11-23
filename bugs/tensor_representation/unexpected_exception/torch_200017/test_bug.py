import pytest
import torch
from torch.autograd.functional import jacobian


def test_issue_200017():
    # Shape-specific tangent representation bug: vector (2,) @ matrix (2,3).
    W = torch.tensor([[1., 2.], [3., 4.], [5., 6.]], dtype=torch.float64)
    x = torch.tensor([0.25, 0.50], dtype=torch.float64)
    f = lambda t: (t @ W.T).exp()

    reverse = jacobian(f, x)
    forward_reference = torch.func.jacfwd(f)(x)
    assert reverse.shape == forward_reference.shape == (3, 2)
    torch.testing.assert_close(reverse, forward_reference, rtol=1e-12, atol=1e-12)

    with pytest.raises(RuntimeError, match="Trying to set a forward gradient that has a different size"):
        jacobian(f, x, vectorize=True, strategy="forward-mode")
