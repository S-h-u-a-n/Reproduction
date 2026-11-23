import torch
from torch import nn
from torch.optim.swa_utils import AveragedModel, get_ema_multi_avg_fn


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = nn.Parameter(torch.tensor(1.0))
        self.register_buffer("state", torch.tensor(1, dtype=torch.int64))


def test_issue_203921():
    model = Model()
    averaged = AveragedModel(model, use_buffers=True, multi_avg_fn=get_ema_multi_avg_fn(0.9))
    averaged.update_parameters(model)
    assert averaged.module.state.item() == 1

    with torch.no_grad():
        model.weight.fill_(3.0)
        model.state.fill_(2)
    averaged.update_parameters(model)
    assert averaged.n_averaged.item() == 2
    # Floating-point parameter EMA should happen; stale integer state is the defect.
    assert 1.0 < averaged.module.weight.item() < 3.0
    assert model.state.item() == 2
    assert averaged.module.state.item() == 1, "Expected stale int64 EMA buffer"
