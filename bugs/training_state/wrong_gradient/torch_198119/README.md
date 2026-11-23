# PyTorch Issue #198119

上游標題：[inductor] `avg_pool1d/2d` backward with `ceil_mode=True` divides the overhanging last window by the full kernel size, so the compiled gradient is wrong where eager and `aot_eager` agree; forward is correct

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198119) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`無`
- Primary Observation：`wrong_gradient`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.nn.functional.avg_pool1d` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

ceil_mode=True，最後 pooling window 只有兩個有效元素。

## 正確行為與實際行為

**Expected Behavior：** 完整梯度 [1/3,1/3,2/3,1/3,5/6,1/2]。

**Actual Behavior：** 完整梯度 [1/3,1/3,2/3,1/3,2/3,1/3]。

## 錯誤簽名（Bug Signature）

完整梯度 [1/3,1/3,2/3,1/3,2/3,1/3]。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Complete compiled gradient is [1/3,1/3,2/3,1/3,2/3,1/3], using the full window divisor in the final window.

## 分類理由與根因證據

上游明確定位 avg_pool backward lowering 的 divisor，forward 正常；以 backward 規則錯誤分類。

上游內文／討論提供機制分析，未自行修補驗證：上游明確定位 avg_pool backward lowering 的 divisor，forward 正常；以 backward 規則錯誤分類。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198119)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198119#issuecomment-6511361696)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_198119`。本案檢查的是「完整梯度 [1/3,1/3,2/3,1/3,2/3,1/3]」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「完整梯度 [1/3,1/3,2/3,1/3,5/6,1/2]」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/wrong_gradient/torch_198119/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198119) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198119/`
- 新路徑：`bugs/training_state/wrong_gradient/torch_198119/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`86a230a09b8bfc6a58e48933d4da6857fc7ce0a320c3a1ad279d2f7e192fee8c`
- metadata.json SHA-256：`da3e6fc2cb6b7d6998b4131a1ae9b344a26d9928c576b39f3091d1ebacceb966`
- 核對時 Issue body SHA-256：`0fef930b2320f6d0d5022f469d5a58a87495a448fe284e62703e1db2f4feb3f1`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
