#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="/workspace/logs/lab4_devcontainer.log"
mkdir -p /workspace/logs
touch "$LOG_FILE"

now_iso() {
  python - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat().replace("+00:00","Z"))
PY
}

log() { printf '%s ts=%s\n' "$1" "$(now_iso)" >> "$LOG_FILE"; }

log "LAB4_POST_START_BEGIN"

# Non-blocking health check each start
python .devcontainer/health_check.py || true

# Show banner once per session if present
if [ -f "/workspace/logs/DEVCONTAINER_STATUS.txt" ]; then
  echo
  cat /workspace/logs/DEVCONTAINER_STATUS.txt || true
  echo
fi

log "LAB4_POST_START_END"
