# needs_review

[總目錄](../README.md)

## 分類定義（Category Definition）

根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

## 分類準則（Classification Criteria）

Primary Cause 必須符合本類機制；觀察錯誤可以屬於不同 Observation。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**14**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_forward_value` | 8 |
| `incorrect_state` | 1 |
| `wrong_metadata` | 0 |
| `unexpected_exception` | 4 |
| `missing_exception` | 0 |
| `other` | 1 |

## API 摘要（API Summary）

唯一 API 數：17；Issue/API 配對數：26。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.compile` | 9 |
| `torch.distributions.kl_divergence` | 2 |
| `collections.OrderedDict.move_to_end` | 1 |
| `torch.Tensor.sum` | 1 |
| `torch.argmin` | 1 |
| `torch.distributions.Normal` | 1 |
| `torch.distributions.TransformedDistribution` | 1 |
| `torch.distributions.transforms.AbsTransform` | 1 |
| `torch.fx.GraphModule` | 1 |
| `torch.isin` | 1 |
| `torch.jit.freeze` | 1 |
| `torch.nn.BatchNorm1d` | 1 |
| `torch.nn.Linear` | 1 |
| `torch.nn.Parameter` | 1 |
| `torch.nn.functional.linear` | 1 |
| `torch.prod` | 1 |
| `torch.var` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197087](unexpected_exception/torch_197087/README.md) | `torch.argmin`：主要受測 API | dynamic=True、相等內維度的 broadcast argmin時，生成 C++ 含 Python ** 而編譯失敗。 | 上游指出 symbolic expression 的 C++ code generation 問題；shape 是觸發條件而非已證實表示錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/197087) |
| [#197087](unexpected_exception/torch_197087/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | dynamic=True、相等內維度的 broadcast argmin時，生成 C++ 含 Python ** 而編譯失敗。 | 上游指出 symbolic expression 的 C++ code generation 問題；shape 是觸發條件而非已證實表示錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/197087) |
| [#197894](wrong_forward_value/torch_197894/README.md) | `torch.fx.GraphModule`：主要受測 API | FX graph 的 operator.pow(-2,x)，x=2時，回傳 -4。 | FX Python codegen 缺少負數底數括號，屬運算優先序問題。 | [原文](https://github.com/pytorch/pytorch/issues/197894) |
| [#198189](incorrect_state/torch_198189/README.md) | `collections.OrderedDict.move_to_end`：主要受測 API | compiled function 重排傳入的 OrderedDict時，重排副作用被省略。 | 上游指出 should_reconstruct_all 未設定；屬 Python 容器狀態而非訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/198189) |
| [#198189](incorrect_state/torch_198189/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled function 重排傳入的 OrderedDict時，重排副作用被省略。 | 上游指出 should_reconstruct_all 未設定；屬 Python 容器狀態而非訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/198189) |
| [#198190](other/torch_198190/README.md) | `torch.compile`：主要受測 API | compiled function 回傳仍存活的 generator時，回傳 tuple_iterator 並丟失 return value。 | 上游指出 generator reconstruction 耗盡後重建成 tuple iterator，非 tensor metadata。 | [原文](https://github.com/pytorch/pytorch/issues/198190) |
| [#198192](unexpected_exception/torch_198192/README.md) | `torch.Tensor.sum`：主要受測 API | compiled function 內以 except IndexError 處理非法維度時，IndexError 直接逸出 compiled call。 | 上游指出 fake-value exception routing 沒有將 IndexError 轉為 observed exception。 | [原文](https://github.com/pytorch/pytorch/issues/198192) |
| [#198192](unexpected_exception/torch_198192/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled function 內以 except IndexError 處理非法維度時，IndexError 直接逸出 compiled call。 | 上游指出 fake-value exception routing 沒有將 IndexError 轉為 observed exception。 | [原文](https://github.com/pytorch/pytorch/issues/198192) |
| [#198484](wrong_forward_value/torch_198484/README.md) | `torch.isin`：主要受測 API | test set 同時含 +inf 與 NaN時，回傳 False。 | 上游分析 searchsorted 對排序後 NaN 的索引處理錯誤；不是 layout 問題。 | [原文](https://github.com/pytorch/pytorch/issues/198484) |
| [#198484](wrong_forward_value/torch_198484/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | test set 同時含 +inf 與 NaN時，回傳 False。 | 上游分析 searchsorted 對排序後 NaN 的索引處理錯誤；不是 layout 問題。 | [原文](https://github.com/pytorch/pytorch/issues/198484) |
| [#200229](wrong_forward_value/torch_200229/README.md) | `torch.var`：主要受測 API | 兩個相同 float64 1e200 的 CPU compiled variance時，回傳 NaN。 | 後續討論更正：實際有 Welford，masked tail 的零權重 lane 在 delta² 溢位後產生 inf*0；不是直接認定未使用 Welford。 | [原文](https://github.com/pytorch/pytorch/issues/200229) |
| [#200229](wrong_forward_value/torch_200229/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 兩個相同 float64 1e200 的 CPU compiled variance時，回傳 NaN。 | 後續討論更正：實際有 Welford，masked tail 的零權重 lane 在 delta² 溢位後產生 inf*0；不是直接認定未使用 Welford。 | [原文](https://github.com/pytorch/pytorch/issues/200229) |
| [#200924](wrong_forward_value/torch_200924/README.md) | `torch.compile`：主要受測 API | 先空 dict 再非空 dict 的 bool(dict)時，重用舊空 dict 路徑。 | 上游指出 dict truthiness 缺少 emptiness guard；一般 Python cache，非訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/200924) |
| [#201082](wrong_forward_value/torch_201082/README.md) | `torch.distributions.kl_divergence`：主要受測 API | float16 極小正 scale 對 Normal(scale=1)時，loss 為 +inf、gradient 為 -inf。 | 先平方 scale ratio 再 log 的下溢，屬機率公式數值穩定性。 | [原文](https://github.com/pytorch/pytorch/issues/201082) |
| [#201082](wrong_forward_value/torch_201082/README.md) | `torch.distributions.Normal`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | float16 極小正 scale 對 Normal(scale=1)時，loss 為 +inf、gradient 為 -inf。 | 先平方 scale ratio 再 log 的下溢，屬機率公式數值穩定性。 | [原文](https://github.com/pytorch/pytorch/issues/201082) |
| [#202526](wrong_forward_value/torch_202526/README.md) | `torch.jit.freeze`：主要受測 API | eval 模式，Linear 結果同時供 BatchNorm 與 residual時，凍結後符合 2*BN(h)。 | 上游指出 Linear-BatchNorm folding 未檢查多 consumer；本測試是推論圖改寫，不是訓練 buffer mutation。 | [原文](https://github.com/pytorch/pytorch/issues/202526) |
| [#202526](wrong_forward_value/torch_202526/README.md) | `torch.nn.Linear`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | eval 模式，Linear 結果同時供 BatchNorm 與 residual時，凍結後符合 2*BN(h)。 | 上游指出 Linear-BatchNorm folding 未檢查多 consumer；本測試是推論圖改寫，不是訓練 buffer mutation。 | [原文](https://github.com/pytorch/pytorch/issues/202526) |
| [#202526](wrong_forward_value/torch_202526/README.md) | `torch.nn.BatchNorm1d`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | eval 模式，Linear 結果同時供 BatchNorm 與 residual時，凍結後符合 2*BN(h)。 | 上游指出 Linear-BatchNorm folding 未檢查多 consumer；本測試是推論圖改寫，不是訓練 buffer mutation。 | [原文](https://github.com/pytorch/pytorch/issues/202526) |
| [#202967](wrong_forward_value/torch_202967/README.md) | `torch.distributions.kl_divergence`：主要受測 API | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#202967](wrong_forward_value/torch_202967/README.md) | `torch.distributions.TransformedDistribution`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#202967](wrong_forward_value/torch_202967/README.md) | `torch.distributions.transforms.AbsTransform`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#204679](wrong_forward_value/torch_204679/README.md) | `torch.prod`：主要受測 API | AVX512 CPU 對 1000 個 BF16 129/128 求積時，本 build 回傳 1632。 | 上游指出 partial product 用輸入 dtype 累加而非寬型別；輸出 dtype 沒錯，屬 accumulator 精度政策。 | [原文](https://github.com/pytorch/pytorch/issues/204679) |
| [#204945](unexpected_exception/torch_204945/README.md) | `torch.nn.Parameter`：主要受測 API | compiled function 內建立 Parameter 後檢查 type(p)時，SYNTHETIC_LOCAL NameError／InternalTorchDynamoError。 | 上游定位一般 type-source guard 引用了不可 guard 的 SyntheticLocalSource；未顯示訓練狀態毀損，故保留 needs_review。 | [原文](https://github.com/pytorch/pytorch/issues/204945) |
| [#204945](unexpected_exception/torch_204945/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled function 內建立 Parameter 後檢查 type(p)時，SYNTHETIC_LOCAL NameError／InternalTorchDynamoError。 | 上游定位一般 type-source guard 引用了不可 guard 的 SyntheticLocalSource；未顯示訓練狀態毀損，故保留 needs_review。 | [原文](https://github.com/pytorch/pytorch/issues/204945) |
| [#205823](unexpected_exception/torch_205823/README.md) | `torch.nn.functional.linear`：主要受測 API | freezing=True 且 enable_linear_binary_folding=True，乘 parameter reciprocal時，FX graph reciprocal use-before-definition 例外。 | 上游定位 linear binary folding 的節點排序；本例推論 graph rewrite，沒有訓練狀態或 tensor 表示根因證據。 | [原文](https://github.com/pytorch/pytorch/issues/205823) |
| [#205823](unexpected_exception/torch_205823/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | freezing=True 且 enable_linear_binary_folding=True，乘 parameter reciprocal時，FX graph reciprocal use-before-definition 例外。 | 上游定位 linear binary folding 的節點排序；本例推論 graph rewrite，沒有訓練狀態或 tensor 表示根因證據。 | [原文](https://github.com/pytorch/pytorch/issues/205823) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#197087](unexpected_exception/torch_197087/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#197894](wrong_forward_value/torch_197894/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198189](incorrect_state/torch_198189/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198190](other/torch_198190/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198192](unexpected_exception/torch_198192/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198484](wrong_forward_value/torch_198484/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#200229](wrong_forward_value/torch_200229/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 後續討論更正原始推測為 masked Welford tail；較大不同長度的 eager 也可能不穩，不能泛化本例控制。
- [#200924](wrong_forward_value/torch_200924/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#201082](wrong_forward_value/torch_201082/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#202526](wrong_forward_value/torch_202526/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 本例 eval/freeze 的 graph folding 錯誤，並非 BatchNorm running buffer 的訓練更新錯誤。
- [#202967](wrong_forward_value/torch_202967/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#204679](wrong_forward_value/torch_204679/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 1632 是這個 AVX512 build 的錯值，不是跨 ISA 常數；本例未測 CSR 或 float16。
- [#204945](unexpected_exception/torch_204945/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 原測試捕捉較寬的外層 Exception，再檢查 SYNTHETIC_LOCAL／NameError 訊息鏈；本次不修改其斷言。
- [#205823](unexpected_exception/torch_205823/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 freezing 與 linear binary folding 兩個開關及 reciprocal 節點順序不可省略。
