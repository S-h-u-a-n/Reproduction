# PyTorch Issue #205654

上游標題：[CPU][Autograd] float64 log_ndtr backward returns 1.55e55 instead of 2**30 in the negative tail

[GitHub Issue](https://github.com/pytorch/pytorch/issues/205654) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`無`
- Primary Observation：`wrong_gradient`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`autograd`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.special.log_ndtr` | 主要受測 API |

## 觸發條件

float64 負尾 x=-2**30、-2**35。

## 正確行為與實際行為

**Expected Behavior：** Mills bounds 在這些點皆捨入為 u=-x。

**Actual Behavior：** 前者為極大錯值，後者為正無限。

## 錯誤簽名（Bug Signature）

前者為極大錯值，後者為正無限。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Forward remains finite; at -2**30 the wrong gradient matches cancellation in exp(-u*u/2-log_ndtr(-u))/sqrt(2*pi), while -2**35 gives positive infinity. This checks the error mechanism at rtol=1e-12, not a copied machine-specific 1.55e55 constant.

## 分類理由與根因證據

上游指出 backward 的指數式含兩個大負數相減，消去導致導數錯誤；以解析界限判定。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 backward 的指數式含兩個大負數相減，消去導致導數錯誤；以解析界限判定。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/205654)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_205654`。本案檢查的是「前者為極大錯值，後者為正無限」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「Mills bounds 在這些點皆捨入為 u=-x」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/wrong_gradient/torch_205654/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/205654) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_205654/`
- 新路徑：`bugs/training_state/wrong_gradient/torch_205654/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`c165bd8701b93eaf292c0ccb7ec07bd6d0d5b1ff15072c8580fd07a65c5aa742`
- metadata.json SHA-256：`741cca197ee001e8fb88e3784e21c59058caae8300aaf74c2b044e2fe576cabd`
- 核對時 Issue body SHA-256：`b938025cd8408855e411a1461421fdf06f6a6e9e56b108dae6f574c678cf4cce`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
