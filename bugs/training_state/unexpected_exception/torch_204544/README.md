# PyTorch #204544 — Dynamic graph retained backward rejects donated buffers

- **Cause:** `training_state`
- **Observation:** `unexpected_exception`
- **Primary API:** `torch.compile / Tensor.backward(retain_graph=True)`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/204544
- **One-sentence summary:** 動態維度編譯後的 retained backward 誤判 donated buffer 不可重複使用。
- **測試說明：** `test_bug.py` 使用固定 CPU 輸入與對照結果，辨識上游所述的故障特徵。
- **Target version:** PyTorch `2.15.0+cpu`；本套件僅提供候選，必須先通過使用者本機驗證。
- **限制：** 若 PyTorch 版本、compiler backend、CPU kernel 或例外包裝改變，此 Bug Signature 可能不成立。不要放寬斷言以換取 PASS。

## Original Issue and verification target

- **Expected:** Compiled backward with retain_graph=True should be usable under dynamic shapes as in static shapes.
- **Observed bug:** Dynamic compiled backward incorrectly raises a donated-buffer restriction exception.
- **Precise signature:** Static backward twice succeeds, dynamic retained backward raises donated buffers error.
- **Upstream version evidence:** Reported 2.14.1+cpu and 2.16 nightly CPU; target 2.15.0+cpu not independently verified
- **Benchmark limitation:** Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
