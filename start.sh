#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv-linux"
PYTHON="$VENV/bin/python"
UVICORN="$VENV/bin/uvicorn"

if [ ! -f "$PYTHON" ]; then
  echo "ERROR: virtualenv not found at $VENV" >&2
  echo "Run: poetry install" >&2
  exit 1
fi

cleanup() {
  echo ""
  echo "Shutting down…"
  kill "$API_PID" "$UI_PID" 2>/dev/null
  wait "$API_PID" "$UI_PID" 2>/dev/null
  exit 0
}
trap cleanup SIGINT SIGTERM

echo "Starting WealthShield API on http://0.0.0.0:8000 …"
PYTHONPATH="$SCRIPT_DIR/api" "$UVICORN" main:app \
  --host 0.0.0.0 --port 8000 \
  --log-level warning &
API_PID=$!

echo "Starting WealthShield UI  on http://127.0.0.1:8550 …"
PYTHONPATH="$SCRIPT_DIR/src" "$PYTHON" -m marketresearch.main &
UI_PID=$!

echo ""
echo "App running at http://127.0.0.1:8550"
echo "Press Ctrl+C to stop."
echo ""

wait "$API_PID" "$UI_PID"
