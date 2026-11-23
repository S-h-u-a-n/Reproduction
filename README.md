# Mirage PyTorch Benchmark

大學研究用的 PyTorch 已知錯誤 reproducer，研究 tensor representation 與 training state。目前有 **100 個案例**；分類與逐案來源見 [案例目錄](bugs/README.md) 及 [Excel Catalog](Mirage_Bug_Catalog.xlsx)。

## 系統與環境

指定環境：Linux / Arch x86-64、Python **3.14.10**、PyTorch **2.15.0+cpu**、pytest **9.0.1**，使用專案 `.venv/bin/python`。目前 PyTorch git build 為 `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`；CPU capability 為 AVX512，GCC/G++ 16.2.1。編譯案例需要可用的 C++ compiler；NumPy 等依賴沿用既有環境。執行入口需要 Bash、GNU findutils 與 coreutils（timeout）。

本 repository 沒有鎖定完整依賴的安裝清單，因此不能宣稱在全新電腦一條 pip 指令即可重建相同 build。現有環境不需重新安裝；若 `.venv` 缺失，請先取得研究者核定的 interpreter 與相符 wheel／依賴清單，不要自動安裝最新版。Git 不保存虛擬環境。

```bash
cd /home/shuan/mirage-benchmark-playground
source .venv/bin/activate   # 可選；run.sh 本身使用指定的 .venv/bin/python
.venv/bin/python -c 'import sys, torch, pytest; print(sys.version); print(torch.__version__, torch.version.git_version); print(pytest.__version__); print(torch.backends.cpu.get_cpu_capability())'
```

## 專案結構

| 路徑 | 用途 |
| --- | --- |
| [bugs/](bugs/) | `Cause/Observation/torch_<id>/`，含原測試、metadata 與逐案 README；路徑及內容不得因整理而改動。 |
| [Mirage_Bug_Catalog.xlsx](Mirage_Bug_Catalog.xlsx) | API、Issue、統計公式與分類定義。 |
| [run.sh](run.sh) | 全套、單案與格式／案例完整性驗證入口。 |
| [tools/validate_metadata.py](tools/validate_metadata.py) | 遞迴驗證既有 Schema v1；預設確認 100 個唯一案例各有測試及 metadata。 |
| [tools/run_isolated_test.sh](tools/run_isolated_test.sh) | 保留的 bubblewrap 隔離診斷工具；不是標準驗收入口，限制見下方。 |
| [AGENTS.md](AGENTS.md) | Agent 的資料保存與執行規範。 |

## 執行全部或單一案例

```bash
./run.sh                    # 全部案例，等同 all
./run.sh all
./run.sh one 205134
./run.sh verify
```

`run.sh` 無論從哪裡呼叫都先切回 repository 根目錄，再動態尋找現有案例，不使用歷史 batch ID 清單。沒有 Python fallback，不變更套件、案例、metadata、compiler cache 或 pytest rootdir；保留 `--import-mode=importlib`，避免同名 test_bug.py 衝突。停用 pytest cache 與 bytecode 寫入，輸出直接顯示在 terminal。

全套 timeout 為 1200 秒，單案 240 秒，逾時後最多再給 10 秒終止。pytest 失敗與 timeout 會以非零 exit code 傳回；skip 或沒有收集到測試都不能當作復現成功。`verify` 只驗證檔案配對、唯一性與 metadata schema，不證明錯誤特徵有效，也不做跨版本認證。

等價的完整 pytest 命令（避免改寫既有 pyc）：

```bash
export PYTHONDONTWRITEBYTECODE=1
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/
```

## 十次獨立復現

下面每輪由 `run.sh one` 啟動新的 Python／pytest process；不把十輪放在同一 Python interpreter。任何失敗會停止迴圈，仍須確認每輪實際輸出為 `1 passed`，不能只看 exit code 將 skip 算成成功。

```bash
for run in {1..10}; do
    echo "Run $run/10"
    ./run.sh one 205134 || break
done
```

保留每個 testcase 自己的暖機、呼叫順序、快取及 backward 歷史。新程序可以重用 compiler disk cache，**十次新程序不等於十次冷編譯**。若需保存日誌，可導向 `/tmp`；不把暫存輸出當成新 review 報告，不自動更新 metadata 中的 runs/passes。

## PASS 的意義與限制

測試的設計用途是辨識已知錯誤：PASS 代表既有斷言通過，不代表 PyTorch 正確、根因已獨立確認、每個上游變體都已測過或 Mirage 已接入。metadata 的歷史 10/10 與 review=pending 不等於新的品質認證；Issue 數也不等於獨立根因數。

本次整理前後都執行指定 importlib 全套，結果均為 **100 passed、7 warnings**。100 個案例、整個 bugs 目錄的 416 個既有檔案路徑及 SHA-256 保持不變；沒有重新做全案十次復現。

## 特殊條件

- 不更動 module name、import path 或 rootdir。歷史 #205991 曾因匯入命名空間改變而改變結果，目前不在這 100 案中；其教訓仍適用。
- #198057、#198134、#198183、#204679 有 CPU 向量化限制；尤其 #204679 的精確錯值不能外推到其他 ISA、CSR 或 float16。
- #197889、#200925、#201970、#204188 依賴案例內呼叫／cache／saved-state 歷史，不可只抽出最後一個操作或任意清 cache。
- #205134 修改 saved tensor 後的正確契約是 version counter 衝突報錯；未修改控制的 [2,4] 不是修改後的合法梯度。
- #204407 必須保留 negative view、stride、offset 及鏈式法則；#199350 依賴指定 build 的內部 operator identity。
- #197084／#198118 有共根因線索；#202966 含不同機制。Needs Review 可能是研究收錄範圍待決，不一定無法復現。細節以各案 README 為準。

舊 bubblewrap 工具會把單檔掛載為 `/case/test_bug.py`、改變 cwd／匯入環境、限制執行緒並使用 60 秒 timeout；不能拿它替代上述 rootdir-sensitive 驗收。保留它是為了既有唯讀、斷網診斷用途，本次只檢查 shell 語法，未將其結果算入 100/100。

歷史審核報告、批次日誌、提案與 manifests 已從工作樹移除，Git 歷史仍可查閱。執行方式以本頁為準，分類與逐案說明見 [案例目錄](bugs/README.md)。文件更新不改動案例測試、metadata 或既有快取，也不建立新備份或 archive。`.agents/`、`.codex/`、`.aws/` 在清理盤點時均為空目錄，保留原狀；不讀取憑證內容。忽略規則不會自動移除已被追蹤的 pyc。
