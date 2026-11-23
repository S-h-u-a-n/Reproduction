# PyTorch Issue #198064

上游標題：[dynamic shapes] `round(x.shape[0], -1)` is a no-op on SymInt (`SymInt.__round__` ignores a negative `ndigits`): bucketed sizes computed with `round(n, -k)` silently differ from eager

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198064) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`medium`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.SymInt.__round__` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

dynamic shape 長度使用 round(n,-1)。

## 正確行為與實際行為

**Expected Behavior：** 按 Python 的十位取整再計算。

**Actual Behavior：** 忽略負 ndigits，使用原 n。

## 錯誤簽名（Bug Signature）

忽略負 ndigits，使用原 n。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Compiled dynamic-shape program drops negative ndigits and scales by n*5 rather than rounded value.

## 分類理由與根因證據

Issue 指出 symbolic size 的 SymInt.__round__ 表示遺失 ndigits，與具體整數語意不同。

上游內文／討論提供機制分析，未自行修補驗證：Issue 指出 symbolic size 的 SymInt.__round__ 表示遺失 ndigits，與具體整數語意不同。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198064)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198064#issuecomment-6013204551)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「忽略負 ndigits，使用原 n」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「按 Python 的十位取整再計算」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_198064/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198064) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198064/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_198064/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`e16e7a6341ce94ac0c16d58107970a49ba594814c353c4550132ae2e0f60cb2e`
- metadata.json SHA-256：`15edc5a9222c74ed11aa9c052956d3d60873d76f7c0fd48388c08eecc3b974e1`
- 核對時 Issue body SHA-256：`47fcfbcd777493993323b5b29c597873603d38616b2297258c31f53bc550fe54`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
