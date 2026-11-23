# PyTorch Issue #205620

上游標題：[CPU and CUDA] `torch.linalg.solve_triangular` silently returns an incorrect solution with `out=A`

[GitHub Issue](https://github.com/pytorch/pytorch/issues/205620) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`storage_aliasing`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.linalg.solve_triangular` | 主要受測 API |

## 觸發條件

A=diag(2,4)、B=diag(6,20)，out=A。

## 正確行為與實際行為

**Expected Behavior：** 合法解為 diag(3,5)，或明確拒絕不支援 alias。

**Actual Behavior：** 回傳 identity。

## 錯誤簽名（Bug Signature）

回傳 identity。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> With out=A, the returned solution is identity rather than diag(3,5).

## 分類理由與根因證據

上游 source inspection 指出先把 B 複製到 out，因 out=A 覆蓋係數矩陣。

上游內文／討論提供機制分析，未自行修補驗證：上游 source inspection 指出先把 B 複製到 out，因 out=A 覆蓋係數矩陣。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/205620)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_205620`。本案檢查的是「回傳 identity」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「合法解為 diag(3,5)，或明確拒絕不支援 alias」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_205620/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/205620) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

out=A 的支援或明確拒絕政策尚待確認；本例只證明現有靜默錯解。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_205620/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_205620/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`74439dc70757ffcdaab9845131ba629573448a6384df5f5a7eb513be90b63f3e`
- metadata.json SHA-256：`5ef26ea0783ec62b3ce829403f7bf8686e9c92a48ba62e62d1dfb0f3fc919079`
- 核對時 Issue body SHA-256：`6fdbc4fa69cab549595508c20fab6642f7f731172211937e20e56fcd00781fc4`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
