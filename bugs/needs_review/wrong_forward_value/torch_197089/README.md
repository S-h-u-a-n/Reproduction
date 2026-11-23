# PyTorch Issue #197089

上游標題：[inductor][cpu] `torch.std`/`var` accumulate in float32: inf/NaN for 1e30-scale inputs, and **zero output with an all-zero gradient** for 1e-30-scale inputs (eager and float64 are correct)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197089) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`wrong_gradient`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`autograd`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.std` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

固定極小 float32 輸入、Inductor reduction。

## 正確行為與實際行為

**Expected Behavior：** float64 參考給出非零 std 與完整有限梯度。

**Actual Behavior：** std 與梯度均變為零。

## 錯誤簽名（Bug Signature）

std 與梯度均變為零。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Inductor float32 accumulation underflows to zero, giving zero std and zero gradient.

## 分類理由與根因證據

上游指出 float32 accumulation 的下溢；主要為數值穩定性，梯度是次要症狀。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 float32 accumulation 的下溢；主要為數值穩定性，梯度是次要症狀。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197089)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/197089#issuecomment-5946359718)、[討論 2](https://github.com/pytorch/pytorch/issues/197089#issuecomment-6101213904)、[討論 3](https://github.com/pytorch/pytorch/issues/197089#issuecomment-6104262251)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「std 與梯度均變為零」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「float64 參考給出非零 std 與完整有限梯度」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_197089/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197089) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197089/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_197089/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`ff03acdbcd9485a2bdfa7b6fe780bb65d4aaf42009d07027d8a1525d4a5b36be`
- metadata.json SHA-256：`eeb900079064bebc0d19b92239742bbfddda38d0f0c28a0b313dfd00bacd0480`
- 核對時 Issue body SHA-256：`3e4d7fc17403220f8dcbd1802d5cd6ecd7ca5eb13196816e14167009b3e49657`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
