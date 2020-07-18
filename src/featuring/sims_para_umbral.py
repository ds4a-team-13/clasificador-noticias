print("Cargando paquetes...")
import numpy as np
import pandas as pd
from gensim.models.keyedvectors import KeyedVectors
from tqdm import tqdm
from nltk import word_tokenize
from sklearn import manifold
print("Listo!")

# Carga el word embedding
print("Cargando word embedding...")
wordvectors_file_vec = 'embeddings-s-model.vec'
cantidad = 100000
wordvectors = KeyedVectors.load_word2vec_format(wordvectors_file_vec)#, limit=cantidad)
print("Listo!")

#Hecho contra la población civil
categoria0 = [
                "homicidio",
                 "masacre",
                 "secuestro",
                 "tortura",
                 "desplazamiento",
                 "forzado",
                 "confinamiento",
                 "accidente",
                 "mina",
#                 "antipersona",
                 "atentado",
                 "reclutamiento",
                 "violencia",
                 "sexual",
                 "ataque",
                 "indiscriminado",
                 "bienes",
                 "civiles"
]

#acciones armadas
categoria1 = [
                "combate",
                "enfrentamiento",
                "hostigamiento",
                "emboscada",
                "acto",
                "terrorismo",
                "ataque",
                "instalación",
                "militar",
                "policía" ,
                "restricción",
                "movilidad",
                "retenes",
                "ilegal",
                "paro",
                "armado",
                "indiscriminado",
                "incursión",
                "población"
]

# Acciones institucionales
categoria2 = [
                "captura",
                "desactivación",
                "artefacto",
                "explosivo",
#                "antinarcotico",
                "incautación",
                "rescate",
                "secuestrado",
                "liberación",
                "misión",
                "humanitaria"
]

#Otro tipo de evento
categoria3 = [
                "pronunciamiento",
                "organismo",
                "internacional",
                "nacional",
                "conflicto",
                "derecho",
                "humano",
                "ddhh",
                "victimización"
]

def vector_media_noticia(cadena:str):

    # Encuentra el centroide de la noticia en términos de la media
    # Input: string, texto noticia

    palabras = word_tokenize(cadena)
    vectores = []
    for w in palabras:
        try:
            vectores.append(wordvectors[w])
        except:
            pass

    vectores = np.matrix(vectores)
    return np.mean(vectores, axis=0).tolist()[0]

def vector_mediana_noticia(cadena:str):

    # Encuentra el centroide de la noticia en términos de la media
    # Input: string, texto noticia

    palabras = word_tokenize(cadena)
    vectores = []
    for w in palabras:
        try:
            vectores.append(wordvectors[w])
        except:
            pass

    vectores = np.matrix(vectores)

    return np.median(vectores, axis=0).tolist()[0]

def similitud_categorias(palabras:list):

    # Calcula la similitud a las cuatro categorias
    # como el promedio de similitud (word embedding)
    # entre todas las palabras de la noticia y todas
    # las palabras de las categorias.
    # Devuelve la similitud máxima.
    # Input: palabras, lista de palabras de la noticia

    sim0 = []
    sim1 = []
    sim2 = []
    sim3 = []
    not_in_we = []
    for w_n in palabras:
        for w in categoria0:
            try:
                sim0.append(wordvectors.similarity(w_n, w))
            except:
                not_in_we.append(w_n)

        for w in categoria1:
            try:
                sim1.append(wordvectors.similarity(w_n, w))
            except:
                not_in_we.append(w_n)

        for w in categoria2:
            try:
                sim2.append(wordvectors.similarity(w_n, w))
            except:
                not_in_we.append(w_n)

        for w in categoria3:
            try:
                sim3.append(wordvectors.similarity(w_n, w))
            except:
                not_in_we.append(w_n)

    sim0 = np.mean(sim0)
    sim1 = np.mean(sim1)
    sim2 = np.mean(sim2)
    sim3 = np.mean(sim3)
    maximo = max([sim0, sim1, sim2, sim3])

    return maximo

def categorizar(palabras:list):

    # Calcula la similitud a las cuatro categorias
    # como el promedio de similitud (word embedding)
    # entre todas las palabras de la noticia y todas
    # las palabras de las categorias.
    # Devuelve la similitud máxima.
    # Input: palabras, lista de palabras de la noticia

    sim0 = []
    sim1 = []
    sim2 = []
    sim3 = []
    not_in_we = []
    for w_n in palabras:
        for w in categoria0:
            try:
                sim0.append(wordvectors.similarity(w_n, w))
            except:
                not_in_we.append(w_n)

        for w in categoria1:
            try:
                sim1.append(wordvectors.similarity(w_n, w))
            except:
                not_in_we.append(w_n)

        for w in categoria2:
            try:
                sim2.append(wordvectors.similarity(w_n, w))
            except:
                not_in_we.append(w_n)

        for w in categoria3:
            try:
                sim3.append(wordvectors.similarity(w_n, w))
            except:
                not_in_we.append(w_n)

    sim0 = np.mean(sim0)
    sim1 = np.mean(sim1)
    sim2 = np.mean(sim2)
    sim3 = np.mean(sim3)
    maximo = max([s0, s1, s2, s3])
    max_value = [s0, s1, s2, s3].index(maximo)
    
    return max_value


# Cargar base de noticias filtradas
print("Cargando datos...")
data = pd.read_csv('data_featuring.txt', sep='|')
print("Listo!")

# Encuentra las similitudes
print("Encontrando similitud maxima...")
data['sim_cats'] = data['text_for_embedding'].apply(similitud_categorias)
print("Listo!")

# Encuentra la categoría
print("Encontrando categoría...")
data['category_bl'] = data['text_for_embedding'].apply(categorizar)
print("Listo!")

# Encuentra los centroides de medias y medianas
print("Encontrando centroides de medias...")
data['centroide_media'] = data['text_for_embedding'].apply(vector_media_noticia)
print("Listo!")
print("Encontrando centroides de medianas...")
data['centroide_mediana'] = data['text_for_embedding'].apply(vector_mediana_noticia)
print("Listo!")

# Guarda en archivo
data.to_csv('data_featuring.csv')
print("Archivo guardado en data_featuring.csv")

# Encontrando TSNE medias 2D
print("Encontrando tsne medias 2D...")
dat = [val for val in data['centroide_media']]
tsne = manifold.TSNE(n_components=2, init='random', random_state=0, perplexity=200)
Y = tsne.fit_transform(dat)
print("Listo!")
dfTSNE=pd.DataFrame(Y)
dfTSNE.to_csv("TSNE_MEDIA_2D.csv",index=False)
print("Archivo guardado en TSNE_MEDIA_2D.csv")

# Encontrando TSNE medias 3D
print("Encontrando tsne medias 3D...")
dat = [val for val in data['centroide_media']]
tsne = manifold.TSNE(n_components=3, init='random', random_state=0, perplexity=200)
Y = tsne.fit_transform(dat)
print("Listo!")
dfTSNE=pd.DataFrame(Y)
dfTSNE.to_csv("TSNE_MEDIA_3D.csv",index=False)
print("Archivo guardado en TSNE_MEDIA_3D.csv")

# Encontrando TSNE medianas 2D
print("Encontrando tsne medianas 2D...")
dat = [val for val in data['centroide_mediana']]
tsne = manifold.TSNE(n_components=2, init='random', random_state=0, perplexity=200)
Y = tsne.fit_transform(dat)
print("Listo!")
dfTSNE=pd.DataFrame(Y)
dfTSNE.to_csv("TSNE_MEDIANA_2D.csv",index=False)
print("Archivo guardado en TSNE_MEDIANA_2D.csv")

# Encontrando TSNE medianas 3D
print("Encontrando tsne medianas 3D...")
dat = [val for val in data['centroide_mediana']]
tsne = manifold.TSNE(n_components=3, init='random', random_state=0, perplexity=200)
Y = tsne.fit_transform(dat)
print("Listo!")
dfTSNE=pd.DataFrame(Y)
dfTSNE.to_csv("TSNE_MEDIANA_3D.csv",index=False)
print("Archivo guardado en TSNE_MEDIANA_3D.csv")

print("Proceso finalizado exitosamente.")
