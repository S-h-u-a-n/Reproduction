import torch


def test_issue_195488():
    def probe():
        current = torch.autocast_increment_nesting()
        torch.autocast_decrement_nesting()
        return current - 1

    def f(x, idx):
        with torch.amp.autocast("cpu", dtype=torch.bfloat16):
            return x.index_select(0, idx)

    compiled = torch.compile(f, backend="eager", fullgraph=True)
    x = torch.arange(16.0).reshape(4, 4)
    bad_index = torch.tensor([99], dtype=torch.long)
    before = probe()
    assert before == 0
    try:
        try:
            compiled(x, bad_index)
        except IndexError as exc:
            assert "out of" in str(exc).lower() or "index" in str(exc).lower()
        else:
            raise AssertionError("Expected the original index_select index exception")
        after = probe()
        assert after > before, f"Expected leaked autocast nesting, got {before}->{after}"
    finally:
        # Important: this test must not contaminate other tests in the same process.
        for _ in range(max(0, probe() - before)):
            torch.autocast_decrement_nesting()
