import torch


def test_issue_205616():
    x = torch.tensor(3.0)
    reference = torch.amax(x, out=torch.empty_like(x))
    actual = torch.amax(x, out=x)
    assert reference.item() == 3.0
    assert actual.item() == float('-inf')
    assert x.item() == float('-inf')
