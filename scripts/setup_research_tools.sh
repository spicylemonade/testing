#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WITH_CALIBRATION="${1:-}"

python3 -m venv "$ROOT_DIR/.venv"
source "$ROOT_DIR/.venv/bin/activate"

python -m pip install --upgrade pip

if [[ "$WITH_CALIBRATION" == "--with-calibration" ]]; then
  python -m pip install -e "$ROOT_DIR[calibration]"
else
  python -m pip install -e "$ROOT_DIR"
fi

python - <<'PY'
from importlib.util import find_spec

modules = ["numpy", "scipy", "pandas", "matplotlib", "seaborn", "pytest", "rebound"]
missing = [name for name in modules if find_spec(name) is None]
if missing:
    raise SystemExit(f"Missing expected packages after setup: {missing}")
print("Research environment ready.")
PY
