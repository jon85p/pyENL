# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import utils


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title ='pYENL web'
app.layout = html.Div(children=[


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
                    ], )
                       
                ,
                )),
            dbc.Col(
                [
                    dbc.Row(html.Div(children=
                            [
                                    dash_table.DataTable(
                                        columns=[{"name": i, "id": str(i)} for i in utils.varsTitles],
                                        style_header={'backgroundColor':'white',
                                                    #'fontWeight':'bold'
                                        },
                                        fixed_rows={'headers':True,'data':0},
                                        style_cell= {'font_family':'Helvetica',
                                                    'font_size':'14px',
                                                    'textAlign':'center'
                                        }
                                    )
                            ],style={ 'height':'40vh','width':'100%'})
                    #,style={'width':'90%'}
                    ),
                    dbc.Row(html.Div(children=
                            [
                                    dash_table.DataTable(
                                        columns=[{"name": i, "id": str(i)} for i in utils.solTitles],
                                        style_header={'backgroundColor':'white',
                                                    #'fontWeight':'bold'
                                        },
                                        fixed_rows={'headers':True,'data':0},
                                        style_cell= {'font_family':'Helvetica',
                                                    'font_size':'14px',
                                                    'textAlign':'center'
                                        }
                                    )
                            ],style={ 'height':'40vh','width':'100%'}),
                    #style={'width':'90%'},
                   )
                ], style={'padding-left':'0px','padding-right':'0px',}
            ),


        ], style={'width':'100%'}
    ),
    ],
    ),

    html.Div(
        html.Button('Resolver',style={'width':'100%'}),
        )
],

)

if __name__ == '__main__':
    app.run_server(debug=True)