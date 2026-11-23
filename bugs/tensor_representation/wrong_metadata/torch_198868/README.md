# PyTorch Issue #198868

上游標題：[Inductor] scatter with an empty index changes a scalar tensor into a length-one tensor

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198868) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_metadata`
- Secondary Observations：`無`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.scatter` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

scalar input 與 empty index。

## 正確行為與實際行為

**Expected Behavior：** 保留 shape=()。

**Actual Behavior：** shape 變成 (1,)。

## 錯誤簽名（Bug Signature）

shape 變成 (1,)。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Inductor changes a scalar tensor output into a one-element tensor with shape (1,).

## 分類理由與根因證據

scalar／空 index 的 tensor rank 表示不一致；上游未確認完整內部根因。

Root cause not confirmed。scalar／空 index 的 tensor rank 表示不一致；上游未確認完整內部根因。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198868)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198868#issuecomment-6985923304)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「shape 變成 (1,)」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「保留 shape=()」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_metadata/torch_198868/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198868) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

根因證據尚不足；分類依已知必要觸發條件。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198868/`
- 新路徑：`bugs/tensor_representation/wrong_metadata/torch_198868/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`56ac03b2592d9a0304bc8f371f9c24b3192e6368346e108b9de0c44d651d5428`
- metadata.json SHA-256：`8cd437a068d5bb5f555ceed7d485e37e9579b3a9cb15099b5c90358502feb7d1`
- 核對時 Issue body SHA-256：`566ef99c840012f922d63f037e9e6b57c681e96c8138b4a5c535ec6439a39866`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
