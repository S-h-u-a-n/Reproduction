# PyTorch Issue #198052

上游標題：[dynamo][numpy] NumPy code under `torch.compile` returns wrong values: `np.fix` rounds instead of truncating, `np.cbrt` is NaN for negatives, `np.clip` with out-of-range Python bounds wraps, `np.sign` / `np.heaviside` drop NaN

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198052) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `numpy.fix` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

torch.compile 處理正負半整數 float32 NumPy 輸入。

## 正確行為與實際行為

**Expected Behavior：** 向零截斷得到 [1,-1,2,-0]。

**Actual Behavior：** 得到 [2,-2,2,-0]。

## 錯誤簽名（Bug Signature）

得到 [2,-2,2,-0]。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Compiled float32 np.fix returns [2,-2,2,-0] rather than [1,-1,2,-0]; shape, dtype and the negative-zero sign are checked.

## 分類理由與根因證據

torch._numpy 把 fix 對應到 round；不把同 Issue 其他 NumPy 症狀當成本地已測。

上游內文／討論提供機制分析，未自行修補驗證：torch._numpy 把 fix 對應到 round；不把同 Issue 其他 NumPy 症狀當成本地已測。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198052)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198052#issuecomment-6143826086)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「得到 [2,-2,2,-0]」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「向零截斷得到 [1,-1,2,-0]」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_198052/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198052) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

Issue 同時包含 fix/cbrt/clip/sign/heaviside；本地只測 numpy.fix，不將整篇 Issue 視為五個已驗證案例。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198052/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_198052/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`261f51e036fa1ae192ad4f02ce160153cc75e91e0da81b97a6b93f0cb00449d7`
- metadata.json SHA-256：`de80b8c499324b8a4d8166df862dbf6beeeb24bc86b5b8ea8259d76cb0769771`
- 核對時 Issue body SHA-256：`421f09915fed1f4ffaeaa6a71a5fc7d389ab71b3ca8613bbf17b6f0c90f402d1`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
