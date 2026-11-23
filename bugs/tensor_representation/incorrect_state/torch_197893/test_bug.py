import torch


def test_issue_197893():
    def f(x):
        return x / 1.0

    eager_x = torch.ones(3)
    eager_out = f(eager_x)
    assert eager_out is not eager_x
    eager_out.add_(5)
    torch.testing.assert_close(eager_x, torch.ones(3))

    torch._dynamo.reset()
    x = torch.ones(3)
    out = torch.compile(f, backend='inductor')(x)
    assert out is x  # issue's reported aliasing behavior
    out.add_(5)
    torch.testing.assert_close(x, torch.full((3,), 6.0))
