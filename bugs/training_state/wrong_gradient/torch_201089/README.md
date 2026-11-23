# PyTorch Issue #201089

上游標題：torch.compile: silently wrong gradients when the forward mutates a buffer

[GitHub Issue](https://github.com/pytorch/pytorch/issues/201089) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`無`
- Primary Observation：`wrong_gradient`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`graph_lifecycle`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.compile` | 主要受測 API |

## 觸發條件

forward 原地增加 counter buffer，再以其算出的 scale 作用在 Linear。

## 正確行為與實際行為

**Expected Behavior：** forward 與 counter 正確，weight gradient 為 0.2。

**Actual Behavior：** forward 正確但 weight gradient 為 0.3。

## 錯誤簽名（Bug Signature）

forward 正確但 weight gradient 為 0.3。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Compiled backward recomputes scale from already-mutated forward buffer, inflating parameter gradients.

## 分類理由與根因證據

上游指出 min-cut 保存已會被 copy_ 改寫的 buffer，backward 重新計算時讀到新值。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 min-cut 保存已會被 copy_ 改寫的 buffer，backward 重新計算時讀到新值。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/201089)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/201089#issuecomment-6704665439)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_201089`。本案檢查的是「forward 正確但 weight gradient 為 0.3」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「forward 與 counter 正確，weight gradient 為 0.2」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/wrong_gradient/torch_201089/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/201089) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_201089/`
- 新路徑：`bugs/training_state/wrong_gradient/torch_201089/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`c47bcea430aaba2e4f17b01fbbf65b5318ba296ae1fd8fed0b218144bafc1169`
- metadata.json SHA-256：`90ef8ade94b98048b0edcd182f07e2107de360f64467bbcec5c261a0ca8caaac`
- 核對時 Issue body SHA-256：`033e90b922f8fe1408407522f46b68c67c55da881e3bdda72efb192beb2b795b`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
