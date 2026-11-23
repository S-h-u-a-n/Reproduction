# PyTorch Issue #200229

上游標題：`[Inductor][CPU] torch.var returns NaN for large-magnitude constant float64 inputs while eager returns 0`

[GitHub Issue](https://github.com/pytorch/pytorch/issues/200229) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.var` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

兩個相同 float64 1e200 的 CPU compiled variance。

## 正確行為與實際行為

**Expected Behavior：** 常數 variance 為零。

**Actual Behavior：** 回傳 NaN。

## 錯誤簽名（Bug Signature）

回傳 NaN。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Inductor gives NaN for constant [1e200,1e200], eager returns zero.

## 分類理由與根因證據

後續討論更正：實際有 Welford，masked tail 的零權重 lane 在 delta² 溢位後產生 inf*0；不是直接認定未使用 Welford。

上游內文／討論提供機制分析，未自行修補驗證：後續討論更正：實際有 Welford，masked tail 的零權重 lane 在 delta² 溢位後產生 inf*0；不是直接認定未使用 Welford。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/200229)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/200229#issuecomment-6051661811)、[討論 2](https://github.com/pytorch/pytorch/issues/200229#issuecomment-6051901145)、[討論 3](https://github.com/pytorch/pytorch/issues/200229#issuecomment-6052282158)、[討論 4](https://github.com/pytorch/pytorch/issues/200229#issuecomment-6069500408)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_200229`。本案檢查的是「回傳 NaN」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「常數 variance 為零」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_200229/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/200229) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

後續討論更正原始推測為 masked Welford tail；較大不同長度的 eager 也可能不穩，不能泛化本例控制。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_200229/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_200229/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`98c2e8bc052994d948011f8383bd3921a8803f1019b9d86b87305ec07a409ba0`
- metadata.json SHA-256：`637d0bd7590875ca66568a0dc805c435583ca54da55d414026d139dbe3590342`
- 核對時 Issue body SHA-256：`bf78ea3e17954d09168ed658d5a25aecf6d5ab161320304fe32e4b5685876203`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
