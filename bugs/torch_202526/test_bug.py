"""PyTorch known bug signature, issue #202526.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch
import torch.nn as nn

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        # Initialize a real nn.Linear without its random initializer.
        layer = nn.Linear.__new__(nn.Linear)
        nn.Module.__init__(layer)
        layer.in_features = 64
        layer.out_features = 32
        layer.weight = nn.Parameter(torch.full((32, 64), 0.0125))
        layer.bias = nn.Parameter(torch.linspace(-0.25, 0.25, 32))
        self.fc = layer
        self.bn = nn.BatchNorm1d(32)
        with torch.no_grad():
            self.bn.running_mean.copy_(torch.linspace(-0.5, 0.5, 32))
            self.bn.running_var.copy_(torch.linspace(0.5, 2.0, 32))
            self.bn.weight.fill_(1.5)
            self.bn.bias.fill_(0.2)

    def forward(self, x):
        h = self.fc(x)
        return self.bn(h) + h

def test_known_bug_signature():
    model = Model().eval()
    x = torch.arange(16 * 64, dtype=torch.float32).reshape(16, 64) / 100.0
    eager = model(x)
    traced = torch.jit.script(model)
    before_freeze = traced(x)
    torch.testing.assert_close(before_freeze, eager)
    frozen = torch.jit.freeze(traced)
    # Evaluation-mode BatchNorm is affine; the residual must still use h.
    h = x @ model.fc.weight.t() + model.fc.bias
    normalized = ((h - model.bn.running_mean)
                  / torch.sqrt(model.bn.running_var + model.bn.eps)
                  * model.bn.weight + model.bn.bias)
    # Float32 length-64 dot products and fusion reorder rounding.
    torch.testing.assert_close(eager, normalized + h, rtol=1e-5, atol=2e-5)
    actual = frozen(x)
    torch.testing.assert_close(actual, 2 * normalized, rtol=1e-5, atol=2e-5)
    assert not torch.allclose(actual, normalized + h, rtol=1e-5, atol=2e-5)
