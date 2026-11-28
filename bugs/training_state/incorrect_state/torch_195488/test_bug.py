import subprocess
import sys
import textwrap


def test_issue_195488():
    code = textwrap.dedent("""
        import pytest
        import torch

        def nesting():
            current = torch.autocast_increment_nesting()
            torch.autocast_decrement_nesting()
            return current - 1

        def f(x, idx):
            with torch.amp.autocast("cpu", dtype=torch.bfloat16):
                return x.index_select(0, idx)

        # 固定輸入，不使用隨機數。
        x = torch.arange(16, dtype=torch.float32).reshape(4, 4)
        bad_index = torch.tensor([99], dtype=torch.long)

        before = nesting()
        assert before == 0, f"Expected clean nesting, got {before}"

        # 對照組：未編譯時，即使拋出例外，也應恢復 nesting。
        eager_counts = []
        for _ in range(3):
            with pytest.raises(IndexError, match=r"(?i)out of range"):
                f(x, bad_index)
            eager_counts.append(nesting())

        correct_counts = [before] * 3
        assert eager_counts == correct_counts, (
            f"Eager execution failed to restore nesting: {eager_counts}"
        )

        # 實驗組：相同函式經過 Dynamo 編譯後，每次例外洩漏一層。
        compiled = torch.compile(f, backend="eager", fullgraph=True)

        compiled_counts = []
        for _ in range(3):
            with pytest.raises(IndexError, match=r"(?i)out of range"):
                compiled(x, bad_index)
            compiled_counts.append(nesting())

        buggy_counts = [before + 1, before + 2, before + 3]

        assert compiled_counts == buggy_counts, (
            f"Expected nesting leak {buggy_counts}, got {compiled_counts}"
        )
        assert compiled_counts != correct_counts
    """)

    # 使用相同 Python 環境，但隔離 autocast 狀態。
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=120,
    )

    assert result.returncode == 0, (
        "Bug reproduction subprocess failed.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )