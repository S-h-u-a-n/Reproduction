# PyTorch Issue #197893

上游標題：[inductor] `x + 0` / `x * 1` / `x / 1.0` as a graph output returns the input tensor itself (`out is x`), so an in-place update of the result silently corrupts the input

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197893) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`incorrect_state`
- Secondary Observations：`wrong_forward_value`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`storage_aliasing`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.div` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

編譯 x/1 後修改回傳 tensor。

## 正確行為與實際行為

**Expected Behavior：** out-of-place 除法產生獨立結果。

**Actual Behavior：** 結果與 input 共用 storage，修改相互影響。

## 錯誤簽名（Bug Signature）

結果與 input 共用 storage，修改相互影響。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Inductor optimizes x / 1 into the same tensor; mutating the result also mutates the input.

## 分類理由與根因證據

remove_no_ops 把圖輸出替換為 input，改變 alias 契約。

上游內文／討論提供機制分析，未自行修補驗證：remove_no_ops 把圖輸出替換為 input，改變 alias 契約。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197893)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/197893#issuecomment-5764735138)、[討論 2](https://github.com/pytorch/pytorch/issues/197893#issuecomment-5770407235)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_197893`。本案檢查的是「結果與 input 共用 storage，修改相互影響」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「out-of-place 除法產生獨立結果」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/incorrect_state/torch_197893/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197893) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197893/`
- 新路徑：`bugs/tensor_representation/incorrect_state/torch_197893/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`71298cd809689c796f6d2667ecf8c81df0592b1585ed02f0f09ce20dd7549fb0`
- metadata.json SHA-256：`267f78aa94ae97e8c24f31485668cbc1eba772f8409e779bbe1a9135eee91e61`
- 核對時 Issue body SHA-256：`97b91544ce752f983701d9310676ff84a94337a3b68052cd2c1baa807214ade8`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
