#!/usr/bin/env bash
# Usage: bash run.sh BATCH [RUNS]; historical batch runner, not Phase 1.
set -u
cd "$(dirname "$0")"
BATCH="${1:-}"
RUNS="${2:-1}"
if [[ $# -gt 2 ]] || ! [[ "$RUNS" =~ ^[1-9][0-9]*$ ]]; then
  echo 'Usage: bash run.sh {04|05|06|07|08|09} [positive_runs]' >&2
  exit 2
fi
case "$BATCH" in
  04) issues=(199211 198102 202806 197887 198119 200229 198484 203485 204679 200444 197092 198095 195451 194347 198134 198851 197097 199350 204825) ;;
  05) issues=(205620 205616 204181 202967 201082 197811 197893 198070 198057 197895 197894 198183) ;;
  06) issues=(205682 202966 196596 202482 198118 199571 198072 198189 198190 198192 198052 205823 202726) ;;
  07) issues=(205112 199941 200572 197716 197810 198669 197087 199214 199920 198056 198155 202862 194593 203927 192639) ;;
  08) issues=(197889 198624 201970 199215 187806 197084 197089 201649 203852 198994 198868 198852 200600 198081 197399) ;;
  09) issues=(202526 198064 198077 197896 205991 203806 200053 203565 201947 193757 199258 200524 198071 199644 200924) ;;
  *) echo 'Usage: bash run.sh {04|05|06|07|08|09} [positive_runs]' >&2; exit 2 ;;
esac
if [[ -x .venv/bin/python ]]; then PYTHON=.venv/bin/python; else PYTHON=python; fi
mkdir -p "reports/batch${BATCH}"
for issue in "${issues[@]}"; do
  passed=0
  echo "===== #$issue ====="
  for ((i=1; i<=RUNS; i++)); do
    log="reports/batch${BATCH}/${issue}_run${i}.log"
    if timeout 180s "$PYTHON" -m pytest -q --import-mode=importlib "bugs/torch_${issue}/test_bug.py" >"$log" 2>&1; then
      passed=$((passed + 1))
      echo "  Run $i: PASS"
    else
      status=$?
      echo "  Run $i: FAIL (exit $status) — $log"
    fi
  done
  echo "  Result: $passed/$RUNS"
done
