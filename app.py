import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash.exceptions

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define el layout de la ventana emergente
ventana_emergente = dbc.Modal(
    [
        dbc.ModalHeader(id='modal-titulo'),
        dbc.ModalBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Proyección de aguas grises reutilizadas"),
                                    dbc.CardBody(
                                        id='proyeccion-aguas-grises',
                                        children=[
                                            html.H4("¡Esta semana has reutilizado aproximadamente {} litros de aguas grises!".format(0)),
                                            html.Hr(),
                                            html.H4("Con un uso normal del agua, serás capaz de ahorrar:"),
                                            html.Ul([
                                                html.Li(id='ahorro-dia'),
                                                html.Li(id='ahorro-mes'),
                                                html.Li(id='ahorro-ano')
                                            ])
                                        ]
                                    ),
                                ],
                                className="my-2",  # Agrega margen en la parte superior e inferior
                                style={"background-color": "#E6F7FF", "border": "2px solid #3399FF", "color": "#003366", "font-size": "1.5em", "padding": "10px", "border-radius": "15px", "height": "400px"},
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Reducción del estrés hídrico"),
                                    dbc.CardBody(
                                        id='reduccion-estres-hidrico',
                                        children=[
                                            html.H4("Porcentaje de agua reutilizada en relación al consumo total: %G")
                                        ]
                                    ),
                                ],
                                className="my-2",  # Agrega margen en la parte superior e inferior
                                style={"background-color": "#E6F7FF", "border": "2px solid #3399FF", "color": "#003366", "font-size": "1.5em", "padding": "10px", "border-radius": "15px", "height": "400px"},
                            ),
                            width=6,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Ahorro económico proyectado"),
                                    dbc.CardBody(
                                        id='ahorro-economico-proyectado',
                                        children=[
                                            html.H4("Al día: ${}".format(0)),
                                            html.H4("Al mes: ${}".format(0)),
                                            html.H4("Al año: ${}".format(0))
                                        ]
                                    ),
                                ],
                                className="my-2",  # Agrega margen en la parte superior e inferior
                                style={"background-color": "#E6F7FF", "border": "2px solid #3399FF", "color": "#003366", "font-size": "1.5em", "padding": "10px", "border-radius": "15px", "height": "400px"},
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Potencial de riego de áreas verdes"),
                                    dbc.CardBody(
                                        id='potencial-riego-areas-verdes',
                                        children=[
                                            html.H4("Pasto: H m²"),
                                            html.H4("Especies nativas (ej: Quillay): I m²")
                                        ]
                                    ),
                                ],
                                className="my-2",  # Agrega margen en la parte superior e inferior
                                style={"background-color": "#E6F7FF", "border": "2px solid #3399FF", "color": "#003366", "font-size": "1.5em", "padding": "10px", "border-radius": "15px", "height": "400px"},
                            ),
                            width=6,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Reducción huella de carbono anual"),
                                    dbc.CardBody(
                                        id='reduccion-huella-carbono-anual',
                                        children=[
                                            html.H4("Reducción asociada al tratamiento de aguas residuales: J kg CO₂ eq"),
                                            html.H4("Reducción asociada a la producción de agua potable: K kg CO₂ eq"),
                                            html.H4("Reducción total huella de carbono: L kg CO₂ eq")
                                        ]
                                    ),
                                ],
                                className="my-2",  # Agrega margen en la parte superior e inferior
                                style={"background-color": "#E6F7FF", "border": "2px solid #3399FF", "color": "#003366", "font-size": "1.5em", "padding": "10px", "border-radius": "15px", "height": "400px"},
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            html.Div(
                            html.Img(
                                src="/assets/icon.png",  # Ruta de la imagen en la carpeta assets
                                style={
                                    "height": '250px',  # Ajusta el tamaño según sea necesario
                                    "width": '250px',  # Ajusta el tamaño según sea necesario
                                    "object-fit": "contain",  # Ajusta la imagen para que se vea bien en el contenedor
                                    "border-radius": "0px"  # Bordes redondeados para que coincidan con el estilo de las tarjetas
                                }
                            ),
                             style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100%",
                                    "width": "100%"
                                }
                            ),
                            width=6,
                        ),
                    ]
                ),
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Cerrar", id="cerrar-modal", className="ml-auto", n_clicks=0)
        ),
    ],
    id="modal",
    centered=True,
    size="xl",
    is_open=False
)

# Define el layout de la aplicación principal
app.layout = html.Div(style={'backgroundColor': '#ADD8E6', 'textAlign': 'center'}, children=[
    html.H1("Modelo de Valorización: Reutilización de aguas grises en recintos educacionales", style={'fontSize': '2.5em', 'color': '#000000', 'padding': '20px'}),
    # Espacio para mostrar mensajes de error
    html.Div(id={'type': 'mensaje-error', 'index': 0}),
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H3(
                        children='Selecciona tu escuela',
                        style={
                            'fontSize': '1.5em',  # Tamaño de fuente más grande
                            'color': '#000000',  # Color de texto negro
                            'text-align': 'left',  # Alineación del texto a la izquierda
                            'padding': '10px',  # Espacio entre la pregunta y la lista desplegable
                            'margin-top': '20px',  # Espacio entre el título y la pregunta
                        }
                    ),
                    dcc.Dropdown(
                        id={'type': 'dropdown', 'index': 0},
                        options=[
                            {'label': 'San Antonio de Naltagua', 'value': 'San Antonio de Naltagua'},
                            {'label': 'Colegio Challay', 'value': 'Colegio Challay'},
                            {'label': 'El Melocotón', 'value': 'El Melocotón'},
                            {'label': 'Liceo de Montenegro', 'value': 'Liceo de Montenegro'},
                            {'label': 'Escuela G-N°346 Santa Matilde', 'value': 'Escuela G-N°346 Santa Matilde'},
                            {'label': 'Escuela Básica G-N°348', 'value': 'Escuela Básica G-N°348'},
                            {'label': 'Escuela Básica G-N°352 Plazuela de Polpaico', 'value': 'Escuela Básica G-N°352 Plazuela de Polpaico'}
                        ],
                        placeholder="--Seleccionar--",
                        style={'width': '50%', 'color': '#555555', 'margin-left': '20px'}
                    ),
                ]
            ),
        ],
        style={'margin': '20px', 'border-radius': '15px', 'box-shadow': '5px 5px 5px #888888', 'backgroundColor': 'white'}
    ),
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H3(
                        children='Número de matrícula',
                        id={'type': 'pregunta-matricula', 'index': 0},
                        style={
                            'fontSize': '1.5em',  # Tamaño de fuente grande
                            'color': '#000000',  # Color de texto negro
                            'text-align': 'left',  # Alineación del texto a la izquierda
                            'padding': '10px',  # Más espacio entre las preguntas
                            'margin-top': '20px',  # Espacio entre las preguntas
                        }
                    ),
                    html.Div([
                        dcc.Input(
                            id={'type': 'matricula-input', 'index': 0},
                            type='number',
                            placeholder='Ingrese la matrícula',
                            style={'width': '30%', 'color': '#555555', 'margin-left': '20px', 'text-align': 'left',
                                   'border-radius': '10px', 'border': '1px solid #888888', 'padding': '10px',
                                   'font-size': '1em'}
                        )
                    ], style={'text-align': 'left', 'padding-left': '20px'})  # Estilo para alinear a la izquierda
                ]
            ),
        ],
        style={'margin': '20px', 'border-radius': '15px', 'box-shadow': '5px 5px 5px #888888', 'backgroundColor': 'white'}
    ),
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H3(
                        children='¿Cuántos días se han usado los lavamanos con normalidad en la última semana?',
                        id={'type': 'pregunta-dias', 'index': 0},
                        style={
                            'fontSize': '1.5em',  # Tamaño de fuente grande
                            'color': '#000000',  # Color de texto negro
                            'text-align': 'left',  # Alineación del texto a la izquierda
                            'padding': '10px',  # Espacio entre la pregunta y el dropdown
                            'margin-top': '20px',  # Espacio entre el título y la pregunta
                        }
                    ),
                    dcc.Dropdown(
                        id={'type': 'dropdown-dias', 'index': 0},
                        options=[{'label': str(i), 'value': i} for i in range(8)],
                        placeholder="Seleccione el número de días",
                        style={'width': '50%', 'color': '#555555', 'margin-left': '20px'}
                    ),
                    html.Br(),  # Línea de separación adicional
                    html.Button(
                        'Calcular',
                        id={'type': 'boton-calcular', 'index': 0},
                        n_clicks=0,
                        style={
                            'fontSize': '1em',  # Tamaño de fuente del botón
                            'color': '#ffffff',  # Color del texto del botón
                            'background-color': '#007bff',  # Color de fondo del botón
                            'border': 'none',  # Sin bordes
                            'padding': '10px 20px',  # Relleno del botón
                            'text-align': 'center',  # Alineación del texto en el centro
                            'text-decoration': 'none',  # Sin subrayado
                            'display': 'inline-block',  # Mostrar en línea
                            'margin': '10px 2px',  # Márgenes del botón
                            'cursor': 'pointer',  # Cambiar el cursor al pasar por encima
                            'border-radius': '10px'  # Bordes redondeados
                        }
                    )
                ]
            )
        ],
        style={'margin': '20px', 'border-radius': '15px', 'box-shadow': '5px 5px 5px #888888', 'backgroundColor': 'white'}
    ),
    ventana_emergente  # Incluye la ventana emergente en el layout
])

# Callback para abrir y actualizar el contenido de la ventana emergente
@app.callback(
    [
        Output('modal', 'is_open'),
        Output('modal-titulo', 'children'),
        Output('proyeccion-aguas-grises', 'children'),
        Output('reduccion-estres-hidrico', 'children'),
        Output('ahorro-economico-proyectado', 'children'),
        Output('potencial-riego-areas-verdes', 'children'),
        Output('reduccion-huella-carbono-anual', 'children'),
        Output({'type': 'mensaje-error', 'index': ALL}, 'children')
    ],
    [
        Input({'type': 'boton-calcular', 'index': ALL}, 'n_clicks'),
        Input("cerrar-modal", 'n_clicks')
    ],
    [
        State('modal', 'is_open'),
        State({'type': 'dropdown', 'index': 0}, 'value'),
        State({'type': 'matricula-input', 'index': 0}, 'value'),
        State({'type': 'dropdown-dias', 'index': 0}, 'value')
    ]
)
def actualizar_modal(n_clicks_calcular, n_clicks_cerrar, is_open, escuela, matricula, dias):
    ctx = callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    # Obtener el id del componente que ha desencadenado el callback
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Si el botón de cerrar ha sido presionado, cierra la ventana modal
    if triggered_id == "cerrar-modal":
        return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, [[]]

    # Si el botón de calcular ha sido presionado, realiza los cálculos y abre la ventana modal
    if not n_clicks_calcular or n_clicks_calcular[0] == 0:
        raise dash.exceptions.PreventUpdate

    # Validación de campos requeridos
    if not escuela or not matricula or dias is None:
        return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, [["Por favor complete todos los campos para continuar."]]

    # Lógica para calcular los valores
    agua_reutilizada = dias * (2.2432 * matricula + 29.563)
    ahorro_dia = 2.2432 * matricula + 29.563
    ahorro_mes = ahorro_dia * 20
    ahorro_ano = ahorro_mes * 10
    ahorro_economico_dia = ahorro_dia * 2
    ahorro_economico_mes = ahorro_mes * 2
    ahorro_economico_ano = ahorro_ano * 2
    reduccion_estres_hidrico = (ahorro_dia / (27 * matricula)) * 100
    riego_pasto = ahorro_dia / 10
    riego_nativas = ahorro_dia / 0.33
    huella_tratamiento = (ahorro_ano / 1000) * 0.325511442155919
    huella_produccion = (ahorro_ano / 1000) * 0.00342809683924821
    huella_total = huella_tratamiento + huella_produccion

    # Preparar el contenido de la ventana modal
    proyeccion_aguas_grises = [
        html.H4(f"¡Esta semana has reutilizado aproximadamente {int(agua_reutilizada)} litros de aguas grises!"),
        html.Hr(),
        html.H4("Con un uso normal del agua, serás capaz de ahorrar:"),
        html.Ul([
            html.Li(f"Al día: {int(ahorro_dia)} litros de agua"),
            html.Li(f"Al mes: {int(ahorro_mes)} litros de agua"),
            html.Li(f"Al año: {int(ahorro_ano)} litros de agua")
        ])
    ]

    reduccion_estres_hidrico = [
        html.H4(f"Porcentaje de agua reutilizada en relación al consumo total: {int(reduccion_estres_hidrico)}%")
    ]

    ahorro_economico_proyectado = [
        html.H4(f"Al día: ${int(ahorro_economico_dia)}"),
        html.H4(f"Al mes: ${int(ahorro_economico_mes)}"),
        html.H4(f"Al año: ${int(ahorro_economico_ano)}")
    ]

    potencial_riego_areas_verdes = [
        html.H4(f"Pasto: {int(riego_pasto)} m²"),
        html.H4(f"Especies nativas (ej: Quillay): {int(riego_nativas)} m²")
    ]

    reduccion_huella_carbono_anual = [
        html.H4(f"Reducción asociada al tratamiento de aguas residuales: {huella_tratamiento:.2f} kg CO₂ eq"),
        html.H4(f"Reducción asociada a la producción de agua potable: {huella_produccion:.2f} kg CO₂ eq"),
        html.H4(f"Reducción total huella de carbono: {huella_total:.2f} kg CO₂ eq")
    ]

    return (
        True,
        html.H3(f"Resultados para {escuela}", style={'fontSize': '2em'}),  # Ajusta el tamaño de la fuente aquí
        proyeccion_aguas_grises,
        reduccion_estres_hidrico,
        ahorro_economico_proyectado,
        potencial_riego_areas_verdes,
        reduccion_huella_carbono_anual,
        [[]]
    )



if __name__ == "__main__":
    app.run_server(debug=True)








#Crear layout
#header = dbc.Row([
 #       dbc.Col(html.H1('Modelo de Valorización: Reutilización de aguas grises en recintos educacionales', 
  #                      style={'fontSize': '3em', 'color': '#000000','margin-top':'2px', 'text-align': 'left'}), width=10),
   #     dbc.Col(html.Img(src="/assets/icon.png", height='180px'), style={'margin-top':'2px', 'text-align': 'right'}, width=2)
    #],
    #style={'backgroundColor': '#ADD8E6'},  # Color de fondo celeste para el rectángulo
    #className="mb-4"  # Margen inferior
#)   

#app.layout = html.Div([
 #   header,
  #  html.H2('Selección de Escuela'),
   # dcc.Dropdown(
    #    id='dropdown-escuela',
     #   options=[
      #      {'label':'--Seleccionar--','value':'__seleccionar__'},
       #     {'label': 'San Antonio de Naltahua', 'value': 'San Antonio de Naltahua'},
        #    {'label': 'Colegio Challay', 'value': 'Colegio Challay'},
         #   {'label': 'El Melocotón', 'value': 'El Melocotón'},
          #  {'label': 'Liceo de Montenegro', 'value': 'Liceo de Montenegro'},
           # {'label': 'Escuela G-N°346 Santa Matilde', 'value': 'Escuela G-N°346 Santa Matilde'},
            #{'label': 'Escuela Básica G-N°348', 'value': 'Escuela Básica G-N°348'},
            #{'label': 'Escuela Básica G-N°352 Plazuela de Polpaico', 'value': 'Escuela Básica G-N°352 Plazuela de Polpaico'},
        #],
        #value='__seleccionar__'
    #),
    #html.Div(id='output-escuela'),
    #html.Div(id='pregunta-matricula', style={'display': 'none', 'margin': '20px'}), 
    #dcc.Input(
     #   id='input-matricula',
      #  type='number',
       # style={'display': 'none'}
    #),

    #html.Div(id='pregunta-lavamanos', style={'display': 'none', 'margin': '20px'}),
    
    
    #dbc.Button('Valorizar', id='btn-valorizar', n_clicks=0, color='success', style={'margin-top': '20px'}),
    
    #dbc.Modal([
     #   dbc.ModalHeader(html.H4('Valorización de aguas grises reutilizadas', style={'font-size': '24px', 'font-weight': 'bold'})),
      #  dbc.ModalBody(id='modal-body'),
       # dbc.ModalFooter(
        #    dbc.Button('Cerrar', id='close-modal', className='ml-auto', n_clicks=0)
        #),
    #], id='modal', size='lg', is_open=False)
#])

#@app.callback(
 #   [Output('output-escuela', 'children'),
  #   Output('pregunta-matricula', 'children'),
   #  Output('pregunta-matricula', 'style'),
    # Output('input-matricula', 'style'),
     #Output('pregunta-lavamanos', 'children'),
     #Output('pregunta-lavamanos', 'style'),
     #Output('input-dias', 'style'),
     #Output('output-dias', 'children')],
    #[Input('dropdown-escuela', 'value')],
#)
#def update_output(escuela_value):
 #   if escuela_value == '__seleccionar__':
  #      return (
   #         'Selecciona una escuela',
    #        None,
     #       {'display': 'none'},
      #      {'display': 'none'},
       #     {'display': 'none'},
        #    None,
         #   {'display': 'none'},
          #  {'display': 'none'},
           # {'display': 'none'},
           # None
        #)

    #output_escuela = f'Has seleccionado la escuela: {escuela_value}'
    #pregunta_matricula = f'¿Cuál es la matrícula actual de alumnos en la escuela {escuela_value}?'
    #pregunta_matricula_style = {'display': 'block', 'margin': '20px'}
    #input_matricula_style = {'display': 'block'}

    #pregunta_lavamanos = '¿Cuántos días se ha utilizado con normalidad el lavamanos en la última semana?'
    #pregunta_lavamanos_style = {'display': 'block', 'margin': '20px'}
    #input_dias_style = {'display': 'block'}
    

    #return (
     #   output_escuela,
      #  pregunta_matricula,
       # pregunta_matricula_style,
       # input_matricula_style,
       # pregunta_lavamanos,
       # pregunta_lavamanos_style,
       # input_dias_style,
    #)

#@app.callback(
 #   [Output('modal', 'is_open'),
  #   Output('modal-body', 'children')],
   # [Input('btn-valorizar', 'n_clicks'),
    # Input('close-modal', 'n_clicks')],
   # [State('dropdown-escuela', 'value'),
   #  State('input-matricula', 'value'),
   #  State('input-dias', 'value')]
#)
#def valorizar(n_clicks_valorizar, n_clicks_cerrar, escuela_value, lavamanos_value, dias_value, matricula_value, dias_lavamanos):
 #   ctx = dash.callback_context
  #  triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
   # if triggered_id == 'btn-valorizar' and n_clicks_valorizar > 0:
    #    p = (dias_value/ 5 if dias_value else 0)
     #   x = int(matricula_value)
        
      #  litros_dia = p * (2.2432 * x + 29.563)
       # litros_semana = litros_dia * 5
        #litros_anio = litros_dia * 180
        
       # ahorro_dia = litros_dia * 2
        #ahorro_semana = (litros_dia * 5) * 2
        #ahorro_anio = (litros_dia * 180) * 2
        
       # reduccion_estres_hidrico = (litros_dia / (27 * x)) * 100
        
       # potencial_riego_pasto = litros_dia / 10
       # potencial_riego_especies = litros_dia / 0.33

       # reduccion_huella_aguaresidual = (litros_anio / 1000) * 0.325511442155919

       # reduccion_huella_aguapotable = (litros_anio/1000) * 0.00342809683924821

       # reduccion_huella_total = reduccion_huella_aguapotable + reduccion_huella_aguaresidual
        
       # modal_content = html.Div([
        #    dbc.Row([
         #       dbc.Col([
          #          html.H4('Proyección de aguas grises reutilizadas', className='mb-4', style={'color': 'white'}),
           #         html.H5('Litros de agua reutilizados al día:', className='mb-2', style={'color': 'white'}),
            #        html.P(format_number(litros_dia), style={'color': 'white','font-size': '18px'}), 
             #       html.H5('Litros de agua reutilizados a la semana:', className='mb-2', style={'color': 'white'}),
              #      html.P(format_number(litros_semana), style={'color': 'white','font-size': '18px'}),  
               #     html.H5('Litros de agua reutilizados al año:', className='mb-2', style={'color': 'white'}),
                #    html.P(format_number(litros_anio), style={'color': 'white','font-size': '18px'}),  
                #], style={'background-color': '#03045D', 'padding': '20px', 'border-radius': '10px'}),
                
                #dbc.Col([
                 #   html.H4('Ahorro económico proyectado', className='mb-4', style={'color': 'white'}),
                  #  html.H5('Al día:', className='mb-2', style={'color': 'white'}),
                   # html.P(f'${format_number(ahorro_dia)}', style={'color': 'white','font-size': '18px'}),
                   # html.H5('A la semana:', className='mb-2', style={'color': 'white'}),
                   # html.P(f'${format_number(ahorro_semana)}', style={'color': 'white','font-size': '18px'}),
                   # html.H5('Al año:', className='mb-2', style={'color': 'white'}),
                   # html.P(f'${format_number(ahorro_anio)}', style={'color': 'white','font-size': '18px'}),
               # ], style={'background-color': '#036566', 'padding': '20px', 'border-radius': '10px', 'margin-left': '20px'}),
           # ]),
           # dbc.Row([
            #    dbc.Col([
             #       html.H4('Reducción del estrés hídrico', className='mb-4', style={'color': 'white'}),
              #      html.P(f'Porcentaje de agua reutilizada en relación al consumo total: {reduccion_estres_hidrico:.2f} %', style={'color': 'white','font-size': '18px'}),
               # ], style={'background-color': '#034D94', 'padding': '20px', 'border-radius': '10px', 'margin-top': '20px'}),
                
               # dbc.Col([
                #    html.H4('Potencial de riego de áreas verdes', className='mb-4', style={'color': 'white'}),
                 #   html.P(f'-Pasto: {potencial_riego_pasto:.2f} m²', style={'color': 'white','font-size': '18px'}),
                  #  html.P(f'-Especies nativas (ej: Quillay): {potencial_riego_especies:.2f} m²', style={'color': 'white','font-size': '18px'}),
               # ], style={'background-color': '#2D897C', 'padding': '20px', 'border-radius': '10px', 'margin-top': '20px', 'margin-left': '20px'}),
           # ]),
           # dbc.Row([
            #    dbc.Col([
             #       html.H4('Reducción huella de carbono anual', className='mb-4', style={'color': 'white'}),
              #      html.P(f'-Reducción asociada al tratamiento de aguas residuales: {reduccion_huella_aguaresidual:.2f} kg CO₂ eq', style={'color': 'white','font-size': '18px'}),
               #     html.P(f'-Reducción asociada a la producción de agua potable: {reduccion_huella_aguapotable:.2f} kg CO₂ eq', style={'color': 'white','font-size': '18px'}),
                #    html.P(f'Reducción total huella de carbono: {reduccion_huella_total:.2f} kg CO₂ eq', style={'color': 'white','font-size': '20px'}),
               # ], style={'background-color': '#5E4B80', 'padding': '20px', 'border-radius': '10px', 'margin-top': '20px'}),
           # ]),
       # ])
        
      #  return True, modal_content
   # elif triggered_id == 'close-modal' and n_clicks_cerrar > 0:
    #    return False, None
   # return False, None

#Iniciar la aplicación

