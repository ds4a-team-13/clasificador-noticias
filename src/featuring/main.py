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
from src.featuring.process_tags_spanish import master_tags_spanish

cnx = sqlite3.connect('data/scraper/data.db')
df  = pd.read_sql_query("SELECT * FROM news", cnx)

df = filter_data(df)
df = master_clean_text(df)
df = master_ubication(df)

df.to_csv('data/featuring/data_featuring.txt', sep = '|', index = False)

### tags
df = pd.read_csv('data/featuring/data_featuring.txt', sep = '|')
df.set_index(['id'], inplace = True)

tags_pos = master_tags_spanish(df['pre_clean_text'])

type(tags_pos)

a_file = open("data/featuring/data_tags_pos.pkl", "wb")
pickle.dump(tags_pos, a_file)
a_file.close()

file_pos = open("data/featuring/data_tags_pos.pkl", "rb")
tag = pickle.load(file_pos)
file_pos.close()
