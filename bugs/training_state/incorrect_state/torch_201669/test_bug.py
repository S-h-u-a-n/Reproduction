import copy
import torch


def test_issue_201669():
    p = torch.nn.Parameter(torch.tensor([1.0, 2.0], dtype=torch.bfloat16))
    source = torch.optim.SGD([p], lr=0.1, momentum=0.9)
    source.state[p]['momentum_buffer'] = torch.tensor([1025.0, 1.00390625], dtype=torch.float32)
    snapshot = copy.deepcopy(source.state_dict())
    assert snapshot['state'][0]['momentum_buffer'].dtype == torch.float32
    restored = torch.optim.SGD([p], lr=0.1, momentum=0.9)
    restored.load_state_dict(snapshot)
    actual = restored.state[p]['momentum_buffer']
    assert actual.dtype == torch.bfloat16
    torch.testing.assert_close(actual.float(), torch.tensor([1024.0, 1.0]), rtol=0, atol=0)
    assert not torch.equal(actual.float(), snapshot['state'][0]['momentum_buffer'])
    assert snapshot['state'][0]['momentum_buffer'].dtype == torch.float32
