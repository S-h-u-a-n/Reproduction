import torch
from torch.ao.quantization.observer import PerChannelMinMaxObserver, MinMaxObserver


def test_issue_199151():
    configured = {"dtype": torch.float64}
    per_channel = PerChannelMinMaxObserver(ch_axis=0, factory_kwargs=configured)
    control = MinMaxObserver(factory_kwargs=configured)
    assert per_channel.min_val.dtype == torch.float64
    assert per_channel.max_val.dtype == torch.float64
    assert control.min_val.dtype == torch.float64

    per_channel.reset_min_max_vals()
    control.reset_min_max_vals()
    assert control.min_val.dtype == torch.float64
    assert control.max_val.dtype == torch.float64
    assert per_channel.min_val.dtype == torch.float32
    assert per_channel.max_val.dtype == torch.float32

    per_channel(torch.arange(12.0, dtype=torch.float64).reshape(3, 4))
    assert per_channel.min_val.dtype == torch.float32
