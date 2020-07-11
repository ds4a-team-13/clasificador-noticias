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

controls = dbc.Card(
    [
        dbc.FormGroup([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=dt(2000, 8, 5),
                max_date_allowed=dt(2019, 2, 1),
                initial_visible_month=dt(2019, 1, 1),
                start_date=dt(2018, 12, 1).date(),
                end_date=dt(2019, 1, 7).date()
            ),
            html.Div(id='output-container-date-picker-range')
        ]),
        dbc.FormGroup(
            [
                dbc.Label("Clase"),
                dcc.Dropdown(
                    id="clase_value",
                    options=[
                        {"label": col, "value": col} for col in [1,2,3,4]
                    ],
                    value=1,
                ),
            ]
        ),
    ],
    body=True,
)

###### VISUALIZATION
content = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

