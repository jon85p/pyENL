#!/usr/bin/env python3
'''Funciones para exportar e importar datos'''


def sols2odt(variables, file_name, user_input):
    '''
    Soluciones a documento Open Document Text
    '''
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties
    from odf.text import H, P, Span
    # Comienza la salida:
    textdoc = OpenDocumentText()
    # Styles
    s = textdoc.styles
    h1style = Style(name="Heading 1", family="paragraph")
    h1style.addElement(TextProperties(attributes={'fontsize': "24pt",
                                                  'fontweight': "bold"}))
    s.addElement(h1style)
    h2style = Style(name="Heading 2", family="paragraph")
    h2style.addElement(TextProperties(attributes={'fontsize': "18pt",
                                                  'fontweight': "bold"}))
    s.addElement(h2style)
    # An automatic style Bold
    boldstyle = Style(name="Bold", family="text")
    boldprop = TextProperties(fontweight="bold")
    boldstyle.addElement(boldprop)
    textdoc.automaticstyles.addElement(boldstyle)
    # Italic
    italicstyle = Style(name="Italic", family="text")
    italicprop = TextProperties(fontstyle="italic")
    italicstyle.addElement(italicprop)
    textdoc.automaticstyles.addElement(italicstyle)
    # Text
    h = H(outlinelevel=1, stylename=h1style, text="Reporte pyENL")
    textdoc.text.addElement(h)
    p = P(text='')
    textdoc.text.addElement(p)
    h = H(outlinelevel=1, stylename=h2style, text="Ecuaciones")
    textdoc.text.addElement(h)
    p = P(text='')
    textdoc.text.addElement(p)
    # Añadimos las ecuaciones:
    for eqn in user_input:
        p = P(text='')
        if '<<' in eqn:
            comentario = eqn
            comentario = comentario.replace('<<', '')
            comentario = comentario.replace('>>', '')
            boldpart = Span(stylename=boldstyle, text=comentario)
            p.addElement(boldpart)
        else:
            italicpart = Span(stylename=italicstyle, text=eqn)
            p.addElement(italicpart)
        textdoc.text.addElement(p)
    # Ahora añadir las soluciones:
    p = P(text='')
    textdoc.text.addElement(p)
    h = H(outlinelevel=1, stylename=h2style, text="Soluciones")
    textdoc.text.addElement(h)
    p = P(text='')
    textdoc.text.addElement(p)

    for variable in variables:
        # Primero insertar el nombre de la variable con su valor y finalmente
        # El comentario de la misma:
        p = P(text=variable.name + ' = ' + str(variable.guess) + ' ' +
              variable.units)
        textdoc.text.addElement(p)
        p = P(text=variable.comment)
        textdoc.text.addElement(p)
        p = P(text='')
        textdoc.text.addElement(p)
    # Guardar...
    textdoc.save(file_name)


def sols2tex(variables, file_name, user_input, autor):
    '''
    Soluciones a documento TeX
    '''
    from pylatex import Document, Section, Subsection, Command, Math, Tabular
    from pylatex.utils import italic, NoEscape
    doc = Document()
    doc.preamble.append(Command('title', 'Reporte pyENL'))
    doc.preamble.append(Command('author', autor))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Section('Ecuaciones:')):
        # Por cada línea de user_input añadir un append y salto de línea
        #(si es comentario de usuario)
        comentario_user = False
        for eqn in user_input:
            if '<<' in eqn:
                # Entonces es un comentario de usuario
                comentario = eqn
                comentario = comentario.replace('<<', '')
                comentario = comentario.replace('>>', '')
                if comentario_user == True:
                    doc.append('\n' + comentario)
                else:
                    # Esto porque no hay necesidad de salto.
                    doc.append(comentario)
                comentario_user = True
            else:
                # Entonces no es un comentario sino una ecuación, entonces
                # insertar con símbolos matemáticos.
                doc.append(Math(data=[eqn]))
                comentario_user = False

    # Ahora insertar los resultados
    with doc.create(Section('Resultados:')):
        # Acá viene una tabla con los resultados.
        with doc.create(Tabular('rc|cl')) as table:
            table.add_hline()
            table.add_row(('Variable', 'Valor', 'Descripción', 'Unidades'))
            table.add_hline(1, 4)
            table.add_empty_row()
            # Ahora por cada variable añadir la información requerida:
            for variable in variables:
                t_var = variable.name  # Nombre variable
                t_val = variable.guess  # Valor de la variable
                t_desc = variable.comment  # Descripción de la variable
                t_unit = variable.units  # Unidades de la variable
                table.add_row((t_var, t_val, t_desc, t_unit))
            #table.add_row(('x', 5, 'Hola', 'm'))

    if file_name[-4::] == '.pdf':
        doc.generate_pdf(file_name[0:-4])
    else:
        doc.generate_tex(file_name[0:-4])


def import_ees(ees_file):
    '''
    Importar texto de documentos EES y convertirlos a formato pyENL
    '''
    f = open(ees_file, mode='r', encoding='iso8859-1')
    salida = f.read()
    end = '{$ID$'
    texto = salida[20:salida.index(end)]
    lista = texto.split('\n')
    # TODO Tratar texto EES para compatibilidad con pyENL
    return lista
