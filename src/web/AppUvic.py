import streamlit as st
import plotly.express as px
import pandas as pd
pd.options.plotting.backend = "plotly"

st.title("Uvic Dashboard")

st.sidebar.header("Análisis de Noticias")
from PIL import Image # Le ponemos una imagen
img = Image.open("c1_logo.jpeg")
st.sidebar.image(img, width=200)
opciones_analisis = ['Análisis Temporal', 'Análisis Espacial', 'Análisis Semántico'] # Y una lista desplegable con los análisis

analisis_seleccionado = st.sidebar.selectbox('Por favor seleccione un análisis de la lista.', opciones_analisis)

if analisis_seleccionado == 'Análisis Temporal':
    df_conteo = pd.read_csv('df_conteo.csv')
    st.header("Histórico de las noticias por categoría")
    fig = px.line(df_conteo, x = "date_year_week", y="num_hechos", title='', color = 'cluster')
    st.plotly_chart(fig)
	