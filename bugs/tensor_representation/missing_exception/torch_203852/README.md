# PyTorch Issue #203852

上游標題：index_add on an integer tensor truncates a float alpha instead of raising (alpha=2.5 adds 2 * source)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/203852) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`missing_exception`
- Secondary Observations：`wrong_forward_value`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.index_add` | 主要受測 API |

## 觸發條件

整數 tensor 配 floating alpha=2.5 或 0.5。

## 正確行為與實際行為

**Expected Behavior：** 依 add／decomposition 控制組拒絕不安全 scalar cast。

**Actual Behavior：** alpha 靜默截為 2 或 0。

## 錯誤簽名（Bug Signature）

alpha 靜默截為 2 或 0。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> index_add(alpha=2.5) truncates alpha to 2 silently; alpha=0.5 becomes zero.

## 分類理由與根因證據

上游提議補 alpha_check，主要是 scalar-to-tensor dtype 相容契約；是否連 2.0 也拒絕仍是上游政策。

上游內文／討論提供機制分析，未自行修補驗證：上游提議補 alpha_check，主要是 scalar-to-tensor dtype 相容契約；是否連 2.0 也拒絕仍是上游政策。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/203852)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/203852#issuecomment-6699708577)、[討論 2](https://github.com/pytorch/pytorch/issues/203852#issuecomment-6935392827)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「alpha 靜默截為 2 或 0」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「依 add／decomposition 控制組拒絕不安全 scalar cast」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/missing_exception/torch_203852/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/203852) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

對整數 tensor 的 integral float alpha 是否也拒絕，仍是上游相容性政策；本例只測非整數值。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_203852/`
- 新路徑：`bugs/tensor_representation/missing_exception/torch_203852/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`467389689cf49e095338b1738fd53b193564f7cbefec027a781393eb3118150d`
- metadata.json SHA-256：`93c1dddb9a05b4897a4589e9e5bb338bba9a38d0b813a4274368d4de85ac73de`
- 核對時 Issue body SHA-256：`7c0f7c865c5833b4d2f2feac25efa5a0f17e760b1e54bd294c924ff034459e5a`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
