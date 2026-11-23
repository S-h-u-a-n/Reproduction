# PyTorch Issue #201590

- **API**: `torch.cond / torch.Tensor.copy_`
- **Cause**: `tensor_representation`
- **Observation**: `incorrect_state`
- **Issue**: https://github.com/pytorch/pytorch/issues/201590
- **摘要**：torch.cond Mutation 分支繞過 Output Alias 檢查而錯誤共享輸入儲存
- **預期**：與 eager 正確結果或獨立數學參考一致；需要驗證原始 API 合約。
- **觀察**：`test_bug.py` 明確檢查該案例的特定錯誤特徵。
- **版本**：候選，需在 torch 2.15.0+cpu 下各 10 次獨立程序確認。
- **限制**：僅驗證此固定輸入與 CPU 路徑；不宣稱修復版本或獨立根因已完全確認。
