import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import State, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

from datetime import datetime as dt
from datetime import timezone
import re


######## COMPONENTS

paragraph1 = "Este citio es una herramienta diseñada para mejorar la intervención humanitaria de emergencia del Estado, con el apoyo del personal profesional de la Unidad de Victimas que actualiza una bitacora de eventos, identificando, recopilando y clasificando manualmente los eventos relacionados con la dinámica de la violencia del conflicto armado que se informa en los noticieros nacionales y locales. Esta herramienta de aprendizaje automático  recoge noticias digitales y las relaciona con una probabilidad de categorización en algunos de los eventos victimizantes."

hechos = ["Hechos contra la población","Acciones armadas","Acciones Institucionales","Otros tipos"]

section2 = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Row([
                dbc.Col(html.Div(
                [
                    html.Div(
                        [
                            html.P(paragraph1),
                            html.P("Entre las distintas categorías podemos encontrar:"),
                            html.Ul(id='my-list', children=[html.Li(i) for i in hechos]),
                            html.P("Basados en estas categorias, se crearon agrupamientos basados en similitures entre las noticias, como se puede observar a continuación.")
                        ]
                    )
                ],),md=6),
                dbc.Col(html.Div(id="categories"),md=6)
                ])
            ]
        ),
    ],
    body=True,
)


section3 = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Row([
                html.P("Se pudo agrupar las notas en 8 grupos, los cuales estaban asociados, en cierta medida, a alguna de las categorías mencionadas. Esto se puede comprobar viendo la nube de palabras asociada a cada uno de ellos."),
                dbc.Col(html.Div(id="umap"),md=6),
                dbc.Col(html.Div(id="wordclouds"),md=6)
                ])
            ]
        ),
    ],
    body=True,
)


section4 = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Row([
                html.P("Sobre los diarios, las siguientes gráficas muestan una breve descripción de la información que se pudo obtener de ellos para los análisis realizados:"),
                dbc.Col(html.Div(id="boxplot"),md=6),
                dbc.Col(html.Div(id="serie"),md=6)
                ])
            ]
        ),
    ],
    body=True,
)



###### VISUALIZATION
content = dbc.Container(
    [
        html.Div(id='none',children=[],style={'display': 'none'}),
        dbc.Row([section2],align="center",),
        dbc.Row([section3],align="center",),
        dbc.Row([section4],align="center",),
    ],
    fluid=True,
)
