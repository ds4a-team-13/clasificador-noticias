#####
import os
# path of work
ruta = 'D:/Documentos/Sebastian/01_CURSOS_VISTOS/02_CURSOS_ONLINE/202005_DATA_SCIENCE/final_project/clasificador-noticias'
os.chdir(ruta)
#####

from src.featuring.requirements import *
from src.featuring.process_filter_data import filter_data
from src.featuring.process_clean_text import master_clean_text
from src.featuring.process_ubication import master_ubication

cnx = sqlite3.connect('data/scraper/data.db')
df  = pd.read_sql_query("SELECT * FROM news", cnx)

df = filter_data(df)
df = master_clean_text(df)
df = master_ubication(df)

