#%%

import pandas as pd
import sqlite3

cnx = sqlite3.connect('../data/data.db')
df = pd.read_sql_query("SELECT * FROM news", cnx)

df.groupby('diario').agg({'fecha_publicacion':['min', 'max'], 'url':'size'})

#%%

import pandas as pd

df = pd.read_csv('news.csv')
df['url'].apply(lambda x: x.split('.com')[0]).value_counts()