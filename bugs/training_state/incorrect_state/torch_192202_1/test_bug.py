import torch
from torch import nn
from torch.distributed.checkpoint.state_dict import (
    get_optimizer_state_dict,
)


def test_partial_optimizer_state_is_not_initialized():
    model = nn.Sequential(
        nn.Linear(2, 2, bias=False),
        nn.Linear(2, 2, bias=False),
    )
    p0, p1 = model.parameters()
    opt = torch.optim.AdamW(model.parameters())

    # 只有 p0 參與計算，因此只有 p0 建立 optimizer state。
    p0.sum().backward()
    assert p0.grad is not None
    assert p1.grad is None

    opt.step()
    opt.zero_grad(set_to_none=True)

    assert set(opt.state_dict()["state"]) == {0}
    assert p0 in opt.state
    assert p1 not in opt.state

    p0.requires_grad_(False)
    assert not p0.requires_grad
    assert p1.requires_grad

    saved = get_optimizer_state_dict(model, opt)

    actual_keys = set(saved["state"])
    buggy_keys = {"0.weight"}
    correct_keys = {"0.weight", "1.weight"}

    # 精確確認：保留了 p0，但沒有補齊仍可訓練的 p1。
    assert actual_keys == buggy_keys, (
        f"Expected missing state for trainable p1, got {actual_keys}"
    )
    assert actual_keys != correct_keys