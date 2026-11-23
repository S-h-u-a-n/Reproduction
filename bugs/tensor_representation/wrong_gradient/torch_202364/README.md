# PyTorch Issue #202364

上游標題：[AOTAutograd] Incorrect gradients after in-place as_strided_ on a non-overlapping view

[GitHub Issue](https://github.com/pytorch/pytorch/issues/202364) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`training_state`
- Primary Observation：`wrong_gradient`
- Secondary Observations：`無`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`autograd`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.as_strided_` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

view 的 shape/stride 原地變更後 mul_，再 compiled backward。

## 正確行為與實際行為

**Expected Behavior：** forward=[2,12,18,8]、gradient=[2,6,6,2]。

**Actual Behavior：** forward 正確、gradient=[2,6,6,6]。

## 錯誤簽名（Bug Signature）

forward 正確、gradient=[2,6,6,6]。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Inductor backward assigns gradient to an element outside the as_strided_ modified view.

## 分類理由與根因證據

原文確認 view metadata mutation 是觸發條件；未確認錯誤 backward 的完整內部根因。

Root cause not confirmed。原文確認 view metadata mutation 是觸發條件；未確認錯誤 backward 的完整內部根因。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/202364)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_202364`。本案檢查的是「forward 正確、gradient=[2,6,6,6]」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「forward=[2,12,18,8]、gradient=[2,6,6,2]」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_gradient/torch_202364/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/202364) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

根因證據尚不足；分類依已知必要觸發條件。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_202364/`
- 新路徑：`bugs/tensor_representation/wrong_gradient/torch_202364/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`f827b4cd2f76e44037c44380c7da52e79e951d00ff6773772fd0721abc94be1e`
- metadata.json SHA-256：`5305eb7fdabf2cbef805427193416b98ecef57a7b144a626dc5acf6a3b352af4`
- 核對時 Issue body SHA-256：`738a05abb6705f7feac535e5bcd2c20654bc41e61c0bf79c309a44ac187150d8`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
