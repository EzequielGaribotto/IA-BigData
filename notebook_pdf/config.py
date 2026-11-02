# nbconvert settings for notebook PDFs. Use it through notebook_pdf/export.sh; rules in notebook_pdf/GUIDELINES.md.
import os
import sys

from nbformat.v4 import new_output
from nbconvert.preprocessors import Preprocessor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tablas import tabla_latex, tablas_en_texto


class QuitarRuido(Preprocessor):
    """Quita del PDF las barras de progreso, los avisos y el mensaje de Sweetviz."""

    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type == 'code':
            cell.outputs = [o for o in cell.outputs
                            if not (o.output_type == 'stream'
                                    and (o.name == 'stderr' or o.text.startswith('Report ')))]
        return cell, resources


class TablasLatex(Preprocessor):
    """Sustituye por tablas LaTeX las tablas de display() y las impresas con print()."""

    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type != 'code':
            return cell, resources
        salidas = []
        for salida in cell.outputs:
            datos = salida.get('data', {})
            es_styler = ''.join(datos.get('text/plain', '')).startswith('<pandas.io.formats.style.Styler')
            if 'class="dataframe"' in datos.get('text/html', '') or es_styler:
                salida.data = {'text/latex': tabla_latex(datos['text/html'])}
            elif salida.output_type == 'stream' and salida.name == 'stdout':
                salidas.extend(new_output('display_data', data={'text/latex': contenido}) if es_tabla
                               else new_output('stream', name='stdout', text=contenido)
                               for es_tabla, contenido in tablas_en_texto(salida.text))
                continue
            elif salida.output_type == 'execute_result' and set(datos) == {'text/plain'}:
                trozos = tablas_en_texto(datos['text/plain'])
                if len(trozos) == 1 and trozos[0][0]:
                    salida.data = {'text/latex': trozos[0][1]}
            salidas.append(salida)
        cell.outputs = salidas
        return cell, resources


c = get_config()
c.NbConvertApp.export_format = 'pdf'
c.TemplateExporter.extra_template_paths = [os.path.dirname(os.path.abspath(__file__))]
c.TemplateExporter.template_file = 'informe.tex.j2'
c.PDFExporter.preprocessors = [QuitarRuido, TablasLatex]
c.TagRemovePreprocessor.enabled = True
c.TagRemovePreprocessor.remove_cell_tags = {'ocultar-pdf'}
c.TagRemovePreprocessor.remove_single_output_tags = {'informe-html'}
