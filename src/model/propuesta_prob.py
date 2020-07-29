######
import os
# path of work
ruta = 'D:/Documentos/Sebastian/01_CURSOS_VISTOS/02_CURSOS_ONLINE/202005_DATA_SCIENCE/final_project/clasificador-noticias'
os.chdir(ruta)
######

print("Cargando paquetes...")
#import ast
import numpy as np
import pandas as pd
from gensim.models.keyedvectors import KeyedVectors

from scipy.stats import binom
#from nltk import word_tokenize
#from wordcloud import WordCloud

# Carga el word embedding
print("Cargando word embedding...")
wordvectors_file_vec = 'data/model/embeddings-s-model.vec'
wordvectors = KeyedVectors.load_word2vec_format(wordvectors_file_vec)
print("Listo!")

select_cols = ['titulo', 'cuerpo', 'text_for_embedding', 'cl_phase01']

df = pd.read_csv('data/model/data_model.csv', 
                 usecols = select_cols)



# Hecho contra la Población Civil
cat0 = [
    'homicidio', 'masacre', 'secuestro', 'rehén', 'prisionero', 'tortura', 'desplazamiento', 'desplazamientos', #"forzado", 
    'confinamiento', 'confinamientos', 'mina', 'minas', 'antipersona', 'antipersonas', 'antipersonal', 'explosivos',
    'atentado', 'atentados', 'perpetró', 'asesinato', 'reclutamiento', 'reclutamientos', 'alistamiento', 'niños', 'niñas', 'adolecentes',
    'violencia', 'sexual', 'victimización', 'maltrato', 'abuso', 'pedofilia', 'niña', 'violador', 'depravado',
    'ataque', 'indiscriminado', 'acribillamiento', 'bienes', 'civiles', 'abusó', 'violó',
    'hostigamiento', 'agresión', 'instigamiento', 'agresiones', 'torturas', 'víctimas',
    'amenaza', 'intimidación', 'agresión', 'brutalidad', 'retaliación', 'amedrentamiento', 'saqueo', 'bandalismo', 'desaparición'
    ]

# Acciones Armadas
cat1 = [
    'combate', 'combates', 'asalto', 'enfrentamiento', 'hostigamiento', 'agresión', 'instigamiento', 'agresiones',
    'emboscada', 'emboscados', 'terrorismo', 'ataque', 'instalación', 'militar', 'destacamiento', 'subestación',
    #"policía",
    'restricción', 'movilidad', 'retén', 'inmovilización', 'ilegal', 'ilícita', 'incautamiento', 'paro', 'armado', 'indiscriminado', 'incursión',
    'insurgente', 'guerrillero', 'guerrilla', 'antiguerrillera', 'paramilitares', 'parapoliciales', 'abigeato', 'bandidaje', 'bloqueos',
    'acorralamiento', 'escrutinios', 'infraestructura', 'disidencias'
    #"población"
    ]

# Acciones Institucionales
cat2 = [
    'captura', 'capturas', 'desactivación', 'artefacto', 'explosivo', 'explosivos', 'detonador',
    'antinarcótico', 'antinarcóticos', 'antinarcotráfico', 'antidrogas', 'incautación', 'incautaciones', 'incautamiento', 'rescate', 'secuestrado',
    'antisecuestro', 'liberación', 'misión', 'misiones', 'humanitarias', 'desvinculación', 'desvinculados', 'niños', 'niñas', 'adolecentes', 'reintegraciones',
    'desmovilizaciones', 'desmovilizadas', 'accionesjudiciales', 'procedimientos', 'emergencias'
    ]

#Otro Tipo de Evento
cat3 = [
    'pronunciamiento', 'organismo', 'internacional', 'nacional', 'conflicto', 'derecho', 'humano', 'ddhh', 'defensoría', 'defensorías',
    'victimización', 'victimizaciones', 'criminalizaciones', 'cnddhh', 'cndh'
    ]


def word_success(wrd : str, dict_thr): # Similarity better or equal to 15 degrees
    # Find the mean and median for each news based on cosine similarity greater
    # or equal to thr
    # Input: news: string, all content from the news
    #        thr: numeric, (Opcional)

    thr_t_cat0 = np.cos(dict_thr['cat0']['thr_t'] * np.pi / 180)
    thr_n_cat0 = np.cos(dict_thr['cat0']['thr_n'] * np.pi / 180)
    
    thr_t_cat1 = np.cos(dict_thr['cat1']['thr_t'] * np.pi / 180)
    thr_n_cat1 = np.cos(dict_thr['cat1']['thr_n'] * np.pi / 180)
    
    thr_t_cat2 = np.cos(dict_thr['cat2']['thr_t'] * np.pi / 180)
    thr_n_cat2 = np.cos(dict_thr['cat2']['thr_n'] * np.pi / 180)
    
    thr_t_cat3 = np.cos(dict_thr['cat3']['thr_t'] * np.pi / 180)
    thr_n_cat3 = np.cos(dict_thr['cat3']['thr_n'] * np.pi / 180)
    
    ax = []
    try:
        ax.append(wordvectors.most_similar_to_given(wrd, cat0))
        ax.append(wordvectors.most_similar_to_given(wrd, cat1))
        ax.append(wordvectors.most_similar_to_given(wrd, cat2))
        ax.append(wordvectors.most_similar_to_given(wrd, cat3))
        bx = [wordvectors.similarity(wrd, wn) for wn in ax]
        
        pass_thr_t = []
        pass_thr_n = []
        
        pass_thr_t.append(bx[0] >= thr_t_cat0)
        pass_thr_t.append(bx[1] >= thr_t_cat1)
        pass_thr_t.append(bx[2] >= thr_t_cat2)
        pass_thr_t.append(bx[3] >= thr_t_cat3)
        
        pass_thr_n.append(bx[0] >= thr_n_cat0)
        pass_thr_n.append(bx[1] >= thr_n_cat1)
        pass_thr_n.append(bx[2] >= thr_n_cat2)
        pass_thr_n.append(bx[3] >= thr_n_cat3)
        
        return np.where(np.array(pass_thr_t), 1, 0), np.where(np.array(pass_thr_n), 1, 0)
    except:
        return np.array([0, 0, 0, 0]), np.array([0, 0, 0, 0])

def news_success(news : str, dict_thr):

    words = pd.Series(list(set(news.split())))
    aux00 = words.apply(lambda x: word_success(x, dict_thr = dict_thr))
    dfaux = pd.DataFrame(aux00.tolist())
    dfaux.rename(columns={0:'Success',1:'N'}, inplace = True)
    succe = np.squeeze(np.asarray(np.matrix(dfaux['Success'].tolist()).sum(axis=0)))
    nn_ar = np.squeeze(np.asarray(np.matrix(dfaux['N'].tolist()).sum(axis=0)))
    
    return succe, nn_ar


#degrees_thr = {'2': {'cat0': {'thr_t': 40, 'thr_n': 55},
#                      'cat1': {'thr_t': 40, 'thr_n': 55},
#                      'cat2': {'thr_t': 40, 'thr_n': 50},
#                      'cat3': {'thr_t': 40, 'thr_n': 55}
#                      },
#                '4': {'cat0': {'thr_t': 40, 'thr_n': 55},
#                      'cat1': {'thr_t': 40, 'thr_n': 55},
#                      'cat2': {'thr_t': 40, 'thr_n': 50},
#                      'cat3': {'thr_t': 40, 'thr_n': 55}
#                      },
#                '5': {'cat0': {'thr_t': 35, 'thr_n': 45},
#                      'cat1': {'thr_t': 40, 'thr_n': 50},
#                      'cat2': {'thr_t': 35, 'thr_n': 45},
#                      'cat3': {'thr_t': 35, 'thr_n': 45}
#                      },
#                '7': {'cat0': {'thr_t': 40, 'thr_n': 50},
#                      'cat1': {'thr_t': 35, 'thr_n': 45},
#                      'cat2': {'thr_t': 35, 'thr_n': 45},
#                      'cat3': {'thr_t': 35, 'thr_n': 45}
#                      }                    
#                }
#
#
#p_hats = {}
#for i in [2, 4, 5, 7]:
#    cl = str(i)
#    degrees_thr_cl = degrees_thr[cl]
#    
#    string = ' '.join(df.loc[df['cl_phase01'] == i, 'text_for_embedding'])
#    a, b = news_success(string, dict_thr = degrees_thr_cl)
#    
#    print(i)
#    print(a)
#    print(b)
#    print(a / b)
#    p_hats[cl] = a / b

p_hats = {
          '2': np.array([0.09245374, 0.1058254 , 0.14000688, 0.06394628]),
          '4': np.array([0.09099777, 0.10575162, 0.15319549, 0.0655883 ]),
          '5': np.array([0.13489135, 0.18307309, 0.09430856, 0.09009009]),
          '7': np.array([0.17840704, 0.12040321, 0.09324072, 0.08269395])
          }

# =============================================================================
# aplicacion a cada noticia
# =============================================================================

degrees_thr = {'2': {'cat0': {'thr_t': 30, 'thr_n': 55},
                      'cat1': {'thr_t': 32, 'thr_n': 55},
                      'cat2': {'thr_t': 40, 'thr_n': 55},
                      'cat3': {'thr_t': 35, 'thr_n': 55}
                      },
                '4': {'cat0': {'thr_t': 30, 'thr_n': 55},
                      'cat1': {'thr_t': 32, 'thr_n': 55},
                      'cat2': {'thr_t': 40, 'thr_n': 55},
                      'cat3': {'thr_t': 35, 'thr_n': 55}
                      },
				
                '5': {'cat0': {'thr_t': 30, 'thr_n': 45},
                      'cat1': {'thr_t': 30, 'thr_n': 50},
                      'cat2': {'thr_t': 30, 'thr_n': 55},
                      'cat3': {'thr_t': 30, 'thr_n': 55}
                      },
                '7': {'cat0': {'thr_t': 30, 'thr_n': 50},
                      'cat1': {'thr_t': 30, 'thr_n': 55},
                      'cat2': {'thr_t': 30, 'thr_n': 55},
                      'cat3': {'thr_t': 30, 'thr_n': 55}
                      }                    
                }

cl = 7
cl_aux = df[df.cl_phase01 == cl]
degrees_thr_cl = degrees_thr[str(cl)]

np.random.seed(123)
idx = np.random.randint(cl_aux.shape[0], size = 50)

Aux_Tup = (
        cl_aux.iloc[idx, :]['text_for_embedding']
        .apply(lambda x: news_success(x, dict_thr = degrees_thr_cl))
         )
Aux_Tup = Aux_Tup.reset_index(drop = True)
Aux_DF = pd.DataFrame(Aux_Tup.tolist(), columns=['news_success','N_words'])

Aux_DF['Prob'] = Aux_DF.apply(lambda x: np.round(binom.cdf(x['news_success'], x['N_words'], p_hats[str(cl)]), 5), axis = 1)
Aux_DF['Prob'] = Aux_DF['Prob'] * 100
Aux_DF.head(10)


#rows = range(10, 20)
rows = range(20, 30)
#rows = range(10)

list(Aux_DF['Prob'].iloc[rows])
list(cl_aux.iloc[idx[rows], :]['titulo'])

cl_aux.iloc[idx[list(rows)[5]], :]['cuerpo']

#list(Aux_DF['Prob'].iloc[10:20])
#list(cl_aux.iloc[idx[10:20], :]['titulo'])


#pd.options.display.float_format = '{:.5f}'.format
