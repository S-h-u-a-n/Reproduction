import torch


def test_issue_198070():
    previous = torch._dynamo.config.capture_scalar_outputs
    try:
        torch._dynamo.config.capture_scalar_outputs = True
        def step(loss, param):
            v = loss.item()
            if v != v:
                return param
            return param - 0.1 * v

        param = torch.ones(2)
        nan = torch.tensor(float('nan'))
        torch.testing.assert_close(step(nan, param), torch.ones(2))
        torch._dynamo.reset()
        actual = torch.compile(step, backend='eager')(nan, param)
        assert torch.isnan(actual).all().item()
    finally:
        torch._dynamo.config.capture_scalar_outputs = previous
