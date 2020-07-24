######
import os
# path of work
ruta = 'D:/Documentos/Sebastian/01_CURSOS_VISTOS/02_CURSOS_ONLINE/202005_DATA_SCIENCE/final_project/clasificador-noticias'
os.chdir(ruta)
######

from src.featuring.import_packages import *
from src.featuring.process_filter_data import filter_data
from src.featuring.process_clean_text import master_clean_text
from src.featuring.process_ubication import master_ubication
from src.featuring.process_tags_spanish import master_tags_spanish

# =============================================================================
# 
# =============================================================================
cnx = sqlite3.connect('data/scraper/data.db')
df  = pd.read_sql_query("SELECT * FROM news", cnx)

df = filter_data(df)

# =============================================================================
# 
# =============================================================================
df = pd.read_csv('data/featuring/data_featuring.txt', sep = '|')
df.head()

df = master_clean_text(df)

df.info()

all_text = ' '.join(df['text_for_embedding'])
all_text_list = all_text.split()
len(all_text_list)

count_words = pd.Series(all_text_list).value_counts()

count_words[:50]
#count_words[50:100]

stopwords_complement = pd.read_csv('data/external/stopwords_complement.txt', sep = '|')
stopwords_complement = list(stopwords_complement['stopwords'])

aux = df['text_for_embedding'].copy()
df['text_for_embedding'] = aux.str.split().apply(lambda x: ' '.join([word for word in x if word not in stopwords_complement]))

len_x = df['text_for_embedding'].apply(len)

len_x.describe()
len_x.quantile(np.arange(0, 1.1, 0.1))

df.to_csv('data/featuring/data_featuring.txt', sep = '|', index = False)

# =============================================================================
# 
# =============================================================================
df = pd.read_csv('data/featuring/data_featuring.txt', sep = '|')
df.head()

df1 = master_ubication(df)

#df['departamentos'].isnull().sum()
#(df1['departamentos'] == '').sum()
#len_depto = df1['departamentos'].str.split('|').apply(len)
#len_depto[df1['departamentos'] == ''] = 0
#len_depto.value_counts() / len_depto.value_counts().sum()
#
#df1['departamentos'].value_counts()
#df1['departamentos'][len_depto == 1].value_counts().sum()

#df['municipios'].fillna('', inplace = True)
#len_muni = df1['municipios'].str.split('|').apply(len)
#len_muni[df1['departamentos'] == ''] = 0
#len_muni.value_counts() / len_muni.value_counts().sum()


#df1['departamentos'][((len_depto > 1) & (len_muni == 1))]
#df1['municipios'][((len_depto > 1) & (len_muni == 1))]
#
#
#x = df1['pre_clean_text'].loc[7]
#df1.loc[7]

#df1.to_csv('data/featuring/data_featuring.txt', sep = '|', index = False)

# =============================================================================
# 
# =============================================================================
### tags
df = pd.read_csv('data/featuring/data_featuring.txt', sep = '|')

df.head()
df.set_index(['id'], inplace = True)

tags_pos = master_tags_spanish(df['pre_clean_text'])

type(tags_pos)

a_file = open("data/featuring/data_tags_pos.pkl", "wb")
pickle.dump(tags_pos, a_file)
a_file.close()

# =============================================================================
# 
# =============================================================================
file_pos = open("data/featuring/data_tags_pos.pkl", "rb")
tag = pickle.load(file_pos)
file_pos.close()

#tag.keys()
#tag['aHR0cHM6Ly93d3cuZWxudWV2b2RpYS5jb20uY28vbnVldm9kaWEvYWN0dWFsaWRhZC9qdWRpY2lhbC8xMzcyMTEtZG9zLW1vdG9jaWNsaXN0YXMtbXVlcmVuLWVuLWFjY2lkZW50ZXMtZGUtdHJhbnNpdG8=']


