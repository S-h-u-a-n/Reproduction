import copy
import torch


def test_issue_196083():
    pa = torch.nn.Parameter(torch.tensor([1.0, 2.0]))
    pb = torch.nn.Parameter(torch.tensor([1.0, 2.0]))
    opt_a = torch.optim.SGD([pa], lr=0.1, momentum=0.9)
    opt_b = torch.optim.SGD([pb], lr=0.1, momentum=0.9)

    pa.grad = torch.tensor([1.0, 2.0])
    opt_a.step()
    buf_a = opt_a.state[pa]['momentum_buffer']
    original = buf_a.clone()
    torch.testing.assert_close(original, torch.tensor([1.0, 2.0]), rtol=0, atol=0)

    saved = opt_a.state_dict()
    assert saved['state'][0]['momentum_buffer'].data_ptr() == buf_a.data_ptr()
    opt_b.load_state_dict(saved)
    buf_b = opt_b.state[pb]['momentum_buffer']
    assert buf_a.data_ptr() == buf_b.data_ptr(), 'Expected upstream in-process state aliasing'

    pb.grad = torch.tensor([3.0, 4.0])
    opt_b.step()
    torch.testing.assert_close(buf_a, 0.9 * original + pb.grad, rtol=1e-6, atol=1e-6)
    assert not torch.equal(buf_a, original), 'Stepping opt_b changed opt_a momentum state'
