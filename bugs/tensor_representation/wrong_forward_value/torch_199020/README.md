# PyTorch Issue #199020

- **API**: `torch.cummax(out=...)`
- **Cause**: `tensor_representation`
- **Observation**: `wrong_forward_value`
- **Issue**: https://github.com/pytorch/pytorch/issues/199020
- **摘要**：values 與 indices 的 out buffer 重疊而產生錯誤數值
- **預期**：與 eager 正確結果或獨立數學參考一致；需要驗證原始 API 合約。
- **觀察**：`test_bug.py` 明確檢查該案例的特定錯誤特徵。
- **版本**：候選，需在 torch 2.15.0+cpu 下各 10 次獨立程序確認。
- **限制**：僅驗證此固定輸入與 CPU 路徑；不宣稱修復版本或獨立根因已完全確認。
