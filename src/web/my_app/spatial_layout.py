import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from datetime import datetime as dt
from datetime import timedelta

import geopandas as gpd
from unidecode import unidecode
import pandas as pd
import random

df = pd.read_pickle('../../data/web/news_dptos.pickle')
df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])
df['class'] = df['url'].apply(lambda x: random.randint(1, 4))

content = dbc.Container(children=[

  html.Div(className="row", children=[
    html.Div(className="col-1"),
    html.Div(className="col-5", children=[
      html.P('Rango de fechas:'),
      dcc.DatePickerRange(
          id='my-date-picker-range',
          min_date_allowed=df['fecha_publicacion'].min().date(),
          max_date_allowed=df['fecha_publicacion'].max().date(),
          initial_visible_month=dt(2019, 1, 1),
          start_date=df['fecha_publicacion'].max() - timedelta(days=10),
          end_date=df['fecha_publicacion'].max().date()
        ),
    ]),
    html.Div(className="col-5", children=[
      dbc.Label("Clase"),
      dcc.Dropdown(
          id="clase",
          options=[
              {"label": col, "value": col} for col in df['class'].unique()
          ],
          value=1,
      ),
    ]),
    html.Div(className="col-1"),
  ]),

  html.Div(id="main-container", className="row", children=[
    html.Div(className="col-1"),
    html.Div(className="col-5", id="map"),
    html.Div(id="wordscloud", className="col-5", children=['Nube de palabras']),
    html.Div(className="col-1"),
  ]),
  
  
])