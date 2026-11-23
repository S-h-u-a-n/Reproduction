import torch


def test_issue_197811():
    def make(op):
        def fn(x, y):
            return op(x, y)
        return fn

    add = make(torch.Tensor.__add__)
    mul = make(torch.Tensor.__mul__)
    x, y = torch.tensor(6.0), torch.tensor(3.0)
    assert add(x, y).item() == 9.0
    assert mul(x, y).item() == 18.0
    torch._dynamo.reset()
    cadd = torch.compile(add, dynamic=True)
    cmul = torch.compile(mul, dynamic=True)
    assert cadd(x, y).item() == 9.0
    assert cmul(x, y).item() == 9.0
