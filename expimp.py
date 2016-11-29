#!/usr/bin/env python3
'''Funciones para exportar e importar datos'''

def sols2odt(variables, file_name, user_input):
    '''
    Soluciones a documento Open Document Text
    '''
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties
    from odf.text import H, P, Span
    #Comienza la salida:
    textdoc = OpenDocumentText()
    # Styles
    s = textdoc.styles
    h1style = Style(name="Heading 1", family="paragraph")
    h1style.addElement(TextProperties(attributes={'fontsize':"24pt",\
    'fontweight':"bold" }))
    s.addElement(h1style)
    h2style = Style(name="Heading 2", family="paragraph")
    h2style.addElement(TextProperties(attributes={'fontsize':"18pt",\
    'fontweight':"bold" }))
    s.addElement(h2style)
    # An automatic style Bold
    boldstyle = Style(name="Bold", family="text")
    boldprop = TextProperties(fontweight="bold")
    boldstyle.addElement(boldprop)
    textdoc.automaticstyles.addElement(boldstyle)
    #Italic
    italicstyle = Style(name="Italic", family="text")
    italicprop = TextProperties(fontstyle="italic")
    italicstyle.addElement(italicprop)
    textdoc.automaticstyles.addElement(italicstyle)
    # Text
    h=H(outlinelevel=1, stylename=h1style, text="Reporte pyENL")
    textdoc.text.addElement(h)
    p = P(text='')
    textdoc.text.addElement(p)
    h=H(outlinelevel=1, stylename=h2style, text="Ecuaciones")
    textdoc.text.addElement(h)
    p = P(text='')
    textdoc.text.addElement(p)
    #Añadimos las ecuaciones:
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
    #Ahora añadir las soluciones:
    p = P(text='')
    textdoc.text.addElement(p)
    h=H(outlinelevel=1, stylename=h2style, text="Soluciones")
    textdoc.text.addElement(h)
    p = P(text='')
    textdoc.text.addElement(p)

    for variable in variables:
        #Primero insertar el nombre de la variable con su valor y finalmente
        #El comentario de la misma:
        p = P(text=variable.name + ' = ' + str(variable.guess))
        textdoc.text.addElement(p)
        p = P(text=variable.comment)
        textdoc.text.addElement(p)
        p = P(text='')
        textdoc.text.addElement(p)
    #Guardar...
    textdoc.save(file_name)


def sols2tex(variables, file_name):
    '''
    Soluciones a documento TeX
    '''
    pass

def import_ees(file):
    '''
    Importar texto de documentos EES y convertirlos a formato pyENL
    '''
    pass
