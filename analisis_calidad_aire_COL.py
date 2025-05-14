import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

"""
Created on Tuesday May 13 16:19:45 2025

@author: Sheilyn Colina
"""

# URL de la API de Datos Abiertos
url = "https://www.datos.gov.co/resource/kekd-7v7h.json"


# Hacemos la solicitud
response = requests.get(url)

# Convertimos la respuesta JSON en un DataFrame
data = response.json()
df = pd.DataFrame(data)

# Mostramos las primeras filas
print(df.head())

#Después de ejecutar lo anterior, vamos a inspeccionar las columnas disponibles:
print(df.columns)


# Y un resumen rapido
df.info()
df.describe(include='all')


#LIMPIEZA BASICA 

# Seleccionar columnas relevantes
columnas_utiles = [
    'estaci_n', 'latitud', 'longitud', 'variable', 'unidades', 'a_o',
    'promedio', 'm_ximo', 'm_nimo', 'mediana', 'percentil_98',
    'nombre_del_municipio', 'tipo_de_estaci_n'
]

df = df[columnas_utiles].copy()

# Renombrar columnas para usarlas más fácil
df.rename(columns={
    'estaci_n': 'estacion',
    'variable': 'contaminante',
    'a_o': 'anio',
    'm_ximo': 'maximo',
    'm_nimo': 'minimo',
    'nombre_del_municipio': 'municipio',
    'tipo_de_estaci_n': 'tipo_estacion',
    'percentil_98': 'percentil_98',
    'mediana': 'mediana'
}, inplace=True)

# Convertir columnas numéricas de texto a float
columnas_numericas = ['latitud', 'longitud', 'promedio', 'maximo', 'minimo', 'mediana', 'percentil_98']
for col in columnas_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Eliminar filas con datos faltantes críticos
df.dropna(subset=['promedio', 'contaminante', 'estacion', 'anio'], inplace=True)

# Verificar el resultado
print("Datos limpios")
df.head()


#Codigo para exploracion basica

# Estilo visual
sns.set(style="whitegrid")

# Contaminantes más frecuentes
contaminantes_freq = df['contaminante'].value_counts()
print("Contaminantes más comunes:")
print(contaminantes_freq)

# Promedio general por contaminante
promedio_contaminantes = df.groupby('contaminante')['promedio'].mean().sort_values(ascending=False)
print("\nPromedio general por contaminante:")
print(promedio_contaminantes)



#Visualizaciones Basicas


#Grafico de barras: Promedio por contaminante
plt.figure(figsize=(12, 6))
sns.barplot(x=promedio_contaminantes.index, y=promedio_contaminantes.values, palette="viridis")
plt.title("Promedio general por contaminante")
plt.ylabel("Valor promedio")
plt.xlabel("Contaminante")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#Boxplot por contaminante (distribución de datos)
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='contaminante', y='promedio', palette="Set3")
plt.title("Distribución de valores promedio por contaminante")
plt.ylabel("Valor")
plt.xlabel("Contaminante")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Gráfico por estación (ejemplo con PM2.5)
pm25 = df[df['contaminante'] == 'PM2.5']

plt.figure(figsize=(14, 6))
sns.barplot(data=pm25, x='estacion', y='promedio', ci=None, palette="cubehelix")
plt.title("Promedio de PM2.5 por estación")
plt.ylabel("PM2.5 promedio")
plt.xlabel("Estación")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


'''Con esto ya tienes una primera exploración y visualización del comportamiento de la calidad del aire.

✅ ¿Siguiente paso?
Podemos ahora:

-Filtrar por años o municipios específicos

-Comparar valores entre estaciones

-Crear un mini dashboard con Plotly o Dash

¿Quieres avanzar hacia un dashboard interactivo básico o agregar más visualizaciones antes de eso?'''




