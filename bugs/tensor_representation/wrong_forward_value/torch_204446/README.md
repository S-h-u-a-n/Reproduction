# PyTorch Issue #204446

上游標題：[Bug][Sparse] In-place add_ of a sparse COO tensor to a dense view silently writes to the wrong offset or corrupts the heap

[GitHub Issue](https://github.com/pytorch/pytorch/issues/204446) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`incorrect_state`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`storage_aliasing`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.add_` | 主要受測 API |
| `torch.sparse_coo_tensor` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

對 base[1] 的 contiguous 非零 offset view 加 COO。

## 正確行為與實際行為

**Expected Behavior：** 只修改 row 1。

**Actual Behavior：** 錯改 row 2。

## 錯誤簽名（Bug Signature）

錯改 row 2。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Contiguous view with storage_offset=8 writes eight ones into row 2. Only the in-bounds numeric case is tested, not the heap-corruption variant.

## 分類理由與根因證據

上游定位 sparse CPU kernel 重複套用 storage_offset；本地刻意只測 allocation 內的錯位寫入。

上游內文／討論提供機制分析，未自行修補驗證：上游定位 sparse CPU kernel 重複套用 storage_offset；本地刻意只測 allocation 內的錯位寫入。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/204446)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/204446#issuecomment-6802629240)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_204446`。本案檢查的是「錯改 row 2」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「只修改 row 1」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_204446/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/204446) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

本地只驗證 allocation 內的錯誤 row，未執行上游 heap corruption／process crash 變體。與 #59101 的重複根因尚未確認。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_204446/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_204446/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`6e279899660a0c4e9c29fd2b6295715400f605ccb3891d5a321400877fc0d2b4`
- metadata.json SHA-256：`9e263e2912d6a8bac9d12031331834ed466b5e8c7f8daa2c7d160d33fea2eb2e`
- 核對時 Issue body SHA-256：`d516c0a37a02e5280add5998a0e6f27aedba9cb0ec99ad3f74d746592f94b714`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
