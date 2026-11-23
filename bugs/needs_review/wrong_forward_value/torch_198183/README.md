# PyTorch Issue #198183

上游標題：[inductor][cpu] Vectorized float32 `torch.erf` loses all relative accuracy near 0 under `torch.compile` (returns 0 for |x| ≤ 1e-7, 1.7e-2 relative error at 1e-5); vector `atanh` returns 0 for |x| below eps

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198183) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.erf` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

AVX512、重複小數值 block 以觸發向量化。

## 正確行為與實際行為

**Expected Behavior：** math.erf 參考的小值仍非零。

**Actual Behavior：** 每個 block 的 1e-8、1e-7 對應結果為零。

## 錯誤簽名（Bug Signature）

每個 block 的 1e-8、1e-7 對應結果為零。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> All eight repeated blocks have zero at both 1e-8 and 1e-7; shape/dtype/finiteness are checked. The other six magnitudes in each block are vectorization padding, not asserted exact wrong values. AVX512 CPU build observation; no universal ISA claim.

## 分類理由與根因證據

erf 多項式 1-p(t)*exp(-x²) 在零附近相消。

上游內文／討論提供機制分析，未自行修補驗證：erf 多項式 1-p(t)*exp(-x²) 在零附近相消。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198183)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_198183`。本案檢查的是「每個 block 的 1e-8、1e-7 對應結果為零」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「math.erf 參考的小值仍非零」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_198183/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198183) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只斷言各 block 的兩個小值為零；其他值作向量化 padding，沒有宣稱整個數值區間都已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198183/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_198183/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`9d8d022d70ae8fd01bc623cbfd910a7996c8030b6707e2c9afcde8521e3de676`
- metadata.json SHA-256：`8ad3164f9f3058b9e9bc56059e59e8c13d3b02f86eebcdbe487d722535fe0536`
- 核對時 Issue body SHA-256：`ba9c6c7077e65aca8e8f39ab6a9d506de1a7db5e0d475de59f121cecd0731e54`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
