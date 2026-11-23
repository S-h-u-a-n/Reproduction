import torch


def test_issue_204033():
    # Upstream's conjugate-imaginary-view example, using fixed CPU input.
    def f(x):
        base = torch.complex(x, x + 1)
        view = base.conj().imag
        view.add_(3)
        return base, view

    x = torch.arange(1, 5, dtype=torch.float32)
    expected_before = torch.tensor([-1., 0., 1., 2.], dtype=torch.float32)
    expected_after = expected_before - 100

    eager_base, eager_view = f(x.clone())
    torch.testing.assert_close(eager_base.imag, expected_before, rtol=0, atol=0)
    assert eager_base.untyped_storage().data_ptr() == eager_view.untyped_storage().data_ptr()
    eager_view.add_(100)
    torch.testing.assert_close(eager_base.imag, expected_after, rtol=0, atol=0)

    compiled_fn = torch.compile(f, backend="inductor", fullgraph=True)
    base, view = compiled_fn(x.clone())
    torch.testing.assert_close(base.imag, expected_before, rtol=0, atol=0)
    torch.testing.assert_close(view, -expected_before, rtol=0, atol=0)

    # Exact reported bug: Inductor's returned conjugate-imag view is detached
    # from the base storage, so a post-return in-place update does not affect it.
    assert base.untyped_storage().data_ptr() != view.untyped_storage().data_ptr()
    view.add_(100)
    torch.testing.assert_close(view, -expected_before + 100, rtol=0, atol=0)
    torch.testing.assert_close(base.imag, expected_before, rtol=0, atol=0)
    assert not torch.equal(base.imag, expected_after)
