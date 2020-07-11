import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

import geopandas as gpd
from unidecode import unidecode
import pandas as pd
import json


df = pd.read_csv('../../data/web/news_dptos.csv')
with open('../../data/web/deptos.json') as response:
    dptos = json.load(response)

data = df.groupby('departamentos').agg({'fid':'min', 'url':'size'})

fig = px.choropleth_mapbox(data, geojson=dptos, locations='fid', color='url', featureidkey='properties.DPTO',
                           color_continuous_scale="Viridis",
                           range_color=(0, 5000),
                           mapbox_style="carto-positron",
                           zoom=4, center = {"lat": 4.90, "lon": -74.16},
                           opacity=0.5,
                           labels={'url':'cantidad de noticias'}
                          )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

content = dbc.Container(children=[
  dcc.Graph(figure=fig)  
])