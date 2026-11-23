# tensor_representation / missing_exception

[總目錄](../../README.md)

## 分類定義（Category Definition）

Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。

Observation 定義：必要的輸入驗證、dtype 契約或 autograd version conflict 沒有拋出應有例外。

## 分類準則（Classification Criteria）

先滿足 `tensor_representation` 的根因分類，再以 `missing_exception` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**2**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `missing_exception` | 2 |

## API 摘要（API Summary）

唯一 API 數：3；Issue/API 配對數：3。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.Tensor.index_add` | 1 |
| `torch.compile` | 1 |
| `torch.softmax` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#198155](torch_198155/README.md) | `torch.softmax`：主要受測 API | int64 輸入的 softmax 經 Inductor時，回傳整數 tensor 而不報錯。 | operator dtype 支援契約在 lowering 被放寬；僅收錄原 Issue 眾多組合中的 int64 softmax。 | [原文](https://github.com/pytorch/pytorch/issues/198155) |
| [#198155](torch_198155/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | int64 輸入的 softmax 經 Inductor時，回傳整數 tensor 而不報錯。 | operator dtype 支援契約在 lowering 被放寬；僅收錄原 Issue 眾多組合中的 int64 softmax。 | [原文](https://github.com/pytorch/pytorch/issues/198155) |
| [#203852](torch_203852/README.md) | `torch.Tensor.index_add`：主要受測 API | 整數 tensor 配 floating alpha=2.5 或 0.5時，alpha 靜默截為 2 或 0。 | 上游提議補 alpha_check，主要是 scalar-to-tensor dtype 相容契約；是否連 2.0 也拒絕仍是上游政策。 | [原文](https://github.com/pytorch/pytorch/issues/203852) |

## 已知限制（Known Limitations）

原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#198155](torch_198155/README.md)：compiled 對不支援 eager dtype 的擴充，是否一律視為漏例外，需確認收錄政策。 Issue 的 134 operators／418 pairs 不屬本地驗證範圍；本地僅 int64 softmax。
- [#203852](torch_203852/README.md)：對整數 tensor 的 integral float alpha 是否也拒絕，仍是上游相容性政策；本例只測非整數值。 
