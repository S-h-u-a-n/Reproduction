import torch
from torch import nn
from torch.distributed.checkpoint.state_dict import (
    get_optimizer_state_dict,
    set_optimizer_state_dict,
)


def test_frozen_parameter_state_is_dropped():
    model = nn.Sequential(
        nn.Linear(2, 2, bias=False),
        nn.Linear(2, 2, bias=False),
    )
    p0, p1 = model.parameters()
    opt = torch.optim.AdamW(model.parameters())

    # 為兩個參數建立 optimizer state。
    (p0.sum() + p1.sum()).backward()
    opt.step()
    opt.zero_grad(set_to_none=True)

    assert set(opt.state_dict()["state"]) == {0, 1}

    p0.requires_grad_(False)
    assert not p0.requires_grad
    assert p1.requires_grad

    # 確認匯出時兩個參數的 state 都完整存在。
    saved = get_optimizer_state_dict(model, opt)
    assert set(saved["state"]) == {"0.weight", "1.weight"}

    loaded_opt = torch.optim.AdamW(model.parameters())
    assert len(loaded_opt.state) == 0

    set_optimizer_state_dict(model, loaded_opt, saved)

    # 原 optimizer 的 state 仍完整。
    assert set(opt.state_dict()["state"]) == {0, 1}

    actual_keys = set(loaded_opt.state_dict()["state"])
    buggy_keys = {1}
    correct_keys = {0, 1}

    # 精確確認：消失的是凍結參數 p0 的 state。
    assert actual_keys == buggy_keys, (
        f"Expected frozen p0's state to be dropped, got {actual_keys}"
    )
    assert actual_keys != correct_keys

    # 未凍結參數 p1 的 state 應正常載入。
    assert set(loaded_opt.state[p1]) == set(opt.state[p1])
    for name, expected in opt.state[p1].items():
        torch.testing.assert_close(
            loaded_opt.state[p1][name],
            expected,
            rtol=0,
            atol=0,
        )