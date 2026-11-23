# PyTorch Issue #201947

上游標題：asinh/acosh backward silently returns zero for large finite inputs, including float16 x=1000

[GitHub Issue](https://github.com/pytorch/pytorch/issues/201947) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`無`
- Primary Observation：`wrong_gradient`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`autograd`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.asinh` | 主要受測 API |
| `torch.acosh` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

float16 x=1000 的 backward。

## 正確行為與實際行為

**Expected Behavior：** 有限導數約 0.001。

**Actual Behavior：** 導數為零。

## 錯誤簽名（Bug Signature）

導數為零。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> The backward formula squares 1000 in float16, overflows, and returns zero gradient.

## 分類理由與根因證據

上游明確定位 backward 公式先平方 x，half 中間值溢位；歸在 backward 規則，非僅因症狀是梯度。

上游內文／討論提供機制分析，未自行修補驗證：上游明確定位 backward 公式先平方 x，half 中間值溢位；歸在 backward 規則，非僅因症狀是梯度。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/201947)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/201947#issuecomment-6383633763)、[討論 2](https://github.com/pytorch/pytorch/issues/201947#issuecomment-6383700206)、[討論 3](https://github.com/pytorch/pytorch/issues/201947#issuecomment-6649173353)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「導數為零」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「有限導數約 0.001」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/wrong_gradient/torch_201947/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/201947) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

上游列為 #203520 數值穩定性 umbrella 的 duplicate；umbrella 不等於已證明所有 operators 共用同一修補。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_201947/`
- 新路徑：`bugs/training_state/wrong_gradient/torch_201947/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`3cebe7368b81b8fa0b76579d8b52bf28fe729bae95603aa8c8d190b248f29780`
- metadata.json SHA-256：`e324755e0a0898ea3bd169c894a18d8f84f66c4bbeeed778c8697700e9e4b5f0`
- 核對時 Issue body SHA-256：`17997cbceb681f86e32eecfeae5c371f33da80ed821318bf314525722127c7cc`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
