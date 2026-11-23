# PyTorch Issue #202862

上游標題：[dynamo] In-place view op called via torch.ops.aten (OpOverload) on a graph input crashes guard creation with IndexError

[GitHub Issue](https://github.com/pytorch/pytorch/issues/202862) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`unexpected_exception`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.ops.aten.unsqueeze_.default` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

直接對 graph input 呼叫 OpOverload 的 inplace rank-changing view。

## 正確行為與實際行為

**Expected Behavior：** 成功 trace 或適當 graph break。

**Actual Behavior：** guard creation 拋 IndexError。

## 錯誤簽名（Bug Signature）

guard creation 拋 IndexError。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> OpOverload in-place view of input triggers guard creation IndexError.

## 分類理由與根因證據

tensor rank metadata 改變與 guard 建立不一致；上游也明確指出是 Python exception 而非 process crash。

上游內文／討論提供機制分析，未自行修補驗證：tensor rank metadata 改變與 guard 建立不一致；上游也明確指出是 Python exception 而非 process crash。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/202862)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/202862#issuecomment-6581993228)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「guard creation 拋 IndexError」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「成功 trace 或適當 graph break」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/unexpected_exception/torch_202862/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/202862) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_202862/`
- 新路徑：`bugs/tensor_representation/unexpected_exception/torch_202862/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`5fe787592d3051f53bf780ec54f9ee6b008ab1b370da90dbec357c0b1f5d9304`
- metadata.json SHA-256：`5ce6d015a85ae1dee3a38fc31d2f9126d5a841f98e723be49f7acc19fb7f0d3f`
- 核對時 Issue body SHA-256：`277a2d198d743b67293f5260a3cda82a1cc739a75257bd32e67a66daddeada10`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
