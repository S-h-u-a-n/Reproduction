# PyTorch Issue #199350

上游標題：[inductor] torch.view_as_complex_copy fails with "Tensor must have a last dimension with stride 1" (fallback lacks the require_contiguous handling view_as_complex got in #100428)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/199350) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`unexpected_exception`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_layout`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.view_as_complex_copy` | 主要受測 API |
| `torch.nn.functional.adaptive_max_pool2d` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

pooling 後接 view_as_complex_copy，Inductor 選擇 layout。

## 正確行為與實際行為

**Expected Behavior：** 維持所需最後維 stride=1，結果等於 eager。

**Actual Behavior：** fallback 拋 last dimension stride 1 RuntimeError。

## 錯誤簽名（Bug Signature）

fallback 拋 last dimension stride 1 RuntimeError。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> InductorError wraps a last-dimension stride-1 RuntimeError; traceback frame operator identity must be aten.view_as_complex_copy.default. The independent eager result is a full complex64 zero tensor of shape (4,4,2). Traceback function/operator matching is specific to this build, without path/line/generated-name pinning.

## 分類理由與根因證據

上游指出 view_as_complex_copy 缺少 require_contiguous fallback 約束。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 view_as_complex_copy 缺少 require_contiguous fallback 約束。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/199350)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/199350#issuecomment-5946317971)、[討論 2](https://github.com/pytorch/pytorch/issues/199350#issuecomment-6719596550)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_199350`。本案檢查的是「fallback 拋 last dimension stride 1 RuntimeError」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「維持所需最後維 stride=1，結果等於 eager」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/unexpected_exception/torch_199350/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/199350) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

例外除了字串亦檢查 traceback 的 operator identity；此內部結構可能隨 build 變動。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_199350/`
- 新路徑：`bugs/tensor_representation/unexpected_exception/torch_199350/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`4682cb2038dcbd74cf8e6ab03a4111342fb408f4e53d9259764e626863d92a84`
- metadata.json SHA-256：`34364b9734134ff92016c4f91e5e6e3e105e517f433f6a9ea422b863a4571187`
- 核對時 Issue body SHA-256：`edf03359cd6cef8b6c686fa8d79e3b7eed5101425120bf666a1d584444bdc91c`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
