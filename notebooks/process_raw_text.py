import os
path = 'D:/Documentos/Sebastian/01_CURSOS_VISTOS/02_CURSOS_ONLINE/202005_DATA_SCIENCE/final_project/analisis_exploratorio/'
os.chdir(path)


import pandas as pd
pd.options.display.max_columns = None

import numpy as np

#if is the first time that you use nltk, please uncomment the following
#two lines and execute it.
#import nltk
#nltk.download('stopwords')
#words will be removing
from nltk.corpus import stopwords
swords = stopwords.words('spanish')
df_names = pd.read_csv('names.csv')

swords = swords + list(df_names['name'])
print('size words dictionary to remove', len(swords))

# Stemming: algorithm proposed by potter for to find the word's root 
from nltk import SnowballStemmer
spanishstemmer = SnowballStemmer('spanish')

# Remove accents
from unidecode import unidecode

# Document term matrix
from sklearn.feature_extraction.text import CountVectorizer

import sqlite3

from wordcloud import WordCloud

cnx = sqlite3.connect('data.db')
df = pd.read_sql_query("SELECT * FROM news", cnx)
df['text'] = df['titulo'] + ' ' + df['cuerpo']


# 
serie_word = df['text']

print('Convirtiendo a minuscula...')
#Lower case
serie_word = serie_word.str.lower()

print('Removiendo puntuacion...')
#Removing Punctuation
serie_word = serie_word.str.replace('[^\w\s]','')

print('Removiendo stopwords...')
#Removal of Stop Words
#pattern = '|'.join(swords)
serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if word not in swords))

print('Removiendo acentos...')
#Removal accents
serie_word = serie_word.apply(lambda x: " ".join(unidecode(word) for word in x.split()))

print('Removiendo numeros...')
#Numbers removing
serie_word = serie_word.str.replace('\d+', '')

print('Stemming words...')
# Stemming (word root)
serie_word = serie_word.apply(lambda x: " ".join(spanishstemmer.stem(word) for word in x.split()))

print('Validando si la palabra es del alfabeto')
serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if word.isalpha()))

print('Si tiene mas de dos letras')
serie_word = serie_word.apply(lambda x: " ".join(word for word in x.split() if len(word) > 2))


# number words by each body
serie_word.apply(lambda x: len(x))

serie_word.apply(lambda x: len(x)).sum()

import matplotlib.pyplot as plt
text = serie_word.values
wordcloud = WordCloud().generate(str(text))

plt.imshow(wordcloud)
plt.axis("off")
plt.show()


#max_features = 20000
vec = CountVectorizer(analyzer = "word", 
					  ngram_range = (1, 1))

X = vec.fit_transform(list(serie_word))
df = pd.DataFrame(X.toarray(), columns = vec.get_feature_names())
df.info()
df.head()

# drop cols
columns_sum = df.sum()
cols_drop = columns_sum[columns_sum == 1].index
del columns_sum
df.drop(columns = cols_drop, inplace = True)

cols_drop = df.columns[~df.columns.str.isalpha()]
df = df.drop(columns = cols_drop)

# drop new with 0 words
df = df[df.sum(axis = 1) != 0]

df.info()
df.head()



# compute similarities
prod_mat = X.dot(X.transpose())

from scipy import sparse
_norma = 1 / np.sqrt(prod_mat.diagonal())
_norma = sparse.diags(_norma)

prod_mat = (_norma.dot(prod_mat)).dot(_norma)

df_sim = pd.DataFrame(prod_mat.toarray())

df_sim['row'] = df_sim.index
df_sim = pd.melt(df_sim, 'row')

df_sim = df_sim[df_sim['row'] != df_sim['variable']]

df_sim['row'] = df_sim['row'].astype(str)
df_sim['variable'] = df_sim['variable'].astype(str)

df_sim['pair'] = df_sim[['row', 'variable']].apply(lambda x: '-'.join(sorted(x)), axis = 1)
df_sim.drop_duplicates(subset = ['pair'], inplace = True)

df_sim['row']      = df_sim['row'].astype(int)
df_sim['variable'] = df_sim['variable'].astype(int)


#from sklearn.metrics.pairwise import pairwise_distances
#jac_sim = 1 - pairwise_distances(df, metric = "hamming")
## optionally convert it to a DataFrame
#jac_sim = pd.DataFrame(jac_sim)
#jac_sim['row'] = jac_sim.index
#
#jac_sim = pd.melt(jac_sim, 'row')
#
#jac_sim = jac_sim[jac_sim['row'] != jac_sim['variable']]

sorted(df_sim['value'])

max_v = df_sim['value'].max()
max_v
#max_v = 90

min_v = df_sim['value'].min()
min_v
#min_v = 1


df_sim[df_sim['value'] == min_v]
df_min = df_sim[df_sim['value'] == min_v].iloc[0, :]
search = list(df_min[['row', 'variable']])
#search = [10, 9]

dfjson.loc[search[0], 'titulo']
dfjson.loc[search[1], 'titulo']

dfjson.loc[search[0], 'cuerpo']
dfjson.loc[search[1], 'cuerpo']

# ===== max values
df_sim[df_sim['value'] == max_v]
df_max = df_sim[df_sim['value'] == max_v].iloc[0, :]
search = list(df_max[['row', 'variable']])

dfjson.loc[search[0], 'titulo']
dfjson.loc[search[1], 'titulo']

dfjson.loc[search[0], 'cuerpo']
dfjson.loc[search[1], 'cuerpo']

