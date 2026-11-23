# PyTorch #204442 — Sparse output layout mismatch causes transposed result

- **Cause:** `tensor_representation`
- **Observation:** `wrong_forward_value`
- **Primary API:** `torch.add / sparse CSR, CSC`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/204442
- **One-sentence summary:** CSR 輸入搭配 CSC out 的 layout 未檢查，回傳轉置的錯誤結果。
- **測試說明：** `test_bug.py` 使用固定 CPU 輸入與對照結果，辨識上游所述的故障特徵。
- **Target version:** PyTorch `2.15.0+cpu`；本套件僅提供候選，必須先通過使用者本機驗證。
- **限制：** 若 PyTorch 版本、compiler backend、CPU kernel 或例外包裝改變，此 Bug Signature 可能不成立。不要放寬斷言以換取 PASS。

## Original Issue and verification target

- **Expected:** Sparse CSR addition should either give the correct values in compatible output layouts or reject incompatible out layouts.
- **Observed bug:** Sparse CSR addition into CSC out yields transposed wrong values.
- **Precise signature:** CSR out control equals 2*A, while CSC out equals (2*A).T instead of 2*A.
- **Upstream version evidence:** Reported stable 2.15.0 and 2.16 nightly CPU; target Linux x86_64 build not independently verified
- **Benchmark limitation:** Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
