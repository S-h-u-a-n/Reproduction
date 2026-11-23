"""https://github.com/pytorch/pytorch/issues/200599 — singleton batch stride."""

import torch


def test_issue_200599():
    # Same minimal reproducer, with explicit dtype instead of a global default.
    matrices = torch.tensor(
        [[[2., 1.], [1., 3.]], [[4., 1.], [2., 5.]]], dtype=torch.float64
    )
    rhs = torch.tensor([[[1.], [2.]]], dtype=torch.float64)
    lu, pivots = torch.linalg.lu_factor(matrices)
    lu4 = lu[:, None]
    assert lu4.stride() == (4, 2, 1, 2)

    actual = torch.linalg.lu_solve(lu4, pivots[:, None], rhs).flatten()
    control = torch.linalg.lu_solve(lu4.contiguous(), pivots[:, None], rhs).flatten()
    expected = torch.tensor([0.2, 0.6, 1 / 6, 1 / 3], dtype=torch.float64)
    buggy = torch.tensor([0.2, 0.6, 5., -1.], dtype=torch.float64)
    torch.testing.assert_close(control, expected, rtol=0, atol=1e-12)
    torch.testing.assert_close(
        torch.linalg.solve(matrices, rhs).flatten(), expected, rtol=0, atol=1e-12
    )
    torch.testing.assert_close(actual, buggy, rtol=0, atol=1e-12)
    assert not torch.allclose(actual, expected, rtol=0, atol=1e-12)
