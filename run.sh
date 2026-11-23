#!/usr/bin/env bash
# Run from the repository root without changing case paths or pytest rootdir.
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_root"
export PYTHONDONTWRITEBYTECODE=1
python=.venv/bin/python
usage() { echo 'Usage: ./run.sh [all | one ISSUE_ID | verify]' >&2; }
[[ -x "$python" ]] || { echo 'Missing .venv/bin/python; restore the project environment first.' >&2; exit 2; }
case "${1:-all}" in
  all)
    (( $# <= 1 )) || { usage; exit 2; }
    exec timeout --kill-after=10s 1200s "$python" -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/
    ;;
  one)
    [[ $# == 2 && "$2" =~ ^[1-9][0-9]*$ ]] || { usage; exit 2; }
    mapfile -d '' -t matches < <(find bugs -type f -path "*/torch_${2}/test_bug.py" -print0)
    [[ ${#matches[@]} == 1 ]] || { echo "Expected exactly one test for Issue $2; found ${#matches[@]}." >&2; exit 2; }
    exec timeout --kill-after=10s 240s "$python" -m pytest -q -p no:cacheprovider --import-mode=importlib "${matches[0]}"
    ;;
  verify)
    [[ $# == 1 ]] || { usage; exit 2; }
    exec "$python" tools/validate_metadata.py
    ;;
  *) usage; exit 2 ;;
esac
