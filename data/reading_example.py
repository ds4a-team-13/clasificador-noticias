import sqlite3
import pandas as pd

cnx = sqlite3.connect('data.db')
df = pd.read_sql_query("SELECT * FROM news", cnx)

print(df.head())