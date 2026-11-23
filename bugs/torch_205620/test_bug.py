import torch


def test_issue_205620():
    a0 = torch.diag(torch.tensor([2., 4.], dtype=torch.float64))
    b0 = torch.diag(torch.tensor([6., 20.], dtype=torch.float64))
    expected = torch.diag(torch.tensor([3., 5.], dtype=torch.float64))
    reference = torch.linalg.solve_triangular(a0.clone(), b0.clone(), upper=False)
    a, b = a0.clone(), b0.clone()
    actual = torch.linalg.solve_triangular(a, b, upper=False, out=a)
    torch.testing.assert_close(reference, expected, rtol=0, atol=0)
    torch.testing.assert_close(actual, torch.eye(2, dtype=torch.float64), rtol=0, atol=0)
    assert not torch.allclose(actual, expected)
    assert (a0 @ actual - b0).abs().max().item() == 16.0
