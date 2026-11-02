"""Checks a notebook against notebook_pdf/GUIDELINES.md.

Usage: python notebook_pdf/check.py notebook.ipynb [...]
Exit code 1 if there are errors. Warnings are worth reading but do not block the export.
"""
import json
import re
import sys
from pathlib import Path

from tablas import tablas_en_texto

MAX_FIGURE_WIDTH = 10
MAX_CODE_LINE = 80
NUMBERED_NAME = re.compile(r'(ejercicio|entregable|\bej)[ _-]*(final[ _-]*)?\d', re.I)
HIDDEN_TAG = 'ocultar-pdf'
REPORT_TAG = 'informe-html'

SECRET = re.compile(r'''sk-[A-Za-z0-9_-]{10,}|gsk_[A-Za-z0-9]{10,}|AIza[A-Za-z0-9_-]{10,}|hf_[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{10,}'''
                    r'''|Bearer\s+[A-Za-z0-9._-]{10,}|api_key\s*=\s*["'][^"']+["']''')
FORWARD_WORDS = re.compile(r'a continuaci[oó]n|m[aá]s adelante|siguiente (secci[oó]n|fase|apartado)'
                           r'|se (analiza|ve|trata|explica)n? en (la|las) secci', re.I)
SECTION_REF = re.compile(r'secci[oó]n(?:es)?\s+((?:\d+(?:\.\d+)?(?:,\s*|\s+y\s+)?)+)', re.I)
HEADING = re.compile(r'^(#{1,6})\s+(.*)$')
NUMBERED = re.compile(r'^(?:(\d+) & )?(\d+)(?:\.(\d+))?\.\s')
LIST_ITEM = re.compile(r'^\s*([-*+]|\d+\.)\s+\S')
FIGSIZE = re.compile(r'figsize\s*=\s*\(\s*([\d.]+)\s*,')
ROW_OF_PANELS = re.compile(r'subplots\(\s*1\s*,\s*(\d+)')
ABSOLUTE_PATH = re.compile(r'''['"](/home/|/Users/|[A-Z]:\\)''')
MISSING_GLYPHS = re.compile('[\u0370-\u03ff\u1d62\u2080-\u2089\U0001f000-\U0001faff]')
MATH = re.compile(r'\$[^$\n]+\$')
IMAGE = re.compile(r'!\[[^\]]*\]\(([^)\s]+)\)')
PLOTS = re.compile(r'\bplt\.|\.plot[.(]|\bsns\.')
ALIGNED_ROW = re.compile(r'^\S.*\S {2,}\S+.* {2,}\S+')
SETUP_LINE = re.compile(r'^\s*($|#|import\s|from\s.*\simport\s|%|!|warnings\.|pd\.set_option|pd\.options|'
                        r'np\.set_printoptions|plt\.rcParams|plt\.style|sns\.set|matplotlib\.|os\.environ|ssl\.|print\()')
OBJECT_REPR = re.compile(r'^<[\w.]+( object)?( at 0x\w+)?>$')


def source(cell):
    return ''.join(cell['source'])


def is_setup(text):
    """True if a cell only has imports, options and installs, with nothing the reader needs."""
    return bool(text.strip()) and all(SETUP_LINE.match(line) for line in text.splitlines())


def section_number(reference):
    major, _, minor = reference.partition('.')
    return int(major), int(minor or 0)


def check(path):
    notebook = json.loads(path.read_text(encoding='utf-8'))
    cells = notebook['cells']
    errors, warnings = [], []
    code_cells = [c for c in cells if c['cell_type'] == 'code']

    def where(index):
        return f'cell {index}'

    if NUMBERED_NAME.search(path.stem):
        errors.append('the file name must describe the work, not an exercise number')

    # Fully and cleanly executed, in order
    counts = [c.get('execution_count') for c in code_cells if source(c).strip()]
    if None in counts:
        errors.append('some code cells were not executed: run the notebook from top to bottom')
    elif counts != sorted(counts):
        errors.append('cells were executed out of order: restart and run the notebook from top to bottom')

    # Setup cell hidden in the PDF
    if code_cells and is_setup(source(code_cells[0])) and HIDDEN_TAG not in code_cells[0]['metadata'].get('tags', []):
        errors.append(f'the setup cell (imports and options) needs the "{HIDDEN_TAG}" tag')

    has_plots = any(PLOTS.search(source(c)) for c in code_cells)
    all_code = '\n'.join(source(c) for c in code_cells)
    if has_plots and 'figure_format' not in all_code:
        errors.append("figures need %config InlineBackend.figure_format = 'retina' in the setup cell")

    current = (0, 0)
    last_major = last_minor = 0
    titles = 0
    long_lines = 0
    for index, cell in enumerate(cells):
        text = source(cell)
        hidden = HIDDEN_TAG in cell['metadata'].get('tags', [])
        place = where(index)

        if SECRET.search(text):
            errors.append(f'{place}: possible secret in the source')

        if cell['cell_type'] == 'markdown':
            previous = ''
            fenced = False
            for line in text.splitlines():
                if line.startswith('```'):
                    fenced = not fenced
                if fenced:
                    continue
                heading = HEADING.match(line)
                if heading:
                    level, title = len(heading.group(1)), heading.group(2)
                    number = NUMBERED.match(title)
                    if level == 1:
                        titles += 1
                        if NUMBERED_NAME.search(title):
                            errors.append(f'{place}: the title must describe the work, not an exercise number')
                    elif number:
                        first = int(number.group(1) or number.group(2))
                        major, minor = int(number.group(2)), int(number.group(3) or 0)
                        expected = '###' if minor else '##'
                        if heading.group(1) != expected:
                            errors.append(f'{place}: section "{title}" must use {expected}')
                        if minor:
                            if major != last_major or minor != last_minor + 1:
                                errors.append(f'{place}: section number {major}.{minor} breaks the sequence')
                        elif first != last_major + 1 and not (first == 0 and last_major == 0):
                            errors.append(f'{place}: section number {major} breaks the sequence')
                        last_major, last_minor = major, minor
                        current = (major, minor)
                if LIST_ITEM.match(line) and previous.strip() and not LIST_ITEM.match(previous) \
                        and not previous.startswith((' ', '\t')) and not HEADING.match(previous):
                    errors.append(f'{place}: a list needs a blank line before it: "{previous[:50]}"')
                previous = line
            for found in MISSING_GLYPHS.findall(MATH.sub('', text)):
                errors.append(f'{place}: the PDF font has no "{found}": write it in words')
            for image in IMAGE.findall(text):
                if not image.startswith(('http://', 'https://', 'data:')) and not (path.parent / image).exists():
                    errors.append(f'{place}: image not found: {image}')

        # Forward references, in text and in code comments
        prose = text if cell['cell_type'] == 'markdown' else '\n'.join(re.findall(r'#.*', text))
        for match in SECTION_REF.finditer(prose):
            for reference in re.findall(r'\d+(?:\.\d+)?', match.group(1)):
                if section_number(reference) > current:
                    errors.append(f'{place}: points ahead to section {reference}; the notebook must read top to bottom')
        forward = FORWARD_WORDS.search(prose)
        if forward:
            warnings.append(f'{place}: possible pointer ahead: "{forward.group(0)}"')

        if cell['cell_type'] != 'code':
            continue

        for match in FIGSIZE.finditer(text):
            if float(match.group(1)) > MAX_FIGURE_WIDTH:
                errors.append(f'{place}: figure {match.group(1)} in wide; the maximum is {MAX_FIGURE_WIDTH}')
        for match in ROW_OF_PANELS.finditer(text):
            if int(match.group(1)) > 2:
                errors.append(f'{place}: {match.group(1)} panels in one row are unreadable: use rows or subplot_mosaic')

        if not hidden:
            if ABSOLUTE_PATH.search(text):
                warnings.append(f'{place}: absolute path in a visible cell')
            long_lines += sum(len(line) > MAX_CODE_LINE for line in text.splitlines())

        for output in cell.get('outputs', []):
            kind = output['output_type']
            if kind == 'error':
                errors.append(f'{place}: stored error ({output.get("ename")})')
                continue
            data = output.get('data', {})
            html = ''.join(data.get('text/html', ''))
            tagged = REPORT_TAG in output.get('metadata', {}).get('tags', [])
            plain = ''.join(data.get('text/plain', '')).strip()
            is_styler = plain.startswith('<pandas.io.formats.style.Styler')
            if html and not tagged and not is_styler and OBJECT_REPR.match(plain) \
                    and not set(data) & {'text/latex', 'image/png', 'text/markdown'}:
                errors.append(f'{place}: HTML output would print {plain[:30]} in the PDF: add the "{REPORT_TAG}" tag')
            if kind == 'stream' and output.get('name') == 'stdout':
                plain_parts = [part for is_table, part in tablas_en_texto(''.join(output['text'])) if not is_table]
                rows = [line for part in plain_parts for line in part.splitlines() if ALIGNED_ROW.match(line)]
                if len(rows) >= 3:
                    warnings.append(f'{place}: printed table will stay as plain text: use display(df)')

    if long_lines:
        warnings.append(f'{long_lines} code line(s) over {MAX_CODE_LINE} characters will wrap in the PDF')
    if titles != 1:
        errors.append(f'the notebook needs exactly one "#" title, it has {titles}')
    return errors, warnings


def main():
    failed = False
    for name in sys.argv[1:]:
        path = Path(name)
        errors, warnings = check(path)
        print(f'{path}: {len(errors)} error(s), {len(warnings)} warning(s)')
        for message in errors:
            print(f'  ERROR    {message}')
        for message in warnings:
            print(f'  warning  {message}')
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
