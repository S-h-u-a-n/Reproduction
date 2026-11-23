# PyTorch Issue #204945

上游標題：[dynamo] `type(p)` on an `nn.Parameter` created in a compiled function fails with `NameError: name 'SYNTHETIC_LOCAL' is not defined`

[GitHub Issue](https://github.com/pytorch/pytorch/issues/204945) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`unexpected_exception`
- Secondary Observations：`無`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`graph_lifecycle`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.nn.Parameter` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

compiled function 內建立 Parameter 後檢查 type(p)。

## 正確行為與實際行為

**Expected Behavior：** 與 eager 一樣回傳正確分支。

**Actual Behavior：** SYNTHETIC_LOCAL NameError／InternalTorchDynamoError。

## 錯誤簽名（Bug Signature）

SYNTHETIC_LOCAL NameError／InternalTorchDynamoError。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Dynamo guard creation incorrectly raises SYNTHETIC_LOCAL NameError for a newly created nn.Parameter.

## 分類理由與根因證據

上游定位一般 type-source guard 引用了不可 guard 的 SyntheticLocalSource；未顯示訓練狀態毀損，故保留 needs_review。

上游內文／討論提供機制分析，未自行修補驗證：上游定位一般 type-source guard 引用了不可 guard 的 SyntheticLocalSource；未顯示訓練狀態毀損，故保留 needs_review。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/204945)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/204945#issuecomment-6924954420)、[討論 2](https://github.com/pytorch/pytorch/issues/204945#issuecomment-6926945914)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_204945`。本案檢查的是「SYNTHETIC_LOCAL NameError／InternalTorchDynamoError」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「與 eager 一樣回傳正確分支」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/unexpected_exception/torch_204945/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/204945) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

原測試捕捉較寬的外層 Exception，再檢查 SYNTHETIC_LOCAL／NameError 訊息鏈；本次不修改其斷言。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_204945/`
- 新路徑：`bugs/needs_review/unexpected_exception/torch_204945/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`3250365aca94ac55efe839e67cea5b8e147e21363ddcbc1d724152fca514ff5d`
- metadata.json SHA-256：`86a00906ed8530b87dd0c2e5e9ee176176971647c732e7c12e056b7e84058cc3`
- 核對時 Issue body SHA-256：`e10d703841c5d0eda9a51a324b11cb631cefedc1878e523bb35e7857ece3c8c3`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
