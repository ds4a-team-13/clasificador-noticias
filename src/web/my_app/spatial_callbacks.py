from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from datetime import datetime as dt
from unidecode import unidecode
from datetime import timedelta
from wordcloud import WordCloud
import geopandas as gpd
from io import BytesIO
import pandas as pd
import random, json
import base64
import dash

import my_app.utils as utils

dptos_path = '../../data/web/deptos.json'
gdf = gpd.read_file(dptos_path)
gdf['nombre'] = gdf['NOMBRE_DPT'].apply(unidecode).str.lower()
dptos_ids = {n: fid for i, n, fid in gdf[['nombre', 'DPTO']].itertuples()}

with open(dptos_path) as response:
    dptos = json.load(response)


def register_callbacks(app):

  @app.callback(
      Output('spatial_data', 'data'), 
      [
        Input('date-picker', 'start_date'), 
        Input('date-picker', 'end_date'), 
        Input('class-picker', 'value'),
        Input('map-object', 'clickData'),
        Input('dptos_data', 'data'),
        Input('url', 'pathname')
      ]
  )
  def initialize_selected_dpt(start_date, end_date, category, clickData, dptosData, pathname):
    ctx = dash.callback_context
    data = {}
    print('>> seting data')

    triggers = [x['prop_id'] for x in ctx.triggered]
    
    data['start_date'] = start_date
    data['end_date']   = end_date
    data['category']   = category
    
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    print(triggers)
    if "map-object.clickData" in triggers:
      idx = clickData['points'][0]['pointIndex']
      data['dpto_index'] = idx
    
    print(data)
    return data

  @app.callback(
      [
        Output('date-picker', 'min_date_allowed'), 
        Output('date-picker', 'max_date_allowed'), 
        Output('date-picker', 'start_date'), 
        Output('date-picker', 'end_date'), 
        Output('date-picker', 'initial_visible_month'), 
      ],
      [Input('url', 'pathname')]
  )
  def load_date_picker(pathname):
      query = '''select min(fecha_publicacion) as min_date, 
                 max(fecha_publicacion) as max_date from featuring_all LIMIT 1'''
      data = utils.db_get_df(query)
      data['min_date'] = pd.to_datetime(data['min_date'])
      data['max_date'] = pd.to_datetime(data['max_date'])
      
      data = data.iloc[0]
      initial_date = data['max_date'] - timedelta(days=10)
      
      return data['min_date'].date(),\
             data['max_date'].date(),\
             initial_date,\
             data['max_date'].date(),\
             initial_date


  @app.callback(
      [
        Output('class-picker', 'options'), 
        Output('class-picker', 'value'),
      ], 
      [Input('url', 'pathname')]
  )
  def load_date_picker(pathname):
    data = utils.db_get_df('SELECT DISTINCT(category_bl) as classes FROM featuring_all')
    return [ {"label": col, "value": col} for col in sorted(data['classes'].values)], 1
  
    
  @app.callback(
      [
	        Output("wordscloud", "children"),
          Output("map-object", "figure"),
      ],
	    [
	        Input('spatial_data', 'data'),
	    ],
	)
  def generate_graphics(data):
    fig_map, dptos_data = generate_map(data['start_date'], data['end_date'], data['category'])
    wordcloud = generate_wordcloud(data)

    return wordcloud, fig_map


  def generate_wordcloud(data):
    print('in', data)
    where_cond = generate_where_cond(data['start_date'], data['end_date'], data['category'])
    query = f"""
              SELECT pre_clean_text, departamentos, url
              FROM featuring_all  
              {where_cond}
            """

    dpto_index = data.get('dpto_index', -1)
    data = utils.db_get_df(query)

    if dpto_index != -1:
      dptos = proccess_dptos(data.copy())
      dpto = dptos.iloc[dpto_index].name

      print(data.shape)
      data = data.query('departamentos == @dpto')
      print(data.shape)


    common_words = utils.get_top_n_words(data['pre_clean_text'], 100, 1)
    frequencies = {x[0]:x[1] for x in common_words}
    wc = WordCloud(background_color='white').generate_from_frequencies(frequencies=frequencies)
    
    wc_img = wc.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        img2 = base64.b64encode(buffer.getvalue()).decode()

    return html.Img(src="data:image/png;base64," + img2)
           
    
  def generate_map(start_date, end_date, cat):
    where_cond = generate_where_cond(start_date, end_date, cat)
    query = f"""
          SELECT titulo, url, departamentos 
          FROM featuring_all  
          {where_cond}
        """

    data = utils.db_get_df(query)
    data = proccess_dptos(data)
    
    fig = px.choropleth_mapbox(
              data,
              geojson=dptos, 
              locations='fid', 
              color='url', 
              featureidkey='properties.DPTO',
              color_continuous_scale="Viridis",
              range_color=(0, data['url'].max()),
              mapbox_style="carto-positron",
              zoom=4, 
              center = {"lat": 4.90, "lon": -74.16},
              opacity=0.5,
              labels={'url':'cantidad de noticias'}
          )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig, {'dptos': data.index.values}


  def proccess_dptos(data):
    data = data[~data['departamentos'].fillna('').str.contains('\|')]
    data = data.dropna(subset=['departamentos'])

    data['departamentos'] = data['departamentos'].str.replace('guania','guainia')\
                                                .str.replace('bogota', 'cundinamarca')\
                                                .str.replace('guajira', 'la guajira')

    data['fid'] = data['departamentos'].apply(lambda x: dptos_ids.get(x, -1))
    data = data.groupby('departamentos').agg({'fid':'min', 'url':'size'})
    return data.sort_index()


  
  def generate_where_cond(date_start, date_end, cat):
    class_cond = f"AND category_bl = {cat}" if cat != None else "" 
    where_cond = f"""
          WHERE strftime('%Y-%m-%d', fecha_publicacion) >= strftime('%Y-%m-%d', \'{date_start}\')
                AND strftime('%Y-%m-%d', fecha_publicacion) <= strftime('%Y-%m-%d', \'{date_end}\')
                {class_cond}
        """

    return where_cond
