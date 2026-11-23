import torch


def test_issue_204426():
    def f(x):
        with torch.no_grad():
            view = x[1:]
        return view, x * 2

    def run(compiled):
        x = torch.arange(1., 5., dtype=torch.float32, requires_grad=True)
        fun = torch.compile(f, backend="inductor", fullgraph=True) if compiled else f
        view, y = fun(x)
        torch.testing.assert_close(view, x.detach()[1:])
        torch.testing.assert_close(y, 2 * x.detach())
        (view.sum() + y.sum()).backward()
        return x.grad.detach().clone()

    eager = run(False)
    got = run(True)
    torch.testing.assert_close(eager, torch.tensor([2., 2., 2., 2.]), rtol=0, atol=0)
    torch.testing.assert_close(got, torch.tensor([2., 3., 3., 3.]), rtol=0, atol=0)
