# needs_review / wrong_forward_value

[總目錄](../../README.md)

## 分類定義（Category Definition）

根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

Observation 定義：forward 或一般數值運算回傳錯誤值，包含 NaN／Inf／signed zero 模式；不把梯度或 optimizer 更新混入。

## 分類準則（Classification Criteria）

先滿足 `needs_review` 的根因分類，再以 `wrong_forward_value` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**3**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_forward_value` | 3 |

## API 摘要（API Summary）

唯一 API 數：5；Issue/API 配對數：6。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.distributions.kl_divergence` | 2 |
| `torch.distributions.Normal` | 1 |
| `torch.distributions.TransformedDistribution` | 1 |
| `torch.distributions.transforms.AbsTransform` | 1 |
| `torch.prod` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#201082](torch_201082/README.md) | `torch.distributions.kl_divergence`：主要受測 API | float16 極小正 scale 對 Normal(scale=1)時，loss 為 +inf、gradient 為 -inf。 | 先平方 scale ratio 再 log 的下溢，屬機率公式數值穩定性。 | [原文](https://github.com/pytorch/pytorch/issues/201082) |
| [#201082](torch_201082/README.md) | `torch.distributions.Normal`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | float16 極小正 scale 對 Normal(scale=1)時，loss 為 +inf、gradient 為 -inf。 | 先平方 scale ratio 再 log 的下溢，屬機率公式數值穩定性。 | [原文](https://github.com/pytorch/pytorch/issues/201082) |
| [#202967](torch_202967/README.md) | `torch.distributions.kl_divergence`：主要受測 API | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#202967](torch_202967/README.md) | `torch.distributions.TransformedDistribution`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#202967](torch_202967/README.md) | `torch.distributions.transforms.AbsTransform`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#204679](torch_204679/README.md) | `torch.prod`：主要受測 API | AVX512 CPU 對 1000 個 BF16 129/128 求積時，本 build 回傳 1632。 | 上游指出 partial product 用輸入 dtype 累加而非寬型別；輸出 dtype 沒錯，屬 accumulator 精度政策。 | [原文](https://github.com/pytorch/pytorch/issues/204679) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#201082](torch_201082/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#202967](torch_202967/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#204679](torch_204679/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 1632 是這個 AVX512 build 的錯值，不是跨 ISA 常數；本例未測 CSR 或 float16。
