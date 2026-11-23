# PyTorch reproducer 品質審核

更新：2026-11-23。100 個案例各列一次；本報告取代舊的重複批次及 30 VERIFIED / 11 AUTO_FIXED / 59 MANUAL 標籤。這些歷史標籤不是獨立有效性認證。pytest PASS 表示測試辨識到已知錯誤，**不是 PyTorch 正確、人工核准或 Mirage 已接入**。

## 範圍與實際環境

已逐案閱讀現有 100 份測試及可用的 97 份 metadata，對照前次摘要，補齊 #201633、#203946、#204446 缺失的 metadata。保留 Schema v1；沒有新增逐案 README 或第二份報告。未更動套件、PyTorch 原始碼或套用掩蓋行為的 monkeypatch。測試既有 #201970 的 monkeypatch fixture 只隔離編譯快取環境變數。

`git status` 回報 not a git repository（工作區未提供可用 Git 索引），因此無法聲稱乾淨工作樹或提供 Git diff。以工作前暫存副本比對變更；沒有 reset、checkout、commit 或 push。先前沙箱重建造成暫存資料消失，因此本報告只計入重建後重新執行的結果。

- Python：`3.14.10 (main, Nov 11 2026, 00:18:44) [Clang 23.1.3 ]`；路徑 `/home/shuan/mirage-benchmark-playground/.venv/bin/python`。
- PyTorch：`2.15.0+cpu`；`torch.version.git_version=d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- pytest `9.0.1`；NumPy `2.5.5`；平台 `Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`。
- CPU：AMD Ryzen 7 8845H、8 cores / 16 logical CPUs；PyTorch CPU capability `AVX512`。其他 SIMD 能力未做相容性驗證。
- 本機 GCC/G++ `16.2.1 20260810`；無可用 clang 命令。Python 的建置標籤為 Clang 23.1.3，不等同本機存在 clang。PyTorch 建置編譯器 GCC 13.3、C++202002、MKL2024.2、MKL-DNN3.13.3、OpenMP201511；CPU-only。

## 驗證方法與統計

每個隔離程序只跑一個案例，保留案例內暖機、呼叫順序、Dynamo reset 與 retained backward。每個隔離批次最多四個 worker；部分獨立批次及診斷同時執行，單程序 timeout 240 秒；整批 timeout 1200 秒。環境固定 `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`、`PYTHONDONTWRITEBYTECODE=1`、`OMP_NUM_THREADS=1`、`MKL_NUM_THREADS=1`、`TORCHINDUCTOR_COMPILE_THREADS=1`，停用 pytest cacheprovider。

compiler cache 在各新程序間重用：`TORCHINDUCTOR_CACHE_DIR=/tmp/mirage-quality/inductor`、`TRITON_CACHE_DIR=/tmp/mirage-quality/triton`、`XDG_CACHE_HOME=/tmp/mirage-quality/cache`、`TMPDIR=/tmp/mirage-quality/tmp`。#201970 以 fixture 另開每次測試快取；不能把整體十次新程序描述成十次冷編譯。暫存診斷檔不納入專案交付，也不是另一份 review 報告。

命令（`PY` 指上列 interpreter；逾時由外層 driver 終止整個程序群組）：

```sh
$PY -m pytest -q -p no:cacheprovider --junitxml=<temp.xml> bugs/torch_<id>/test_bug.py
$PY -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/
$PY -m pytest -q -p no:cacheprovider bugs/
```

| 階段 | 程序嘗試 | PASS | FAIL | 收集/其他不確定 | skip（測試） | timeout |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 100 | 100 | 0 | 0 | 0 | 0 |
| fixed | 46 | 43 | 3 | 0 | 0 | 0 |
| corrected | 3 | 3 | 0 | 0 | 0 | 0 |
| final_extra | 7 | 7 | 0 | 0 | 0 | 0 |
| repeat | 990 | 990 | 0 | 0 | 0 | 0 |
| repeat_extra | 60 | 60 | 0 | 0 | 0 | 0 |
| importlib | 1 | 1 | 0 | 0 | 0 | 0 |
| batch_default | 1 | 0 | 0 | 1 | 0 | 0 |
| batch | 1 | 1 | 0 | 0 | 0 | 0 |
| batch_original | 1 | 0 | 1 | 0 | 0 | 0 |
| batch_final | 1 | 1 | 0 | 0 | 0 | 0 |
| batch_config | 1 | 0 | 1 | 0 | 0 | 0 |
| batch_class | 1 | 0 | 1 | 0 | 0 | 0 |
| batch_oldclass | 1 | 0 | 1 | 0 | 0 | 0 |
| batch_copy | 1 | 0 | 1 | 0 | 0 | 0 |
| repeat_importlib | 10 | 10 | 0 | 0 | 0 | 0 |
| batch_acceptance | 1 | 1 | 0 | 0 | 0 | 0 |

目前 **100 個案例完成最終版本十次隔離復現**。基線 100/100 PASS 只證明原斷言通過，不能消除原有誤判風險。`fixed` 的三次失敗是收緊斷言初稿：#197399 外層實際為 IndexError、#199215 內層文字不含 complex、#199350 文字未包含算子名。已按實際例外鏈/算子身份修正，`corrected` 三案均通過。沒有將這三次失敗刪除或算成復現成功。

`repeat` 保留修訂前 #197895/#198057/#198183 及 #187806/#197089 各十次的歷史嘗試；這五案及後來修妥的 #197084 以 `repeat_extra` 的最終十次計算，不能重複計數。metadata verification.runs/passes **只記錄最終版本的隔離重複階段**，其餘嘗試在本報告分列；review 統一 pending，代表本次修訂尚未人工核准，不是舊成果無效。

`batch` 是最後兩個數值控制加強前的整批，`batch_final` 是 99 案重複完成後的整批，`batch_acceptance` 是 #205991 調查及所有最終重複完成後的整批；`batch_original` 是修改前副本的診斷；`batch_config/class/oldclass/copy` 是交叉替換與原樣複製診斷，均不混入最終十次計數。整批與隔離結果分開：預設 pytest import mode 在收集階段因各目錄同名 test_bug 模組而發生 99 個 import-file-mismatch，沒有執行任何測試。這是收集不相容，不算 99 個未復現，更不能算成功。importlib 結果如下；不使用預設模式失敗來掩蓋 importlib 的實際執行結果。

完整 importlib 整批：tests=100, passed=100, failures=0, errors=0, skipped=0, timeout=False；耗時 10.14 秒。

## 修改摘要與 AUTO_FIXED 複查

共 52 個案例修改測試或補資料（完整對應在下表）；所有 100 份 metadata 同步本輪實測計數。重點：

- 例外案例同時辨識目標操作、外層類別及具辨識力的內層原因，移除任意 Exception 與普通關鍵字 OR。#199350 用 traceback 的 operator identity 補足訊息未帶算子名；#202862 限定 guard 生成位置，未鎖路徑/行號。
- 數值案例改為解析參考、完整錯值模式及獨立控制；#197084/#198118 用缺共軛公式，#202482 用覆寫 buffer 模型，#202526 用 2*BN(h)，#202966 用跨批次自由度項及梯度斷開。
- #205134 的未修改梯度 [2,4] 僅是控制；修改後的正確行為是版本增加並報錯。#204407 確認 negative-view、alias、stride/offset，分清局部 A^-T 與 z.grad.imag=-A^-T。
- #199644 恢復全域 capture_scalar_outputs；#205991 恢復類別屬性，但保留目標函式及必要前置呼叫。
- 舊 AUTO_FIXED 的 11 案均複查：#197087 移除 GCC 特定診斷文字、#198057 補必要子模式與範圍、#198155 移除整段固定引號格式、#205654 改取消誤差公式、#205823 不鎖完整生成名稱。#198192、#198851、#199258、#201649、#201970、#205112 保留必要控制與既有精確模式；沒有刪去正確性斷言來換取通過。

## #205991：匯入命名空間調查

單案 default、單案 importlib、收集全部但只執行本案（99 deselected）都得到 compiled=0、eager=5、class K.n=5。另用同一模組定義的新程序交叉檢查 eager 前置呼叫有/無、capture_scalar_outputs 開/關：四組均為 output=0、K.n=5，故這兩個因素單獨不足以解釋歷史整批差異。這些是診斷，沒有改被測語意，也沒有計入十次正式重複。

診斷腳本曾因放在含 triton 快取資料夾的暫存目錄而遇到 Python namespace 遮蔽；使用 `python -P` 排除該腳本路徑後重跑。正式 pytest 子程序從專案目錄執行，沒有採用這個受污染的診斷結果。

已解釋差異：同一測試檔只改 `--rootdir=bugs` 即得到 `torch_205991.test_bug` 並回傳 5；專案根目錄得到 `bugs.torch_205991.test_bug` 並回傳 0。指定 build 的 [UserDefinedClassVariable.get_value_for_setattr](.venv/lib/python3.14/site-packages/torch/_dynamo/variables/user_defined.py:387) 明確對 `torch`、`torch.`、`torch_` 名稱回傳 None，採取另一個類別寫入處理路徑。這是匯入命名空間條件，不是已證實的隨機或快取不穩定。已將此條件寫入測試及 metadata；沒有改寫類別 __module__ 或將正確輸出 5 算作復現。原先 execution_sensitive 調查轉為 **namespace-scoped**。當前完整整批結果：PASS。

## 待辦分類

### A. Testcase 品質

本輪已處理發現且有依據的寬鬆例外、部分模式、缺控制與狀態洩漏。未宣稱每個測試涵蓋 Issue 的所有變體：#198057 只聲稱前五項，#198183 只聲稱兩個小輸入的所有重複區塊，其他輸入保留向量化觸發。預設整批 pytest 同名模組收集問題仍存在；目前已明列可用的 importlib 命令，沒有為此重命名百個檔案或改 pytest 配置。#205991 的匯入命名空間限制列 D，差異原因已定位。

### B. 需要收錄範圍或根因計數政策

需決定：(1) 是否收錄支援缺口、無效輸入驗證、Python 語意與 needs-design eager 契約；(2) 同根因的前向/反向與不同算子是否各計一案；(3) 是否擴展現有最小變體。下表 B 欄保留逐案具體問題。這些不是「復現無效」判定；未證實的根因連結只是待調查線索。

### C. 背景版本資訊

首個修復正式版本一律記為 **unknown**，本輪不為此無限追查。歷史報告中的候選 PR/commit 不等同已進入 wheel；尚未在其他版本驗證。這不阻擋針對本報告指定 git build 的局部復現。

### D. 不穩定、環境範圍、證據限制

- #205991：namespace-scoped。只在外部模組名稱下驗收；torch_* 根目錄匯入回傳正確 5、不復現。原因已定位，不能把這個未復現模式隱藏或算成 PASS。標準單案和專案根目錄 importlib 各十次另列。
- #198057/#198134/#198183/#204679 等向量化數值案例只驗證本機 CPU；#204679 的精確 1632 尤其不得泛化至其他 ISA、CSR 或 float16。
- #194593/#198624/#200053/#200444/#203927 等有支援或設計政策問題：可記錄穩定症狀，但是否稱為 Mirage 的 correctness bug 尚須 B 類決策。
- 來源核對使用現有摘要、測試及 metadata，必要時讀原 Issue/討論與指定 build 原始碼；沒有聲稱所有上游 PR 的最新狀態均重新查證。

### #205991 額外診斷結果（不混入正式十次）

| 診斷 | 嘗試 | 結果 |
|---|---:|---|
| 全收集只執行本案 | 1 | PASS；99 deselected |
| eager 前置呼叫有/無 × capture_scalar_outputs True/False | 4 | 全部 output=0、K.n=5 |
| 原副本只換 #199644；只換 #205991；現版換舊 #205991 | 各1 | 每批99 PASS、#205991 output=5 |
| 現版原樣複製到另一 root | 1 | 99 PASS、#205991 output=5；證明不能歸功於修復 |
| 觀察 plugin：專案單案、複本單案、專案整批、複本整批 | 各1 | PASS、PASS、100 PASS、99 PASS/本案 output=5 |
| 同一專案檔案加 --rootdir=bugs --import-mode=importlib | 1 | output=5，不復現；單案即可排除前案歷史因素 |

上述「不復現」是實際測試 FAIL，沒有 skip 或 timeout。正式 default-mode 十次在逐案表；專案根目錄 importlib 額外十次在 repeat_importlib 列，不能再算成另一個案例。原副本和交叉替換的路徑不同，不能直接推論修復因果；後續同一檔案改 rootdir 的控制才隔離出命名空間因素。

## 100 案唯一明細

最終隔離欄為「成功/嘗試」；基線全為 1/1。修復驗證欄另列本輪改動後嘗試的 P/F/S/T（成功/失敗/跳過/逾時）。十次成功僅指目前固定輸入與環境。C=首修版本 unknown，全案適用。

| Issue / 測試 | 最終隔離 | 修復驗證 P/F/S/T | importlib 整批 | 本輪修改或範圍；B/D 待辦 |
|---|---:|---|---|---|
| [#187806](https://github.com/pytorch/pytorch/issues/187806) / [test](bugs/torch_187806/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 加入scalar erfc獨立參考與完整負尾端非零控制 |
| [#192639](https://github.com/pytorch/pytorch/issues/192639) / [test](bugs/torch_192639/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制；B：與外部 #192629 的包裝路徑是否按同根因去重 |
| [#193757](https://github.com/pytorch/pytorch/issues/193757) / [test](bugs/torch_193757/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 明確範圍診斷；以BCE log(0)夾制-100的公式辨識錯值 |
| [#194347](https://github.com/pytorch/pytorch/issues/194347) / [test](bugs/torch_194347/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制；B：signed-zero 的 eager 相容性是否納入，而非跨函式庫一般契約 |
| [#194593](https://github.com/pytorch/pytorch/issues/194593) / [test](bugs/torch_194593/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；B：fullgraph 擷取缺口/enhancement 是否收錄；相關 #194596/#194764 |
| [#195451](https://github.com/pytorch/pytorch/issues/195451) / [test](bugs/torch_195451/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#196596](https://github.com/pytorch/pytorch/issues/196596) / [test](bugs/torch_196596/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 完整NaN錯值模式；B：目前只收錄 beta=0；是否另擴 alpha=0 |
| [#197084](https://github.com/pytorch/pytorch/issues/197084) / [test](bugs/torch_197084/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 解析完整正確梯度及缺少共軛保存值的VJP錯誤模型；B：與 #198118 同根因的梯度表現是否獨立計數；未擴 matrix_sqrth |
| [#197087](https://github.com/pytorch/pytorch/issues/197087) / [test](bugs/torch_197087/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 不依賴GCC診斷措辭，保留CppCompileError及生成式 |
| [#197089](https://github.com/pytorch/pytorch/issues/197089) / [test](bugs/torch_197089/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 補float64解析標準差與完整梯度控制 |
| [#197092](https://github.com/pytorch/pytorch/issues/197092) / [test](bugs/torch_197092/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；補完整 bilinear 梯度控制 |
| [#197097](https://github.com/pytorch/pytorch/issues/197097) / [test](bugs/torch_197097/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；補等價正維度編譯控制 |
| [#197399](https://github.com/pytorch/pytorch/issues/197399) / [test](bugs/torch_197399/test_bug.py) | 10/10 | 1/1/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；確認重綁的形狀、步幅、偏移與別名 |
| [#197716](https://github.com/pytorch/pytorch/issues/197716) / [test](bugs/torch_197716/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤 |
| [#197810](https://github.com/pytorch/pytorch/issues/197810) / [test](bugs/torch_197810/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；B：與舊 #131897 根因關係未證明，不能逕行合併 |
| [#197811](https://github.com/pytorch/pytorch/issues/197811) / [test](bugs/torch_197811/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#197887](https://github.com/pytorch/pytorch/issues/197887) / [test](bugs/torch_197887/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#197889](https://github.com/pytorch/pytorch/issues/197889) / [test](bugs/torch_197889/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 檢查四次呼叫完整 stale-shape 序列；B：與外部 #194976 快取根因是否合併 |
| [#197893](https://github.com/pytorch/pytorch/issues/197893) / [test](bugs/torch_197893/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#197894](https://github.com/pytorch/pytorch/issues/197894) / [test](bugs/torch_197894/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#197895](https://github.com/pytorch/pytorch/issues/197895) / [test](bugs/torch_197895/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 精確有理數floor參考及先除後floor的完整錯值模型 |
| [#197896](https://github.com/pytorch/pytorch/issues/197896) / [test](bugs/torch_197896/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198052](https://github.com/pytorch/pytorch/issues/198052) / [test](bugs/torch_198052/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 檢查完整截斷參考；補負半整數、dtype及負零；B：目前只涵蓋 np.fix |
| [#198056](https://github.com/pytorch/pytorch/issues/198056) / [test](bugs/torch_198056/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 完整cumsum參考；完整int8回繞模式 |
| [#198057](https://github.com/pytorch/pytorch/issues/198057) / [test](bugs/torch_198057/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 補前三項及兩個大商的完整子模式，明列padding範圍；D：僅本機CPU路徑 |
| [#198064](https://github.com/pytorch/pytorch/issues/198064) / [test](bugs/torch_198064/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198070](https://github.com/pytorch/pytorch/issues/198070) / [test](bugs/torch_198070/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198071](https://github.com/pytorch/pytorch/issues/198071) / [test](bugs/torch_198071/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 移除吞例外，確認目標版本 eager 語意；B：目前只涵蓋 int8 max=300；不能泛化版本 eager 行為 |
| [#198072](https://github.com/pytorch/pytorch/issues/198072) / [test](bugs/torch_198072/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198077](https://github.com/pytorch/pytorch/issues/198077) / [test](bugs/torch_198077/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198081](https://github.com/pytorch/pytorch/issues/198081) / [test](bugs/torch_198081/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198095](https://github.com/pytorch/pytorch/issues/198095) / [test](bugs/torch_198095/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198102](https://github.com/pytorch/pytorch/issues/198102) / [test](bugs/torch_198102/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制；B：目前非重疊 unfold；重疊變體未納入 |
| [#198118](https://github.com/pytorch/pytorch/issues/198118) / [test](bugs/torch_198118/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 以SVD遺漏共軛公式辨識完整錯值；B：與 #197084 合併根因或保留前向/梯度兩案例 |
| [#198119](https://github.com/pytorch/pytorch/issues/198119) / [test](bugs/torch_198119/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 完整視窗梯度分配參考與錯值 |
| [#198134](https://github.com/pytorch/pytorch/issues/198134) / [test](bugs/torch_198134/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 完整值及正無窮符號；D：僅本機CPU路徑 |
| [#198155](https://github.com/pytorch/pytorch/issues/198155) / [test](bugs/torch_198155/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 保留算子及dtype，不鎖完整引號格式 |
| [#198183](https://github.com/pytorch/pytorch/issues/198183) / [test](bugs/torch_198183/test_bug.py) | 10/10 | 1/0/0/0 | PASS | math.erf控制及所有重複區塊的兩個小輸入零值模式；D：僅本機CPU路徑 |
| [#198189](https://github.com/pytorch/pytorch/issues/198189) / [test](bugs/torch_198189/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198190](https://github.com/pytorch/pytorch/issues/198190) / [test](bugs/torch_198190/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制；B：目前只涵蓋直接回傳 generator |
| [#198192](https://github.com/pytorch/pytorch/issues/198192) / [test](bugs/torch_198192/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198484](https://github.com/pytorch/pytorch/issues/198484) / [test](bugs/torch_198484/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198624](https://github.com/pytorch/pytorch/issues/198624) / [test](bugs/torch_198624/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 補eager別名、數值與梯度；確認compiled前向正確但梯度歷史遺失；B：needs-design 的 eager alias/autograd 契約是否納入 |
| [#198669](https://github.com/pytorch/pytorch/issues/198669) / [test](bugs/torch_198669/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；B：與外部 #196743 改寫根因是否合併 |
| [#198851](https://github.com/pytorch/pytorch/issues/198851) / [test](bugs/torch_198851/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198852](https://github.com/pytorch/pytorch/issues/198852) / [test](bugs/torch_198852/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198868](https://github.com/pytorch/pytorch/issues/198868) / [test](bugs/torch_198868/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#198994](https://github.com/pytorch/pytorch/issues/198994) / [test](bugs/torch_198994/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#199211](https://github.com/pytorch/pytorch/issues/199211) / [test](bugs/torch_199211/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#199214](https://github.com/pytorch/pytorch/issues/199214) / [test](bugs/torch_199214/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；確認 dequantize 的必要別名語意；B：dequantize 路徑是否與 #136064/#178952 合併；根因仍需論證 |
| [#199215](https://github.com/pytorch/pytorch/issues/199215) / [test](bugs/torch_199215/test_bug.py) | 10/10 | 1/1/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；檢查整數參數及完整索引控制 |
| [#199258](https://github.com/pytorch/pytorch/issues/199258) / [test](bugs/torch_199258/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#199350](https://github.com/pytorch/pytorch/issues/199350) / [test](bugs/torch_199350/test_bug.py) | 10/10 | 1/1/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；補 eager 全值控制 |
| [#199571](https://github.com/pytorch/pytorch/issues/199571) / [test](bugs/torch_199571/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；加入右側複數求解的解析控制 |
| [#199644](https://github.com/pytorch/pytorch/issues/199644) / [test](bugs/torch_199644/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 離開測試時還原全域設定 |
| [#199920](https://github.com/pytorch/pytorch/issues/199920) / [test](bugs/torch_199920/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#199941](https://github.com/pytorch/pytorch/issues/199941) / [test](bugs/torch_199941/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 解析Vandermonde梯度；移除普通關鍵字OR；B：與外部 #60197 是否合併 |
| [#200053](https://github.com/pytorch/pytorch/issues/200053) / [test](bugs/torch_200053/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 一步RMSprop負二階動量的解析錯值；B：無效參數驗證/enhancement 是否收錄 |
| [#200229](https://github.com/pytorch/pytorch/issues/200229) / [test](bugs/torch_200229/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制；B：與 #197089 的數值極端案例是否分開；未證明同根因 |
| [#200444](https://github.com/pytorch/pytorch/issues/200444) / [test](bugs/torch_200444/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；B：巢狀 context_fn 支援/回退缺口是否收錄 |
| [#200524](https://github.com/pytorch/pytorch/issues/200524) / [test](bugs/torch_200524/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#200572](https://github.com/pytorch/pytorch/issues/200572) / [test](bugs/torch_200572/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#200599](https://github.com/pytorch/pytorch/issues/200599) / [test](bugs/torch_200599/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#200600](https://github.com/pytorch/pytorch/issues/200600) / [test](bugs/torch_200600/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#200924](https://github.com/pytorch/pytorch/issues/200924) / [test](bugs/torch_200924/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#201082](https://github.com/pytorch/pytorch/issues/201082) / [test](bugs/torch_201082/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#201633](https://github.com/pytorch/pytorch/issues/201633) / [test](bugs/torch_201633/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 依既有Schema補缺失Metadata，不補造歷史驗證 |
| [#201649](https://github.com/pytorch/pytorch/issues/201649) / [test](bugs/torch_201649/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#201947](https://github.com/pytorch/pytorch/issues/201947) / [test](bugs/torch_201947/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制；B：與外部 #203520 的溢位根因是否合併 |
| [#201970](https://github.com/pytorch/pytorch/issues/201970) / [test](bugs/torch_201970/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#202482](https://github.com/pytorch/pytorch/issues/202482) / [test](bugs/torch_202482/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 以被覆寫cat子視圖模型辨識完整錯值，增加獨立矩陣乘參考；B：與外部 #177821 是否按同根因計數 |
| [#202526](https://github.com/pytorch/pytorch/issues/202526) / [test](bugs/torch_202526/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 解析BN控制與完整雙重折疊錯值模式 |
| [#202726](https://github.com/pytorch/pytorch/issues/202726) / [test](bugs/torch_202726/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤 |
| [#202806](https://github.com/pytorch/pytorch/issues/202806) / [test](bugs/torch_202806/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#202862](https://github.com/pytorch/pytorch/issues/202862) / [test](bugs/torch_202862/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；B：直接 OpOverload 與 #198100/#198103 是否合併 |
| [#202965](https://github.com/pytorch/pytorch/issues/202965) / [test](bugs/torch_202965/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#202966](https://github.com/pytorch/pytorch/issues/202966) / [test](bugs/torch_202966/test_bug.py) | 10/10 | 1/0/0/0 | PASS | Wishart解析KL、跨批自由度誤加總及參數梯度斷開；B：目前同案檢查 KL 批次值及 p 梯度斷開；是否拆成兩根因 |
| [#202967](https://github.com/pytorch/pytorch/issues/202967) / [test](bugs/torch_202967/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#203078](https://github.com/pytorch/pytorch/issues/203078) / [test](bugs/torch_203078/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 從列總和加強為完整錯誤寫入張量 |
| [#203485](https://github.com/pytorch/pytorch/issues/203485) / [test](bugs/torch_203485/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 補密集上游梯度的解析控制；同時驗證步幅與尺寸 |
| [#203565](https://github.com/pytorch/pytorch/issues/203565) / [test](bugs/torch_203565/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 鎖定完整batch_sizes與資料列數；B：無效長度驗證是否收錄；與外部 #146744 的去重 |
| [#203806](https://github.com/pytorch/pytorch/issues/203806) / [test](bugs/torch_203806/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#203852](https://github.com/pytorch/pytorch/issues/203852) / [test](bugs/torch_203852/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 鎖定整數alpha型別控制；B：目前只測非整數值 alpha，未主張 2.0 的驗證政策 |
| [#203927](https://github.com/pytorch/pytorch/issues/203927) / [test](bugs/torch_203927/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 限定例外型別、目標操作及內層錯誤；補八次 VJP 的解析等比級數；B：cached VJP/while_loop 支援缺口是否收錄；相關 #172386/#193809 |
| [#203946](https://github.com/pytorch/pytorch/issues/203946) / [test](bugs/torch_203946/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 依既有Schema補缺失Metadata，不補造歷史驗證 |
| [#204181](https://github.com/pytorch/pytorch/issues/204181) / [test](bugs/torch_204181/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制；B：維持欄切片靜默錯寫範圍，未擴其他布局 |
| [#204407](https://github.com/pytorch/pytorch/issues/204407) / [test](bugs/torch_204407/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 驗證negative-view、偏移、局部梯度與鏈式法則 |
| [#204446](https://github.com/pytorch/pytorch/issues/204446) / [test](bugs/torch_204446/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 依既有Schema補缺失Metadata，不補造歷史驗證；B：僅三列、寫入仍在配置內的數值案例；未執行堆積損毀變體 |
| [#204679](https://github.com/pytorch/pytorch/issues/204679) / [test](bugs/torch_204679/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 60位十進位及float64參考，限定公開dense CPU錯值，不泛化到其他ISA；B：dense BF16/CSR/外部 #204045 是否分開；只驗證本機 AVX512 dense；D：僅本機CPU路徑 |
| [#204825](https://github.com/pytorch/pytorch/issues/204825) / [test](bugs/torch_204825/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制；B：與外部 #145231 是否共根因，未證實 |
| [#205112](https://github.com/pytorch/pytorch/issues/205112) / [test](bugs/torch_205112/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#205134](https://github.com/pytorch/pytorch/issues/205134) / [test](bugs/torch_205134/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 區分未修改梯度與修改後應報錯的契約，補mul_版本控制 |
| [#205497](https://github.com/pytorch/pytorch/issues/205497) / [test](bugs/torch_205497/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#205616](https://github.com/pytorch/pytorch/issues/205616) / [test](bugs/torch_205616/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#205620](https://github.com/pytorch/pytorch/issues/205620) / [test](bugs/torch_205620/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#205653](https://github.com/pytorch/pytorch/issues/205653) / [test](bugs/torch_205653/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#205654](https://github.com/pytorch/pytorch/issues/205654) / [test](bugs/torch_205654/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 以取消誤差公式取代本機錯值常數，保留Mills界正確性控制 |
| [#205682](https://github.com/pytorch/pytorch/issues/205682) / [test](bugs/torch_205682/test_bug.py) | 10/10 | 0/0/0/0 | PASS | 測試保留；核對現有模式及控制 |
| [#205823](https://github.com/pytorch/pytorch/issues/205823) / [test](bugs/torch_205823/test_bug.py) | 10/10 | 1/0/0/0 | PASS | 移除生成節點完整名稱限制，保留依賴順序特徵 |
| [#205991](https://github.com/pytorch/pytorch/issues/205991) / [test](bugs/torch_205991/test_bug.py) | 10/10 | 2/0/0/0 | PASS | 還原測試自身的類別狀態，保留被測函式與前置呼叫；同時檢查類別寫入副作用；定位torch_*匯入命名空間分支，保留不復現模式並檢查適用條件；B：Python 類別屬性語意是否屬 Mirage 主統計範圍；D：namespace-scoped（原因已定位） |

## 最終靜態驗證

100 份 metadata 通過既有 Schema v1 驗證；100 份測試通過 AST parse，編輯器沒有回報問題。與修改前副本比較：49 份既有 test_bug.py 修改、97 份既有 metadata 更新、3 份 metadata 補齊，另更新本報告；52 是測試修改或補資料的案例數，不將純驗證計數更新另算成新修復。所有最終隔離十次的 skip/fail/timeout 均為零；診斷與修復初稿失敗另列，不能抹除。

## 建議優先做 Mirage 接入實驗

先選解析參考清楚、必要觸發條件已檢查、沒有收錄語意爭議且完成十次的案例：#205134（保存張量版本）、#204407（negative-view 與梯度鏈式法則）、#203078（stride-zero 索引）、#200599（LU singleton stride）、#205497（optimizer 梯度布局）、#205112（完整 Jacobian 重複模式）。再選 #202482/#202526 做編譯 buffer/folding 類實驗。這只是接入優先順序；尚未實作 Mirage adapter、量測或根因去重統計。

主要補強依據：[197084 後續根因修正](https://github.com/pytorch/pytorch/issues/197084)、[指定 build pinv VJP](https://github.com/pytorch/pytorch/blob/d0f2af8b66b20da4baa50644c0cd3f887a2eae2e/torch/csrc/autograd/FunctionsManual.cpp#L2259)、[205134 版本契約](https://github.com/pytorch/pytorch/issues/205134)、[204407 negative-view](https://github.com/pytorch/pytorch/issues/204407)、[202966 Wishart](https://github.com/pytorch/pytorch/issues/202966)、[204679 dense BF16](https://github.com/pytorch/pytorch/issues/204679)、[205654 Mills/cancellation](https://github.com/pytorch/pytorch/issues/205654)、[205991 類別屬性](https://github.com/pytorch/pytorch/issues/205991)。其餘來源逐案見上表及 metadata.issue_url。
