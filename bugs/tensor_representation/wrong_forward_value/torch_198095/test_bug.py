import torch

def test_issue_198095():
    def fn(base, alias):
        base.add_(100)
        return alias[0]
    original = torch.arange(24, dtype=torch.float64).reshape(4, 6)
    eager_base = original.clone()
    eager = fn(eager_base, eager_base[1:])
    compiled_base = original.clone()
    compiled = torch.compile(fn, backend="aot_eager")(compiled_base, compiled_base[1:])
    torch.testing.assert_close(eager, torch.arange(106, 112, dtype=torch.float64))
    torch.testing.assert_close(compiled, torch.arange(100, 106, dtype=torch.float64))
    assert not torch.equal(eager, compiled)
