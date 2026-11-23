"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/202966 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch
from torch.distributions import Wishart, kl_divergence


def test_known_bug_signature():
    dtype = torch.float64
    # Fixed diagonal SPD covariances: no random sampling.
    diag = torch.tensor([[1.2, 1.5, 1.8], [1.4, 2.0, 2.5],
                         [2.0, 1.3, 1.7], [1.1, 2.1, 3.1],
                         [2.2, 2.3, 2.4]], dtype=dtype)
    covariance = torch.diag_embed(diag)
    df = torch.tensor([4., 6., 10., 20., 50.], dtype=dtype)
    q = Wishart(torch.tensor(5., dtype=dtype),
                covariance_matrix=torch.eye(3, dtype=dtype))
    actual = kl_divergence(Wishart(df, covariance_matrix=covariance), q)
    expected = torch.stack([
        kl_divergence(Wishart(df[i], covariance_matrix=covariance[i]), q)
        for i in range(len(df))
    ])
    def closed_form(degrees, diagonal):
        # W_3(n,V) versus W_3(5,I); diagonal V, no sampled quantities.
        psi = torch.digamma((degrees[...,None] - torch.arange(3,dtype=dtype))/2).sum(-1)
        return ((degrees-5)*psi/2 - 5*diagonal.log().sum(-1)/2
                + degrees*(diagonal.sum(-1)-3)/2
                + torch.mvlgamma(torch.tensor(2.5,dtype=dtype),3)
                - torch.mvlgamma(degrees/2,3))
    reference = closed_form(df,diag)
    # Float64 special-function and small-matrix rounding.
    torch.testing.assert_close(expected,reference,rtol=1e-10,atol=1e-10)
    psi = torch.digamma((df[:,None]-torch.arange(3,dtype=dtype))/2).sum(-1)
    df_term = (5-df)/2*(diag.log().sum(-1)+3*torch.log(torch.tensor(2.,dtype=dtype))+psi)
    buggy = reference + df_term - df_term.sum()
    torch.testing.assert_close(actual,buggy,rtol=1e-10,atol=1e-10)
    assert not torch.allclose(actual,reference,rtol=1e-10,atol=1e-10)
    # The same issue also reports detaching p's natural parameters.
    df0 = df[1].clone().requires_grad_()
    diag0 = diag[1].clone().requires_grad_()
    scalar = kl_divergence(Wishart(df0,covariance_matrix=torch.diag(diag0)),q)
    grads = torch.autograd.grad(scalar,(df0,diag0),allow_unused=True)
    reference_grads = torch.autograd.grad(closed_form(df0,diag0),(df0,diag0))
    assert grads == (None,None)
    assert all(torch.isfinite(g).all() and torch.count_nonzero(g) for g in reference_grads)
    h = 1e-4  # Central difference balances truncation and cancellation.
    fd = (closed_form(df[1]+h,diag[1])-closed_form(df[1]-h,diag[1]))/(2*h)
    torch.testing.assert_close(reference_grads[0],fd,rtol=1e-6,atol=1e-7)
