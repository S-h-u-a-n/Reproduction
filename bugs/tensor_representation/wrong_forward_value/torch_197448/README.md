# PyTorch Issue #197448

- **API**: `torch.Tensor.expand / fill_ / torch.compile`
- **Cause**: `tensor_representation`
- **Observation**: `wrong_forward_value`
- **Issue**: https://github.com/pytorch/pytorch/issues/197448
- **摘要**：對展開視圖進行 fill_ 後 compiled base 值不同於 eager
- **預期**：與 eager 正確結果或獨立數學參考一致；需要驗證原始 API 合約。
- **觀察**：`test_bug.py` 明確檢查該案例的特定錯誤特徵。
- **版本**：候選，需在 torch 2.15.0+cpu 下各 10 次獨立程序確認。
- **限制**：僅驗證此固定輸入與 CPU 路徑；不宣稱修復版本或獨立根因已完全確認。
