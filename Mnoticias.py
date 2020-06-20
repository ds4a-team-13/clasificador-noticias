import sqlite3
import pandas as pd

def read_news():
    cnx = sqlite3.connect('../data.db')
    df = pd.read_sql_query("SELECT * FROM news", cnx)

    return df
