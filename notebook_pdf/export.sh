#!/usr/bin/env bash
# Checks a notebook and, if it has no errors, exports it to a PDF next to it.
# Usage: notebook_pdf/export.sh path/to/notebook.ipynb
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python="${NOTEBOOK_PYTHON:-$here/../venv_autoeda/bin/python}"
notebook="$(realpath "$1")"

"$python" "$here/check.py" "$notebook"
cd "$(dirname "$notebook")"
"$python" -m jupyter nbconvert --config "$here/config.py" "$(basename "$notebook")"
