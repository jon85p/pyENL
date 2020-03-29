# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from utils import *
from copy import deepcopy
from entrada import pyENL_variable, entradaTexto

varsTitles = ['Variable','Initial Guess','Lower','Upper','Units','Comment']
solTitles = ['Variable','Solution','Units','Comment']
resTitles = ['Ecuación','Residual']
timeout = 10 # TODO self.timeout Se debe traer de la configuración

opciones_ = configFile(pyENL_path + "config.txt")
opt_method = opciones_.method # self.opt_method
opt_tol = opciones_.tol # self.opt_tol
formateo = opciones_.format

variables = [] # TODO self.variables revisar de donde sale!


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title ='pYENL web'
app.layout = html.Div(children=[

    dcc.ConfirmDialog(
        id='confirm',
        message='Notificación simplificada de resultado de cálculos',
    ),


    html.Div(children='''
        UNDER CONSTRUCTION pyENL web : an app where you can solve your problems! ... almost all! 
    ''',style={'height':'5vh'}),

    html.Div(children=
    [
        dbc.Row(
        [    
            dbc.Col(
                html.Div(children=
                    dcc.Tabs([
                            dcc.Tab(label='Ecuations box', children=[
                                    html.Div(
                                        dcc.Textarea(
                                            id='cajaTexto',
                                            placeholder='Start write your ecuations!',
                                            style = {
                                                        'width' :'100%',
                                                        'padding-right':'0px',
                                                        'padding-left':'0px',
                                                        'height':'100%'
                                                    },

                                        ),style={'height':'80vh'}
                                    )
                            ],style={'padding':'1px'},selected_style={'padding':'2px','fontWeight':'bold'}
                            ),
                            dcc.Tab(label='Rendered equations', children=[
                                    html.Div(
                                        dcc.Textarea(
                                            id ='cajaSol',
                                            placeholder='Here will go the formatted equations',
                                            style = {
                                                        'width' :'100%',
                                                        'padding-right':'0px',
                                                        'padding-left':'0px',
                                                        'height':'100%'
                                                    },

                                        ),style={'height':'80vh'}
                                    )
                            ],style={'padding':'1px'},selected_style={'padding':'2px','fontWeight':'bold'}
                            ),
                    ], )
                ,
                )),
            dbc.Col(
                [
                    dbc.Row(html.Div(children=
                            [
                                    dash_table.DataTable(
                                        id='table-vars',
                                        columns=[{"name": i, "id": str(i)} for i in varsTitles],
                                        style_header={'backgroundColor':'white',
                                                    #'fontWeight':'bold'
                                        },
                                        # fixed_rows={'headers':True,'data':0},
                                        style_cell= {'font_family':'Helvetica',
                                                    'font_size':'14px',
                                                    'textAlign':'center'
                                        },
                                        style_table={'maxHeight': '40vh',
                                                    'height':'40vh', # para ajustar el tamaño al del div
                                                    #'overflowY': 'auto',
                                                    }
                                    )
                            ],style={ 'height':'40vh','width':'100%'}),
                    #por defecto el row tiene -15px entonces queda sobremontado
                    # style={'margin-left':'0px','margin-right':'0px'},
                    ),
                    dbc.Row(html.Div(children=
                            [
                                dcc.Tabs(
                                    [   
                                        dcc.Tab(label='Soluciones', children=
                                            [
                                                dash_table.DataTable(
                                                    id='table-sol',
                                                    columns=[{"name": i, "id": str(i)} for i in solTitles],
                                                    style_header={'backgroundColor':'white',
                                                                    #'width':'10%'
                                                    },
                                                    # fixed_rows={'headers':True,'data':0},
                                                    style_cell= {'font_family':'Helvetica',
                                                                'font_size':'14px',
                                                                'textAlign':'center',                
                                                    },
                                                    style_table={'maxHeight': '40vh',
                                                                'height':'40vh', # para ajustar el tamaño al del div
                                                    },    
                                                )
                                            ],style={'padding':'1px'},selected_style={'padding':'2px','fontWeight':'bold'}
                                            ),
                                        dcc.Tab(label='Residuos', children=
                                            [
                                                dash_table.DataTable(
                                                    id='table-res',
                                                    columns=[{"name": i, "id": str(i)} for i in resTitles],
                                                    style_header={'backgroundColor':'white',
                                                                    #'width':'10%'
                                                    },
                                                    # fixed_rows={'headers':True,'data':0},
                                                    style_cell= {'font_family':'Helvetica',
                                                                'font_size':'14px',
                                                                'textAlign':'center', 
                                                    },
                                                    style_table={'maxHeight': '40vh',
                                                                'height':'40vh', # para ajustar el tamaño al del div
                                                                # 'overflowY': 'auto',
                                                    },               
                                                    
                                                )
                                            ],style={'padding':'1px'},selected_style={'padding':'2px','fontWeight':'bold'}
                                            ),
                                    ])
                            ],style={ 'height':'40vh','width':'100%'}),
                    #por defecto el row tiene -15px entonces queda sobremontado
                    # style={'margin-left':'0px','margin-right':'0px'},
                   )
                ], style={'padding-left':'0px','padding-right':'0px',}
            ),


        ], style={'width':'100%'}
    ),
    ],
    ),
    html.Div(id = 'div-infoLabel', children='''
    ''',style={'height':'3vh'}),

    html.Div(
        html.Button('Resolver',id='solve_button',style={'width':'100%'}),
        )
],

)

@app.callback(
    [
        dash.dependencies.Output('table-sol','data'),
        dash.dependencies.Output('confirm','message'),
        dash.dependencies.Output('confirm', 'displayed')
    ],
    [
        dash.dependencies.Input('solve_button', 'n_clicks')
    ],
    [
        dash.dependencies.State('cajaTexto','value')
    ],
    )
def solve(n_clicks,cajaTexto):
    '''
    Pasa el contenido de la caja de texto y de la tabla de variables al
    solver principal y calcula. (FUNCIÓN adaptada desde el pyENL Desktop)
    '''
    global variables
    if cajaTexto is None:
        # Evita que se ejecute el la función cuando es llamada sin data
        raise dash.exceptions.PreventUpdate("cancel the callback")
    # 10 segundos de espera
    # self.actualizaInfo() # TODO
    backup_var = deepcopy(variables) # TODO
    try:
        pyENL_timeout = timeout

        ecuaciones = cajaTexto.splitlines()
        # Para poder soportar variables tipo texto
        ecuaciones = variables_string(ecuaciones)
        # Quitar los comentarios de las ecuaciones:
        ecuaciones_s = quitaComentarios(ecuaciones)

        solucion = entradaTexto(
            ecuaciones, pyENL_timeout, varsObj=variables, tol = opt_tol, method=opt_method)
        
        tiempo = solucion[1]
        tiempo = '{:,.4}'.format(tiempo)
        variables = solucion[0][0]
        residuos = solucion[0][1]
        solved = solucion[0][2]

        # TODO traducciones pendientes
        
        # # Ahora a imprimir la respuesta en la tabla si solved es True
        if solved:
            resultMenssage = "Solucionado en" + tiempo + ' segundos.\nMayor desviación de ' + str(max(residuos))
            dataSol = imprimeSol(variables) 
        else:
            resultMenssage ="Problema, No hubo convergencia a solución..."
            dataSol = []
    except Exception as e:
        resultMenssage = "Error: " + str(e)
    #     # Restaurar acá las variables copiadas
    #     # TODO Restaurar solo las variables que no se pudieron resolver (bloques)
        dataSol = []
    #     # [print(varr.solved, varr.name) for varr in variables]
        for i, var_ in enumerate(backup_var):
            if not variables[i].solved:
                variables[i] = var_
#self.solve_button.setEnabled()
    return dataSol, resultMenssage, True




@app.callback(
    [
        dash.dependencies.Output('table-vars','data'),
        dash.dependencies.Output('div-infoLabel','children')
    ],
    [
        dash.dependencies.Input('cajaTexto', 'value')
    ],
    [
        # dash.dependencies.State('cajaTexto','value')
    ],
    )
def actualizaInfo(cajaTexto):
        '''
        Actualiza la información del label inferior y de la lista interna de
        variables con respecto al sistema de ecuaciones que el usuario está
        ingresando
        '''
        if cajaTexto is None:
            # Evita que se ejecute el la función cuando es llamada sin data
            return dash.no_update, '0 ecuaciones / 0 variables'

        texto = cajaTexto.splitlines()
        # Ahora definir la cantidad de ecuaciones y de variables en la caja
        try:
            cantidad_eqn, var_reco = cantidadEqnVar(texto)
            cantidad_var = len(var_reco)
            a_mostrar = str(cantidad_eqn) + ' ecuaciones / '  + \
                str(cantidad_var) + ' variables'

            # Ahora actualizar la lista de variables si es necesario
            # Recordar que var_reco contiene las variables reconocidas en la
            # actualización.
            varsSelf = [obj.name for obj in variables]
            for varGUI in var_reco:
                if varGUI not in varsSelf:
                    # Si no está entonces agregar!
                    new_var = pyENL_variable(varGUI)
                    variables.append(new_var)
            # Si no está en var_reco pero está en self.variables...
            for i, varSelf in enumerate(variables):
                if varSelf.name not in var_reco:
                    variables.pop(i)


            dataVars=[{
            varsTitles[0]:var.name,
            varsTitles[1]:formateo.format(var.guess),
            varsTitles[2]:(var.lowerlim),
            varsTitles[3]:var.upperlim,
            varsTitles[4]:str(var.units),
            varsTitles[5]:var.comment,
            } for var in variables]
        except Exception as e:
            a_mostrar= 'Error encontrando cantidad de variables y de ecuaciones'
            dataVars = dash.no_update
        return dataVars, a_mostrar

############# Creo que todas las funciones de aquí pa bajo deberian estar en utils, no?

def imprimeSol(variables):
    '''
    Imprime en la pestaña de soluciones, las respuestas al sistema de
    ecuaciones ingresado por el usuario en la caja de texto que se usa para
    tal fin.
    '''
    dataSol=[{
                solTitles[0]:var.name,
                solTitles[1]:formateo.format(var.guess),
                solTitles[2]:str(var.units),
                solTitles[3]:var.comment
                } for var in variables]
    return dataSol

def quitaComentarios(eqns):
    '''
    Elimina los comentarios de la lista de ecuaciones para solucionar problema
    de que se muestren en la lista de residuos
    '''
    b = []
    for eqn in eqns:
        if ('<<' not in eqn) and not (eqn.replace(' ','').replace('\t', '') == ''):
            b.append(eqn)
    return b

if __name__ == '__main__':
    app.run_server(debug=True)