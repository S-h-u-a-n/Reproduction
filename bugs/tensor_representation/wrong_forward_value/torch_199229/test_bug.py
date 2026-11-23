import torch


def test_issue_199229():
    def fn(dest, src, backing):
        dest.set_(src)
        backing[0] = 10.0
        return dest[0].clone()

    def fresh():
        backing = torch.arange(5, dtype=torch.float32)
        return backing[:3], torch.full((3,), 7.0), backing

    eager = fn(*fresh())
    torch.testing.assert_close(eager, torch.tensor(7.0), rtol=0, atol=0)
    torch._dynamo.reset()
    dynamo_only = torch.compile(fn, backend='eager')(*fresh())
    torch.testing.assert_close(dynamo_only, eager, rtol=0, atol=0)
    torch._dynamo.reset()
    compiled = torch.compile(fn, backend='inductor')(*fresh())
    torch.testing.assert_close(compiled, torch.tensor(10.0), rtol=0, atol=0)
    assert not torch.equal(compiled, eager)
