import torch
from torch import nn
from torch.distributed.checkpoint.state_dict import get_optimizer_state_dict, set_optimizer_state_dict


def test_issue_192202():
    model = nn.Sequential(nn.Linear(2, 2, bias=False), nn.Linear(2, 2, bias=False))
    p0, p1 = list(model.parameters())
    opt = torch.optim.AdamW(model.parameters())
    # Both optimizer states genuinely exist before one parameter is frozen.
    (p0.sum() + p1.sum()).backward()
    opt.step()
    opt.zero_grad(set_to_none=True)
    assert len(opt.state_dict()["state"]) == 2
    p0.requires_grad_(False)

    saved = get_optimizer_state_dict(model, opt)
    loaded_opt = torch.optim.AdamW(model.parameters())
    set_optimizer_state_dict(model, loaded_opt, saved)
    assert len(opt.state_dict()["state"]) == 2
    assert len(loaded_opt.state_dict()["state"]) == 1, (
        "Expected checkpoint load to drop optimizer state belonging to frozen parameter"
    )
