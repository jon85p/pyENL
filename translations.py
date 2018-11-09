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

    # TODO: Traducción de excepciones

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

    dicc_gen['Residuos'] = {'es': 'Residuos', 'en': 'Residual',
                            'pt': 'Residuos', 'fr': 'Residuos'}

    dicc_gen['x Ecuaciones/y Variables'] = {'es': 'x Ecuaciones/y Variables', 'en': 'x Ecuaciones/y Variables',
                                            'pt': 'x Ecuaciones/y Variables', 'fr': 'x Ecuaciones/y Variables'}

    dicc_gen['Archivo'] = {'es': 'Archivo', 'en': 'File',
                           'pt': 'Archivo', 'fr': 'Archivo'}

    dicc_gen['Exportar reporte'] = {'es': 'Exportar reporte', 'en': 'Export report',
                                    'pt': 'Exportar reporte', 'fr': 'Exportar reporte'}

    dicc_gen['Importar'] = {'es': 'Importar', 'en': 'Import',
                            'pt': 'Importar', 'fr': 'Importar'}

    dicc_gen['Editar'] = {'es': 'Editar', 'en': 'Edit',
                          'pt': 'Editar', 'fr': 'Editar'}

    dicc_gen['Opciones'] = {'es': 'Opciones', 'en': 'Options',
                            'pt': 'Opciones', 'fr': 'Opciones'}

    dicc_gen['Herramientas'] = {'es': 'Herramientas', 'en': 'Tools',
                                'pt': 'Herramientas', 'fr': 'Herramientas'}

    dicc_gen['Funciones Ingeniería'] = {'es': 'Funciones Ingeniería', 'en': 'Engineering Functions',
                                        'pt': 'Funciones Ingeniería', 'fr': 'Funciones Ingeniería'}

    dicc_gen['Funciones de usuario'] = {'es': 'Funciones de usuario', 'en': 'User functions',
                                        'pt': 'Funciones de usuario', 'fr': 'Funciones de usuario'}

    dicc_gen['Ayuda'] = {'es': 'Ayuda', 'en': 'Help',
                         'pt': 'Ayuda', 'fr': 'Ayuda'}

    dicc_gen['Abrir'] = {'es': 'Abrir', 'en': 'Open',
                         'pt': 'Abrir', 'fr': 'Abrir'}

    dicc_gen['Guardar'] = {'es': 'Guardar', 'en': 'Save',
                           'pt': 'Guardar', 'fr': 'Guardar'}

    dicc_gen['Guardar Como...'] = {'es': 'Guardar Como...', 'en': 'Save as...',
                                   'pt': 'Guardar Como...', 'fr': 'Guardar Como...'}

    dicc_gen['Cerrar'] = {'es': 'Cerrar', 'en': 'Close',
                          'pt': 'Cerrar', 'fr': 'Cerrar'}

    dicc_gen['Salir'] = {'es': 'Salir', 'en': 'Exit',
                         'pt': 'Salir', 'fr': 'Salir'}

    dicc_gen['Seleccionar todo'] = {'es': 'Seleccionar todo', 'en': 'Select all',
                                    'pt': 'Seleccionar todo', 'fr': 'Seleccionar todo'}

    dicc_gen['Deshacer'] = {'es': 'Deshacer', 'en': 'Undo',
                            'pt': 'Deshacer', 'fr': 'Deshacer'}

    dicc_gen['Rehacer'] = {'es': 'Rehacer', 'en': 'Redo',
                           'pt': 'Rehacer', 'fr': 'Rehacer'}

    dicc_gen['Copiar'] = {'es': 'Copiar', 'en': 'Copy',
                          'pt': 'Copiar', 'fr': 'Copiar'}

    dicc_gen['Cortar'] = {'es': 'Cortar', 'en': 'Cut',
                          'pt': 'Cortar', 'fr': 'Cortar'}

    dicc_gen['Pegar'] = {'es': 'Pegar', 'en': 'Paste',
                         'pt': 'Pegar', 'fr': 'Pegar'}

    dicc_gen['Ayuda pyENL'] = {'es': 'Ayuda pyENL', 'en': 'pyENL Help',
                               'pt': 'Ayuda pyENL', 'fr': 'Ayuda pyENL'}

    dicc_gen['Ayuda NumPy'] = {'es': 'Ayuda NumPy', 'en': 'NumPy Help',
                               'pt': 'Ayuda NumPy', 'fr': 'Ayuda NumPy'}

    dicc_gen['Ayuda CoolProp'] = {'es': 'Ayuda CoolProp', 'en': 'CoolProp Help',
                                  'pt': 'Ayuda CoolProp', 'fr': 'Ayuda CoolProp'}

    dicc_gen['Sobre pyENL'] = {'es': 'Sobre pyENL', 'en': 'About pyENL',
                               'pt': 'Sobre pyENL', 'fr': 'Sobre pyENL'}

    dicc_gen['Licencias'] = {'es': 'Licencias', 'en': 'Licences',
                             'pt': 'Licencias', 'fr': 'Licencias'}

    dicc_gen['Termodinámicas'] = {'es': 'Termodinámicas', 'en': 'Thermodynamical',
                                  'pt': 'Termodinámicas', 'fr': 'Termodinámicas'}

    dicc_gen['Por agregar...'] = {'es': 'Por agregar...', 'en': 'TODO',
                                  'pt': 'Por agregar...', 'fr': 'Por agregar...'}

    dicc_gen['Disponibles'] = {'es': 'Disponibles', 'en': 'Availables',
                               'pt': 'Disponibles', 'fr': 'Disponibles'}

    dicc_gen['Agregar...'] = {'es': 'Agregar...', 'en': 'TODO...',
                              'pt': 'Agregar...', 'fr': 'Agregar...'}

    dicc_gen['Comentario'] = {'es': 'Comentario', 'en': 'Comment',
                              'pt': 'Comentario', 'fr': 'Comentario'}

    dicc_gen['Unidades'] = {'es': 'Unidades', 'en': 'Units',
                            'pt': 'Unidades', 'fr': 'Unidades'}

    dicc_gen['Configuración'] = {'es': 'Configuración', 'en': 'Settings',
                                 'pt': 'Configuración', 'fr': 'Configuración'}

    dicc_gen['Imprimir'] = {'es': 'Imprimir', 'en': 'Print',
                            'pt': 'Imprimir', 'fr': 'Imprimir'}

    dicc_gen['Open Document Text'] = {'es': 'Open Document Text', 'en': 'Open Document Text',
                                      'pt': 'Open Document Text', 'fr': 'Open Document Text'}

    dicc_gen['Archivo LaTeX'] = {'es': 'Archivo LaTeX', 'en': 'LaTeX file',
                                 'pt': 'Archivo LaTeX', 'fr': 'Archivo LaTeX'}

    dicc_gen['Archivo EES'] = {'es': 'Archivo EES', 'en': 'EES file',
                               'pt': 'Archivo EES', 'fr': 'Archivo EES'}

    dicc_gen['Información'] = {'es': 'Información', 'en': 'Information',
                               'pt': 'Información', 'fr': 'Información'}

    dicc_gen['Solucionado en '] = {'es': 'Solucionado en ', 'en': 'Solved in ',
                                   'pt': 'Información', 'fr': 'Información'}

    dicc_gen[' segundos.\nMayor desviación de '] = {'es': ' segundos.\nMayor desviación de ', 'en': ' seconds.\nGreater Desviation: ',
                                                    'pt': 'Información', 'fr': 'Información'}

    dicc_gen['Ecuación'] = {'es': 'Ecuación', 'en': 'Equation',
                            'pt': 'Información', 'fr': 'Información'}

    dicc_gen['Residuo'] = {'es': 'Residuo', 'en': 'Residual',
                           'pt': 'Información', 'fr': 'Información'}

    dicc_gen['Solución'] = {'es': 'Solución', 'en': 'Solution',
                            'pt': 'Información', 'fr': 'Información'}

    dicc_gen['No hubo convergencia a solución...'] = {'es': 'No hubo convergencia a solución...',
                                                      'en': 'No convergence to solution...',
                                                      'pt': 'No hubo convergencia a solución...',
                                                      'fr': 'No hubo convergencia a solución...'}

    dicc_gen['Problema'] = {'es': 'Problema', 'en': 'Problem',
                            'pt': 'Problema', 'fr': 'Problema'}

    dicc_gen['Variable'] = {'es': 'Variable', 'en': 'Variable',
                            'pt': 'Variable', 'fr': 'Variable'}

    dicc_gen['Valor Inicial'] = {'es': 'Valor Inicial', 'en': 'Initial Guess',
                                 'pt': 'Valor Inicial', 'fr': 'Valor Inicial'}

    dicc_gen['Inferior'] = {'es': 'Inferior', 'en': 'Lower',
                            'pt': 'Inferior', 'fr': 'Inferior'}

    dicc_gen['Superior'] = {'es': 'Superior', 'en': 'Upper',
                            'pt': 'Superior', 'fr': 'Superior'}

    dicc_gen['El número '] = {'es': 'El número ', 'en': 'The number ',
                              'pt': 'El número ', 'fr': 'El número '}

    dicc_gen[' es mayor a '] = {'es': ' es mayor a ', 'en': 'is greater than ',
                                'pt': ' es mayor a ', 'fr': ' es mayor a '}

    dicc_gen[' en la variable '] = {'es': ' en la variable ', 'en': ' in variable ',
                                    'pt': ' en la variable ', 'fr': ' en la variable '}

    dicc_gen['El valor inicial de '] = {'es': 'El valor inicial de ', 'en': 'The initial guess of ',
                                        'pt': 'El valor inicial de ', 'fr': 'El valor inicial de '}

    dicc_gen[' debe estar entre los dos límites.'] = {'es': ' debe estar entre los dos límites.',
                                                      'en': ' must is between the limits.',
                                                      'pt': ' debe estar entre los dos límites.', 'fr': ' debe estar entre los dos límites.'}

    dicc_gen[' ecuaciones / '] = {'es': ' ecuaciones / ', 'en': ' equations /',
                                  'pt': ' ecuaciones / ', 'fr': ' ecuaciones / '}

    dicc_gen[' variables'] = {'es': ' variables', 'en': ' variables',
                              'pt': ' variables', 'fr': ' variables'}

    dicc_gen['Error encontrando cantidad de variables y de ecuaciones'] = {'es': 'Error encontrando cantidad de variables y de ecuaciones',
                                                                           'en': 'Error finding variable lenght and equations',
                                                                           'pt': 'Error encontrando cantidad de variables y de ecuaciones',
                                                                           'fr': 'Error encontrando cantidad de variables y de ecuaciones'}

    dicc_gen["x Ecuaciones/y Variables"] = {'es': "x Ecuaciones/y Variables", 'en': 'x Equations/y Variables',
                                            'pt': "x Ecuaciones/y Variables", 'fr': "x Ecuaciones/y Variables"}

    dicc_gen['Información'] = {'es': 'Información', 'en': 'Information',
                               'pt': 'Información', 'fr': 'Información'}

    dicc_gen['Información'] = {'es': 'Información', 'en': 'Information',
                               'pt': 'Información', 'fr': 'Información'}

    dicc_gen['Información'] = {'es': 'Información', 'en': 'Information',
                               'pt': 'Información', 'fr': 'Información'}
    
    dicc_gen['Acá va el comentario'] = {'es': 'Acá va el comentario', 'en': 'Comment goes here',
                                        'pt': 'Acá va el comentario', 'fr': 'Acá va el comentario'}
    dicc_gen['El documento se ha modificado'] = {'es' : 'El documento se ha modificado',
                                                 'en': 'The file was modified',
                                                 'pt': 'El archivo ha sido modificado',
                                                 'fr': 'El archivo ha sido modificado'}

    dicc_gen["¿Desea guardar los cambios?"] = {'es' : '¿Desea guardar los cambios?',
                                                 'en': 'Save changes?',
                                                 'pt': '¿Desea guardar los cambios?',
                                                 'fr': '¿Desea guardar los cambios?'}
    
    dicc_gen["Idioma (requiere reiniciar pyENL)"] = {'es' : "Idioma (requiere reiniciar pyENL)",
                                                     'en': 'Language (pyENL restart)',
                                                     'pt': '"Idioma (requiere reiniciar pyENL)"',
                                                     'fr': '"Idioma (requiere reiniciar pyENL)"'}    
    
    dicc_gen['Spanish'] = {'es' : 'Español', 'en': 'Spanish',
                        'pt': 'Espanhol', 'fr': 'Español'}
    
    dicc_gen['English'] = {'es' : 'Inglés', 'en': 'English',
                        'pt': 'Inglês', 'fr': 'Anglais'}
    
    dicc_gen['French'] = {'es' : 'Francés', 'en': 'French',
                        'pt': 'Francês', 'fr': 'Français'}
    
    dicc_gen['Portuguese'] = {'es' : 'Portugués', 'en': 'Portiguese',
                        'pt': 'Portugues', 'fr': 'Portugais'}
    
    dicc_gen['Formato'] = {'es' : 'Formato', 'en': 'Format',
                        'pt': 'Format', 'fr': 'Format'}

    dicc_gen['Interfaz'] = {'es' : 'Interfaz', 'en': 'Interface',
                        'pt': 'Interface', 'fr': 'Interface'}    
    
    dicc_gen['Método'] = {'es' : 'Método', 'en': 'Method',
                        'pt': 'Method', 'fr': 'Method'}
    
    dicc_gen['Formato'] = {'es' : 'Formato', 'en': 'Format',
                        'pt': 'Format', 'fr': 'Format'}
    
    dicc_gen['Tolerancia'] = {'es' : 'Tolerancia', 'en': 'Tolerance',
                        'pt': 'Tolerance', 'fr': 'Tolerance'}
    
    dicc_gen['Tiempo máximo de espera en segundos'] = {'es' : 'Tiempo máximo de espera (segundos)', 'en': 'Timeout (seconds)',
                        'pt': 'Timeout (seconds)', 'fr': 'Timeout (seconds)'}
    
    dicc_gen['Solver'] = {'es' : 'Solucionador', 'en': 'Solver',
                        'pt': 'Solver', 'fr': 'Solver'}
    
    dicc_gen['Unidades'] = {'es' : 'Unidades', 'en': 'Units',
                        'pt': 'Units', 'fr': 'Units'}

    dicc_gen['Tema'] = {'es' : 'Tema', 'en': 'Theme',
                        'pt': 'Theme', 'fr': 'Theme'}
    
    dicc_gen['Predeterminado'] = {'es' : 'Predeterminado', 'en': 'Default',
                        'pt': 'Default', 'fr': 'Default'}
    
    dicc_gen['Fuente'] = {'es' : 'Fuente', 'en': 'Font',
                        'pt': 'Font', 'fr': 'Font'}
    
    # dicc_gen['Algo'] = {'es' : 'Algo', 'en': 'Something',
    #                     'pt': 'Alginho', 'fr': 'Algué'}

    # Salida de la función
    output = {}
    for clave in list(dicc_gen.keys()):
        output[clave] = (dicc_gen[clave])[lang]
    return output
