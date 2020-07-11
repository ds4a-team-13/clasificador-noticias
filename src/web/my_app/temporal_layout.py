import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df_conteo = pd.read_csv('../../data/web/conteo_noticias.csv', nrows=100)
df = pd.read_csv('../../data/web/news_categorized.csv', nrows=100)
df['fecha_publicacion']=pd.to_datetime(df['fecha_publicacion'])
df['year']=df['fecha_publicacion'].dt.year
df['week']=df['fecha_publicacion'].dt.week

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

fig = px.line(df_conteo, x = "date_year_week", y="num_hechos",
    title='', color = 'cluster')
fig.layout.plot_bgcolor = '#000000'
fig.layout.paper_bgcolor = '#000000'


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

content = dbc.Container(children=[
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
