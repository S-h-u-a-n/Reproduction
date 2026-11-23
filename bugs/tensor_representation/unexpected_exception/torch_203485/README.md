# PyTorch Issue #203485

上游標題：F.grouped_mm backward fails on a broadcast gradient: "Invalid strides/sizes, got [0, 0]"

[GitHub Issue](https://github.com/pytorch/pytorch/issues/203485) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`training_state`
- Primary Observation：`unexpected_exception`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_layout`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.nn.functional.grouped_mm` | 主要受測 API |

## 觸發條件

sum().backward() 傳入 stride=[0,0] 的 broadcast gradient。

## 正確行為與實際行為

**Expected Behavior：** 與 dense upstream gradient 得到相同完整梯度。

**Actual Behavior：** Invalid strides/sizes RuntimeError。

## 錯誤簽名（Bug Signature）

Invalid strides/sizes RuntimeError。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Broadcasted upstream gradient raises RuntimeError identifying strides [0,0] and sizes [8,32]; dense-gradient controls are checked completely.

## 分類理由與根因證據

上游確認零 stride gradient 未被 grouped_mm backward 適當 materialize；根因分類依 layout 觸發。

上游內文／討論提供機制分析，未自行修補驗證：上游確認零 stride gradient 未被 grouped_mm backward 適當 materialize；根因分類依 layout 觸發。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/203485)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/203485#issuecomment-6649446165)、[討論 2](https://github.com/pytorch/pytorch/issues/203485#issuecomment-6689151903)、[討論 3](https://github.com/pytorch/pytorch/issues/203485#issuecomment-6778269068)、[討論 4](https://github.com/pytorch/pytorch/issues/203485#issuecomment-6779330245)、[討論 5](https://github.com/pytorch/pytorch/issues/203485#issuecomment-6786438508)、[討論 6](https://github.com/pytorch/pytorch/issues/203485#issuecomment-6799897677)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_203485`。本案檢查的是「Invalid strides/sizes RuntimeError」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「與 dense upstream gradient 得到相同完整梯度」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/unexpected_exception/torch_203485/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/203485) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_203485/`
- 新路徑：`bugs/tensor_representation/unexpected_exception/torch_203485/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`0c0caa930ab9f7cfbe479aff98f96037a0cb31f4ac5047119a6cce1200c2510f`
- metadata.json SHA-256：`ab9b89108d9c2eae8537408e19eb9edebc609703821328402f814a14ef57497b`
- 核對時 Issue body SHA-256：`9dd4e8eaa24a258093cbf8094ac036f109d9d9fd8239f4d4495135e140f0b335`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
