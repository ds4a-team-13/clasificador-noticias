import plotly.graph_objects as go
import dash
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np
from Mnoticias import *

df = read_news()
df = df.iloc[0:10]

external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
app.title='UVict'
mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

lista_news = []
categoria_noticia = 'HECHO ARMADO'
probabilidad_noticia = '(90%)'
titulo_noticia = 'TITULO DE LA NOTICIA'
fecha_noticia = 'HOY'
cuerpo_noticia = 'En el dia de hoy se inicio por primera vez'
cuerpo_noticia += ' el arduo trabajo de consolidar un borrador'
cuerpo_noticia += ' del front-end para el repositorio de noticias.'
hiper_vinculo_noticia = 'http://aqui_vamos.com'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

departamentos = get_geojson()
print("t: ", departamentos.shape)
import plotly.express as px

"""
fig = px.scatter_mapbox(departamentos, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
"""

fig = px.scatter_mapbox(center=dict(lat=38.72490, lon=-95.61446,), zoom=3, height=300)
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "sourcetype": "geojson",
            "source": [ get_geojson_path()]
        }
      ])

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


analisis_temporal = dbc.Container(children=[
    # EL LAYOUT ESTÁ PENSADO EN TRES FILAS, CADA UNA CON TRES COLUMNAS
    dbc.Row(children=[
        dbc.Col(html.P('COLUMNA1'),
                width=2
        ),
        dbc.Col(width=3,
            children=[
            html.H5('Listado de noticias'),
            dbc.RadioItems(options=lista_news,
                id="Listado_noticias",
                style={"overflow":"scroll","height":500},
                value=-1
            )
        ]),
        dbc.Col(width=7,
            children=
            [
                dbc.Row(children=
                    [
                        dbc.Col
                            (
                                html.H5('Clasificacion de la noticia:'),
                                width={'size':'auto', 'offset':0}
                            ),
                        dbc.Col
                            (
                                html.H5(categoria_noticia),
                                width='auto'
                            ),
                        dbc.Col
                            (
                                html.H5(probabilidad_noticia),
                                width={'offset':0}
                            )
                    ]),
                html.Div(children=
                    [
                        html.Br(),
                        html.H3(
                                    titulo_noticia,
                                    style={'text-align':'center',
                                            'width':700,
                                            'offset':1},
                                    id="Titulo noticia"
                                ),
                        dbc.Row(children=
                            [
                                dbc.Col
                                    (
                                        dcc.Markdown('**Fecha:**'),
                                        width={'size':'auto', 'offset':1}
                                    ),
                                dbc.Col(html.P(fecha_noticia,
                                                id="fecha noticia"))
                            ]),
                        dbc.Row(children=
                            [
                                dbc.Col
                                    (
                                        dcc.Markdown(cuerpo_noticia,
                                                    id="cuerpo noticia",
                                                    style={"overflow":"scroll",
                                                    "height":200,
                                                    "width":'auto'}),
                                        width={'size':10, 'offset':1}
                                    ),
                                dbc.Col(width=1)
                            ]),
                        dbc.Row(children=
                            [
                                dbc.Col
                                    (
                                        dcc.Link(children=hiper_vinculo_noticia,
                                                href='',
                                                target="_blank",
                                                id="vinculo noticia"),
                                        width={'size':'auto', 'offset':1}
                                    ),
                                dbc.Col(dcc.Markdown('''
                                        [hiper_vinculo_noticia](hiper_vinculo_noticia)
                                        ''')
                                    )
                            ]
                        )
                    ],
                    style={'border':'1px black solid'}
                )
            ]
        )
    ]),
    html.Br(),
    dbc.Row(children=
        [
            dbc.Col(html.P('OK'), width=2),
            dbc.Col(dbc.Button(
                                "Obtener noticias",
                                outline=True,
                                id="Obtener noticias",
                                color="primary"
                              )
                    ),
            dbc.Col(children=
                [
                    dbc.Button(
                        "Noticia anterior",
                        outline=True,
                        disabled=True
                    ),
                    dbc.Button(
                        "Siguiente noticia",
                        outline=True,
                        disabled=True
                    )
                ]),
            dbc.Col(width=1)
        ]
    ),
    dcc.Graph(figure=fig),

])

app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    ## Top
    html.H1(children = 'Repositorio de noticias',
        style = {'textAlign': 'center'}
    ),
    html.Br(),
    navbar,
    html.Br(),
    analisis_temporal
])

# Pone las noticias en la lista
@app.callback(Output('Listado_noticias', 'options'), [Input('Obtener noticias', 'n_clicks')])
def on_button_click(n_clicks):

    global lista_news
    global df

    if n_clicks is None:
        return lista_news
    else:
        lista_news = []
        return crear_listado_noticias(df, lista_news)

# Pone la noticia seleccionada en la ventanita
@app.callback([
    Output('Titulo noticia', 'children'),
    Output('fecha noticia', 'children'),
    Output('cuerpo noticia', 'children'),
    Output('vinculo noticia', 'children'),
    Output('vinculo noticia', 'href')
], [Input('Listado_noticias', 'value')])
def on_button_click(valor):
    if valor>=0:
        return df['titulo'].iloc[valor],\
                df['fecha_publicacion'].iloc[valor],\
                df['cuerpo'].iloc[valor],\
                df['url'].iloc[valor],\
                df['url'].iloc[valor]
    else:
        return titulo_noticia,\
                fecha_noticia,\
                cuerpo_noticia,\
                hiper_vinculo_noticia,\
                hiper_vinculo_noticia


if __name__ == '__main__':
    app.run_server(debug=True)
