# PyTorch Issue #204407

上游標題：[Autograd] Incorrect first-order gradient for torch.linalg.slogdet with conj().imag input

[GitHub Issue](https://github.com/pytorch/pytorch/issues/204407) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`training_state`
- Primary Observation：`wrong_gradient`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`autograd`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.linalg.slogdet` | 主要受測 API |
| `torch.Tensor.conj` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.Tensor.imag` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

A=z.conj().imag，negative view、stride=(4,2)、offset=1。

## 正確行為與實際行為

**Expected Behavior：** local gradient=A^-T；鏈式 z.grad.imag=-A^-T。

**Actual Behavior：** off-diagonal gradient 轉置，real gradient 仍零。

## 錯誤簽名（Bug Signature）

off-diagonal gradient 轉置，real gradient 仍零。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Required operand is a negative view, float64 shape (2,2), stride (4,2), storage_offset=1, aliasing z. Local a.grad has off-diagonal transpose error; chained z.grad.imag=[[-0.3,0.1],[0.2,-0.4]]. Full gradients checked at atol=1e-12, rtol=0; negative-view trigger distinguished from merely noncontiguous layout.

## 分類理由與根因證據

上游分析指出 negative fallback clone 改變 layout，forward LU 與 backward 對原 layout 的轉置判斷不一致。

上游內文／討論提供機制分析，未自行修補驗證：上游分析指出 negative fallback clone 改變 layout，forward LU 與 backward 對原 layout 的轉置判斷不一致。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/204407)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/204407#issuecomment-6977006695)、[討論 2](https://github.com/pytorch/pytorch/issues/204407#issuecomment-6977162538)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_204407`。本案檢查的是「off-diagonal gradient 轉置，real gradient 仍零」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「local gradient=A^-T；鏈式 z.grad.imag=-A^-T」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_gradient/torch_204407/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/204407) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

必須同時保留 negative bit、stride=(4,2)、offset=1 與 alias；z.grad.imag 必須包含 A=-imag(z) 的負號鏈式法則。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_204407/`
- 新路徑：`bugs/tensor_representation/wrong_gradient/torch_204407/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`074586e03f1b760ff51ed7141181877f7b50390009cb4313149dba8ad67a1d21`
- metadata.json SHA-256：`53a3090829458f8782f7d6b392d53dcf16b4d0ef6b38313eee26c2086a7c7a0c`
- 核對時 Issue body SHA-256：`04207b9d734b5d6cfa193b704393d17daf3c11e8219045d3b254b7c8e23554e6`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
