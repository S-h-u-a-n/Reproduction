# PyTorch Issue #198669

上游標題：torch.compile (Inductor): NotImplementedError negating a bool tensor when softmax follows eq→div; eager works

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198669) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`unexpected_exception`
- Secondary Observations：`無`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.softmax` | 主要受測 API |
| `torch.eq` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.div` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

eq 產生 bool，除法升成 floating 後 softmax。

## 正確行為與實際行為

**Expected Behavior：** softmax 應成功。

**Actual Behavior：** rewrite 嘗試對 bool 做 negation 而拋例外。

## 錯誤簽名（Bug Signature）

rewrite 嘗試對 bool 做 negation 而拋例外。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Inductor attempts invalid boolean negation while lowering softmax.

## 分類理由與根因證據

上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198669)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198669#issuecomment-5837948073)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「rewrite 嘗試對 bool 做 negation 而拋例外」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「softmax 應成功」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/unexpected_exception/torch_198669/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198669) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

上游討論連至 #196743 的 scaled-softmax rewrite；該 Issue 不在本次清單，未另增案例。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198669/`
- 新路徑：`bugs/tensor_representation/unexpected_exception/torch_198669/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`6a2e1307cc83acd34a0cf08be5fc80c8445c6eeb58426ef80bf16b4a7f6babc3`
- metadata.json SHA-256：`626f22bf4b04b812147591a2d067e1d33a7012e9a3d321cf0b5b279306947e12`
- 核對時 Issue body SHA-256：`36306cae40287dcf04c72d6bafbfbc296c1670876ebc36e2a9ca74fcedba7986`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
