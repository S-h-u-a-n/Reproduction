import pytest
import torch
import torch.nn as nn

class FixedConv2d(nn.Conv2d):
    def reset_parameters(self):
        # Called during construction; initialize without RNG.
        with torch.no_grad():
            self.weight.copy_(
                torch.arange(
                    self.weight.numel(),
                    dtype=self.weight.dtype,
                    device=self.weight.device,
                ).reshape_as(self.weight) / 100.0
            )


def test_issue_205810():
    def build():
        return FixedConv2d(
            4,
            4,
            3,
            padding=1,
            padding_mode="replicate",
            bias=False,
            device="cpu",
            dtype=torch.float32,
        )

    data = (
        torch.arange(2 * 4 * 16 * 16, dtype=torch.float32)
        .reshape(2, 4, 16, 16) / 100.0
    )

    # Control: eager backward succeeds.
    eager_x = data.clone().requires_grad_()
    eager_model = build()
    eager_model(eager_x).sum().backward()
    assert eager_x.grad is not None
    assert torch.isfinite(eager_x.grad).all().item()

    # Control: aot_eager backward agrees with eager.
    aot_x = data.clone().requires_grad_()
    aot_model = build()
    torch._dynamo.reset()
    torch.compile(aot_model, backend="aot_eager")(aot_x).sum().backward()
    torch.testing.assert_close(aot_x.grad, eager_x.grad)

    # Inductor forward must succeed before checking the backward failure.
    compiled_x = data.clone().requires_grad_()
    compiled_model = build()
    torch._dynamo.reset()
    compiled_loss = torch.compile(
        compiled_model, backend="inductor"
    )(compiled_x).sum()

    # Known bug: backward rejects replication_pad2d_backward output strides.
    with pytest.raises(
        AssertionError,
        match=r"expected size 4==4, stride 1==256 at dim=1",
    ) as info:
        compiled_loss.backward()

    assert (
        "torch.ops.aten.replication_pad2d_backward.default"
        in str(info.value)
    )