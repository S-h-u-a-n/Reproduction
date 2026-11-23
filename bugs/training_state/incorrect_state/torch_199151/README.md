# PyTorch #199151 — Observer reset discards configured buffer dtype

- **Cause:** `training_state`
- **Observation:** `incorrect_state`
- **Primary API:** `torch.ao.quantization.observer.PerChannelMinMaxObserver`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/199151
- **One-sentence summary:** PerChannelMinMaxObserver 在 reset 後丟失 float64 dtype 設定，導致狀態 dtype 回退。
- **測試說明：** `test_bug.py` 使用固定 CPU 輸入與對照結果，辨識上游所述的故障特徵。
- **Target version:** PyTorch `2.15.0+cpu`；本套件僅提供候選，必須先通過使用者本機驗證。
- **限制：** 若 PyTorch 版本、compiler backend、CPU kernel 或例外包裝改變，此 Bug Signature 可能不成立。不要放寬斷言以換取 PASS。

## Original Issue and verification target

- **Expected:** Observer reset preserves the configured float64 dtype of min_val and max_val buffers.
- **Observed bug:** Per-channel reset allocates fresh float32 buffer tensors.
- **Precise signature:** PerChannelMinMaxObserver loses float64 on reset, unlike MinMaxObserver.
- **Upstream version evidence:** Reported 2.14.0+cpu; target 2.15.0+cpu not independently verified
- **Benchmark limitation:** Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
