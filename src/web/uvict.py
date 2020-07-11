import plotly.graph_objects as go
import dash
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np
from Mnoticias import *
import plotly.express as px
import pandas as pd
pd.options.plotting.backend = "plotly"

###############################################################
# VARIABLES GLOBALES
###############################################################
anho = -1
semana = -1
###############################################################

df_conteo = pd.read_csv('../../data/web/conteo_noticias.csv', nrows=100)
df = pd.read_csv('../../data/web/news_categorized.csv', nrows=100)
df['fecha_publicacion']=pd.to_datetime(df['fecha_publicacion'])
df['year']=df['fecha_publicacion'].dt.year
df['week']=df['fecha_publicacion'].dt.week
fig = px.line(df_conteo, x = "date_year_week", y="num_hechos",
    title='', color = 'cluster')
fig.layout.plot_bgcolor = '#000000'
fig.layout.paper_bgcolor = '#000000'
lista_news_categoria_0 = []
lista_news_categoria_1 = []
lista_news_categoria_2 = []
lista_news_categoria_3 = []
lista_anhos = df.year.unique()
lista_semanas = range(1, 10)
tituloNotica = "Titulo noticia"
fechaNoticia = "Fecha noticia"
cuerpoNoticia = "Cuerpo noticia"
urlNoticia = ""
valor_lista_cat_0 = -1
valor_lista_cat_1 = -1
valor_lista_cat_2 = -1
valor_lista_cat_3 = -1

#df_conteo, df1, fig, lista_news_categoria_0, lista_anhos, lista_semanas = inicializar_analisis_temporal

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
app.title='UVict'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Analisis Temporal", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Analisis espacial", href="#"),
                dbc.DropdownMenuItem("Análisis semántico", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="UVict",
    brand_href="#",
    color="primary",
    dark=True,
)

muestra_noticia = dbc.Container(children=[
    html.Br(),
    html.Div(children=[
        html.H3(
            "Titulo noticia",
            style={'text-align':'center',
                'width':700,
                'offset':1},
            id="Titulo noticia"
        ),
        dbc.Row(children=[
            dbc.Col(
                dcc.Markdown('**Fecha:**'),
                width={'size':'auto', 'offset':1}
            ),
            dbc.Col(html.P("fecha noticia",
                            id="fecha noticia"))
        ]),
        dbc.Row(children=[
            dbc.Col(
                dcc.Markdown("cuerpo noticia",
                            id="cuerpo noticia",
                            style={"overflow":"scroll",
                            "height":200,
                            "width":'auto'}),
                width={'size':10, 'offset':1}
            ),
            dbc.Col(width=1)
        ]),
        dbc.Row(children=[
            dbc.Col
                (
                    dcc.Link(children="hipervinculo",
                            href='',
                            target="_blank",
                            id="vinculo noticia"),
                    width={'size':'auto', 'offset':1}
                ),
        ])
    ], style={'border':'2px black solid', 'display':'none'},
    id='mostrar_noticia')
])

analisis_temporal = dbc.Container(children=[
    # EL LAYOUT ESTÁ PENSADO EN DOS FILAS
    # PRIMERA FILA CONTIENE EL GRAFICO
    # SEGUNDA FILA CONTIENE LAS CUATRO CATEGORIAS
    html.H2("Histórico de las noticias por categoría"),
    dbc.Row(children=[
        dcc.Graph(figure=fig)
    ]),
    html.Br(),
    html.Br(),
    dbc.Row(children=[
        dbc.Col(children=[
            html.H5("Categoria 0"),
            html.Br(),
            html.Div(children=[
            dbc.RadioItems(options=lista_news_categoria_0,
                id="noticias_categoria_0",
                style={"overflow":"scroll","height":200},
                value=-1
            )
            ], style={'border':'1px black solid'}),
            html.Br(),
            dcc.Dropdown(id="noticia_c0",
                options=[{'label':"Mostrar noticia", 'value':-1},
                    {'label':"Categoria 0", 'value':0},
                    {'label':"Categoria 1", 'value':1},
                    {'label':"Categoria 2", 'value':2},
                    {'label':"Categoria 3", 'value':3}],
                value=-1,
                disabled=True
            )
        ]),
        dbc.Col(children=[
            html.H5("Categoria 1"),
            html.Br(),
            html.Div(children=[
            dbc.RadioItems(options=lista_news_categoria_1,
                id="noticias_categoria_1",
                style={"overflow":"scroll","height":200},
                value=-1
            )
            ], style={'border':'1px black solid'}),
        ]),
        dbc.Col(children=[
            html.H5("Categoria 2"),
            html.Br(),
            html.Div(children=[
            dbc.RadioItems(options=lista_news_categoria_2,
                id="noticias_categoria_2",
                style={"overflow":"scroll","height":200},
                value=-1
            )
            ], style={'border':'1px black solid'}),
        ]),
        dbc.Col(children=[
            html.H5("Categoria 3"),
            html.Br(),
            html.Div(children=[
            dbc.RadioItems(options=lista_news_categoria_3,
                id="noticias_categoria_3",
                style={"overflow":"scroll","height":200},
                value=-1
            )
            ], style={'border':'1px black solid'}),
        ]),
        dbc.Col(children=[
            html.H5("Seleccione un año"),
            dcc.Dropdown(id="anho",
                options=[{"label":x,"value":x} for x in
                lista_anhos]),
            html.H5("Seleccione una semana"),
            dcc.Dropdown(id="semana",
                options=[{"label":x,"value":x} for x in
                lista_semanas])
        ])
    ]),
    dbc.Row(children=[
        html.Br(),
        muestra_noticia
        ]),
    dbc.Row(children=[
        html.P("OK", id="Prueba")
    ])
], style = {'height':'500vh'})

###############################################################
# AQUI EL LAYOUT
###############################################################

app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    ## Top
    html.H1(children = 'Repositorio de noticias',
        style = {'textAlign': 'center'}
    ),
    html.Br(),
    navbar,
    html.Br(),
    analisis_temporal,
])

#######################################################################
# CALLBACKS
#######################################################################
# Actualiza la lista desplegable de semana dependiendo del año seleccionado
@app.callback(Output('semana', 'options'), [Input('anho', 'value')])
def actualiza_semanas(valor):

    global lista_semanas
    global anho

    if valor:
        anho = valor
        lista_semanas = df[df['year']==anho].week.unique()
    return [{"label":x,"value":x} for x in lista_semanas]

# Actualiza la lista de noticias de cada categoria
# dependiendo de la semana seleccionada
@app.callback([Output('noticias_categoria_0', 'options'),
Output('noticias_categoria_1', 'options'),
Output('noticias_categoria_2', 'options'),
Output('noticias_categoria_3', 'options')], [Input('semana', 'value')])
def actualiza_semanas(valor):

    global lista_news_categoria_0
    global lista_news_categoria_1
    global lista_news_categoria_2
    global lista_news_categoria_3
    global semana
    global anho

    if valor:
        semana = valor
        lista_news_categoria_0 = crear_listado_noticias(df, 0, semana, anho)
        lista_news_categoria_1 = crear_listado_noticias(df, 1, semana, anho)
        lista_news_categoria_2 = crear_listado_noticias(df, 2, semana, anho)
        lista_news_categoria_3 = crear_listado_noticias(df, 3, semana, anho)

    return lista_news_categoria_0,\
            lista_news_categoria_1,\
            lista_news_categoria_2,\
            lista_news_categoria_3


# Se selecciona una noticia en las listas
# y se activa la lista desplegable de mostrar noticia
# y rellena el modal de mostrar noticia con la info de la noticia
@app.callback(Output('noticia_c0', 'disabled'),
    [Input('noticias_categoria_0', 'value'),
    Input('noticias_categoria_1', 'value'),
    Input('noticias_categoria_2', 'value'),
    Input('noticias_categoria_3', 'value')])
def activa_boton_c0(valor0, valor1, valor2, valor3):

    global tituloNotica
    global fechaNoticia
    global cuerpoNoticia
    global urlNoticia
    global valor_lista_cat_0
    global valor_lista_cat_1
    global valor_lista_cat_2
    global valor_lista_cat_3

    valor_lista_cat_0 = valor0
    valor_lista_cat_1 = valor1
    valor_lista_cat_2 = valor2
    valor_lista_cat_3 = valor3

    if valor0>=0:
        return False
    elif valor1>=0:
        return False
    elif valor2>=0:
        return False
    elif valor3>=0:
        return False
    else:
        return True


# # Activa la ventanita
@app.callback([Output('mostrar_noticia', 'style'),
    Output('Titulo noticia', 'children'),
    Output('fecha noticia', 'children'),
    Output('cuerpo noticia', 'children'),
    Output('vinculo noticia', 'children'),
    Output('vinculo noticia', 'href')],
    [Input('noticia_c0', 'value')])
def activa_modal_noticia(value):

    global tituloNotica
    global fechaNoticia
    global cuerpoNoticia
    global urlNoticia

    if value==0:
        valor = valor_lista_cat_0
    elif value==1:
        valor = valor_lista_cat_1
    elif value==2:
        valor = valor_lista_cat_2
    elif value==3:
        valor = valor_lista_cat_3

    try:
        tituloNotica = df[df['ID']==valor].titulo
        fechaNoticia = df[df['ID']==valor].fecha_publicacion
        cuerpoNoticia = df[df['ID']==valor].cuerpo.values[0]
        urlNoticia = df[df['ID']==valor].url.values[0]
    except:
        tituloNotica = "Titulo noticia"
        fechaNoticia = "Fecha noticia"
        cuerpoNoticia = "Cuerpo noticia"
        urlNoticia = ""

    if value and value>=0:
        return {'border':'2px black solid', 'display':'block'},\
            tituloNotica, fechaNoticia, cuerpoNoticia, urlNoticia, urlNoticia

    else:
        return {'border':'2px black solid', 'display':'none'},\
            tituloNotica, fechaNoticia, cuerpoNoticia, urlNoticia, urlNoticia


if __name__ == '__main__':
    app.run_server(debug=True)
