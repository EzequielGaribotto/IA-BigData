# Notebook guidelines

Rules for every notebook in this repo that is delivered or exported to PDF. They apply from the first cell, not as a cleanup at the end.

## Workflow

1. Write the notebook following the rules below.
2. Restart the kernel and run it from top to bottom.
3. Check it and export it:

```bash
notebook_pdf/export.sh path/to/notebook.ipynb
```

This runs `check.py` first and only exports if there are no errors. The PDF is written next to the notebook. To check without exporting, run `venv_autoeda/bin/python notebook_pdf/check.py path/to/notebook.ipynb`. Set `NOTEBOOK_PYTHON` to use another environment.

If running a notebook overwrites something you want to keep, such as a saved model, run a copy in another folder and compare results first.

4. Read the PDF. The checker cannot judge the first two rules below or how a page looks.

To export a Markdown file, such as a results document, run `notebook_pdf/export_md.sh path/to/file.md`. It uses the same fonts and writes the PDF next to the file.

## Reading

- **No redundancy.** Text, images and annotations must add something the reader does not have yet. Do not explain a result that was already known or could be inferred from earlier analysis, even if the exact number is new. State each finding once, where it is analysed. No closing summary that repeats the sections.
- **Top to bottom.** Never point to a later section. Put the content where it belongs, or remove the sentence. Pointing back is allowed but keep it rare. No section-by-section index at the top: one sentence on what the notebook covers is enough.

## Structure

- Name the file and write the title after what the notebook does, for example `clasificacion_iris_knn.ipynb`, never after an exercise number. To mention another notebook, describe it by its topic.
- One `#` title. Sections are `## N.` and subsections `### N.M.`, numbered in sequence from 0 or 1. Do not skip levels.
- Put imports, display options, paths and helpers in the first code cell, with the `ocultar-pdf` tag. It is hidden in the PDF, so keep exercise answers and results out of it. Values the reader needs, such as the dates in the assignment, go in a visible cell.
- All other relevant code stays visible. Avoid absolute paths in visible cells, and keep lines under 80 characters so they do not wrap.
- Leave a blank line before every Markdown list, or the PDF runs it into the paragraph.
- Greek letters and subscripts are missing from the PDF font. Write them in words or as math: `$\varepsilon$`. Emoji may be dropped from the PDF, so do not rely on them to carry meaning. Common symbols such as `≥` and `≠`, and box characters in outputs, are handled by the template.

## Figures

Add this to the setup cell:

```python
plt.rcParams['figure.figsize'] = (10, 4)
%config InlineBackend.figure_format = 'retina'
```

- **Always 10 inches wide**, so that text is the same size in every figure. Change the height, not the width: `figsize=(10, 3)` for a simple chart.
- **At most 2 panels in a row.** For 3 related charts use `plt.subplots(3, 1, figsize=(10, 7))`, or `plt.subplot_mosaic([['a', 'a'], ['b', 'c']], figsize=(10, 7))` with the widest chart across the top.

## Tables

- Prefer ending a cell with the DataFrame or using `display(df)`. The export also recognises what these print: `print(df)`, `.to_string()`, Series and `df.dtypes`, `df.info()`, `classification_report`, NumPy matrices, R data frames, Polars tables and Spark `.show()`.
- Tables with more than 9 columns are split into blocks, and long ones continue on the next page.
- Do not build tables by hand with `print` and f-strings: they stay as plain text, and the checker warns about most of them.

## HTML reports and captures

- Save each report in `eda_reports/<group>/<library>/html/` and captures in `.../<library>/capturas/`.
- Show a report inside the notebook with an iframe whose output has the `informe-html` tag: `display(HTML(...), metadata={'tags': ['informe-html']})`. Without it, the PDF prints `<IPython.core.display.HTML object>`.
- The PDF only gets captures. Add one only if it shows something new, cropped to that part, with a short note below on what to look at. Captures do not update themselves: redo them if the data changes.
- Check that notebook outputs and captures contain no secrets and no course material: the repo is public.

## What the checker covers

| Errors (block the export) | Warnings (read them) | Only a person can judge |
|---|---|---|
| Not run, run out of order, or stored errors | Words that may point ahead | Redundant findings or captures |
| Setup cell without its tag, no `retina` | Absolute paths in visible cells | Whether a capture adds something |
| Figures over 10 in, 3+ panels in a row | Code lines that will wrap | Page layout and legibility |
| Numbered references to later sections | Printed tables left as text | |
| Heading levels or numbering out of sequence | | |
| Exercise numbers in the file name or title | | |
| List without a blank line, missing glyphs | | |
| Missing images, untagged HTML, possible secrets | | |
