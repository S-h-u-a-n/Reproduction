import pytest
import torch
import torch.nn as nn


def test_issue_205810():
    def build():
        layer = nn.Conv2d(4, 4, 3, padding=1, padding_mode='replicate', bias=False)
        with torch.no_grad():
            layer.weight.copy_(torch.arange(layer.weight.numel(), dtype=torch.float32).reshape_as(layer.weight) / 100.0)
        return layer

    data = torch.arange(2 * 4 * 16 * 16, dtype=torch.float32).reshape(2, 4, 16, 16) / 100.0
    eager_x = data.clone().requires_grad_()
    eager_model = build()
    eager_out = eager_model(eager_x).sum()
    eager_out.backward()
    assert eager_x.grad is not None and torch.isfinite(eager_x.grad).all().item()

    aot_x = data.clone().requires_grad_()
    aot_model = build()
    torch._dynamo.reset()
    torch.compile(aot_model, backend='aot_eager')(aot_x).sum().backward()
    torch.testing.assert_close(aot_x.grad, eager_x.grad)

    compiled_x = data.clone().requires_grad_()
    compiled_model = build()
    torch._dynamo.reset()
    with pytest.raises(Exception) as info:
        torch.compile(compiled_model, backend='inductor')(compiled_x).sum().backward()
    message = str(info.value)
    chain = []
    obj = info.value
    seen = set()
    while obj is not None and id(obj) not in seen:
        seen.add(id(obj)); chain.append(str(obj)); obj = obj.__cause__ or obj.__context__
    chain_text = '\n'.join(chain)
    assert ('replication_pad2d_backward' in chain_text and
            ('stride' in chain_text or 'assert_tensor_metadata' in chain_text)), chain_text
