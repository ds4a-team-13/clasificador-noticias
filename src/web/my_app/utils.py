import sqlite3
import pandas as pd
import dash
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os

def inicializar_analisis_temporal():
    # Método que inicializa los dataframes, figuras, y opciones
    df_conteo = pd.read_csv('../../data/web/conteo_noticias.csv', nrows=100)
    df1 = pd.read_csv('../../data/web/news_categorized.csv', nrows=100)
    fig = px.line(df_conteo, x = "date_year_week", y="num_hechos",
        title='', color = 'cluster')
    fig.layout.plot_bgcolor = '#000000'
    fig.layout.paper_bgcolor = '#000000'
    lista_news_categoria_0 = []
    lista_anhos = df_conteo.year.unique()
    lista_semanas = range(1, 10)

    return df_conteo, df1, fig, lista_news_categoria_0, lista_anhos, lista_semanas


def read_news():
    path = os.path.dirname(os.path.abspath(__file__))
    # db_path = path + '/../../data/web/'
    # cnx = sqlite3.connect(db_path)
    # df = pd.read_sql_query("SELECT * FROM news", cnx)
    df = pd.read_csv(path + '/../../data/web/news_categorized.csv')
    # df.sort_values(by='Ranking', ascending=False, inplace=True)

    return df

def crear_listado_noticias(df, categoria, semana, anho):

    df1 = df[df['cluster']==categoria].copy()
    df1 = df1[df1['year']==anho]
    df1 = df1[df1['week']==semana]

    if df1.shape[0] > 0:
        listado = []
        for i in range(df1.shape[0]):
            titulo = df1['titulo'].iloc[i]
            titulo = titulo[:20] + '...'
            id_noticia = df1['ID'].iloc[i]
            listado.append({'label':titulo, 'value':id_noticia})
    else:
        # listado = [{'label':'No se encontraron noticias', 'value':1}]
        listado = [{'label':'No hay noticias', 'value':-1}]

    return listado

def get_geojson():
    path = os.path.dirname(os.path.abspath(__file__))
    return pd.read_json(path + '/../../data/web/departamentos.json')

def get_geojson_path():
    path = os.path.dirname(os.path.abspath(__file__))
    return path + '/../../data/web/departamentos.json'
