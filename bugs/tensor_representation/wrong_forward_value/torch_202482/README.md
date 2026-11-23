# PyTorch Issue #202482

上游標題：[inductor] Wrong result: mm/linear output written directly into torch.cat buffer is clobbered by a later index_put on the cat result

[GitHub Issue](https://github.com/pytorch/pytorch/issues/202482) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`storage_aliasing`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.cat` | 主要受測 API |
| `torch.nn.functional.linear` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.Tensor.index_put_` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear。

## 正確行為與實際行為

**Expected Behavior：** 讀取原始 Linear 結果，完整 tensor 符合獨立參考。

**Actual Behavior：** 符合讀到已被覆寫 cat storage 的完整錯誤模式。

## 錯誤簽名（Bug Signature）

符合讀到已被覆寫 cat storage 的完整錯誤模式。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> The complete wrong output matches reading the Linear view after overwriting cat storage; only rows 1,5,7 differ. Preserve the fixed index order. rtol=1e-5, atol=1e-6 allows length-five float32 dot-product rounding.

## 分類理由與根因證據

Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。

上游內文／討論提供機制分析，未自行修補驗證：Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/202482)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「符合讀到已被覆寫 cat storage 的完整錯誤模式」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「讀取原始 Linear 結果，完整 tensor 符合獨立參考」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_202482/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/202482) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_202482/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_202482/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`15b9bd23d18ca994dfad6eb6eb4a155adb96b3474f28678fa756cb3a2ccf25cf`
- metadata.json SHA-256：`d32a634f44d926c89fd739b4fd9a0d8d9e6ba8832cb9e30671b0b597402b02a7`
- 核對時 Issue body SHA-256：`2c823f698adadc10e9cf73f034a57d7fbc228b6f47c6ea25a815170421b1190e`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
