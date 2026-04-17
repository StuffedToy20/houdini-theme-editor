#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="${SCRIPT_DIR}/hcs_theme_editor.py"

if [[ ! -f "${SCRIPT_PATH}" ]]; then
  echo "Could not find hcs_theme_editor.py next to this launcher."
  exit 1
fi

if [[ -n "${HCS_THEME_EDITOR_PYTHON:-}" && -x "${HCS_THEME_EDITOR_PYTHON}" ]]; then
  exec "${HCS_THEME_EDITOR_PYTHON}" "${SCRIPT_PATH}" "$@"
fi

if [[ -x "${SCRIPT_DIR}/.venv/bin/python" ]]; then
  exec "${SCRIPT_DIR}/.venv/bin/python" "${SCRIPT_PATH}" "$@"
fi

if command -v python3 >/dev/null 2>&1; then
  exec python3 "${SCRIPT_PATH}" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "${SCRIPT_PATH}" "$@"
fi

echo "Python 3 was not found."
echo "Install Python 3, or set HCS_THEME_EDITOR_PYTHON to a Python executable path."
exit 1
