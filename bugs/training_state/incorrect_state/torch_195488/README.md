# PyTorch #195488 — Autocast nesting leaked after compiled exception

- **Cause:** `training_state`
- **Observation:** `incorrect_state`
- **Primary API:** `torch.amp.autocast / torch.compile`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/195488
- **One-sentence summary:** 編譯區域發生例外時 autocast nesting 未正常清理，造成後續訓練狀態洩漏。
- **測試說明：** `test_bug.py` 使用固定 CPU 輸入與對照結果，辨識上游所述的故障特徵。
- **Target version:** PyTorch `2.15.0+cpu`；本套件僅提供候選，必須先通過使用者本機驗證。
- **限制：** 若 PyTorch 版本、compiler backend、CPU kernel 或例外包裝改變，此 Bug Signature 可能不成立。不要放寬斷言以換取 PASS。

## Original Issue and verification target

- **Expected:** Autocast context and nesting are restored after an exception inside compiled region.
- **Observed bug:** Compiled runtime exception leaves an unmatched autocast nesting level.
- **Precise signature:** index_select throws IndexError, compiled context retains the nesting count while eager would restore it.
- **Upstream version evidence:** Reported on main; target 2.15.0+cpu not independently verified
- **Benchmark limitation:** Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
