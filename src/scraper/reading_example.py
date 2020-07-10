#%%

import pandas as pd
pd.options.display.max_columns = None
import sqlite3

#####
import os
# path of work
ruta = 'D:/Documentos/Sebastian/01_CURSOS_VISTOS/02_CURSOS_ONLINE/202005_DATA_SCIENCE/final_project/clasificador-noticias/data'
os.chdir(ruta)
#####

cnx = sqlite3.connect('../data/data.db')

#def delete_all_news(conn):
#    """
#    Delete all rows in the tasks table
#    :param conn: Connection to the SQLite database
#    :return:
#    """
#    sql = 'DELETE FROM news'
#    cur = conn.cursor()
#    cur.execute(sql)
#    conn.commit()
#	
#delete_all_news(cnx)

df = pd.read_sql_query("SELECT * FROM news", cnx)

print(df.shape)
print(df['diario'].unique())

(
 df
 .groupby('diario')
 .agg({'fecha_publicacion': ['min', 'max'], 
	   'url': 'size'})
)


df['year'] = df['fecha_publicacion'].str[:4]
df['year'].value_counts()

# filtering dates out of analysis
df = df.query('year >= "2012"')
df = df.query('year != "2999"')

df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])

df.info()

#%%

import pandas as pd

df = pd.read_csv('news.csv')
df['url'].apply(lambda x: x.split('.com')[0]).value_counts()