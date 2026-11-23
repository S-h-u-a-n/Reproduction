# needs_review / wrong_forward_value

[總目錄](../../README.md)

## 分類定義（Category Definition）

根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

Observation 定義：forward 或一般數值運算回傳錯誤值，包含 NaN／Inf／signed zero 模式；不把梯度或 optimizer 更新混入。

## 分類準則（Classification Criteria）

先滿足 `needs_review` 的根因分類，再以 `wrong_forward_value` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**16**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_forward_value` | 16 |

## API 摘要（API Summary）

唯一 API 數：22；Issue/API 配對數：32。

| API | 涉及 Issue 數 |
| --- | ---: |
| `numpy.fix` | 1 |
| `torch.Tensor.__add__` | 1 |
| `torch.Tensor.__mul__` | 1 |
| `torch.Tensor.item` | 1 |
| `torch.acosh` | 1 |
| `torch.compile` | 10 |
| `torch.distributions.Normal` | 1 |
| `torch.distributions.TransformedDistribution` | 1 |
| `torch.distributions.kl_divergence` | 2 |
| `torch.distributions.transforms.AbsTransform` | 1 |
| `torch.erf` | 1 |
| `torch.floor_divide` | 1 |
| `torch.fx.GraphModule` | 1 |
| `torch.fx.symbolic_trace` | 1 |
| `torch.isin` | 1 |
| `torch.jit.freeze` | 1 |
| `torch.nn.BatchNorm1d` | 1 |
| `torch.nn.Linear` | 1 |
| `torch.prod` | 1 |
| `torch.remainder` | 1 |
| `torch.var` | 1 |
| `torch.where` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197811](torch_197811/README.md) | `torch.Tensor.__add__`：主要受測 API | 兩個 closure 分別擷取 Tensor 的加法與乘法 descriptor時，乘法 closure 重用加法圖而回傳 9。 | 捕獲 descriptor 的 guard 不完整，屬一般 Python callable 快取語意。 | [原文](https://github.com/pytorch/pytorch/issues/197811) |
| [#197811](torch_197811/README.md) | `torch.Tensor.__mul__`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 兩個 closure 分別擷取 Tensor 的加法與乘法 descriptor時，乘法 closure 重用加法圖而回傳 9。 | 捕獲 descriptor 的 guard 不完整，屬一般 Python callable 快取語意。 | [原文](https://github.com/pytorch/pytorch/issues/197811) |
| [#197811](torch_197811/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 兩個 closure 分別擷取 Tensor 的加法與乘法 descriptor時，乘法 closure 重用加法圖而回傳 9。 | 捕獲 descriptor 的 guard 不完整，屬一般 Python callable 快取語意。 | [原文](https://github.com/pytorch/pytorch/issues/197811) |
| [#197894](torch_197894/README.md) | `torch.fx.GraphModule`：主要受測 API | FX graph 的 operator.pow(-2,x)，x=2時，回傳 -4。 | FX Python codegen 缺少負數底數括號，屬運算優先序問題。 | [原文](https://github.com/pytorch/pytorch/issues/197894) |
| [#197895](torch_197895/README.md) | `torch.floor_divide`：主要受測 API | binary64 商在整數下緣的固定輸入時，回傳 [10,5,30,3]。 | lowering 對已四捨五入的商取 floor，而非正確餘數演算法。 | [原文](https://github.com/pytorch/pytorch/issues/197895) |
| [#197895](torch_197895/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | binary64 商在整數下緣的固定輸入時，回傳 [10,5,30,3]。 | lowering 對已四捨五入的商取 floor，而非正確餘數演算法。 | [原文](https://github.com/pytorch/pytorch/issues/197895) |
| [#198052](torch_198052/README.md) | `numpy.fix`：主要受測 API | torch.compile 處理正負半整數 float32 NumPy 輸入時，得到 [2,-2,2,-0]。 | torch._numpy 把 fix 對應到 round；不把同 Issue 其他 NumPy 症狀當成本地已測。 | [原文](https://github.com/pytorch/pytorch/issues/198052) |
| [#198052](torch_198052/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | torch.compile 處理正負半整數 float32 NumPy 輸入時，得到 [2,-2,2,-0]。 | torch._numpy 把 fix 對應到 round；不把同 Issue 其他 NumPy 症狀當成本地已測。 | [原文](https://github.com/pytorch/pytorch/issues/198052) |
| [#198057](torch_198057/README.md) | `torch.remainder`：主要受測 API | AVX512 CPU 向量路徑，無限除數及極大商時，前三個為 NaN、後兩個為零。 | 向量公式 a-floor(a/b)*b 的非有限值與消去問題；CPU 寬度影響觸發。 | [原文](https://github.com/pytorch/pytorch/issues/198057) |
| [#198057](torch_198057/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | AVX512 CPU 向量路徑，無限除數及極大商時，前三個為 NaN、後兩個為零。 | 向量公式 a-floor(a/b)*b 的非有限值與消去問題；CPU 寬度影響觸發。 | [原文](https://github.com/pytorch/pytorch/issues/198057) |
| [#198070](torch_198070/README.md) | `torch.Tensor.item`：主要受測 API | capture_scalar_outputs=True，以 v!=v 判斷 NaN時，條件被化簡而輸出 NaN。 | unbacked SymFloat 被視為有限實數，屬 symbolic 數值假設；測試中的參數名稱不構成訓練狀態證據。 | [原文](https://github.com/pytorch/pytorch/issues/198070) |
| [#198070](torch_198070/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | capture_scalar_outputs=True，以 v!=v 判斷 NaN時，條件被化簡而輸出 NaN。 | unbacked SymFloat 被視為有限實數，屬 symbolic 數值假設；測試中的參數名稱不構成訓練狀態證據。 | [原文](https://github.com/pytorch/pytorch/issues/198070) |
| [#198072](torch_198072/README.md) | `torch.fx.symbolic_trace`：主要受測 API | FX 函式有名為 nan 的參數並使用 NaN 常數時，NaN 常數被布林參數遮蔽。 | 生成 Python 程式的名稱衝突，非 tensor metadata。 | [原文](https://github.com/pytorch/pytorch/issues/198072) |
| [#198072](torch_198072/README.md) | `torch.where`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | FX 函式有名為 nan 的參數並使用 NaN 常數時，NaN 常數被布林參數遮蔽。 | 生成 Python 程式的名稱衝突，非 tensor metadata。 | [原文](https://github.com/pytorch/pytorch/issues/198072) |
| [#198134](torch_198134/README.md) | `torch.acosh`：主要受測 API | 長度八的 float64 1e200，CPU 向量路徑時，編譯結果為正無限。 | 向量 acosh 公式平方中間值溢位；一般數值穩定性問題。 | [原文](https://github.com/pytorch/pytorch/issues/198134) |
| [#198134](torch_198134/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 長度八的 float64 1e200，CPU 向量路徑時，編譯結果為正無限。 | 向量 acosh 公式平方中間值溢位；一般數值穩定性問題。 | [原文](https://github.com/pytorch/pytorch/issues/198134) |
| [#198183](torch_198183/README.md) | `torch.erf`：主要受測 API | AVX512、重複小數值 block 以觸發向量化時，每個 block 的 1e-8、1e-7 對應結果為零。 | erf 多項式 1-p(t)*exp(-x²) 在零附近相消。 | [原文](https://github.com/pytorch/pytorch/issues/198183) |
| [#198183](torch_198183/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | AVX512、重複小數值 block 以觸發向量化時，每個 block 的 1e-8、1e-7 對應結果為零。 | erf 多項式 1-p(t)*exp(-x²) 在零附近相消。 | [原文](https://github.com/pytorch/pytorch/issues/198183) |
| [#198484](torch_198484/README.md) | `torch.isin`：主要受測 API | test set 同時含 +inf 與 NaN時，回傳 False。 | 上游分析 searchsorted 對排序後 NaN 的索引處理錯誤；不是 layout 問題。 | [原文](https://github.com/pytorch/pytorch/issues/198484) |
| [#198484](torch_198484/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | test set 同時含 +inf 與 NaN時，回傳 False。 | 上游分析 searchsorted 對排序後 NaN 的索引處理錯誤；不是 layout 問題。 | [原文](https://github.com/pytorch/pytorch/issues/198484) |
| [#200229](torch_200229/README.md) | `torch.var`：主要受測 API | 兩個相同 float64 1e200 的 CPU compiled variance時，回傳 NaN。 | 後續討論更正：實際有 Welford，masked tail 的零權重 lane 在 delta² 溢位後產生 inf*0；不是直接認定未使用 Welford。 | [原文](https://github.com/pytorch/pytorch/issues/200229) |
| [#200229](torch_200229/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 兩個相同 float64 1e200 的 CPU compiled variance時，回傳 NaN。 | 後續討論更正：實際有 Welford，masked tail 的零權重 lane 在 delta² 溢位後產生 inf*0；不是直接認定未使用 Welford。 | [原文](https://github.com/pytorch/pytorch/issues/200229) |
| [#200924](torch_200924/README.md) | `torch.compile`：主要受測 API | 先空 dict 再非空 dict 的 bool(dict)時，重用舊空 dict 路徑。 | 上游指出 dict truthiness 缺少 emptiness guard；一般 Python cache，非訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/200924) |
| [#201082](torch_201082/README.md) | `torch.distributions.kl_divergence`：主要受測 API | float16 極小正 scale 對 Normal(scale=1)時，loss 為 +inf、gradient 為 -inf。 | 先平方 scale ratio 再 log 的下溢，屬機率公式數值穩定性。 | [原文](https://github.com/pytorch/pytorch/issues/201082) |
| [#201082](torch_201082/README.md) | `torch.distributions.Normal`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | float16 極小正 scale 對 Normal(scale=1)時，loss 為 +inf、gradient 為 -inf。 | 先平方 scale ratio 再 log 的下溢，屬機率公式數值穩定性。 | [原文](https://github.com/pytorch/pytorch/issues/201082) |
| [#202526](torch_202526/README.md) | `torch.jit.freeze`：主要受測 API | eval 模式，Linear 結果同時供 BatchNorm 與 residual時，凍結後符合 2*BN(h)。 | 上游指出 Linear-BatchNorm folding 未檢查多 consumer；本測試是推論圖改寫，不是訓練 buffer mutation。 | [原文](https://github.com/pytorch/pytorch/issues/202526) |
| [#202526](torch_202526/README.md) | `torch.nn.Linear`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | eval 模式，Linear 結果同時供 BatchNorm 與 residual時，凍結後符合 2*BN(h)。 | 上游指出 Linear-BatchNorm folding 未檢查多 consumer；本測試是推論圖改寫，不是訓練 buffer mutation。 | [原文](https://github.com/pytorch/pytorch/issues/202526) |
| [#202526](torch_202526/README.md) | `torch.nn.BatchNorm1d`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | eval 模式，Linear 結果同時供 BatchNorm 與 residual時，凍結後符合 2*BN(h)。 | 上游指出 Linear-BatchNorm folding 未檢查多 consumer；本測試是推論圖改寫，不是訓練 buffer mutation。 | [原文](https://github.com/pytorch/pytorch/issues/202526) |
| [#202967](torch_202967/README.md) | `torch.distributions.kl_divergence`：主要受測 API | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#202967](torch_202967/README.md) | `torch.distributions.TransformedDistribution`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#202967](torch_202967/README.md) | `torch.distributions.transforms.AbsTransform`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | KL invariant 被錯套用到非單射 transform；屬數學公式適用條件。 | [原文](https://github.com/pytorch/pytorch/issues/202967) |
| [#204679](torch_204679/README.md) | `torch.prod`：主要受測 API | AVX512 CPU 對 1000 個 BF16 129/128 求積時，本 build 回傳 1632。 | 上游指出 partial product 用輸入 dtype 累加而非寬型別；輸出 dtype 沒錯，屬 accumulator 精度政策。 | [原文](https://github.com/pytorch/pytorch/issues/204679) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#197811](torch_197811/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#197894](torch_197894/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#197895](torch_197895/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198052](torch_198052/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 Issue 同時包含 fix/cbrt/clip/sign/heaviside；本地只測 numpy.fix，不將整篇 Issue 視為五個已驗證案例。
- [#198057](torch_198057/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 前五個元素才屬聲稱的錯誤簽名，其他 lanes 用於觸發向量化；目前 AVX512，不外推 scalar tail 或其他 SIMD。
- [#198070](torch_198070/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198072](torch_198072/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198134](torch_198134/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198183](torch_198183/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 只斷言各 block 的兩個小值為零；其他值作向量化 padding，沒有宣稱整個數值區間都已驗證。
- [#198484](torch_198484/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#200229](torch_200229/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 後續討論更正原始推測為 masked Welford tail；較大不同長度的 eager 也可能不穩，不能泛化本例控制。
- [#200924](torch_200924/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#201082](torch_201082/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#202526](torch_202526/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 本例 eval/freeze 的 graph folding 錯誤，並非 BatchNorm running buffer 的訓練更新錯誤。
- [#202967](torch_202967/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#204679](torch_204679/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 1632 是這個 AVX512 build 的錯值，不是跨 ISA 常數；本例未測 CSR 或 float16。
