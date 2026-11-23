# PyTorch Issue #204188

上游標題：DCP save-plan cache accepts dtype changes and persists stale dtype metadata (enable_plan_caching=True)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/204188) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`tensor_representation`
- Primary Observation：`wrong_metadata`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`graph_lifecycle`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.distributed.checkpoint.save` | 主要受測 API |
| `torch.distributed.checkpoint.DefaultSavePlanner` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

enable_plan_caching=True，兩次 save 只有 dtype 由 bf16 變 fp16。

## 正確行為與實際行為

**Expected Behavior：** 第二份 checkpoint metadata 應記錄 fp16。

**Actual Behavior：** 仍記錄 bf16，無 cache 控制組正確。

## 錯誤簽名（Bug Signature）

仍記錄 bf16，無 cache 控制組正確。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> DCP cached save plan reports stale dtype for a second state_dict with changed tensor dtype.

## 分類理由與根因證據

上游定位 class-level save plan cache 比較沒有 tensor_data.properties，屬 checkpoint state lifecycle。

上游內文／討論提供機制分析，未自行修補驗證：上游定位 class-level save plan cache 比較沒有 tensor_data.properties，屬 checkpoint state lifecycle。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/204188)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/204188#issuecomment-6760966948)、[討論 2](https://github.com/pytorch/pytorch/issues/204188#issuecomment-6761070737)、[討論 3](https://github.com/pytorch/pytorch/issues/204188#issuecomment-6794507738)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_204188`。本案檢查的是「仍記錄 bf16，無 cache 控制組正確」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「第二份 checkpoint metadata 應記錄 fp16」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/wrong_metadata/torch_204188/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/204188) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

兩次保存與 planner class cache 的順序是觸發條件；完整批次驗證仍保留測試原有清理邏輯。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_204188/`
- 新路徑：`bugs/training_state/wrong_metadata/torch_204188/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`456fbd72d8fab06172e9cd97cebd27ffc950a7a204be0f4b10679747767e8196`
- metadata.json SHA-256：`02d058ba0d665e2dc4a009a36e3dc533af9759e3fe2855d74350a62c4731f73b`
- 核對時 Issue body SHA-256：`a7910491b97719bde94039faf295fd546bf5111154219b15a0527499f8eeb457`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
