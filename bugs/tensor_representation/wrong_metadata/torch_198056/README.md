# PyTorch Issue #198056

上游標題：[dynamo][numpy] dtype and shape divergences of NumPy code under `torch.compile`: `np.cumsum(int8)` overflows in int8, `np.square(int8)` returns float64, `np.median` returns shape `(1,)`, `np.any` returns uint8, uint16/32/64 arithmetic raises

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198056) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_metadata`
- Secondary Observations：`wrong_forward_value`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `numpy.cumsum` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

編譯 int8 NumPy 累加。

## 正確行為與實際行為

**Expected Behavior：** 使用 int64 累加並保留完整參考結果。

**Actual Behavior：** 維持 int8 dtype 並發生 wraparound。

## 錯誤簽名（Bug Signature）

維持 int8 dtype 並發生 wraparound。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Complete seven-element cumsum reference uses NumPy int64 accumulation; compiled int8 values follow wraparound. Full arrays and dtype are checked.

## 分類理由與根因證據

NumPy 到 tensor 的 dtype promotion 表示未保存。

上游內文／討論提供機制分析，未自行修補驗證：NumPy 到 tensor 的 dtype promotion 表示未保存。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198056)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198056#issuecomment-6122337726)、[討論 2](https://github.com/pytorch/pytorch/issues/198056#issuecomment-6143825592)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「維持 int8 dtype 並發生 wraparound」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「使用 int64 累加並保留完整參考結果」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_metadata/torch_198056/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198056) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

Issue 包含多種 dtype/shape 症狀；本地只測 int8 cumsum。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198056/`
- 新路徑：`bugs/tensor_representation/wrong_metadata/torch_198056/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`87d8cb06e2453e83098b6aea670da9959d758e97ce8bc7c6d0fac91ca617c3f6`
- metadata.json SHA-256：`db33b81746071da7482203e5b64b0e200a4accf5c5a2d65456dabe9765cdc04d`
- 核對時 Issue body SHA-256：`d409208f65c0c025d65d261820623dd5f892d853bc8a000953bbfcee6fd0635d`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
