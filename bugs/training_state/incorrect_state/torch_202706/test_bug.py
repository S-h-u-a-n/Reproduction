import torch


def test_issue_202706():
    initial = torch.is_autocast_enabled('cpu')
    assert not initial, 'Test requires a clean autocast state'
    @torch.autocast('cpu', dtype=torch.bfloat16)
    def nested(n):
        if n:
            nested(n - 1)
    try:
        nested(1)
        assert torch.is_autocast_enabled('cpu') is True, 'Expected decorator reuse to leak autocast enabled state'
    finally:
        torch.set_autocast_enabled('cpu', initial)
