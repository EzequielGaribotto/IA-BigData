"""Convierte en tablas LaTeX las tablas de los notebooks, tanto las de display() como las impresas con print()."""
import re

from bs4 import BeautifulSoup

MAX_FILAS_EN_PAGINA = 35
MAX_COLUMNAS_POR_BLOQUE = 9
MAX_CARACTERES_EN_LINEA = 45
MIN_FILAS_SIN_CABECERA = 3
LATEX_ESPECIALES = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
                    '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
                    'γ': r'$\gamma$', '₁': r'$_1$'}
NUMERO = re.compile(r'^[-−+£]?[\d,]*\.?\d+%?$|^(NaN|NaT|None|null|)$')
CABECERA_INFO = re.compile(r'^\s*#\s+Column\s+(Non-Null Count\s+)?Dtype\s*$')
FILA_INFO = re.compile(r'^\s*(\d+)\s+(\S.*?)\s+(\d+ non-null)\s+(\S+)\s*$')
FILA_INFO_CORTA = re.compile(r'^\s*(\d+)\s+(\S.*?)\s+(\S+)\s*$')
FINAL_SERIE = re.compile(r'^(?:Name: (.+), )?dtype: \w+$')
FILA_SERIE = re.compile(r'^\S.*\s-?[\d.,]+$')
FILA_ETIQUETA_VALOR = re.compile(r'^\S(?:.*\S)? {2,}(\S+)$')
BORDE_SPARK = re.compile(r'^\+(-+\+)+$')
FILA_MATRIZ = re.compile(r'^\s*\[+([-\d.e\s]+)\]+\s*$')


def escapar(texto):
    return ''.join(LATEX_ESPECIALES.get(ch, ch) for ch in texto)


def leer_filas(filas_html):
    """Convierte filas HTML en una matriz, repartiendo colspan y rowspan."""
    filas, pendientes = [], {}
    for tr in filas_html:
        fila, col = [], 0
        celdas = iter(tr.find_all(['th', 'td']))
        while True:
            if col in pendientes:
                pendientes[col] -= 1
                if not pendientes[col]:
                    del pendientes[col]
                fila.append('')
                col += 1
                continue
            celda = next(celdas, None)
            if celda is None:
                break
            if int(celda.get('rowspan', 1)) > 1:
                pendientes[col] = int(celda['rowspan']) - 1
            fila.append(celda.get_text(' ', strip=True))
            fila.extend([''] * (int(celda.get('colspan', 1)) - 1))
            col += int(celda.get('colspan', 1))
        filas.append(fila)
    return filas


def tipo_columna(valores):
    """Alinea a la derecha los números y deja que el texto largo ocupe varias líneas."""
    if all(NUMERO.match(v) for v in valores):
        return 'r'
    if max(len(v) for v in valores) > MAX_CARACTERES_EN_LINEA:
        return r'>{\raggedright\arraybackslash}p{6cm}'
    return 'l'


def bloque_latex(cabecera, cuerpo):
    n_cols = len(cuerpo[0])
    alinear = ''.join(tipo_columna([f[c] for f in cuerpo]) for c in range(n_cols))
    render = lambda f: ' & '.join(escapar(v) for v in f) + r' \\'
    lineas_cabecera = [render(f) for f in cabecera] + [r'\midrule'] if cabecera else []
    lineas_cuerpo = [render(f) for f in cuerpo]
    if len(cuerpo) > MAX_FILAS_EN_PAGINA:
        return '\n'.join([r'{\footnotesize', rf'\begin{{longtable}}{{{alinear}}}', r'\toprule', *lineas_cabecera,
                          r'\endhead', *lineas_cuerpo, r'\bottomrule', r'\end{longtable}', '}'])
    return '\n'.join([r'\begin{center}', r'\begin{adjustbox}{max width=\linewidth}', r'\small',
                      rf'\begin{{tabular}}{{{alinear}}}', r'\toprule', *lineas_cabecera,
                      *lineas_cuerpo, r'\bottomrule', r'\end{tabular}', r'\end{adjustbox}', r'\end{center}'])


def bloques_latex(cabecera, cuerpo, n_indice):
    """Parte las tablas muy anchas en bloques que repiten el índice, para que sigan siendo legibles."""
    n_cols = len(cuerpo[0])
    bloques = []
    for inicio in range(n_indice, n_cols, MAX_COLUMNAS_POR_BLOQUE):
        columnas = list(range(n_indice)) + list(range(inicio, min(inicio + MAX_COLUMNAS_POR_BLOQUE, n_cols)))
        recorta = lambda filas: [[f[c] for c in columnas] for f in filas]
        bloques.append(bloque_latex(recorta(cabecera), recorta(cuerpo)))
    return '\n'.join(bloques)


def tabla_latex(html):
    """Crea tablas a partir del HTML de un DataFrame, con los valores tal como se muestran."""
    sopa = BeautifulSoup(html, 'html.parser')
    tabla = sopa.find('table')
    filas_cuerpo = tabla.find('tbody').find_all('tr')
    n_indice = len(filas_cuerpo[0].find_all('th'))
    cabecera = leer_filas(tabla.find('thead').find_all('tr'))
    cuerpo = leer_filas(filas_cuerpo)
    n_cols = max(len(f) for f in cabecera + cuerpo)
    for fila in cabecera + cuerpo:
        fila.extend([''] * (n_cols - len(fila)))
    nota = [p.get_text(strip=True) for p in sopa.find_all('p')]
    return bloques_latex(cabecera, cuerpo, n_indice) + ''.join(rf'\par{{\footnotesize {escapar(n)}}}' for n in nota)


def leer_info(lineas, i):
    """Lee la tabla de df.info(), con o sin la columna Non-Null Count."""
    con_nulos = 'Non-Null' in lineas[i]
    patron = FILA_INFO if con_nulos else FILA_INFO_CORTA
    cabecera = ['#', 'Column', 'Non-Null Count', 'Dtype'] if con_nulos else ['#', 'Column', 'Dtype']
    i += 2  # cabecera y línea de guiones
    filas = []
    while i < len(lineas) and patron.match(lineas[i]):
        filas.append(list(patron.match(lineas[i]).groups()))
        i += 1
    return cabecera, filas, i


def leer_spark(lineas, i):
    """Lee una tabla de .show() de Spark. Corta por los bordes porque los valores pueden contener '|'."""
    cortes = [p for p, ch in enumerate(lineas[i]) if ch == '+']
    celdas = lambda l: [l[a + 1:b].strip() for a, b in zip(cortes, cortes[1:])]
    if i + 2 >= len(lineas) or not BORDE_SPARK.match(lineas[i + 2]):
        return None
    cabecera, filas = [celdas(lineas[i + 1])], []
    i += 3
    while i < len(lineas) and lineas[i].startswith('|'):
        filas.append(celdas(lineas[i]))
        i += 1
    if not filas or i >= len(lineas) or not BORDE_SPARK.match(lineas[i]):
        return None
    return cabecera, filas, i + 1


def leer_polars(lineas, i):
    """Lee una tabla de Polars con sus bordes de caracteres."""
    celdas = lambda l: [c.strip() for c in re.split('[│┆]', l)[1:-1]]
    i += 1
    cabecera, filas = [], []
    while i < len(lineas) and not lineas[i].startswith('╞'):
        if lineas[i].startswith('│') and set(''.join(celdas(lineas[i]))) != {'-'}:
            cabecera.append(celdas(lineas[i]))
        i += 1
    i += 1
    while i < len(lineas) and lineas[i].startswith('│'):
        filas.append(celdas(lineas[i]))
        i += 1
    if not filas or i >= len(lineas) or not lineas[i].startswith('└'):
        return None
    return cabecera, filas, i + 1


def leer_matriz(lineas, i):
    """Lee una matriz de NumPy, como una matriz de confusión."""
    if not lineas[i].lstrip().startswith('[['):
        return None
    filas = []
    while i < len(lineas) and FILA_MATRIZ.match(lineas[i]):
        filas.append(FILA_MATRIZ.match(lineas[i]).group(1).split())
        i += 1
        if lineas[i - 1].rstrip().endswith(']]'):
            break
    if len(filas) < 2 or len({len(f) for f in filas}) != 1:
        return None
    return [], filas, i


def bordes_columnas(cabecera):
    """Devuelve dónde termina cada columna: los valores se alinean a la derecha con su título."""
    return [m.end() for m in re.finditer(r'\S+(?: \S+)*', cabecera)]


def encaja_en_columnas(fila, bordes):
    """Comprueba que todos los valores de una fila terminan justo donde termina su columna."""
    fila = fila.rstrip()
    if not fila or len(fila) > bordes[-1]:
        return False
    if bordes[0] < len(fila) and fila[bordes[0]] != ' ':
        return False
    # La primera zona también contiene el índice, y su valor puede estar vacío, como en 'accuracy' de un informe
    primer_valor = len(fila) >= bordes[0] and fila[bordes[0] - 1] != ' '
    hay_valores = primer_valor
    for principio, borde in zip(bordes, bordes[1:]):
        celda = fila[principio:borde]
        if not celda.strip():
            continue
        if len(fila) < borde or fila[borde - 1] == ' ' or (borde < len(fila) and fila[borde] != ' '):
            return False
        hay_valores = True
    return hay_valores


def separar_titulos_pegados(cabecera, bordes, filas):
    """Separa títulos con un solo espacio entre ellos: 'Tiempo (s)' es uno, pero 'ahorro_rs segmento_precio' son dos."""
    nuevos = []
    for m in re.finditer(r'\S+', cabecera):
        fin = m.end()
        if fin in bordes or all(fin <= len(f) and f[fin - 1] != ' ' and (fin == len(f) or f[fin] == ' ')
                                for f in filas):
            nuevos.append(fin)
    return nuevos


def columna_del_indice(filas, primer_borde):
    """Busca el hueco que separa el índice de la primera columna; None si la tabla no tiene índice."""
    for p in range(primer_borde - 1, 0, -1):
        if all(p >= len(f) or f[p] == ' ' for f in filas) and all(f[:p].strip() for f in filas):
            return p
    return None


def leer_pandas(lineas, i):
    """Lee una tabla de ancho fijo: print(df), df.to_string(), classification_report o data.frame de R."""
    cabecera = lineas[i].rstrip().removesuffix('\\').rstrip()
    if not cabecera.startswith(' ') or not cabecera.strip():
        return None
    bordes = bordes_columnas(cabecera)
    titulos = re.findall(r'\S+(?: \S+)*', cabecera)
    if len(titulos) == 1 and not re.fullmatch(r'\w+', titulos[0]):
        return None
    j = i + 1
    nombre_indice = ''
    if j < len(lineas) and len(lineas[j].split()) == 1 and not lineas[j].startswith(' ') \
            and j + 1 < len(lineas) and encaja_en_columnas(lineas[j + 1].rstrip().removesuffix('\\'), bordes):
        nombre_indice = lineas[j].strip()
        j += 1
    filas = []
    while j < len(lineas):
        fila = lineas[j].rstrip().removesuffix('\\').rstrip()
        if not fila and j + 1 < len(lineas) and encaja_en_columnas(lineas[j + 1].rstrip().removesuffix('\\'), bordes) \
                and lineas[j + 1].strip():
            j += 1
            continue
        if not encaja_en_columnas(fila, bordes):
            break
        filas.append(fila)
        j += 1
    if len(filas) < 2:
        return None
    bordes = separar_titulos_pegados(cabecera, bordes, filas)
    inicios = [0] + bordes
    titulos = [cabecera[a:b].strip() for a, b in zip(inicios, bordes)]
    hueco = columna_del_indice(filas, bordes[0])
    tabla = []
    for fila in filas:
        celdas = [fila[a:b].strip() for a, b in zip([hueco or 0] + bordes, bordes)]
        tabla.append(([fila[:hueco].strip()] if hueco else []) + celdas)
    return [([nombre_indice] if hueco else []) + titulos], tabla, j


def leer_etiquetas(lineas, i):
    """Lee etiqueta y valor alineados, sin cabecera: Series impresas, con su pie 'dtype' o sin él."""
    filas, borde = [], None
    j = i
    while j < len(lineas):
        m = FILA_ETIQUETA_VALOR.match(lineas[j].rstrip())
        if not m or (borde is not None and len(lineas[j].rstrip()) != borde):
            break
        borde = len(lineas[j].rstrip())
        filas.append(lineas[j].rstrip().rsplit(None, 1))
        j += 1
    pie = FINAL_SERIE.match(lineas[j]) if j < len(lineas) else None
    if not filas or (len(filas) < MIN_FILAS_SIN_CABECERA and not pie):
        return None
    if pie:
        return pie.group(1) or '', filas, j + 1
    return None, filas, j


def tablas_en_texto(texto):
    """Separa una salida de texto en trozos (es_tabla, contenido), detectando las tablas impresas."""
    trozos, texto_actual = [], []

    def cerrar_texto():
        if ''.join(texto_actual).strip():
            trozos.append((False, '\n'.join(texto_actual).strip('\n') + '\n'))
        texto_actual.clear()

    def anadir_tabla(cabecera, filas):
        cerrar_texto()
        trozos.append((True, bloques_latex(cabecera, filas, 1) if len(filas[0]) > 1 else bloque_latex(cabecera, filas)))

    lineas = texto.splitlines()
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if CABECERA_INFO.match(linea):
            cabecera, filas, i = leer_info(lineas, i)
            anadir_tabla([cabecera], filas)
            continue
        leida = (leer_spark(lineas, i) if BORDE_SPARK.match(linea) else
                 leer_polars(lineas, i) if linea.startswith('┌') else
                 leer_matriz(lineas, i) or leer_pandas(lineas, i))
        if leida:
            cabecera, filas, i = leida
            anadir_tabla(cabecera, filas)
            continue
        etiquetas = leer_etiquetas(lineas, i)
        if etiquetas:
            titulo, filas, i = etiquetas
            indice = ''
            if texto_actual and len(texto_actual[-1].split()) == 1 and titulo is not None:
                indice = texto_actual.pop().strip()
            cabecera = [['' if indice == '0' else indice, titulo]] if indice or titulo else []
            anadir_tabla(cabecera, filas)
            continue
        final_serie = FINAL_SERIE.match(linea)
        if final_serie:  # Series cortas o con valores vacíos: se recogen mirando hacia atrás
            filas = []
            while texto_actual and FILA_SERIE.match(texto_actual[-1]):
                filas.insert(0, texto_actual.pop().rsplit(None, 1))
            if filas:
                indice = texto_actual.pop().strip() if texto_actual and len(texto_actual[-1].split()) == 1 else ''
                anadir_tabla([['' if indice == '0' else indice, final_serie.group(1) or '']], filas)
                i += 1
                continue
        texto_actual.append(linea)
        i += 1
    cerrar_texto()
    return trozos
