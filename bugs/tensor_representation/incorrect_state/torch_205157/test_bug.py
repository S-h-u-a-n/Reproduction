import torch


def test_issue_205157():
    def f(x):
        base = x.clone()
        return base, base.unfold(1, 1, 2).unfold(2, 4, 2)

    x = torch.ones((2, 4, 4), dtype=torch.bool)
    expected = x.clone()
    expected[:, ::2] = False

    eager_base, eager_view = f(x)
    assert eager_base.untyped_storage().data_ptr() == eager_view.untyped_storage().data_ptr()
    eager_view.fill_(False)
    assert torch.equal(eager_base, expected)

    base, view = torch.compile(f, backend="inductor", fullgraph=True)(x.clone())
    assert base.shape == x.shape
    assert view.shape == (2, 2, 1, 1, 4)
    assert torch.equal(base, x) and bool(view.all())
    # Returned alias is materialized independently by Inductor (specific wrong metadata).
    assert base.untyped_storage().data_ptr() != view.untyped_storage().data_ptr()
    view.fill_(False)
    assert not bool(view.any())
    assert torch.equal(base, x)  # should have reflected alternating-row mutation
    assert not torch.equal(base, expected)
