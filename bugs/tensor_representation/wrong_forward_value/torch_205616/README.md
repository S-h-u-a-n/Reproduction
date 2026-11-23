# PyTorch Issue #205616

上游標題：[CPU] Eager scalar reductions return incorrect values when `out` aliases the input

[GitHub Issue](https://github.com/pytorch/pytorch/issues/205616) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`incorrect_state`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`storage_aliasing`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.amax` | 主要受測 API |

## 觸發條件

零維 CPU tensor x=3，out=x。

## 正確行為與實際行為

**Expected Behavior：** 獨立 out 控制為 3；alias 情境不得靜默產生錯值。

**Actual Behavior：** 輸出與 input 都被改為 -inf。

## 錯誤簽名（Bug Signature）

輸出與 input 都被改為 -inf。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> CPU torch.amax(x, out=x) returns -inf and overwrites the scalar input.

## 分類理由與根因證據

上游定位 reduction 先把 out 初始化為 identity，覆蓋尚未讀取的 aliased input；是否應明確拒絕 overlap 待上游決策。

上游內文／討論提供機制分析，未自行修補驗證：上游定位 reduction 先把 out 初始化為 identity，覆蓋尚未讀取的 aliased input；是否應明確拒絕 overlap 待上游決策。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/205616)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/205616#issuecomment-7002164585)、[討論 2](https://github.com/pytorch/pytorch/issues/205616#issuecomment-7009161004)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_205616`。本案檢查的是「輸出與 input 都被改為 -inf」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「獨立 out 控制為 3；alias 情境不得靜默產生錯值」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_205616/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/205616) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

上游傾向拒絕 input/output overlap；需區分支援 alias 的正確值與明確拒絕兩種修復契約。

本地只測 amax scalar alias，不把上游其他 reductions 都列為已測 API。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_205616/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_205616/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`5865b532d9d20665d9e65d5282e5e3db433427051eb5ea144235adb5571b1377`
- metadata.json SHA-256：`163b8217e1bd16f21e6ee0cb2fd973e60210e4c5a4509bd1b8564028cb13cb82`
- 核對時 Issue body SHA-256：`9c695cd568cf96f7949c00667c4d1821fa828565a61dd98740e0b35cd9d152f4`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
