# PyTorch Issue #197092

上游標題：[compiled autograd] backward of `F.interpolate(mode="bilinear"/"bicubic"/"linear"/"trilinear")` fails with `isIntList() INTERNAL ASSERT FAILED` while running meta for `aten.upsample_bilinear2d_backward`

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197092) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`無`
- Primary Observation：`unexpected_exception`
- Secondary Observations：`無`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.nn.functional.interpolate` | 主要受測 API |
| `torch._dynamo.compiled_autograd._enable` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

compiled autograd、bilinear interpolation backward。

## 正確行為與實際行為

**Expected Behavior：** 反向成功或受支援的 fallback。

**Actual Behavior：** fake-tensor propagation 出現 isIntList INTERNAL ASSERT。

## 錯誤簽名（Bug Signature）

fake-tensor propagation 出現 isIntList INTERNAL ASSERT。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Compiled backward fails fake tensor propagation with isIntList INTERNAL ASSERT.

## 分類理由與根因證據

問題位於 backward node 的參數傳遞；上游僅提出 int-list／scalar packing 的疑似原因，未確認完整根因。

Root cause not confirmed。問題位於 backward node 的參數傳遞；上游僅提出 int-list／scalar packing 的疑似原因，未確認完整根因。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197092)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_197092`。本案檢查的是「fake-tensor propagation 出現 isIntList INTERNAL ASSERT」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「反向成功或受支援的 fallback」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/unexpected_exception/torch_197092/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197092) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

根因證據尚不足；分類依已知必要觸發條件。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197092/`
- 新路徑：`bugs/training_state/unexpected_exception/torch_197092/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`634fd1ddbd5e89ee1d495a32f835618fc12472e384311303b47f95a53d4c7692`
- metadata.json SHA-256：`5509d752d3d2ef8f931ea52e6b8bb0f0f5268c7ed7bb6240877dfe206699c7b7`
- 核對時 Issue body SHA-256：`63f7bc62bc4bc9472c8664fdd028ca861cff4b01b183efb00b56ebdaf8a301db`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
