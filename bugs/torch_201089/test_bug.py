# Source: https://github.com/pytorch/pytorch/issues/201089
import torch
import torch.nn as nn


def test_issue_201089():
    class Counter(nn.Module):
        def __init__(self):
            super().__init__()
            self.lin = nn.Linear(4, 4)
            with torch.no_grad():
                self.lin.weight.fill_(1.)
                self.lin.bias.fill_(0.5)
            self.register_buffer("n", torch.zeros(()))

        def forward(self, x):
            self.n.add_(1)
            scale = torch.clamp((self.n + 1) / 20, max=1.0)
            return self.lin(x) * scale

    def run(backend):
        model = Counter()
        x = torch.ones((2, 4))
        fn = model if backend is None else torch.compile(model, backend=backend, fullgraph=True)
        output = fn(x)
        output.sum().backward()
        return output.detach().clone(), model.lin.weight.grad.detach().clone(), model.n.item()

    torch._dynamo.reset()
    expected_out, expected_grad, expected_counter = run(None)
    torch._dynamo.reset()
    got_out, got_grad, got_counter = run("aot_eager")
    torch.testing.assert_close(expected_out, torch.full((2, 4), 0.45), rtol=0, atol=1e-6)
    torch.testing.assert_close(got_out, expected_out, rtol=0, atol=1e-6)
    assert expected_counter == got_counter == 1.0
    torch.testing.assert_close(expected_grad, torch.full((4, 4), 0.2), rtol=0, atol=1e-6)
    torch.testing.assert_close(got_grad, torch.full((4, 4), 0.3), rtol=0, atol=1e-6)
