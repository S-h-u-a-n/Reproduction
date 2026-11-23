# PyTorch Issue #202526

上游標題：torch.jit.freeze gives wrong results when a Linear output feeding BatchNorm is also used elsewhere

[GitHub Issue](https://github.com/pytorch/pytorch/issues/202526) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.jit.freeze` | 主要受測 API |
| `torch.nn.Linear` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.nn.BatchNorm1d` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

eval 模式，Linear 結果同時供 BatchNorm 與 residual。

## 正確行為與實際行為

**Expected Behavior：** 結果為 BN(h)+h。

**Actual Behavior：** 凍結後符合 2*BN(h)。

## 錯誤簽名（Bug Signature）

凍結後符合 2*BN(h)。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Frozen output matches 2*BN(h) over the full tensor. rtol=1e-5, atol=2e-5 covers float32 length-64 products and fusion reordering, while retaining the separate residual-control check.

## 分類理由與根因證據

上游指出 Linear-BatchNorm folding 未檢查多 consumer；本測試是推論圖改寫，不是訓練 buffer mutation。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 Linear-BatchNorm folding 未檢查多 consumer；本測試是推論圖改寫，不是訓練 buffer mutation。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/202526)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「凍結後符合 2*BN(h)」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「結果為 BN(h)+h」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_202526/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/202526) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

本例 eval/freeze 的 graph folding 錯誤，並非 BatchNorm running buffer 的訓練更新錯誤。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_202526/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_202526/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`cbb66fa44862d89e0403096bb75753204f2a035612764b9e75957511e916531d`
- metadata.json SHA-256：`3781d147205f22894c3d9b008256a4c7f81b67236ec14a228ef38ef417e4690f`
- 核對時 Issue body SHA-256：`a826dde237a57c56870cece453e34bd66489e0229a51385aaf8d2ff9605d63ed`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
