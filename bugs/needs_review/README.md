# needs_review

[總目錄](../README.md)

## 分類定義（Category Definition）

根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

## 分類準則（Classification Criteria）

Primary Cause 必須符合本類機制；觀察錯誤可以屬於不同 Observation。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**25**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_forward_value` | 16 |
| `incorrect_state` | 3 |
| `wrong_metadata` | 1 |
| `unexpected_exception` | 4 |
| `missing_exception` | 0 |
| `other` | 1 |

## API 摘要（API Summary）

唯一 API 數：28；Issue/API 配對數：47。

| API | 涉及 Issue 數 |
| --- | ---: |
| `collections.OrderedDict.move_to_end` | 1 |
| `numpy.fix` | 1 |
| `torch.Tensor.__add__` | 1 |
| `torch.Tensor.__mul__` | 1 |
| `torch.Tensor.item` | 1 |
| `torch.Tensor.sum` | 1 |
| `torch.acosh` | 1 |
| `torch.argmin` | 1 |
| `torch.compile` | 18 |
| `torch.distributions.Normal` | 1 |
| `torch.distributions.TransformedDistribution` | 1 |
| `torch.distributions.kl_divergence` | 2 |
| `torch.distributions.transforms.AbsTransform` | 1 |
| `torch.erf` | 1 |
| `torch.floor_divide` | 1 |
| `torch.fx.GraphModule` | 2 |
| `torch.fx.symbolic_trace` | 1 |
| `torch.isin` | 1 |
| `torch.jit.freeze` | 1 |
| `torch.nn.BatchNorm1d` | 1 |
| `torch.nn.Linear` | 1 |
| `torch.nn.Parameter` | 1 |
| `torch.nn.functional.interpolate` | 1 |
| `torch.nn.functional.linear` | 1 |
| `torch.prod` | 1 |
| `torch.remainder` | 1 |
| `torch.var` | 1 |
| `torch.where` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197087](unexpected_exception/torch_197087/README.md) | `torch.argmin`：主要受測 API | dynamic=True、相等內維度的 broadcast argmin時，生成 C++ 含 Python ** 而編譯失敗。 | 上游指出 symbolic expression 的 C++ code generation 問題；shape 是觸發條件而非已證實表示錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/197087) |
| [#197087](unexpected_exception/torch_197087/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | dynamic=True、相等內維度的 broadcast argmin時，生成 C++ 含 Python ** 而編譯失敗。 | 上游指出 symbolic expression 的 C++ code generation 問題；shape 是觸發條件而非已證實表示錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/197087) |
| [#197811](wrong_forward_value/torch_197811/README.md) | `torch.Tensor.__add__`：主要受測 API | 兩個 closure 分別擷取 Tensor 的加法與乘法 descriptor時，乘法 closure 重用加法圖而回傳 9。 | 捕獲 descriptor 的 guard 不完整，屬一般 Python callable 快取語意。 | [原文](https://github.com/pytorch/pytorch/issues/197811) |
| [#197811](wrong_forward_value/torch_197811/README.md) | `torch.Tensor.__mul__`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 兩個 closure 分別擷取 Tensor 的加法與乘法 descriptor時，乘法 closure 重用加法圖而回傳 9。 | 捕獲 descriptor 的 guard 不完整，屬一般 Python callable 快取語意。 | [原文](https://github.com/pytorch/pytorch/issues/197811) |
| [#197811](wrong_forward_value/torch_197811/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 兩個 closure 分別擷取 Tensor 的加法與乘法 descriptor時，乘法 closure 重用加法圖而回傳 9。 | 捕獲 descriptor 的 guard 不完整，屬一般 Python callable 快取語意。 | [原文](https://github.com/pytorch/pytorch/issues/197811) |
| [#197889](wrong_metadata/torch_197889/README.md) | `torch.nn.functional.interpolate`：主要受測 API | 同程序依序傳入 scale 0.9、0.5、0.25、2.0時，實際為 7、6、6、6，後兩次 shape 過期。 | 上游指向 AOT cache 省略 float specialization guards；本例沒有訓練狀態，不能因 cache 名稱而歸入 training_state。 | [原文](https://github.com/pytorch/pytorch/issues/197889) |
| [#197889](wrong_metadata/torch_197889/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 同程序依序傳入 scale 0.9、0.5、0.25、2.0時，實際為 7、6、6、6，後兩次 shape 過期。 | 上游指向 AOT cache 省略 float specialization guards；本例沒有訓練狀態，不能因 cache 名稱而歸入 training_state。 | [原文](https://github.com/pytorch/pytorch/issues/197889) |
| [#197894](wrong_forward_value/torch_197894/README.md) | `torch.fx.GraphModule`：主要受測 API | FX graph 的 operator.pow(-2,x)，x=2時，回傳 -4。 | FX Python codegen 缺少負數底數括號，屬運算優先序問題。 | [原文](https://github.com/pytorch/pytorch/issues/197894) |
| [#197895](wrong_forward_value/torch_197895/README.md) | `torch.floor_divide`：主要受測 API | binary64 商在整數下緣的固定輸入時，回傳 [10,5,30,3]。 | lowering 對已四捨五入的商取 floor，而非正確餘數演算法。 | [原文](https://github.com/pytorch/pytorch/issues/197895) |
| [#197895](wrong_forward_value/torch_197895/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | binary64 商在整數下緣的固定輸入時，回傳 [10,5,30,3]。 | lowering 對已四捨五入的商取 floor，而非正確餘數演算法。 | [原文](https://github.com/pytorch/pytorch/issues/197895) |
| [#197896](incorrect_state/torch_197896/README.md) | `torch.compile`：主要受測 API | compiled function 內建立 local class，方法修改 closure list時，tensor 結果正常但 list 未更新。 | 上游指出 local class method 的來源追蹤遺失，屬 Python side-effect replay。 | [原文](https://github.com/pytorch/pytorch/issues/197896) |
| [#198052](wrong_forward_value/torch_198052/README.md) | `numpy.fix`：主要受測 API | torch.compile 處理正負半整數 float32 NumPy 輸入時，得到 [2,-2,2,-0]。 | torch._numpy 把 fix 對應到 round；不把同 Issue 其他 NumPy 症狀當成本地已測。 | [原文](https://github.com/pytorch/pytorch/issues/198052) |
| [#198052](wrong_forward_value/torch_198052/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | torch.compile 處理正負半整數 float32 NumPy 輸入時，得到 [2,-2,2,-0]。 | torch._numpy 把 fix 對應到 round；不把同 Issue 其他 NumPy 症狀當成本地已測。 | [原文](https://github.com/pytorch/pytorch/issues/198052) |
| [#198057](wrong_forward_value/torch_198057/README.md) | `torch.remainder`：主要受測 API | AVX512 CPU 向量路徑，無限除數及極大商時，前三個為 NaN、後兩個為零。 | 向量公式 a-floor(a/b)*b 的非有限值與消去問題；CPU 寬度影響觸發。 | [原文](https://github.com/pytorch/pytorch/issues/198057) |
| [#198057](wrong_forward_value/torch_198057/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | AVX512 CPU 向量路徑，無限除數及極大商時，前三個為 NaN、後兩個為零。 | 向量公式 a-floor(a/b)*b 的非有限值與消去問題；CPU 寬度影響觸發。 | [原文](https://github.com/pytorch/pytorch/issues/198057) |
| [#198070](wrong_forward_value/torch_198070/README.md) | `torch.Tensor.item`：主要受測 API | capture_scalar_outputs=True，以 v!=v 判斷 NaN時，條件被化簡而輸出 NaN。 | unbacked SymFloat 被視為有限實數，屬 symbolic 數值假設；測試中的參數名稱不構成訓練狀態證據。 | [原文](https://github.com/pytorch/pytorch/issues/198070) |
| [#198070](wrong_forward_value/torch_198070/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | capture_scalar_outputs=True，以 v!=v 判斷 NaN時，條件被化簡而輸出 NaN。 | unbacked SymFloat 被視為有限實數，屬 symbolic 數值假設；測試中的參數名稱不構成訓練狀態證據。 | [原文](https://github.com/pytorch/pytorch/issues/198070) |
| [#198072](wrong_forward_value/torch_198072/README.md) | `torch.fx.symbolic_trace`：主要受測 API | FX 函式有名為 nan 的參數並使用 NaN 常數時，NaN 常數被布林參數遮蔽。 | 生成 Python 程式的名稱衝突，非 tensor metadata。 | [原文](https://github.com/pytorch/pytorch/issues/198072) |
| [#198072](wrong_forward_value/torch_198072/README.md) | `torch.where`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | FX 函式有名為 nan 的參數並使用 NaN 常數時，NaN 常數被布林參數遮蔽。 | 生成 Python 程式的名稱衝突，非 tensor metadata。 | [原文](https://github.com/pytorch/pytorch/issues/198072) |
| [#198077](incorrect_state/torch_198077/README.md) | `torch.fx.GraphModule`：主要受測 API | 含 operator.iadd 的 GraphModule 經 pickle round trip時，恢復後變成 out-of-place add，input 不變。 | FX 由程式碼重建圖時缺少 Proxy.__iadd__ 語意；未涉及 autograd graph lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/198077) |
| [#198134](wrong_forward_value/torch_198134/README.md) | `torch.acosh`：主要受測 API | 長度八的 float64 1e200，CPU 向量路徑時，編譯結果為正無限。 | 向量 acosh 公式平方中間值溢位；一般數值穩定性問題。 | [原文](https://github.com/pytorch/pytorch/issues/198134) |
| [#198134](wrong_forward_value/torch_198134/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 長度八的 float64 1e200，CPU 向量路徑時，編譯結果為正無限。 | 向量 acosh 公式平方中間值溢位；一般數值穩定性問題。 | [原文](https://github.com/pytorch/pytorch/issues/198134) |
| [#198183](wrong_forward_value/torch_198183/README.md) | `torch.erf`：主要受測 API | AVX512、重複小數值 block 以觸發向量化時，每個 block 的 1e-8、1e-7 對應結果為零。 | erf 多項式 1-p(t)*exp(-x²) 在零附近相消。 | [原文](https://github.com/pytorch/pytorch/issues/198183) |
| [#198183](wrong_forward_value/torch_198183/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | AVX512、重複小數值 block 以觸發向量化時，每個 block 的 1e-8、1e-7 對應結果為零。 | erf 多項式 1-p(t)*exp(-x²) 在零附近相消。 | [原文](https://github.com/pytorch/pytorch/issues/198183) |
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
- [#197811](wrong_forward_value/torch_197811/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#197889](wrong_metadata/torch_197889/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 四次 scale 呼叫的程序歷史是必要條件；不得將四次拆成四個互不相關程序。
- [#197894](wrong_forward_value/torch_197894/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#197895](wrong_forward_value/torch_197895/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#197896](incorrect_state/torch_197896/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198052](wrong_forward_value/torch_198052/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 Issue 同時包含 fix/cbrt/clip/sign/heaviside；本地只測 numpy.fix，不將整篇 Issue 視為五個已驗證案例。
- [#198057](wrong_forward_value/torch_198057/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 前五個元素才屬聲稱的錯誤簽名，其他 lanes 用於觸發向量化；目前 AVX512，不外推 scalar tail 或其他 SIMD。
- [#198070](wrong_forward_value/torch_198070/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198072](wrong_forward_value/torch_198072/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198077](incorrect_state/torch_198077/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198134](wrong_forward_value/torch_198134/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198183](wrong_forward_value/torch_198183/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 只斷言各 block 的兩個小值為零；其他值作向量化 padding，沒有宣稱整個數值區間都已驗證。
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
