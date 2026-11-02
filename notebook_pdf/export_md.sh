#!/usr/bin/env bash
# Exports a Markdown file to a PDF next to it, with the same fonts as the notebooks.
# Usage: notebook_pdf/export_md.sh path/to/file.md
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
markdown="$(realpath "$1")"

cd "$(dirname "$markdown")"
pandoc "$(basename "$markdown")" -o "$(basename "${markdown%.md}").pdf" \
  --from markdown+lists_without_preceding_blankline --pdf-engine=xelatex \
  --lua-filter="$here/anchos.lua" \
  -V geometry:margin=2.5cm -V lang=es \
  -H "$here/fuentes.tex" -H "$here/markdown.tex"
