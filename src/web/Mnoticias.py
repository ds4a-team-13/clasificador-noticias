import sqlite3
import pandas as pd
import dash
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os


def read_news():
    path = os.path.dirname(os.path.abspath(__file__))
    # db_path = path + '/../../data/web/'
    # cnx = sqlite3.connect(db_path)
    # df = pd.read_sql_query("SELECT * FROM news", cnx)
    df = pd.read_csv(path + '/../../data/web/news_categorized.csv')
    # df.sort_values(by='Ranking', ascending=False, inplace=True)

    return df

def crear_listado_noticias(df, listado):

    for i in range(df.shape[0]):
        # listado.append(dbc.ListGroupItem(df['titulo'].loc[i]))
        listado.append({'label':df['titulo'].loc[i], 'value':i})

    return listado
