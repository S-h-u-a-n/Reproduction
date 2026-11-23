import torch


def test_issue_197448():
    def f(base):
        v = base.expand(3, -1)
        v.fill_(2.0)
        return base

    source = torch.tensor([-1.0, -0.5, 0.0, 0.5], dtype=torch.float32)
    expected = f(source.clone())
    torch.testing.assert_close(expected, torch.full_like(source, 2.0), rtol=0, atol=0)
    got = torch.compile(f, backend="inductor")(source.clone())
    assert got.shape == expected.shape
    assert torch.isfinite(got).all().item()
    # A concrete CPU observed wrong-value signature, not arbitrary mismatches.
    torch.testing.assert_close(got, torch.tensor([8.0, 7.0, 6.0, 5.0]), rtol=0, atol=0)
    assert not torch.equal(got, expected)
