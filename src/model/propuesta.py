import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
#import plotly.express as px
from gensim.models.keyedvectors import KeyedVectors
from nltk import word_tokenize
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

wordvectors_file_vec = 'C:/Users/Sebastian/Downloads/embeddings-s-model.vec'
#cantidad = 100000
wordvectors = KeyedVectors.load_word2vec_format(wordvectors_file_vec)#, limit=cantidad)

df = pd.read_csv('data/featuring/data_featuring.txt', sep = '|')
df.head()

#len_x = df['text_for_embedding'].apply(lambda x: len(list(set(x))))
#len_x.describe()


def coords_news(x: str):
    """
    
    """
    vectores = []
    scaler   = StandardScaler()
    pca      = PCA(n_components = 1)
    
    words = word_tokenize(x)
	#words = list()
    # coords for each word in a space with k dimensions
    for w in words:
        try:
            vectores.append(wordvectors[w])
        except:
            pass
        
    X = np.matrix(vectores)
    # applying PCA
    n_samples = X.shape[0]
    # standarized the dimensions of one news
    X = scaler.fit_transform(X)
    # compute the PCA
    pca.fit(X)
    # coords individuals
    components_ind = pca.transform(X)
    
    #eigenvalues
    eigenvalues = np.var(components_ind, 0)
    #eigenvector in variables cloud
    vs = components_ind / np.sqrt(eigenvalues)
    # final components
    components_var = np.dot(X.T / n_samples, vs)
    components_var = components_var[:,0].tolist()
    
    return components_var

components = df['text_for_embedding'].apply(coords_news)
df_components = pd.DataFrame.from_dict(dict(zip(components.index, components.values))).T
df_components.head()
df_components.columns = ['x' + str(i) for i in df_components.columns]

df_components.to_csv('data/featuring/componentes_news.txt', sep = '|', index = False)

# =============================================================================
# descomposition
# =============================================================================
df_components_aux  = pd.read_csv('data/featuring/componentes_news.txt', sep = '|')

#df_components_aux = df_components.copy()
random = np.random.randint(df_components_aux.shape[0], size = 10000)
df_components_aux = df_components_aux.iloc[random, :]

param_perp = np.sqrt(df_components_aux.shape[0])
param_perp = int(np.round(param_perp))
param_perp = 1000

tsne = TSNE(n_components = 2,
			init = 'random',
			random_state = 0,
			perplexity = param_perp,
			#metric = 'eucli'
			)

coords_tsne = tsne.fit_transform(df_components_aux.values)
dfTSNE = pd.DataFrame(coords_tsne)

dfTSNE.columns = ['x1', 'x2']

sns.scatterplot('x1', 'x2', data = dfTSNE)



from umap import UMAP

reducer = UMAP(random_state = 42, n_neighbors = 5, metric = 'manhattan', min_dist = 0.01)
umap_reduce = reducer.fit_transform(df_components_aux.values)

dfUMAP = pd.DataFrame(umap_reduce)
dfUMAP.columns = ['x1', 'x2']

sns.scatterplot('x1', 'x2', data = dfUMAP)

