import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from datetime import datetime as dt

content = dbc.Container(children=[

  dcc.Store(id='spatial_data'),
  dcc.Store(id='dptos_data'),

  html.Div(className="row", children=[
    html.Div(className="col-1"),
    html.Div(id='date-picker-container', className="col-5", children=[
      html.P('Rango de fechas:'),
      dcc.DatePickerRange(id='date-picker'),
    ]),
    html.Div(id='class-picker-container', className="col-5", children=[
      dbc.Label("Clase"),
      dcc.Dropdown(id="class-picker"),
    ]),
    html.Div(className="col-1"),
  ]),

  html.Div(id="main-container", className="row", children=[
    html.Div(className="col-1"),
    html.Div(className="col-5", children=[
      dcc.Graph(id='map-object',)
    ]),
    html.Div([dcc.Graph( id='wordscloud' ),]),
    html.Div(className="col-1"),
  ]),
    
])