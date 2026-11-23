import torch

def test_issue_202806():
    def mutate(weight, alias):
        alias.add_(1)
        return weight.sum()

    weight = torch.tensor([1.0])
    x = torch.ones_like(weight, requires_grad=True)
    loss = (x * weight).sum()
    previous_version = weight._version
    torch.compile(mutate, backend="inductor", fullgraph=True)(weight, weight.detach())
    (grad,) = torch.autograd.grad(loss, x)
    assert weight.item() == 2.0
    assert weight._version == previous_version
    assert grad.item() == 2.0
    assert grad.item() != 1.0
