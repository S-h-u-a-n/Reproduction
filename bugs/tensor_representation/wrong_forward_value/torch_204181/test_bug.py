import torch


def test_issue_204181():
    reference = torch.zeros(7, 2)
    reference.fill_diagonal_(1, wrap=True)
    base = torch.zeros(7, 3)
    view = base.narrow(1, 0, 2)
    assert not view.is_contiguous()
    view.fill_diagonal_(1, wrap=True)
    assert not torch.equal(view, reference)
    assert base[5, 2].item() == 1.0  # outside the selected view
    assert reference[6, 0].item() == 1.0
    assert view[6, 0].item() == 0.0
