from dash.dependencies import Output, Input
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import random
import json


df = pd.read_pickle('../../data/web/news_dptos.pickle')
df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])

# Generate random class
df['cat'] = df['url'].apply(lambda x: random.randint(1, 4))
data = None

with open('../../data/web/deptos.json') as response:
    dptos = json.load(response)


def register_callbacks(app):
  
  @app.callback(
	    Output("map", "children"),
	    [
	        Input('my-date-picker-range', 'start_date'),
	        Input('my-date-picker-range', 'end_date'),
	        Input('clase', 'value'),
	    ],
	)
  def generate_map(date_start, date_end, cat):
    global df, data

    criteria = df['fecha_publicacion'] >= date_start 
    criteria &= df['fecha_publicacion'] <= date_end
    if cat:
      criteria &= (df['cat'] == cat)

    data = df[criteria].groupby('departamentos').agg({'fid':'min', 'url':'size'})

    fig = px.choropleth_mapbox(data, geojson=dptos, locations='fid', color='url', featureidkey='properties.DPTO',
                           color_continuous_scale="Viridis",
                           range_color=(0, data['url'].max()),
                           mapbox_style="carto-positron",
                           zoom=4, center = {"lat": 4.90, "lon": -74.16},
                           opacity=0.5,
                           labels={'url':'cantidad de noticias'}
                          )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return dcc.Graph(figure=fig)

  
  @app.callback(
	    Output("wordscloud", "children"),
	    [
	        Input('map', 'children'),
	    ],
	)
  def generate_wordcloud(map):
    print(data.shape)
    return "actualizado"