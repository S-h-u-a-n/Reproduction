import torch


def test_issue_206126():
    n = 3
    d = torch.arange(2.0, 2.0 + n, dtype=torch.float64)
    lower = torch.eye(n, dtype=torch.float64) + torch.diag(torch.ones(n - 1, dtype=torch.float64), diagonal=-1)
    exact = torch.diag(d + 1) + torch.diag(torch.ones(n - 1, dtype=torch.float64), diagonal=-1)
    a = lower @ torch.diag(d) @ lower.T
    b = a @ exact
    factor, pivots = torch.linalg.lu_factor(a)
    reference = torch.linalg.lu_solve(factor.clone(), pivots, b.clone())
    torch.testing.assert_close(reference, exact, atol=1e-10, rtol=1e-10)

    good_factor, good_rhs = factor.clone(), b.clone()
    separate = torch.linalg.lu_solve(good_factor, pivots, good_rhs, out=torch.empty_like(b))
    torch.testing.assert_close(separate, exact, atol=1e-10, rtol=1e-10)

    rhs_factor, rhs = factor.clone(), b.clone()
    rhs_out = torch.linalg.lu_solve(rhs_factor, pivots, rhs, out=rhs)
    torch.testing.assert_close(rhs_out, exact, atol=1e-10, rtol=1e-10)

    aliased_factor, aliased_rhs = factor.clone(), b.clone()
    assert aliased_factor.data_ptr() != aliased_rhs.data_ptr()
    corrupted = torch.linalg.lu_solve(aliased_factor, pivots, aliased_rhs, out=aliased_factor)
    assert corrupted.data_ptr() == aliased_factor.data_ptr()
    assert torch.isfinite(corrupted).all().item()
    residual = (a @ corrupted - b).abs().max().item()
    assert residual > 1.0, f"Expected in-place LU factor corruption; residual={residual}"
