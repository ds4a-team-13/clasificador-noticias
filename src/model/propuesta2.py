import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

######
import os
# path of work
ruta = 'D:/Documentos/Sebastian/01_CURSOS_VISTOS/02_CURSOS_ONLINE/202005_DATA_SCIENCE/final_project/clasificador-noticias'
os.chdir(ruta)
######


df = pd.read_csv('data/featuring/data_featuring.txt', sep = '|')
df.head()
df.info()


#all_text = ' '.join(df['pre_clean_text'])
#all_text_list = all_text.split()
#len(all_text_list)
#all_text_list = pd.Series(all_text_list).value_counts()
#pd.DataFrame(all_text_list [all_text_list <= 2]).to_csv('data/external/stop_low_count.csv')
#sorted(all_text_list [(all_text_list >= 3) & (all_text_list < 5)].index)[-100:-50]



#x = df['clean_text'].iloc[50000]
n_ = 50000
random = np.random.randint(df.shape[0], size = n_)
df = df.iloc[random, :]

#df.to_csv('data/model/data_train.txt', sep = '|')
df = pd.read_csv('data/model/data_train.txt', sep = '|')
df.head()

vectorizer = TfidfVectorizer(max_features = 7000, ngram_range = (1, 1))
X = vectorizer.fit_transform(df['clean_text'])
X

import pickle
#pickle.dump(vectorizer, open("data/model/tfidf.pickle", "wb"))
tfidf = pickle.load(open("data/model/tfidf.pickle", "rb"))
#tfidf.vocabulary_
#X = tfidf.transform(df['clean_text'][:10])

#pd.DataFrame(X.toarray(),
#			 columns = tfidf.get_feature_names())
#df['clean_text'][8]

from umap import UMAP
import matplotlib.pyplot as plt
import seaborn as sns

n_neigh = 11
reducer = UMAP(random_state = 42,
			   n_neighbors  = n_neigh,
			   metric       = 'cosine',
			   low_memory   = True)
umap_reduce = reducer.fit_transform(X)

import joblib
joblib.dump(reducer, "data/model/UMAP.sav")
#loaded_reducer = joblib.load(filename)

sns.scatterplot(umap_reduce[:,0], umap_reduce[:,1])
plt.title('number neighbors ' + str(n_neigh))

from sklearn.cluster import KMeans


distortions = []
K = range(2, 10)
for k in K:
    print(k)
    kmeanModel = KMeans(n_clusters = k)
    kmeanModel.fit(umap_reduce)
    distortions.append(kmeanModel.inertia_)

plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()

k = 4
kmeanModel = KMeans(n_clusters = k)
kmeanModel.fit(umap_reduce)

#pickle.dump(kmeanModel, open("data/model/KmeansModel.pickle", "wb"))
pickle.dump(kmeanModel, open("data/model/KmeansModel.pickle", "wb"))

clust = kmeanModel.predict(umap_reduce)
clust = ['cl ' + str(x) for x in clust]
clust = np.array(clust)

sns.scatterplot(umap_reduce[:,0], umap_reduce[:,1], hue = clust)
plt.title('number neighbors ' + str(n_neigh))


from wordcloud import WordCloud

cl = 'cl 0'
df.loc[clust == cl, 'titulo'].iloc[9]

#cluster 0-> cluster de marvel
#cluster 1-> accidentes de transito
#cluster 2-> ataques, asesinatos entre familiares o conocidos
#cluster 3-> incautaciones, droga, capturas

text = df.loc[clust == cl, 'clean_text']
wordcloud = WordCloud().generate(str(text))

plt.imshow(wordcloud)
plt.axis("off")
plt.title(cl)
plt.show()


kmeanModel = pickle.load(open("data/model/KmeansModel.pickle", "rb"))

pd.Series(kmeanModel.labels_).value_counts()
pd.Series(kmeanModel.labels_).value_counts() / pd.Series(kmeanModel.labels_).value_counts().sum() 

#from sklearn.decomposition import PCA
#from sklearn.preprocessing import StandardScaler
#
#scaler = StandardScaler()
#pca    = PCA(n_components = 2)
#
#X = scaler.fit_transform(df_tfidf)
## compute the PCA
#pca.fit(X)
## coords individuals
#components_ind = pca.transform(X)
#
#sns.scatterplot(components_ind[:,0], components_ind[:,1])
#plt.title('number neighbors ' + str(n_neigh))
