import sqlite3
import pandas as pd
import dash
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def read_news():
    cnx = sqlite3.connect('data.db')
    df = pd.read_sql_query("SELECT * FROM news", cnx)

    return df

def crear_listado_noticias(df, listado):

    for i in range(df.shape[0]):
        listado.append(dbc.ListGroupItem(
            df['titulo'].loc[i])
            id="noticia_" + str(i)
            )

    return listado
