#!/usr/bin/env python3

'''
Traducciones para pyENL
'''


def translations(lang='en'):
    '''
    Devuelve un diccionario con las traducciones de cada string.
    '''

    dicc_gen = {}

    # Por cada opción de texto a mostrar al usuario agregar una entrada al
    # diccionario general; cada valor de diccionario será otro diccionario donde
    # las claves son los códigos de los idiomas y los valores son las
    # correspondientes traducciones.
    idiomas = ['es', 'en', 'pt', 'fr']
    if lang not in idiomas:
        raise Exception('Idioma no listado, verificar opciones.')
    dicc_gen['Resolver'] = {'es': 'Resolver', 'en': 'Solve', 'pt': 'Resolver',
                            'fr': 'Resolver'}

    dicc_gen['Ecuaciones'] = {'es': 'Ecuaciones', 'en': 'Equations',
                              'pt': 'Ecuaciones', 'fr': 'Ecuaciones'}

    dicc_gen['Actualizar'] = {'es': 'Actualizar', 'en': 'Update',
                              'pt': 'Actualizar', 'fr': 'Actualizar'}

    dicc_gen['Limpiar'] = {'es': 'Limpiar', 'en': 'Clear', 'pt': 'Limpiar',
                           'fr': 'Limpiar'}

    dicc_gen['Variables'] = {'es': 'Variables', 'en': 'Variables',
                             'pt': 'Variables', 'fr': 'Variables'}

    dicc_gen['Información'] = {'es': 'Información', 'en': 'Information',
                               'pt': 'Información', 'fr': 'Información'}

    dicc_gen['Soluciones'] = {'es': 'Soluciones', 'en': 'Solutions',
                              'pt': 'Soluciones', 'fr': 'Soluciones'}

    dicc_gen['Residuos'] = {'es': 'Residuos', 'en': 'Residuos',
                            'pt': 'Residuos', 'fr' : 'Residuos'}

    dicc_gen['x Ecuaciones/y Variables'] = {'es': 'x Ecuaciones/y Variables', 'en': 'x Ecuaciones/y Variables',
                                            'pt': 'x Ecuaciones/y Variables', 'fr' : 'x Ecuaciones/y Variables'}

    dicc_gen['Archivo'] = {'es': 'Archivo', 'en': 'File',
                           'pt': 'Archivo', 'fr' : 'Archivo'}

    dicc_gen['Exportar reporte'] = {'es': 'Exportar reporte', 'en': 'Export report',
                                    'pt': 'Exportar reporte', 'fr' : 'Exportar reporte'}

    dicc_gen['Importar'] = {'es': 'Importar', 'en': 'Import',
                            'pt': 'Importar', 'fr' : 'Importar'}

    dicc_gen['Editar'] = {'es': 'Editar', 'en': 'Edit',
                          'pt': 'Editar', 'fr' : 'Editar'}

    dicc_gen['Opciones'] = {'es': 'Opciones', 'en': 'Options',
                            'pt': 'Opciones', 'fr' : 'Opciones'}

    dicc_gen['Herramientas'] = {'es': 'Herramientas', 'en': 'Tools',
                                'pt': 'Herramientas', 'fr' : 'Herramientas'}

    dicc_gen['Funciones Ingeniería'] = {'es': 'Funciones Ingeniería', 'en': 'Funciones Ingeniería',
                                        'pt': 'Funciones Ingeniería', 'fr' : 'Funciones Ingeniería'}

    dicc_gen['Funciones de usuario'] = {'es': 'Funciones de usuario', 'en': 'Funciones de usuario',
                                        'pt': 'Funciones de usuario', 'fr' : 'Funciones de usuario'}

    dicc_gen['Ayuda'] = {'es': 'Ayuda', 'en': 'Ayuda',
                         'pt': 'Ayuda', 'fr' : 'Ayuda'}

    dicc_gen['Abrir'] = {'es': 'Abrir', 'en': 'Abrir',
                         'pt': 'Abrir', 'fr' : 'Abrir'}

    dicc_gen['Guardar'] = {'es': 'Guardar', 'en': 'Guardar',
                           'pt': 'Guardar', 'fr' : 'Guardar'}

    dicc_gen['Guardar Como...'] = {'es': 'Guardar Como...', 'en': 'Guardar Como...',
                                   'pt': 'Guardar Como...', 'fr' : 'Guardar Como...'}

    dicc_gen['Cerrar'] = {'es': 'Cerrar', 'en': 'Cerrar',
                          'pt': 'Cerrar', 'fr' : 'Cerrar'}

    dicc_gen['Salir'] = {'es': 'Salir', 'en': 'Salir',
                         'pt': 'Salir', 'fr' : 'Salir'}

    dicc_gen['Seleccionar todo'] = {'es': 'Seleccionar todo', 'en': 'Seleccionar todo',
                                    'pt': 'Seleccionar todo', 'fr' : 'Seleccionar todo'}

    dicc_gen['Deshacer'] = {'es': 'Deshacer', 'en': 'Deshacer',
                            'pt': 'Deshacer', 'fr' : 'Deshacer'}

    dicc_gen['Rehacer'] = {'es': 'Rehacer', 'en': 'Rehacer',
                           'pt': 'Rehacer', 'fr' : 'Rehacer'}

    dicc_gen['Copiar'] = {'es': 'Copiar', 'en': 'Copiar',
                          'pt': 'Copiar', 'fr' : 'Copiar'}

    dicc_gen['Cortar'] = {'es': 'Cortar', 'en': 'Cortar',
                          'pt': 'Cortar', 'fr' : 'Cortar'}

    dicc_gen['Pegar'] = {'es': 'Pegar', 'en': 'Pegar',
                         'pt': 'Pegar', 'fr' : 'Pegar'}

    dicc_gen['Ayuda pyENL'] = {'es': 'Ayuda pyENL', 'en': 'Ayuda pyENL',
                               'pt': 'Ayuda pyENL', 'fr' : 'Ayuda pyENL'}

    dicc_gen['Ayuda NumPy'] = {'es': 'Ayuda NumPy', 'en': 'Ayuda NumPy',
                               'pt': 'Ayuda NumPy', 'fr' : 'Ayuda NumPy'}

    dicc_gen['Ayuda CoolProp'] = {'es': 'Ayuda CoolProp', 'en': 'Ayuda CoolProp',
                                  'pt': 'Ayuda CoolProp', 'fr' : 'Ayuda CoolProp'}

    dicc_gen['Sobre pyENL'] = {'es': 'Sobre pyENL', 'en': 'Sobre pyENL',
                               'pt': 'Sobre pyENL', 'fr' : 'Sobre pyENL'}

    dicc_gen['Licencias'] = {'es': 'Licencias', 'en': 'Licencias',
                             'pt': 'Licencias', 'fr' : 'Licencias'}

    dicc_gen['Termodinámicas'] = {'es': 'Termodinámicas', 'en': 'Termodinámicas',
                                  'pt': 'Termodinámicas', 'fr' : 'Termodinámicas'}

    dicc_gen['Por agregar...'] = {'es': 'Por agregar...', 'en': 'Por agregar...',
                                  'pt': 'Por agregar...', 'fr' : 'Por agregar...'}

    dicc_gen['Disponibles'] = {'es': 'Disponibles', 'en': 'Disponibles',
                               'pt': 'Disponibles', 'fr' : 'Disponibles'}

    dicc_gen['Agregar...'] = {'es': 'Agregar...', 'en': 'Agregar...',
                              'pt': 'Agregar...', 'fr' : 'Agregar...'}

    dicc_gen['Comentario'] = {'es': 'Comentario', 'en': 'Comment',
                              'pt': 'Comentario', 'fr' : 'Comentario'}

    dicc_gen['Unidades'] = {'es': 'Unidades', 'en': 'Unidades',
                            'pt': 'Unidades', 'fr' : 'Unidades'}

    dicc_gen['Configuración'] = {'es': 'Configuración', 'en': 'Configuración',
                                 'pt': 'Configuración', 'fr' : 'Configuración'}

    dicc_gen['Imprimir'] = {'es': 'Imprimir', 'en': 'Imprimir',
                            'pt': 'Imprimir', 'fr' : 'Imprimir'}

    dicc_gen['Open Document Text'] = {'es': 'Open Document Text', 'en': 'Open Document Text',
                                      'pt': 'Open Document Text', 'fr' : 'Open Document Text'}

    dicc_gen['Archivo LaTeX'] = {'es': 'Archivo LaTeX', 'en': 'Archivo LaTeX',
                                 'pt': 'Archivo LaTeX', 'fr' : 'Archivo LaTeX'}

    dicc_gen['Archivo EES'] = {'es': 'Archivo EES', 'en': 'Archivo EES',
                               'pt': 'Archivo EES', 'fr' : 'Archivo EES'}

    # Salida de la función
    output = {}
    for clave in list(dicc_gen.keys()):
        output[clave] = (dicc_gen[clave])[lang]
    return output
