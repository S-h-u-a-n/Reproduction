# PyTorch Issue #198155

上游標題：[inductor] 134 operators run under `torch.compile` on dtypes their eager kernels reject with `NotImplementedError` (bool conv, int softmax/losses, float bitwise ops, half special functions, complex norms): full list

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198155) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`missing_exception`
- Secondary Observations：`無`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.softmax` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

int64 輸入的 softmax 經 Inductor。

## 正確行為與實際行為

**Expected Behavior：** 和 eager 一樣拒絕不支援的 dtype。

**Actual Behavior：** 回傳整數 tensor 而不報錯。

## 錯誤簽名（Bug Signature）

回傳整數 tensor 而不報錯。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Compiled softmax(int64) silently returns an integer tensor instead of raising.

## 分類理由與根因證據

operator dtype 支援契約在 lowering 被放寬；僅收錄原 Issue 眾多組合中的 int64 softmax。

上游內文／討論提供機制分析，未自行修補驗證：operator dtype 支援契約在 lowering 被放寬；僅收錄原 Issue 眾多組合中的 int64 softmax。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198155)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198155#issuecomment-5773214257)、[討論 2](https://github.com/pytorch/pytorch/issues/198155#issuecomment-5777996235)、[討論 3](https://github.com/pytorch/pytorch/issues/198155#issuecomment-5789079879)、[討論 4](https://github.com/pytorch/pytorch/issues/198155#issuecomment-5789205432)、[討論 5](https://github.com/pytorch/pytorch/issues/198155#issuecomment-6945969045)、[討論 6](https://github.com/pytorch/pytorch/issues/198155#issuecomment-7009443652)、[討論 7](https://github.com/pytorch/pytorch/issues/198155#issuecomment-7010819184)、[討論 8](https://github.com/pytorch/pytorch/issues/198155#issuecomment-7039710648)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「回傳整數 tensor 而不報錯」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「和 eager 一樣拒絕不支援的 dtype」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/missing_exception/torch_198155/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198155) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

compiled 對不支援 eager dtype 的擴充，是否一律視為漏例外，需確認收錄政策。

Issue 的 134 operators／418 pairs 不屬本地驗證範圍；本地僅 int64 softmax。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198155/`
- 新路徑：`bugs/tensor_representation/missing_exception/torch_198155/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`cc7f7a7d9930c97675f9e4152f7bb1dfd6e1690c9da3f375bc00a8ced180e05c`
- metadata.json SHA-256：`b3fc33bfbfd8e28f018771a22a14dd7b3740478a2dea6e6446e338761b9cbc89`
- 核對時 Issue body SHA-256：`82a2be13df446e6c8b807eb35854a9241db26a7551fcba2fe6b575193bed83c3`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
