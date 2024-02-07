#importar librerias
 
import pandas as pd
import plotly.express as px
import streamlit as st
import openpyxl
import matplotlib as plt
import numpy as np
 
st.set_page_config(page_title= 'TOP 50 canciones destacadas (2023)', # nombre de la pagina
                   page_icon= 'musical_note:',
                   layout="wide")
 
st.title(':headphones: TOP 50 Canciones destacadas (2023)') # titulo del dash
st.markdown('##') #para poner espacios entre el titulo y los Kpis
 
# poner el subtitulo con el logo
from PIL import Image
import streamlit as st
 
# carga la imagen desde la ubicacion en que esta
image = Image.open("C:\\Users\\joanc\\OneDrive\\Escritorio\\proyecto_dashboard\\proyecto_dashboard\\spotify_logo.png")
 
# Crea una columna para la imagen y el título en la misma línea
col1, col2 = st.columns([1, 18])
 
# coloca la imagen en la primera columna
col1.image(image, width=45)
 
# coloca el título en la segunda columna
col2.subheader("Spotify")
 
st.markdown('##') #para poner espacios entre el titulo y los Kpis

archivo_excel = 'data_spotify.xlsx'
hoja_excel = 'Hoja1'
 
df = pd.read_excel(archivo_excel,
                   sheet_name= hoja_excel,
                   usecols= 'A:H')
                   #header= 0
 
#filtros
 
# Filtro para el nombre de la canción
nombre_cancion = st.sidebar.selectbox("Selecciona el nombre de la canción:", ["Todos"] + list(df["Nombre canción"].unique()))
 
# Filtro para el nombre del artista
nombre_artista = st.sidebar.selectbox("Selecciona el nombre del artista:", ["Todos"] + list(df["Nombre artista"].unique()))
 
# Filtrar datos de acuerdo a los filtros seleccionados
if nombre_cancion == "Todos" and nombre_artista == "Todos":
    df_filtrado = df.copy()
elif nombre_cancion == "Todos":
    df_filtrado = df[df["Nombre artista"] == nombre_artista]
elif nombre_artista == "Todos":
    df_filtrado = df[df["Nombre canción"] == nombre_cancion]
else:
    df_filtrado = df[(df["Nombre canción"] == nombre_cancion) & (df["Nombre artista"] == nombre_artista)]
 
# KPIs
total_canciones = df_filtrado["Nombre canción"].nunique()
total_artistas = df_filtrado["Nombre artista"].nunique()
 
# Mostrar KPIs
st.write(f"Total de canciones: {total_canciones}")
st.write(f"Total de artistas: {total_artistas}")
 
# Mostrar tabla
st.write("### Datos")
st.write(df_filtrado)

# Figura 1
# Graficos del panel
st.write("## Canciones con más Streams")

# Gráfico de barras con colores específicos
colores_barras = ['#98FB98', '#00FF7F', '#00CED1', '#2F4F4F', '#008080', '#4682B4']
fig = px.bar(df_filtrado.nlargest(10, 'Streams'), x='Nombre canción', y='Streams', title='Top 10 Canciones con más Streams',
             color='Streams', color_continuous_scale=colores_barras)

# Figura 2
# Crear un gráfico de treemap con colores personalizados y orden invertido
fig_treemap_colores_orden = px.treemap(df, path=['Año lanzamiento', 'Nombre artista'], values='En listas spotify',
                                        title='Listas en Spotify por Artista (Treemap)',
                                        labels={'En listas spotify': 'Listas en Spotify', 'Año lanzamiento': 'Año'},
                                        color_discrete_sequence=['#4682B4', '#008080', '#2F4F4F', '#00CED1', '#00FF7F', '#98FB98'])

# Figura 3
# Gráfico de pastel con combinación de colores específicos
colores_combinados = ['#98FB98', '#00FF7F', '#00CED1', '#2F4F4F', '#008080', '#4682B4']
fig_pie = px.pie(df_filtrado, values='Streams', names='Año lanzamiento', title='Distribución de Streams por Año',
                 color_discrete_sequence=colores_combinados)

# Crear dos columnas para colocar los gráficos uno al lado del otro
col1, col2 = st.columns(2)

# Mostrar el gráfico de barras en la primera columna
col1.plotly_chart(fig)

# Mostrar el gráfico de pastel en la segunda columna
col2.plotly_chart(fig_pie)

# Mostrar el gráfico de treemap debajo de las dos columnas
st.plotly_chart(fig_treemap_colores_orden)





