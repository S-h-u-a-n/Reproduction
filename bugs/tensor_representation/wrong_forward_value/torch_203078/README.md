# PyTorch Issue #203078

上游標題：`scatter_add` / `scatter_reduce` on CPU write to the wrong rows when the index is expanded and self has more columns than the index

[GitHub Issue](https://github.com/pytorch/pytorch/issues/203078) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_layout`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.scatter_add` | 主要受測 API |
| `torch.Tensor.scatter_reduce` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

expanded index stride=(1,0)，self 比 index 更寬。

## 正確行為與實際行為

**Expected Behavior：** 完整結果寫入 row 0、2，row sums=[16,0,16]。

**Actual Behavior：** 寫入 row 0、1，row sums=[16,16,0]。

## 錯誤簽名（Bug Signature）

寫入 row 0、1，row sums=[16,16,0]。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Expanded-index stride (1,0) makes scatter_add and scatter_reduce(sum) write sixteen ones into rows 0 and 1 instead of rows 0 and 2. Full tensors, not only row sums, are checked; contiguous-index controls match the correct reference.

## 分類理由與根因證據

上游定位 expanded-index fast path 把 index width 當成 destination row stride。

上游內文／討論提供機制分析，未自行修補驗證：上游定位 expanded-index fast path 把 index width 當成 destination row stride。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/203078)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/203078#issuecomment-6636347031)、[討論 2](https://github.com/pytorch/pytorch/issues/203078#issuecomment-6729893149)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_203078`。本案檢查的是「寫入 row 0、1，row sums=[16,16,0]」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「完整結果寫入 row 0、2，row sums=[16,0,16]」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_203078/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/203078) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_203078/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_203078/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`c9afff72738df5b46ab4918de38b70b6dc2566a0c1ffcbda6f80093500df2e5f`
- metadata.json SHA-256：`8219a192ac41f60be3180e6fc1d6ab2d00aa45b1650891c4586cdf686d123962`
- 核對時 Issue body SHA-256：`1fceeb6eb7e8e8e1bc7c64f17425bb9c2082ec5ead7319c5034e0c49e3494430`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
