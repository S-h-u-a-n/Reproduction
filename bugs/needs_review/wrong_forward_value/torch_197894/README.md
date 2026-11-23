# PyTorch Issue #197894

上游標題：[fx] Generated code for `operator.pow(-2, x)` is `-2 ** x`, which Python evaluates as `-(2 ** x)`: `GraphModule.forward` returns the wrong sign (`Interpreter` is correct); reachable from `torch.compile(dynamic=True)` via `(-1) ** x.shape[0]`

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197894) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.fx.GraphModule` | 主要受測 API |

## 觸發條件

FX graph 的 operator.pow(-2,x)，x=2。

## 正確行為與實際行為

**Expected Behavior：** 回傳 4。

**Actual Behavior：** 回傳 -4。

## 錯誤簽名（Bug Signature）

回傳 -4。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> FX GraphModule emits -2 ** x without parentheses and evaluates exponent 2 to -4.

## 分類理由與根因證據

FX Python codegen 缺少負數底數括號，屬運算優先序問題。

上游內文／討論提供機制分析，未自行修補驗證：FX Python codegen 缺少負數底數括號，屬運算優先序問題。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197894)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/197894#issuecomment-5764646986)、[討論 2](https://github.com/pytorch/pytorch/issues/197894#issuecomment-6983314738)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_197894`。本案檢查的是「回傳 -4」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「回傳 4」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_197894/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197894) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197894/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_197894/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`ecc1b4a741478c10cb98f651ed5aa90112c0072497c7e6ca4e10c16cae47ce16`
- metadata.json SHA-256：`0fc4d0864acf83c5686e57ef0f89481cbb13a9e0168e85d9ff365e4ea3a8a56f`
- 核對時 Issue body SHA-256：`3836995e2485aed7a7ea913f361e4305f3983eefd5f7428a990386abeaa5d7e0`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
