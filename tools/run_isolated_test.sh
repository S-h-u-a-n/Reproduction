#!/usr/bin/env bash
# Run one reviewed test file with no network or host home-directory access.
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
test_file="$(realpath -- "${1:?usage: bash tools/run_isolated_test.sh TEST_FILE}")"
runtime_dir="$(dirname -- "$(dirname -- "$(readlink -f -- "$project_root/.venv/bin/python")")")"
# The existing venv points at this interpreter alias. Mount only its runtime.
runtime_alias="$(dirname -- "$(dirname -- "$(readlink -- "$project_root/.venv/bin/python")")")"
exec timeout 60s bwrap \
  --unshare-all --die-with-parent --new-session --cap-drop ALL \
  --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib /lib64 \
  --ro-bind "$runtime_dir" "$runtime_alias" \
  --ro-bind "$project_root/.venv" /venv \
  --ro-bind "$test_file" /case/test_bug.py \
  --proc /proc --dev /dev --tmpfs /tmp --dir /work --chdir /work \
  --clearenv --setenv PATH /usr/bin --setenv HOME /tmp \
  --setenv OMP_NUM_THREADS 1 --setenv MKL_NUM_THREADS 1 \
  --setenv PYTEST_DISABLE_PLUGIN_AUTOLOAD 1 \
  -- /venv/bin/python -I -B -m pytest -q -p no:cacheprovider /case/test_bug.py
