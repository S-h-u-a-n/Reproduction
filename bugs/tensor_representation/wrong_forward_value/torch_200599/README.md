# PyTorch Issue #200599

上游標題：CPU `torch.linalg.lu_solve` reads the wrong LU matrices when a size-1 batch dimension has a non-canonical stride (wrong results under nested `vmap` and `vmap(jacfwd)`)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/200599) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_layout`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.linalg.lu_solve` | 主要受測 API |

## 觸發條件

LU[:,None] 的 singleton batch stride 非標準。

## 正確行為與實際行為

**Expected Behavior：** 解為 [0.2,0.6,1/6,1/3]。

**Actual Behavior：** 解為 [0.2,0.6,5,-1]。

## 錯誤簽名（Bug Signature）

解為 [0.2,0.6,5,-1]。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> LU[:, None] has stride (4, 2, 1, 2); the kernel mistakes the singleton dimension stride for the batch matrix distance. Noncanonical LU stride returns [0.2, 0.6, 5.0, -1.0] instead. Fixed float64 inputs, rtol=0 and atol=1e-12; both correct reference paths are checked.

## 分類理由與根因證據

CPU kernel 用 singleton 維度 stride 當作相鄰矩陣距離。

上游內文／討論提供機制分析，未自行修補驗證：CPU kernel 用 singleton 維度 stride 當作相鄰矩陣距離。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/200599)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/200599#issuecomment-6195309493)、[討論 2](https://github.com/pytorch/pytorch/issues/200599#issuecomment-6409682704)、[討論 3](https://github.com/pytorch/pytorch/issues/200599#issuecomment-6710647011)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_200599`。本案檢查的是「解為 [0.2,0.6,5,-1]」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「解為 [0.2,0.6,1/6,1/3]」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_200599/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/200599) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_200599/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_200599/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`f9d5b788695094f8fe1b843021d844a5f7391abde1b65e8572a488c1aaa65f6b`
- metadata.json SHA-256：`59e3e6f53c3242beb7b3be0324a4017eb991221b3649ed7f52c7550b5c763264`
- 核對時 Issue body SHA-256：`024b140dfb81c2ca4c14e455623086adaaa72963cbeb8c565c7bbd0b2cf4bf54`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
