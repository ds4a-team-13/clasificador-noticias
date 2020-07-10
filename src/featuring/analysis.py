#####
import os
# path of work
ruta = 'D:/Documentos/Sebastian/01_CURSOS_VISTOS/02_CURSOS_ONLINE/202005_DATA_SCIENCE/final_project/clasificador-noticias'
os.chdir(ruta)
#####

from src.featuring.requirements import *

# =============================================================================
# 
# =============================================================================
cnx = sqlite3.connect('data/scraper/data.db')
df = pd.read_sql_query("SELECT * FROM news", cnx)

print(df.shape)
#print(df['diario'].unique())
#(
# df
# .groupby('diario')
# .agg({'fecha_publicacion': ['min', 'max'], 
#	   'url': 'size'})
#)

df['year'] = df['fecha_publicacion'].str[:4]
df['year'].value_counts()

# filtering dates out of analysis
df = df.query('year >= "2012"')
df = df.query('year != "2999"')
# cast date
df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])

df['month'] = [datetime.strftime(x, '%m') for x in df['fecha_publicacion']]
# Week number of year, Sunday as the first day of week, 00-53
df['week'] = [datetime.strftime(x, '%U') for x in df['fecha_publicacion']]

# In order for the id to look actually like a unique identifier, let's use base64 encode to convert the id to a base64 string
# The command converts the newly created id column into bytes, and then gets the base64 encoded value for the same. 
# Then the base64 value is converted to string again and then stored in the id column.
df['id'] = df['url'].apply(lambda x: b64encode(x.encode()).decode())

# how long is the body per news
df['long_cuerpo'] = df['cuerpo'].apply(lambda x: len(x.split()))
df['long_cuerpo'].value_counts().sort_values()

print('Number of news with 0 words in the body:', sum(df['long_cuerpo'] == 0))
print('Number of news with less than 10 words in the body:', sum(df['long_cuerpo'] <= 10))

df = df[df['long_cuerpo'] > 10]

# =============================================================================
# 
# =============================================================================

# stopwords from packages
stopwords_scipy = get_stop_words('spanish')
stopwords_nltk  = stopwords.words('spanish')

swords_from_packages = stopwords_scipy + stopwords_nltk
#Removal of accents in stopwords and lower case
swords_from_packages = [unidecode(word).lower() for word in swords_from_packages]
# removal stopwords duplicated
swords_from_packages = list(set(swords_from_packages))
print('size words from packages to remove', len(swords_from_packages))

# stop words from file
df_names = pd.read_csv('data/external/stopwords_names.txt')
swords_file = list(df_names['name'])
#Removal of accents in stopwords and lower case
swords_file = [unidecode(word).lower() for word in swords_file]

# consolidate all stopwords
swords_all = swords_from_packages + swords_file
swords_all = list(set(swords_all))
print('total words dictionary to remove', len(swords_all))

# Stemming (word root)
spanishstemmer = SnowballStemmer('spanish')

# function for clean text
def clean_text(serie_word: pd.Series, 
			   stop_words: list,
			   make_stemming: bool) -> pd.Series:
	"""
	This function clean the text: transform to lowercase, removing punctuation,
	removing stopwords, removing accents, removing numbers, stemming words, 
	validate if word is in alphabet and validate if word has more than two letters
	
	@input: 
		-serie_word: serie contains text per news
		-stop_words: list contains stopwords to remove.
		-make_stemming: True if you want to make stemming, False otherwise.
	@return: serie contains clean text per news
	"""
	print('Transform to lowercase...')
	#Lower case
	serie_word = serie_word.str.lower()
	
	print('Removing punctuation...')
	#Removing Punctuation
	serie_word = serie_word.str.replace('[^\w\s]','')
	
	print('Removing accents...')
	#Removal accents
	serie_word = serie_word.apply(lambda x: " ".join(unidecode(word) for word in x.split()))
		
	print('Removing numbers...')
	#Numbers removing
	serie_word = serie_word.str.replace('\d+', '')

	print('Validate if word is in alphabet...')
	serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if word.isalpha()))
	
	print('Validate if word has more than two letters...')
	serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if len(word) > 2))

	print('Removing stopwords...')
	print('Size list stopwords:', len(stop_words))
	#Removal of Stop Words
	serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if word not in stop_words))
	
	if make_stemming:
		print('Stemming words...')
		# Stemming (word root)
		serie_word = serie_word.apply(lambda x: " ".join(spanishstemmer.stem(word) for word in x.split()))
	
	print('Process finished')
	
	return serie_word

df['text'] = df['titulo'] + ' ' + df['cuerpo']

df['pre_clean_text'] = clean_text(serie_word    = df['text'],
								  stop_words    = swords_from_packages,
								  make_stemming = False)

df['clean_text'] = clean_text(serie_word    = df['text'],
							  stop_words    = swords_all,
							  make_stemming = True)

#df.to_csv('df.txt', sep = '|', index = False)
# =============================================================================
# 
# =============================================================================
#df = pd.read_csv('data/featuring/df.txt', sep = '|')

df_dane = pd.read_csv('data/external/dane_municipios_colombia.txt', sep = '|')

def ubication_news(x: str, region: str):
	"""
	This function search the ubications involved in each new
	
	@input:
		-x     : string contains the news
		-region: string contains if the search is by municipio or departamento
	@return:
		ubication_x: string contains all ubications involved in the news
	"""
	ubication_x = [ub for ub in df_dane[region] if ub in x.split()]
	ubication_x = set(ubication_x) - set(['colombia'])
	ubication_x = list(ubication_x)
	ubication_x = '|'.join(ubication_x)
	print(region, ubication_x)
	return ubication_x

# search municipios and departamentos in each news
df['municipios']    = df['pre_clean_text'].apply(lambda x: ubication_news(x, 'municipio'))
df['departamentos'] = df['pre_clean_text'].apply(lambda x: ubication_news(x, 'departamento'))

df['municipios'].fillna('', inplace = True)
df['municipios'].str.split('|').apply(len).value_counts()

df['departamentos'].fillna('', inplace = True)
df['departamentos'].str.split('|').apply(len).value_counts()

x = df['municipios'].iloc[2]
df_dane[df_dane['municipio'].isin(x.split('|'))]['departamento']

#df.to_csv('data/featuring/df.txt', sep = '|', index = False)

df = pd.read_csv('data/featuring/df.txt', sep = '|')


x = df['pre_clean_text'].iloc[:3]

nlp = es_core_news_sm.load()

doc = nlp(x)

df_names = pd.read_csv('data/external/stopwords_names.txt')
	
names = list(df_names['name'])
#tags = [(w.text, w.pos_) for w in doc]

tags_pos = x.apply(process_tags_spanish)

dict(tags_pos)

len(tags_pos.iloc[1])

tags_pos.iloc[1]

len(list(pd.core.common.flatten(tags_pos.iloc[1].values())))


df.head()
aux = df[df['id'].duplicated()]

df.shape
df.drop_duplicates(['id']).shape
