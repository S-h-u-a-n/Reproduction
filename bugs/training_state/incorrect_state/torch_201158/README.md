# PyTorch #201158 — Selective activation checkpoint cache aliases reused compiler buffer

- **Cause:** `training_state`
- **Observation:** `incorrect_state`
- **Primary API:** `torch.utils.checkpoint.create_selective_checkpoint_contexts`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/201158
- **One-sentence summary:** Selective checkpointing 快取持有 Inductor 之後重用的 buffer，導致已儲存的中間 Tensor 被覆寫。
- **測試說明：** `test_bug.py` 使用固定 CPU 輸入與對照結果，辨識上游所述的故障特徵。
- **Target version:** PyTorch `2.15.0+cpu`；本套件僅提供候選，必須先通過使用者本機驗證。
- **限制：** 若 PyTorch 版本、compiler backend、CPU kernel 或例外包裝改變，此 Bug Signature 可能不成立。不要放寬斷言以換取 PASS。

## Original Issue and verification target

- **Expected:** Selective checkpoint cache must retain the original activation values after compilation.
- **Observed bug:** An Inductor memory-planning buffer reuse overwrites a tensor stored by selective checkpointing.
- **Precise signature:** Forward output matches eager but forward.storage contains different activation values.
- **Upstream version evidence:** Reported with CPU reproducer and accelerator training evidence; target 2.15.0+cpu not independently verified
- **Benchmark limitation:** Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
