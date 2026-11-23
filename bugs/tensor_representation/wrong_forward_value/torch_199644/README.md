# PyTorch Issue #199644

上游標題：CPU Inductor rounds unbacked floats from .item() to float32 in C++ kernels

[GitHub Issue](https://github.com/pytorch/pytorch/issues/199644) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.item` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

擷取 float64 scalar 16777219 再傳入 CPU 編譯 kernel。

## 正確行為與實際行為

**Expected Behavior：** float64 與 int64 結果皆保持 16777219。

**Actual Behavior：** 兩者皆變成 16777220。

## 錯誤簽名（Bug Signature）

兩者皆變成 16777220。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Captured scalar 16777219 becomes 16777220 in both float64 and int64 outputs; capture_scalar_outputs is scoped and restored after the testcase.

## 分類理由與根因證據

上游定位 C++ kernel scalar 參數宣告為 const float，縮窄原本的 float64 表示。

上游內文／討論提供機制分析，未自行修補驗證：上游定位 C++ kernel scalar 參數宣告為 const float，縮窄原本的 float64 表示。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/199644)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「兩者皆變成 16777220」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「float64 與 int64 結果皆保持 16777219」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_199644/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/199644) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_199644/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_199644/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`d11f8f15e23149c0bb5d50ab3913f0f9c6eebf2e34dd9b3f47eb75b92bcc2f05`
- metadata.json SHA-256：`ddd2de02fe1726b604f1423fd12fddabd2772077b3053a4511ecdbf46eacae2b`
- 核對時 Issue body SHA-256：`ea16d8717dc34dc6ebb84761f2fa29b358407fdd609105a5a333d29fb26d0b8f`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
