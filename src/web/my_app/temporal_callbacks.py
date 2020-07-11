from dash.dependencies import Output, Input
from my_app.utils import *
import pandas as pd


###############################################################
# VARIABLES GLOBALES
###############################################################
anho = -1
semana = -1
###############################################################

df = pd.read_csv('../../data/web/news_categorized.csv', nrows=100)
df['fecha_publicacion']=pd.to_datetime(df['fecha_publicacion'])
df['year']=df['fecha_publicacion'].dt.year
df['week']=df['fecha_publicacion'].dt.week

lista_news_categoria_0 = []
lista_news_categoria_1 = []
lista_news_categoria_2 = []
lista_news_categoria_3 = []
lista_anhos = df.year.unique()
lista_semanas = range(1, 10)
tituloNotica = "Titulo noticia"
fechaNoticia = "Fecha noticia"
cuerpoNoticia = "Cuerpo noticia"
urlNoticia = ""
valor_lista_cat_0 = -1
valor_lista_cat_1 = -1
valor_lista_cat_2 = -1
valor_lista_cat_3 = -1

def register_callbacks(app):

  # Actualiza la lista desplegable de semana dependiendo del año seleccionado
  @app.callback(Output('semana', 'options'), [Input('anho', 'value')])
  def actualiza_semanas(valor):

      global lista_semanas
      global anho

      if valor:
          anho = valor
          lista_semanas = df[df['year']==anho].week.unique()
      return [{"label":x,"value":x} for x in lista_semanas]

  # Actualiza la lista de noticias de cada categoria
  # dependiendo de la semana seleccionada
  @app.callback([Output('noticias_categoria_0', 'options'),
  Output('noticias_categoria_1', 'options'),
  Output('noticias_categoria_2', 'options'),
  Output('noticias_categoria_3', 'options')], [Input('semana', 'value')])
  def actualiza_semanas(valor):

      global lista_news_categoria_0
      global lista_news_categoria_1
      global lista_news_categoria_2
      global lista_news_categoria_3
      global semana
      global anho

      if valor:
          semana = valor
          lista_news_categoria_0 = crear_listado_noticias(df, 0, semana, anho)
          lista_news_categoria_1 = crear_listado_noticias(df, 1, semana, anho)
          lista_news_categoria_2 = crear_listado_noticias(df, 2, semana, anho)
          lista_news_categoria_3 = crear_listado_noticias(df, 3, semana, anho)

      return lista_news_categoria_0,\
              lista_news_categoria_1,\
              lista_news_categoria_2,\
              lista_news_categoria_3


  # Se selecciona una noticia en las listas
  # y se activa la lista desplegable de mostrar noticia
  # y rellena el modal de mostrar noticia con la info de la noticia
  @app.callback(Output('noticia_c0', 'disabled'),
      [Input('noticias_categoria_0', 'value'),
      Input('noticias_categoria_1', 'value'),
      Input('noticias_categoria_2', 'value'),
      Input('noticias_categoria_3', 'value')])
  def activa_boton_c0(valor0, valor1, valor2, valor3):

      global tituloNotica
      global fechaNoticia
      global cuerpoNoticia
      global urlNoticia
      global valor_lista_cat_0
      global valor_lista_cat_1
      global valor_lista_cat_2
      global valor_lista_cat_3

      valor_lista_cat_0 = valor0
      valor_lista_cat_1 = valor1
      valor_lista_cat_2 = valor2
      valor_lista_cat_3 = valor3

      if valor0>=0:
          return False
      elif valor1>=0:
          return False
      elif valor2>=0:
          return False
      elif valor3>=0:
          return False
      else:
          return True


  # # Activa la ventanita
  @app.callback([Output('mostrar_noticia', 'style'),
      Output('Titulo noticia', 'children'),
      Output('fecha noticia', 'children'),
      Output('cuerpo noticia', 'children'),
      Output('vinculo noticia', 'children'),
      Output('vinculo noticia', 'href')],
      [Input('noticia_c0', 'value')])
  def activa_modal_noticia(value):

      global tituloNotica
      global fechaNoticia
      global cuerpoNoticia
      global urlNoticia

      if value==0:
          valor = valor_lista_cat_0
      elif value==1:
          valor = valor_lista_cat_1
      elif value==2:
          valor = valor_lista_cat_2
      elif value==3:
          valor = valor_lista_cat_3

      try:
          tituloNotica = df[df['ID']==valor].titulo
          fechaNoticia = df[df['ID']==valor].fecha_publicacion
          cuerpoNoticia = df[df['ID']==valor].cuerpo.values[0]
          urlNoticia = df[df['ID']==valor].url.values[0]
      except:
          tituloNotica = "Titulo noticia"
          fechaNoticia = "Fecha noticia"
          cuerpoNoticia = "Cuerpo noticia"
          urlNoticia = ""

      if value and value>=0:
          return {'border':'2px black solid', 'display':'block'},\
              tituloNotica, fechaNoticia, cuerpoNoticia, urlNoticia, urlNoticia

      else:
          return {'border':'2px black solid', 'display':'none'},\
              tituloNotica, fechaNoticia, cuerpoNoticia, urlNoticia, urlNoticia


  