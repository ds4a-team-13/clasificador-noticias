import sqlite3
import pandas as pd
import dash
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

path = os.path.dirname(os.path.abspath(__file__))

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


def db_get_df(query):
    global path
    db_path = path + '/../../../data/data_featuring.db'
    
    cnx = sqlite3.connect(db_path)
    return pd.read_sql_query(query, cnx)

# Following code grabbed from:
# https://towardsdatascience.com/a-complete-exploratory-data-analysis-and-visualization-for-text-data-29fb1b96fb6a
# we will use it in our context to create some visualizations.
def get_top_n_words(corpus, n=1,k=1):
    swords = stopwords.words('spanish')

    vec = CountVectorizer(ngram_range=(k,k),stop_words=swords).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]
