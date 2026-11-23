# Mirage PyTorch Bug 分類目錄

本目錄收錄目前實際存在的 **100 個唯一 Issue**。分類依本地 reproducer 與已讀取的 GitHub Issue 內文／可見討論，沒有修改任何原始測試或 metadata。

[Excel Catalog](../Mirage_Bug_Catalog.xlsx) 是 API／Issue 可篩選索引；本目錄提供分類、來源、驗證與還原資訊。PASS 代表既有錯誤簽名仍被觀察到，不代表 PyTorch 正確，也不代表 Mirage 已接入。

## 分類定義與準則

- [tensor_representation](tensor_representation/README.md)：Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。
- [training_state](training_state/README.md)：autograd graph／saved tensor、version counter／inplace mutation、backward／高階梯度規則、optimizer／parameter lifecycle、checkpoint／activation recomputation、training buffer mutation 與 retained graph 狀態。
- [needs_review](needs_review/README.md)：根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

- **主次分類**：每個 Issue 只選一個 Primary Cause 與一個 Primary Observation；其他症狀放 Secondary 欄，Issue 統計不重複。
- **證據優先**：以目前 test_bug.py 的必要觸發條件對照原 Issue 內文及可見討論；不以 metadata.bug_type 或 API 名稱直接決定分類。
- **梯度不等於訓練根因**：已知 layout／view／batching 表示導致 wrong_gradient 時優先 tensor_representation；已定位 backward 規則或 saved/version 狀態時歸 training_state。
- **編譯不等於訓練狀態**：torch.compile、AOT cache 或 BatchNorm 名稱本身不是 training_state 證據；一般推論 graph rewrite、Python guards 可歸 needs_review。
- **數值與 dtype 邊界**：輸出 dtype、scalar 縮窄或 promotion 遺失屬表示；僅累加精度或數值公式不穩定列 needs_review。
- **未知根因**：沒有完整上游根因說明時標示 Root cause not confirmed；可依必要觸發條件暫分，但保留 medium confidence 與 Review Needed。
- **confidence**：high／medium 只描述分類依據強度，並非 PyTorch 根因已獨立認證、testcase 品質通過或 Mirage 已接入。
- **Issue 與根因**：Issue 數、唯一 API 數及 Issue/API 配對數分開；跨 Issue 共根因與單 Issue 多根因保留，不自動合併或拆分。
- **歷史驗證**：metadata 中既有 runs/passes/review 原樣保存；安裝結果記錄替換案的獨立執行，本次目錄同步另執行一次全套驗證。
- **PASS 的意義**：pytest PASS 代表原斷言仍觀察到已知錯誤簽名；不是 PyTorch 正確，也不是 Mirage 接入完成。

## 資料夾摘要與 Issue 數量

| Primary Cause | Issue 數 |
| --- | ---: |
| [tensor_representation](tensor_representation/README.md) | 53 |
| [training_state](training_state/README.md) | 27 |
| [needs_review](needs_review/README.md) | 20 |

| Observation | Issue 數 | 定義 |
| --- | ---: | --- |
| `wrong_gradient` | 20 | 第一階／高階導數、Jacobian 或 tangent 與正確參考不符。 |
| `wrong_forward_value` | 30 | forward 或一般數值運算回傳錯誤值，包含 NaN／Inf／signed zero 模式；不把梯度或 optimizer 更新混入。 |
| `wrong_optimizer_update` | 1 | optimizer step 對 parameter 產生錯誤數值更新。 |
| `incorrect_state` | 11 | alias 寫入後的可觀察狀態、Python 容器副作用、物件／parameter 存活等狀態不符；不代表 Primary Cause 必為 training_state。 |
| `wrong_metadata` | 10 | shape、dtype、rank、tangent 表示或 checkpoint tensor metadata 錯誤。 |
| `unexpected_exception` | 21 | 本應成功或可由使用者 handler 處理的操作，拋出非預期 Python／編譯例外；不等同 process crash。 |
| `missing_exception` | 6 | 必要的輸入驗證、dtype 契約或 autograd version conflict 沒有拋出應有例外。 |
| `process_crash` | 0 | 程序因 signal、abort、segfault 等非 Python 例外而終止；本次沒有把單純 traceback 計入。 |
| `memory_corruption` | 0 | 本地案例實際驗證 allocation 外或其他記憶體毀損；僅有上游宣稱、或 backing tensor 內錯位寫入，不自動算入。 |
| `other` | 1 | 其他可觀察差異，例如 Python generator 型別及 return value 遺失。 |

只有有案例的 Observation 才建立子資料夾；零件數仍列於 Excel 統計與 Taxonomy。

## API 摘要

唯一 API **114**；Issue/API 配對 **194**。配對數不當作 Issue 數；每個分類 README 列出各 API 的案例數與作用。

## 全部 Issue／API 說明與來源

| Issue／路徑 | API | 說明 | Primary Cause / Observation | 來源 |
| --- | --- | --- | --- | --- |
| [#192639](tensor_representation/wrong_metadata/torch_192639/README.md) | `torch.autograd.forward_ad.unpack_dual`<br>`torch._subclasses.functional_tensor.dispatch_functionalize` | dual tensor 經 dispatch_functionalize 包裝時，tangent 變成 None。 | `tensor_representation` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/192639) |
| [#195451](tensor_representation/incorrect_state/torch_195451/README.md) | `torch.slice_scatter`<br>`torch.compile` | functional scatter、輸入 mutation 與回傳結果時，回傳結果 alias 輸入，修改結果連帶改變輸入。 | `tensor_representation` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/195451) |
| [#195488](training_state/incorrect_state/torch_195488/README.md) | `torch.amp.autocast`<br>`torch.compile` | 編譯區域發生例外時 autocast nesting 未正常清理，造成後續訓練狀態洩漏。 | `training_state` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/195488) |
| [#197084](tensor_representation/wrong_gradient/torch_197084/README.md) | `torch.linalg.pinv`<br>`torch.compile` | 固定 full-column-rank complex64 矩陣、編譯後反向時，完整梯度符合缺少 conjugation 的 SVD 結果所導出的錯誤 VJP。 | `tensor_representation` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/197084) |
| [#197087](needs_review/unexpected_exception/torch_197087/README.md) | `torch.argmin`<br>`torch.compile` | dynamic=True、相等內維度的 broadcast argmin時，生成 C++ 含 Python ** 而編譯失敗。 | `needs_review` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/197087) |
| [#197092](training_state/unexpected_exception/torch_197092/README.md) | `torch.nn.functional.interpolate`<br>`torch._dynamo.compiled_autograd._enable`<br>`torch.compile` | compiled autograd、bilinear interpolation backward時，fake-tensor propagation 出現 isIntList INTERNAL ASSERT。 | `training_state` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/197092) |
| [#197097](tensor_representation/unexpected_exception/torch_197097/README.md) | `torch.linalg.vector_norm`<br>`torch.compile` | shape=(0,5)、ord=inf、dim=-1時，錯判 reduction 維度為空並拋例外。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/197097) |
| [#197399](tensor_representation/unexpected_exception/torch_197399/README.md) | `torch.Tensor.set_`<br>`torch.compile` | 把空 tensor 的 storage 重綁成長度一後讀 x[0]時，仍以舊空 shape 追蹤並拋 IndexError。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/197399) |
| [#197811](needs_review/wrong_forward_value/torch_197811/README.md) | `torch.Tensor.__add__`<br>`torch.Tensor.__mul__`<br>`torch.compile` | 兩個 closure 分別擷取 Tensor 的加法與乘法 descriptor時，乘法 closure 重用加法圖而回傳 9。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/197811) |
| [#197887](training_state/missing_exception/torch_197887/README.md) | `torch.matmul`<br>`torch.compile` | forward 保存 input view 後，原地修改 input 再 backward時，沒有例外，使用已修改資料計算梯度。 | `training_state` / `missing_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/197887) |
| [#197888](tensor_representation/wrong_gradient/torch_197888/README.md) | `torch.ops.aten.adaptive_max_pool3d_backward`<br>`torch.nn.functional.adaptive_max_pool3d` | CPU adaptive max pool backward scatters gradients to the wrong input elements when it reads channels_last_3d indices in storage order. | `tensor_representation` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/197888) |
| [#197889](needs_review/wrong_metadata/torch_197889/README.md) | `torch.nn.functional.interpolate`<br>`torch.compile` | 同程序依序傳入 scale 0.9、0.5、0.25、2.0時，實際為 7、6、6、6，後兩次 shape 過期。 | `needs_review` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/197889) |
| [#197893](tensor_representation/incorrect_state/torch_197893/README.md) | `torch.Tensor.div`<br>`torch.compile` | 編譯 x/1 後修改回傳 tensor時，結果與 input 共用 storage，修改相互影響。 | `tensor_representation` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/197893) |
| [#197894](needs_review/wrong_forward_value/torch_197894/README.md) | `torch.fx.GraphModule` | FX graph 的 operator.pow(-2,x)，x=2時，回傳 -4。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/197894) |
| [#197896](needs_review/incorrect_state/torch_197896/README.md) | `torch.compile` | compiled function 內建立 local class，方法修改 closure list時，tensor 結果正常但 list 未更新。 | `needs_review` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/197896) |
| [#198056](tensor_representation/wrong_metadata/torch_198056/README.md) | `numpy.cumsum`<br>`torch.compile` | 編譯 int8 NumPy 累加時，維持 int8 dtype 並發生 wraparound。 | `tensor_representation` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/198056) |
| [#198064](tensor_representation/wrong_forward_value/torch_198064/README.md) | `torch.SymInt.__round__`<br>`torch.compile` | dynamic shape 長度使用 round(n,-1)時，忽略負 ndigits，使用原 n。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/198064) |
| [#198071](tensor_representation/wrong_forward_value/torch_198071/README.md) | `torch.clamp`<br>`torch.compile` | int8 輸入與超出範圍的 Python max=300時，bound 轉成 int8 的 44，127 被截到 44。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/198071) |
| [#198077](needs_review/incorrect_state/torch_198077/README.md) | `torch.fx.GraphModule` | 含 operator.iadd 的 GraphModule 經 pickle round trip時，恢復後變成 out-of-place add，input 不變。 | `needs_review` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/198077) |
| [#198081](tensor_representation/wrong_metadata/torch_198081/README.md) | `torch.any`<br>`torch.compile` | uint8 reduction 後再做整數算術時，變成 bool，後續計算變為 int64 的 300。 | `tensor_representation` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/198081) |
| [#198095](tensor_representation/wrong_forward_value/torch_198095/README.md) | `torch.compile` | 共享 storage 的 base 與切片輸入，修改 base 後回傳切片的 view時，錯誤回傳 t0 第一列。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/198095) |
| [#198102](tensor_representation/wrong_forward_value/torch_198102/README.md) | `torch.Tensor.unfold`<br>`torch.compile` | 不重疊 unfold view 的寫入，base 中間有未覆蓋位置時，未覆蓋的位置被歸零。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/198102) |
| [#198118](tensor_representation/wrong_forward_value/torch_198118/README.md) | `torch.linalg.pinv`<br>`torch.utils._python_dispatch.TorchDispatchMode` | complex128 pinv 經 pass-through TorchDispatchMode時，符合缺少 conjugation 的完整 SVD 公式。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/198118) |
| [#198119](training_state/wrong_gradient/torch_198119/README.md) | `torch.nn.functional.avg_pool1d`<br>`torch.compile` | ceil_mode=True，最後 pooling window 只有兩個有效元素時，完整梯度 [1/3,1/3,2/3,1/3,2/3,1/3]。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/198119) |
| [#198134](needs_review/wrong_forward_value/torch_198134/README.md) | `torch.acosh`<br>`torch.compile` | 長度八的 float64 1e200，CPU 向量路徑時，編譯結果為正無限。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/198134) |
| [#198155](tensor_representation/missing_exception/torch_198155/README.md) | `torch.softmax`<br>`torch.compile` | int64 輸入的 softmax 經 Inductor時，回傳整數 tensor 而不報錯。 | `tensor_representation` / `missing_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/198155) |
| [#198183](needs_review/wrong_forward_value/torch_198183/README.md) | `torch.erf`<br>`torch.compile` | AVX512、重複小數值 block 以觸發向量化時，每個 block 的 1e-8、1e-7 對應結果為零。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/198183) |
| [#198189](needs_review/incorrect_state/torch_198189/README.md) | `collections.OrderedDict.move_to_end`<br>`torch.compile` | compiled function 重排傳入的 OrderedDict時，重排副作用被省略。 | `needs_review` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/198189) |
| [#198190](needs_review/other/torch_198190/README.md) | `torch.compile` | compiled function 回傳仍存活的 generator時，回傳 tuple_iterator 並丟失 return value。 | `needs_review` / `other` | [GitHub](https://github.com/pytorch/pytorch/issues/198190) |
| [#198192](needs_review/unexpected_exception/torch_198192/README.md) | `torch.Tensor.sum`<br>`torch.compile` | compiled function 內以 except IndexError 處理非法維度時，IndexError 直接逸出 compiled call。 | `needs_review` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/198192) |
| [#198484](needs_review/wrong_forward_value/torch_198484/README.md) | `torch.isin`<br>`torch.compile` | test set 同時含 +inf 與 NaN時，回傳 False。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/198484) |
| [#198669](tensor_representation/unexpected_exception/torch_198669/README.md) | `torch.softmax`<br>`torch.eq`<br>`torch.div`<br>`torch.compile` | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/198669) |
| [#198851](tensor_representation/wrong_metadata/torch_198851/README.md) | `torch.any`<br>`torch.all`<br>`torch.compile` | reduction 指定 dim=()時，編譯後回傳 scalar。 | `tensor_representation` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/198851) |
| [#198852](tensor_representation/wrong_metadata/torch_198852/README.md) | `torch.cat`<br>`torch.compile` | 空 float64 tensor 與多個非空 float32 tensor 串接時，輸出 float32。 | `tensor_representation` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/198852) |
| [#198868](tensor_representation/wrong_metadata/torch_198868/README.md) | `torch.scatter`<br>`torch.compile` | scalar input 與 empty index時，shape 變成 (1,)。 | `tensor_representation` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/198868) |
| [#198994](tensor_representation/wrong_metadata/torch_198994/README.md) | `torch.nn.functional.soft_margin_loss`<br>`torch.compile` | input float32、target float64時，Inductor 回傳 float64。 | `tensor_representation` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/198994) |
| [#199151](training_state/incorrect_state/torch_199151/README.md) | `torch.ao.quantization.observer.PerChannelMinMaxObserver` | PerChannelMinMaxObserver 在 reset 後丟失 float64 dtype 設定，導致狀態 dtype 回退。 | `training_state` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/199151) |
| [#199211](tensor_representation/unexpected_exception/torch_199211/README.md) | `torch.isin` | test_elements 為無法直接 flatten 的非連續多維 tensor時，view-size compatibility RuntimeError。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/199211) |
| [#199214](tensor_representation/unexpected_exception/torch_199214/README.md) | `torch.dequantize`<br>`torch.Tensor.trunc_`<br>`torch.compile` | 普通 float input 先 dequantize 再原地 trunc_時，functionalization 拋 copy_／dequantize assertion。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/199214) |
| [#199215](training_state/unexpected_exception/torch_199215/README.md) | `torch.nn.Parameter`<br>`torch.compile` | 整數 Parameter(requires_grad=False)，freezing 且 discard_parameters時，內層 RuntimeError 指出僅浮點 dtype 可要求梯度。 | `training_state` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/199215) |
| [#199258](training_state/unexpected_exception/torch_199258/README.md) | `torch.utils.checkpoint.checkpoint`<br>`torch.compile` | use_reentrant=False，區域中含 x*1.0時，NetworkXError: node source not in graph。 | `training_state` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/199258) |
| [#199350](tensor_representation/unexpected_exception/torch_199350/README.md) | `torch.view_as_complex_copy`<br>`torch.nn.functional.adaptive_max_pool2d`<br>`torch.compile` | pooling 後接 view_as_complex_copy，Inductor 選擇 layout時，fallback 拋 last dimension stride 1 RuntimeError。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/199350) |
| [#199571](tensor_representation/unexpected_exception/torch_199571/README.md) | `torch.linalg.solve`<br>`torch.imag`<br>`torch.compile` | complex right solve(left=False) 的輸出取 imag時，view_as_real 不接受 unresolved conjugated tensor。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/199571) |
| [#199644](tensor_representation/wrong_forward_value/torch_199644/README.md) | `torch.Tensor.item`<br>`torch.compile` | 擷取 float64 scalar 16777219 再傳入 CPU 編譯 kernel時，兩者皆變成 16777220。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/199644) |
| [#199920](tensor_representation/wrong_metadata/torch_199920/README.md) | `torch.ops.aten._fused_moving_avg_obs_fq_helper_functional`<br>`torch._subclasses.fake_tensor.FakeTensorMode` | per-channel fake quant observer 首次使用，八個 channel時，min/max 仍為零長、scale/zero-point 仍為一。 | `tensor_representation` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/199920) |
| [#199941](training_state/unexpected_exception/torch_199941/README.md) | `torch.vander`<br>`torch.linalg.vander` | vander 輸出求和後 backward時，saved-variable inplace-modification RuntimeError。 | `training_state` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/199941) |
| [#200229](needs_review/wrong_forward_value/torch_200229/README.md) | `torch.var`<br>`torch.compile` | 兩個相同 float64 1e200 的 CPU compiled variance時，回傳 NaN。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/200229) |
| [#200524](training_state/missing_exception/torch_200524/README.md) | `torch.full`<br>`torch.compile` | fill value 是 requires_grad=True 的零維 tensor時，接受並建立可向 fill 反傳的 graph。 | `training_state` / `missing_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/200524) |
| [#200572](tensor_representation/wrong_gradient/torch_200572/README.md) | `torch.autograd.Function`<br>`torch.Tensor.unsqueeze`<br>`torch.compile` | custom Function 輸出為 input view，再回傳其 view時，custom backward 被跳過。 | `tensor_representation` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/200572) |
| [#200599](tensor_representation/wrong_forward_value/torch_200599/README.md) | `torch.linalg.lu_solve` | LU[:,None] 的 singleton batch stride 非標準時，解為 [0.2,0.6,5,-1]。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/200599) |
| [#200600](training_state/wrong_gradient/torch_200600/README.md) | `torch.linalg.solve`<br>`torch.autograd.forward_ad` | forward-over-reverse，backward 的 create_graph=False時，一個 tangent 消失、另一個只剩一半。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/200600) |
| [#200924](needs_review/wrong_forward_value/torch_200924/README.md) | `torch.compile` | 先空 dict 再非空 dict 的 bool(dict)時，重用舊空 dict 路徑。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/200924) |
| [#200925](tensor_representation/wrong_forward_value/torch_200925/README.md) | `torch.compile` | 先以不同 offset 的重疊 views 暖機，再傳同 offset aliases時，沿用第一次 synthetic-base offset，寫錯位置。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/200925) |
| [#201082](needs_review/wrong_forward_value/torch_201082/README.md) | `torch.distributions.kl_divergence`<br>`torch.distributions.Normal` | float16 極小正 scale 對 Normal(scale=1)時，loss 為 +inf、gradient 為 -inf。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/201082) |
| [#201089](training_state/wrong_gradient/torch_201089/README.md) | `torch.compile` | forward 原地增加 counter buffer，再以其算出的 scale 作用在 Linear時，forward 正確但 weight gradient 為 0.3。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/201089) |
| [#201158](training_state/incorrect_state/torch_201158/README.md) | `torch.utils.checkpoint.create_selective_checkpoint_contexts` | Selective checkpointing 快取持有 Inductor 之後重用的 buffer，導致已儲存的中間 Tensor 被覆寫。 | `training_state` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/201158) |
| [#201268](tensor_representation/wrong_forward_value/torch_201268/README.md) | `torch.add`<br>`torch.sparse_csr_tensor` | CSR out.values() 為合法 stride=2 view時，values 為 [11,-99]，寫入相鄰 storage 而非第二個 logical element。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/201268) |
| [#201633](training_state/wrong_gradient/torch_201633/README.md) | `torch.segment_reduce` | max/min 有兩個相同 extrema，incoming gradient 為負時，回傳 [-1,-1,0]，正梯度控制正常。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/201633) |
| [#201649](tensor_representation/wrong_gradient/torch_201649/README.md) | `torch.compiler.nested_compile_region`<br>`torch.compile` | 連續呼叫 nested region，forward 保存 region input 供 backward時，第一個梯度錯誤依賴 y。 | `tensor_representation` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/201649) |
| [#201947](training_state/wrong_gradient/torch_201947/README.md) | `torch.asinh`<br>`torch.acosh` | float16 x=1000 的 backward時，導數為零。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/201947) |
| [#201970](training_state/wrong_gradient/torch_201970/README.md) | `torch.compile`<br>`torch.Tensor.backward` | 先普通 backward 編譯暖機，再相同 graph 以 retain_graph=True 重複 backward時，第二次梯度變成 8。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/201970) |
| [#202364](tensor_representation/wrong_gradient/torch_202364/README.md) | `torch.Tensor.as_strided_`<br>`torch.compile` | view 的 shape/stride 原地變更後 mul_，再 compiled backward時，forward 正確、gradient=[2,6,6,6]。 | `tensor_representation` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/202364) |
| [#202416](tensor_representation/unexpected_exception/torch_202416/README.md) | `torch.compile`<br>`torch.Tensor.detach` | Inductor raises a ViewMeta output-shape assertion while eager works. | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/202416) |
| [#202482](tensor_representation/wrong_forward_value/torch_202482/README.md) | `torch.cat`<br>`torch.nn.functional.linear`<br>`torch.Tensor.index_put_`<br>`torch.compile` | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/202482) |
| [#202526](needs_review/wrong_forward_value/torch_202526/README.md) | `torch.jit.freeze`<br>`torch.nn.Linear`<br>`torch.nn.BatchNorm1d` | eval 模式，Linear 結果同時供 BatchNorm 與 residual時，凍結後符合 2*BN(h)。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/202526) |
| [#202726](tensor_representation/unexpected_exception/torch_202726/README.md) | `torch.Tensor.real`<br>`torch.Tensor.__torch_function__`<br>`torch.compile` | real dtype 的 __torch_function__ subclass 在 compiled 中取 .real時，source must be None 的 AssertionError。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/202726) |
| [#202806](training_state/missing_exception/torch_202806/README.md) | `torch.Tensor.detach`<br>`torch.compile` | eager 已保存 weight，再透過 compiled detached alias 修改時，沒有版本遞增，backward 靜默使用新 weight。 | `training_state` / `missing_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/202806) |
| [#202862](tensor_representation/unexpected_exception/torch_202862/README.md) | `torch.ops.aten.unsqueeze_.default`<br>`torch.compile` | 直接對 graph input 呼叫 OpOverload 的 inplace rank-changing view時，guard creation 拋 IndexError。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/202862) |
| [#202965](training_state/wrong_gradient/torch_202965/README.md) | `torch.distributions.kl_divergence`<br>`torch.distributions.Categorical` | p logits 含 -inf，對其求 KL gradient時，loss 正確但整列梯度 NaN。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/202965) |
| [#202966](tensor_representation/wrong_forward_value/torch_202966/README.md) | `torch.distributions.kl_divergence`<br>`torch.distributions.Wishart` | batched Wishart KL 且 p 的 df/covariance 要求梯度時，df term 錯跨 batch 加總，兩類 p 參數梯度皆 None。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/202966) |
| [#202967](needs_review/wrong_forward_value/torch_202967/README.md) | `torch.distributions.kl_divergence`<br>`torch.distributions.TransformedDistribution`<br>`torch.distributions.transforms.AbsTransform` | 相同 AbsTransform 作用於 N(-1,1) 與 N(1,1)時，回傳 base Normal KL=2。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/202967) |
| [#203078](tensor_representation/wrong_forward_value/torch_203078/README.md) | `torch.Tensor.scatter_add`<br>`torch.Tensor.scatter_reduce` | expanded index stride=(1,0)，self 比 index 更寬時，寫入 row 0、1，row sums=[16,16,0]。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/203078) |
| [#203485](tensor_representation/unexpected_exception/torch_203485/README.md) | `torch.nn.functional.grouped_mm` | sum().backward() 傳入 stride=[0,0] 的 broadcast gradient時，Invalid strides/sizes RuntimeError。 | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/203485) |
| [#203806](tensor_representation/wrong_forward_value/torch_203806/README.md) | `torch._foreach_copy_`<br>`torch.compile` | 以 [b.clone(),a.clone()] 複製回 [a,b]時，兩個 tensor 都得到原 b 的值。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/203806) |
| [#203852](tensor_representation/missing_exception/torch_203852/README.md) | `torch.Tensor.index_add` | 整數 tensor 配 floating alpha=2.5 或 0.5時，alpha 靜默截為 2 或 0。 | `tensor_representation` / `missing_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/203852) |
| [#203866](tensor_representation/unexpected_exception/torch_203866/README.md) | `DTensor.from_local`<br>`torch.save` | torch.save raises an invalid-storage RuntimeError for a DTensor with a nonzero storage offset while the zero-offset control serializes. | `tensor_representation` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/203866) |
| [#203946](training_state/wrong_gradient/torch_203946/README.md) | `torch.nn.functional.cosine_similarity` | norm(x1)<eps<norm(x2)，float64 固定向量時，第一分量只有一半，第二分量正確。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/203946) |
| [#204181](tensor_representation/wrong_forward_value/torch_204181/README.md) | `torch.Tensor.fill_diagonal_` | 非連續 7x2 column view，wrap=True時，寫入 view 外的第三欄，漏掉 wrapped cell。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/204181) |
| [#204188](training_state/wrong_metadata/torch_204188/README.md) | `torch.distributed.checkpoint.save`<br>`torch.distributed.checkpoint.DefaultSavePlanner` | enable_plan_caching=True，兩次 save 只有 dtype 由 bf16 變 fp16時，仍記錄 bf16，無 cache 控制組正確。 | `training_state` / `wrong_metadata` | [GitHub](https://github.com/pytorch/pytorch/issues/204188) |
| [#204269](training_state/incorrect_state/torch_204269/README.md) | `torch.nn.utils.clip_grad_norm_`<br>`torch.nn.utils.get_total_norm` | A pair of gradient tensors with three nonzero elements returns a total 0-norm of two. | `training_state` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/204269) |
| [#204339](training_state/incorrect_state/torch_204339/README.md) | `torch.optim.Adam`<br>`torch._dynamo.graph_break`<br>`torch.compile` | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | `training_state` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/204339) |
| [#204407](tensor_representation/wrong_gradient/torch_204407/README.md) | `torch.linalg.slogdet`<br>`torch.Tensor.conj`<br>`torch.Tensor.imag` | A=z.conj().imag，negative view、stride=(4,2)、offset=1時，off-diagonal gradient 轉置，real gradient 仍零。 | `tensor_representation` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/204407) |
| [#204426](tensor_representation/wrong_gradient/torch_204426/README.md) | `torch.compile`<br>`torch.no_grad`<br>`torch.Tensor.view` | Compiled autograd connects a view created under no_grad back to its input, producing gradient [2,3,3,3] where eager produces [2,2,2,2]. | `tensor_representation` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/204426) |
| [#204442](tensor_representation/wrong_forward_value/torch_204442/README.md) | `torch.add` | CSR 輸入搭配 CSC out 的 layout 未檢查，回傳轉置的錯誤結果。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/204442) |
| [#204446](tensor_representation/wrong_forward_value/torch_204446/README.md) | `torch.Tensor.add_`<br>`torch.sparse_coo_tensor` | 對 base[1] 的 contiguous 非零 offset view 加 COO時，錯改 row 2。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/204446) |
| [#204478](training_state/wrong_gradient/torch_204478/README.md) | `torch.nn.functional.layer_norm`<br>`torch.autograd.grad` | A parameter gradient of a loss involving second input derivatives differs from an independent formula. | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/204478) |
| [#204544](training_state/unexpected_exception/torch_204544/README.md) | `torch.compile`<br>`torch.Tensor.backward` | 動態維度編譯後的 retained backward 誤判 donated buffer 不可重複使用。 | `training_state` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/204544) |
| [#204679](needs_review/wrong_forward_value/torch_204679/README.md) | `torch.prod` | AVX512 CPU 對 1000 個 BF16 129/128 求積時，本 build 回傳 1632。 | `needs_review` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/204679) |
| [#204825](training_state/wrong_gradient/torch_204825/README.md) | `torch.autograd.Function`<br>`torch.autograd.grad`<br>`torch.compile` | compiled custom Function 的可微 backward，再求二階導數時，只剩普通路徑的 1。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/204825) |
| [#204945](needs_review/unexpected_exception/torch_204945/README.md) | `torch.nn.Parameter`<br>`torch.compile` | compiled function 內建立 Parameter 後檢查 type(p)時，SYNTHETIC_LOCAL NameError／InternalTorchDynamoError。 | `needs_review` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/204945) |
| [#205112](tensor_representation/wrong_gradient/torch_205112/README.md) | `torch.func.jacrev`<br>`torch.cdist` | cdist(p=1) 的 jacrev 使用 batched cotangents時，各 Jacobian slice 重複第一個 cotangent 的結果。 | `tensor_representation` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/205112) |
| [#205134](training_state/missing_exception/torch_205134/README.md) | `torch.Tensor.apply_`<br>`torch.Tensor.detach` | 保存 x 後，對 detach alias 執行 apply_ 乘十時，版本不變，backward 靜默回傳 [20,40]。 | `training_state` / `missing_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/205134) |
| [#205497](tensor_representation/wrong_optimizer_update/torch_205497/README.md) | `torch.optim.SGD` | CPU fused=True，parameter 與 transposed gradient 的 stride 不同時，依 memory order 配對，形成置換的錯誤更新。 | `tensor_representation` / `wrong_optimizer_update` | [GitHub](https://github.com/pytorch/pytorch/issues/205497) |
| [#205616](tensor_representation/wrong_forward_value/torch_205616/README.md) | `torch.amax` | 零維 CPU tensor x=3，out=x時，輸出與 input 都被改為 -inf。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/205616) |
| [#205620](tensor_representation/wrong_forward_value/torch_205620/README.md) | `torch.linalg.solve_triangular` | A=diag(2,4)、B=diag(6,20)，out=A時，回傳 identity。 | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/205620) |
| [#205653](training_state/wrong_gradient/torch_205653/README.md) | `torch.hypot` | float64 x=3s,y=4s，incoming=1.25s，s=2**±600時，大 scale 為 inf，小 scale 為零。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/205653) |
| [#205654](training_state/wrong_gradient/torch_205654/README.md) | `torch.special.log_ndtr` | float64 負尾 x=-2**30、-2**35時，前者為極大錯值，後者為正無限。 | `training_state` / `wrong_gradient` | [GitHub](https://github.com/pytorch/pytorch/issues/205654) |
| [#205682](tensor_representation/incorrect_state/torch_205682/README.md) | `torch.cat`<br>`torch.Tensor.split`<br>`torch.compile` | 同正軸 cat 後按原長度 split，另有 mixed dtype 控制時，寫 split 修改 input；第一份 mixed output 留在 int32。 | `tensor_representation` / `incorrect_state` | [GitHub](https://github.com/pytorch/pytorch/issues/205682) |
| [#205823](needs_review/unexpected_exception/torch_205823/README.md) | `torch.nn.functional.linear`<br>`torch.compile` | freezing=True 且 enable_linear_binary_folding=True，乘 parameter reciprocal時，FX graph reciprocal use-before-definition 例外。 | `needs_review` / `unexpected_exception` | [GitHub](https://github.com/pytorch/pytorch/issues/205823) |
| [#206126](tensor_representation/wrong_forward_value/torch_206126/README.md) | `torch.linalg.lu_solve` | LU factor aliases the out argument and yields a large residual while independent/rhs output are correct. | `tensor_representation` / `wrong_forward_value` | [GitHub](https://github.com/pytorch/pytorch/issues/206126) |

## 來源與目前版本

原始批次於 2026-11-23 取得並讀取 100 個 Issue 內文與頁面載入的討論；不是只存 URL，也不聲稱完整讀取所有分頁或獨立驗證上游修補。 來源核對沒有聲稱已驗證上游 patch；沒有完整根因說明時在各案標示 `Root cause not confirmed`。

```text
{
  "python": "3.14.10 (main, Nov 11 2026, 00:18:44) [Clang 23.1.3 ]",
  "python_executable": "/home/shuan/mirage-benchmark-playground/.venv/bin/python",
  "torch": "2.15.0+cpu",
  "torch_git": "d0f2af8b66b20da4baa50644c0cd3f887a2eae2e",
  "pytest": "9.0.1",
  "platform": "Linux-7.3.5-arch1-1-x86_64-with-glibc2.44",
  "cpu_capability": "AVX512",
  "cache": "/tmp/vscode-agent-codex-sandbox-yUIInk/torchinductor_shuan",
  "compilers": {
    "gcc": "gcc (GCC) 16.2.1 20260810",
    "g++": "g++ (GCC) 16.2.1 20260810",
    "clang": "not available",
    "cmake": "not available"
  }
}
```

## 驗證

Batch 01 v4 全套驗證：99 passed、1 failed、7 warnings；#203866 在 Gloo 初始化時無法解析本機 loopback 位址。

Batch 02 安裝記錄：5 個替換案各通過十次獨立執行，3 個舊案保留於 needs_review。

Batch 02 目錄同步全套驗證：99 passed、1 failed、6 warnings。#203866 在 Gloo 初始化時無法解析本機 loopback 位址。

### 歷史搬移相容性驗證

原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

| 階段 | 結果 | 執行秒數 |
| --- | --- | ---: |
| 原始結構 | 100 passed，7 warnings，0 failed／skipped／timeout | 41.98 |
| 暫存新結構 | 100 passed，7 warnings，0 failed／skipped／timeout | 8.25 |
| 正式新結構 | 100 passed, 7 warnings，0 failed／skipped／timeout | 7.42 |

每次批次 timeout 1200 秒，使用新 Python 程序，但既有 compiler cache 可重用，沒有清除案例需要的暖機／狀態。`PYTHONDONTWRITEBYTECODE=1` 用於避免改寫既有 pyc；測試與 metadata 不變。

歷史搬移驗證未觀察到新路徑使任何案例失去原錯誤簽名；這是指定 build 與 importlib 整批模式的結論，不宣稱所有 import modes 都等價。歷史路徑敏感案例 #205991 目前不在資料集，沒有被補回或計入。

從專案根目錄執行：

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/
```

## 執行工具與文件

- [run.sh](../run.sh) 從 repository 根目錄執行，動態尋找現有案例；預設與 `all` 執行全套，`one ISSUE_ID` 執行單案，並保留 `--import-mode=importlib`。
- [tools/validate_metadata.py](../tools/validate_metadata.py) 預設遞迴掃描 metadata，確認 100 個唯一案例各有測試與 metadata，再驗證 Schema v1；可透過 `./run.sh verify` 執行。原 metadata 分類不改寫，新的 Cause／Observation 以 Excel 與本目錄為準。
- [tools/run_isolated_test.sh](../tools/run_isolated_test.sh) 保留作為選用的 bubblewrap 隔離診斷工具；其掛載路徑、匯入環境與 timeout 不同，不能代替標準驗收入口。
- [根目錄 README](../README.md) 統一說明環境、執行方式與限制。歷史審核報告與批次產物已移除，可從 Git 歷史查閱；不建立可能造成重複收集的舊路徑 symlink。

```bash
# 從 repository 根目錄執行
./run.sh all
./run.sh one 205134
./run.sh verify
```

## 已知限制與人工決策

- 20 個 needs_review 多為已知數值／Python／一般 compiler 機制，需決定是否納入 Mirage 的兩個主要研究範圍；不等於未復現。
- #197084 與 #198118 有共根因線索；#202966 在同一 Issue 包含兩個機制。保留一 Issue 一 Case，獨立根因計數另待政策。
- #198669 與外部 #196743、#201947 與 umbrella #203520、#204446 與 #59101 的關係均保留在各案限制；沒有把關聯全部當成確定重複。
- #197092、#198851、#198868、#202364、#202726、#204181、#204339 缺完整根因確認；分類依已知觸發機制，標為 medium。
- #198155 dtype 擴充、#203852 alpha 驗證、#205616／#205620 out-alias 支援或明確拒絕，需要區分本機差異與上游契約決策。
- #198183、#204679 有 CPU 向量化／ISA 限制；#199350 有 build-specific 內部 traceback identity 檢查；#204945 保留原較寬的外層例外捕捉。分類工作沒有修正這些測試。
- 全部 metadata 目前仍是 review=pending 並記錄既有 10/10；沒有將這些欄位視為本次獨立品質認證。

## 保存與完整性

目前共有 100 個唯一 Issue，每案的測試、metadata 與逐案 README 均保留。替換前的版本可從 Git 歷史查閱。
