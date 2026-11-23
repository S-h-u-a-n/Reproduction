# PyTorch Issue #198071

上游標題：[inductor] `torch.clamp` with a Python bound outside the dtype's range wraps the bound: `clamp(int8_tensor, -1000, 1000)` returns `-24` for every element

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198071) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.clamp` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

int8 輸入與超出範圍的 Python max=300。

## 正確行為與實際行為

**Expected Behavior：** 本 build eager 保留 [-128,-3,0,5,127]。

**Actual Behavior：** bound 轉成 int8 的 44，127 被截到 44。

## 錯誤簽名（Bug Signature）

bound 轉成 int8 的 44，127 被截到 44。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Inductor wraps the upper bound to 44 and clamps valid 127 down to 44.

## 分類理由與根因證據

上游指出 scalar bound 過早縮窄到 tensor dtype。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 scalar bound 過早縮窄到 tensor dtype。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198071)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198071#issuecomment-5770296071)、[討論 2](https://github.com/pytorch/pytorch/issues/198071#issuecomment-6255356342)、[討論 3](https://github.com/pytorch/pytorch/issues/198071#issuecomment-6454126370)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「bound 轉成 int8 的 44，127 被截到 44」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「本 build eager 保留 [-128,-3,0,5,127]」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_198071/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198071) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198071/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_198071/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`782d1e88090c46c41bc1193ecf938ac4f9b19b8b2dee2029e347fb4c28de0569`
- metadata.json SHA-256：`133c40b119db76ef5fe1d2cc53fcbb027f34336211b19e2489d9a95aeed52a6a`
- 核對時 Issue body SHA-256：`4407dd8a580ef2da7f4443990ab238da868ca3b74f7131c2da1224fe82ad2b7c`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
