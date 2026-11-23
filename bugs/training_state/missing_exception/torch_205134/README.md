# PyTorch Issue #205134

上游標題：Tensor.apply_ / Tensor.map_ do not bump the version counter: backward silently uses the overwritten saved tensor

[GitHub Issue](https://github.com/pytorch/pytorch/issues/205134) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`無`
- Primary Observation：`missing_exception`
- Secondary Observations：`wrong_gradient, incorrect_state`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.apply_` | 主要受測 API |
| `torch.Tensor.detach` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

保存 x 後，對 detach alias 執行 apply_ 乘十。

## 正確行為與實際行為

**Expected Behavior：** 版本應遞增且 backward 報錯；未修改控制梯度另為 [2,4]。

**Actual Behavior：** 版本不變，backward 靜默回傳 [20,40]。

## 錯誤簽名（Bug Signature）

版本不變，backward 靜默回傳 [20,40]。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> detach().apply_(lambda v:v*10) changes values to [10,20] without increasing the version, then backward incorrectly succeeds with [20,40]. The unchanged control [2,4] is not presented as the correct gradient after mutation.

## 分類理由與根因證據

上游確認 apply_ 原地寫入沒有 bump version；[2,4] 不可當作已修改情境的合法答案。

上游內文／討論提供機制分析，未自行修補驗證：上游確認 apply_ 原地寫入沒有 bump version；[2,4] 不可當作已修改情境的合法答案。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/205134)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_205134`。本案檢查的是「版本不變，backward 靜默回傳 [20,40]」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「版本應遞增且 backward 報錯；未修改控制梯度另為 [2,4]」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/missing_exception/torch_205134/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/205134) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

未修改控制的 [2,4] 不能作為修改後的正確梯度；正確契約是版本衝突例外。本例只測 apply_，未測 Issue 的 map_ 變體。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_205134/`
- 新路徑：`bugs/training_state/missing_exception/torch_205134/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`79014fd7a6fd55d63aa9fea8a6b08b2857485537df74e3033a333943f8f9d0a9`
- metadata.json SHA-256：`b596b853ee8c8f20ec5ac0816a1080cf61767f181b63a0aaca9bbbf6f86200f6`
- 核對時 Issue body SHA-256：`04112af5f2647533b2cde58a7e9008a54f147d510d8f13e9be503953d85211da`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
