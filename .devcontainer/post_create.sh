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

# Markers for autograder
log "LAB4_POST_CREATE_START"
log "LAB4_DEVCONTAINER_OK"
python --version >> "$LOG_FILE" 2>&1 || true
pip --version   >> "$LOG_FILE" 2>&1 || true

# Deep health check (blocks if unhealthy)
python .devcontainer/health_check.py --deep || {
  echo
  echo "[Lab 4] Devcontainer health check FAILED."
  echo "See /workspace/logs/DEVCONTAINER_STATUS.txt and /workspace/logs/devcontainer_health.log"
  echo
  log "LAB4_POST_CREATE_HEALTH_FAIL"
  exit 1
}

# Echo installed requirements for rubric convenience
log "LAB4_REQUIREMENTS_SNAPSHOT_BEGIN"
pip freeze >> "$LOG_FILE" 2>&1 || true
log "LAB4_REQUIREMENTS_SNAPSHOT_END"

log "LAB4_POST_CREATE_END"
